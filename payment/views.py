from datetime import datetime
from django.utils import timezone
from django.core.serializers.json import DjangoJSONEncoder
from django.shortcuts import render, get_object_or_404
import iyzipay
import json
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseServerError
from django.urls import reverse
from django.views.decorators.http import require_http_methods, require_POST
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
import random
from account.models import UyeAdresi, Uye
from pages.models import Kategori
from payment.models import SessionTokens
from satis.models import Sepet, Siparis, SiparisSatiri
import logging
import random
logger = logging.getLogger(__name__)
import base64
import hashlib
import hmac
import json
import requests
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
@require_POST
def callback(request):
    if request.method != 'POST':
        return HttpResponse(str(''))

    post = request.POST

    merchant_key = b'zwuMXnMht326nSUn'
    merchant_salt = '2itjpGfzEKrTNmEo'

    hash_str = post['merchant_oid'] + merchant_salt + post['status'] + post['total_amount']
    hash_value = base64.b64encode(hmac.new(merchant_key, hash_str.encode(), hashlib.sha256).digest())
    data = SessionTokens.objects.get(user=request.user, active=True)
    if hash_value != post['hash']:
        return HttpResponse(str('PAYTR notification failed: bad hash'))

    if post['status'] == 'success':  # Ödeme Onaylandı
        data = SessionTokens.objects.get(temp=post['merchant_oid'])
        order = create_order(data.user, data.sepet, payment_id=post['merchant_oid'],
                             tutar=data.payment_amount)
        move_cart_items_to_order(data.sepet, order)
        update_cart_status(data.sepet, payment_id=post['merchant_oid'])
        update_token_status(data.sepet)
        """
        BURADA YAPILMASI GEREKENLER
        1) Siparişi onaylayın.
        2) Eğer müşterinize mesaj / SMS / e-posta gibi bilgilendirme yapacaksanız bu aşamada yapmalısınız.
        3) 1. ADIM'da gönderilen payment_amount sipariş tutarı taksitli alışveriş yapılması durumunda değişebilir. 
        Güncel tutarı post['total_amount'] değerinden alarak muhasebe işlemlerinizde kullanabilirsiniz.
        """
        print(request)
    else:
        """
        BURADA YAPILMASI GEREKENLER
        1) Siparişi iptal edin.
        2) Eğer ödemenin onaylanmama sebebini kayıt edecekseniz aşağıdaki değerleri kullanabilirsiniz.
        post['failed_reason_code'] - başarısız hata kodu
        post['failed_reason_msg'] - başarısız hata mesajı
        """
        print(request)

    return HttpResponse(str('OK'))
def paytr_payment(request):
    # API Entegrasyon Bilgileri
    merchant_id = '446373'
    merchant_key = b'zwuMXnMht326nSUn'
    merchant_salt = b'2itjpGfzEKrTNmEo'
    selected_address_id = request.POST.get('selectedAddress')
    selected_address = UyeAdresi.objects.get(id=selected_address_id)
    user = request.user
    selected_user = Uye.objects.get(email=user.email)
    user_ip = get_client_ip(request)
    if user_ip == '127.0.0.1':
            user_ip = '78.174.127.25'

    user_cart = get_object_or_404(Sepet, user=user, durum=Sepet.HAZIRLIKTA)
    cart_items = user_cart.sepetsatiri_set.all()
    context = dict()
    buyer = {
        'id': selected_user.id,
        'name': selected_user.isim,
        'surname': selected_user.soyisim,
        'gsmNumber': selected_address.tel,
        'email': selected_user.email,
        'identityNumber': selected_user.tc,
        'lastLoginDate': user.date_joined.strftime('%Y-%m-%d %H:%M:%S'),
        'registrationDate': user.date_joined.strftime('%Y-%m-%d %H:%M:%S'),
        'registrationAddress': selected_address.adres,
        'ip': user_ip,
        'city': selected_address.il,
        'country': 'Turkey',
        'zipCode': selected_address.posta_kodu
    }

    address = {
        'contactName': selected_address.isim,
        'city': selected_address.il,
        'country': 'Turkey',
        'address': selected_address.adres,
        'zipCode': selected_address.posta_kodu
    }
    basket_items = []
    total_amount = 0
    temp = random.randint(0, 999999999)
    for cart_item in cart_items:
        basket_item = {
            'id': cart_item.urun.id,  # Use the appropriate field for the product ID
            'name': cart_item.urun.isim,
            'category1': KategoriEncoder().encode(cart_item.urun.kategori),  # Adjust as per your model structure
            'itemType': 'PHYSICAL',  # Adjust as per your model structure
            'price': str(cart_item.urun.fiyat * cart_item.adet),  # Convert the price to a string
        }
        basket_items.append(basket_item)
        total_amount += cart_item.fiyat
    total_amount = float(total_amount)
    # Müşteri Bilgileri
    email = selected_user.email
    payment_amount = int(total_amount * 100) # 9.99 için 9.99 * 100 = 999 gönderilmelidir.
    merchant_oid = str(user_cart.id)
    user_name = selected_user.isim + ' ' + selected_user.soyisim
    user_address = selected_address.adres
    user_phone = selected_address.tel
    user_basket = json.dumps(basket_items)  # Convert basket_items list to JSON string
    currency = 'TL'
    test_mode = '1'
    no_installment = '0'
    max_installment = '0'

    payment_amount_str = str(payment_amount)
    user_basket_str = json.dumps(basket_items)  # Convert basket_items list to JSON string
    temp_str = str(temp)
    # Construct the hash string
    hash_str = (
            merchant_id + user_ip + temp_str + email +
            payment_amount_str + user_basket_str +
            no_installment + max_installment +
            currency + test_mode
    )

    # Calculate the hash value
    paytr_token = base64.b64encode(hmac.new(merchant_key, hash_str.encode() + merchant_salt, hashlib.sha256).digest())
    order = SessionTokens.objects.create(
                        user=user,
                        sepet=user_cart,
                        token=paytr_token,
                        temp=temp_str,
                        payment_amount=payment_amount
                    )
    # PayTR API'ye gönderilecek parametreler
    params = {
        'merchant_id': merchant_id,
        'user_ip': user_ip,
        'merchant_oid': temp_str,
        'email': email,
        'paytr_token': paytr_token,
        'payment_amount': payment_amount,
        'user_basket': user_basket,
        'debug_on': '1',
        'no_installment': no_installment,
        'max_installment': max_installment,
        'user_name': user_name,
        'user_address': user_address,
        'user_phone': user_phone,
        'merchant_ok_url': 'https://laylabutik.com/payment/success',
        'merchant_fail_url': 'https://laylabutik.com/payment/failure',
        'timeout_limit': 30,  # Convert timeout_limit to integer
        'currency': currency,
        'test_mode': test_mode
    }
    print(params)
    # PayTR API'ye istek gönder
    result = requests.post('https://www.paytr.com/odeme/api/get-token', params)
    print(result)
    response = json.loads(result.text)
    print(response)
    if response['status'] == 'success':
        # Ödeme token'ını al
        token = response['token']

        # Ödeme formunu göstermek için HTML kodunu oluştur
        html = f"""
        <script src="https://www.paytr.com/js/iframeResizer.min.js"></script>
        <iframe src="https://www.paytr.com/odeme/guvenli/{token}" id="paytriframe" frameborder="0" scrolling="no" style="width: 100%;"></iframe>
        <script>iFrameResize('{token},#paytriframe');</script>
        """

        return HttpResponse(html)
    else:
        return HttpResponse(str(response))

# api_key = 'sandbox-F4nYkhziRRvqnjhMV9u0IQMrekBwalBk'
# secret_key = 'sandbox-DxkGCnUj3dH9hglAI9MZrU7T4uFdd1jg'
# base_url = 'https://api.iyzipay.com'
#
# options = {
#     'api_key': api_key,
#     'secret_key': secret_key,
#     'base_url': base_url
# }
# sozlukToken = list()
# random_value = random.randint(100000000, 999999999)
# conversationId = random_value

def index(request):
    context = dict()

    context['message'] = 'Django ile Iyzico Ödeme Entegrasyonu'

    template = 'payment/index.html'
    return render(request, template, context)


class KategoriEncoder(DjangoJSONEncoder):
    def default(self, obj):
        if isinstance(obj, Kategori):
            # Convert your Kategori object to a dictionary or any serializable format
            return {
                'id': obj.id,
                'name': obj.baslik,
            }
        return super().default(obj)


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0].strip()
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


# def payment(request):
#     selected_address_id = request.POST.get('selectedAddress')
#     # Do something with the selected_address_id, such as retrieving the address from the database
#     selected_address = UyeAdresi.objects.get(id=selected_address_id)
#     user = request.user
#     selected_user = Uye.objects.get(email=user.email)
#     user_ip = get_client_ip(request)
#     # Rest of your payment logic goes here
#     user_cart = get_object_or_404(Sepet, user=user, durum=Sepet.HAZIRLIKTA)
#     cart_items = user_cart.sepetsatiri_set.all()
#     context = dict()
#     buyer = {
#         'id': selected_user.id,
#         'name': selected_user.isim,
#         'surname': selected_user.soyisim,
#         'gsmNumber': selected_address.tel,
#         'email': selected_user.email,
#         'identityNumber': selected_user.tc,
#         'lastLoginDate': user.date_joined.strftime('%Y-%m-%d %H:%M:%S'),
#         'registrationDate': user.date_joined.strftime('%Y-%m-%d %H:%M:%S'),
#         'registrationAddress': selected_address.adres,
#         'ip': user_ip,
#         'city': selected_address.il,
#         'country': 'Turkey',
#         'zipCode': selected_address.posta_kodu
#     }
#
#     address = {
#         'contactName': selected_address.isim,
#         'city': selected_address.il,
#         'country': 'Turkey',
#         'address': selected_address.adres,
#         'zipCode': selected_address.posta_kodu
#     }
#     basket_items = []
#     total_amount = 0
#     for cart_item in cart_items:
#         basket_item = {
#             'id': cart_item.urun.id,  # Use the appropriate field for the product ID
#             'name': cart_item.urun.isim,
#             'category1': KategoriEncoder().encode(cart_item.urun.kategori),  # Adjust as per your model structure
#             'itemType': 'PHYSICAL',  # Adjust as per your model structure
#             'price': str(cart_item.urun.fiyat * cart_item.adet),  # Convert the price to a string
#         }
#         basket_items.append(basket_item)
#         total_amount += cart_item.fiyat
#     total_amount = float(total_amount)
#
#     payment_request = {
#         'locale': 'tr',
#         'conversationId': str(conversationId),
#         'price': total_amount,
#         'paidPrice': total_amount,
#         'currency': 'TRY',
#         'basketId': user_cart.id,
#         'paymentGroup': 'PRODUCT',
#         "callbackUrl": "https://www.laylabutik.com/payment/result/",
#         "enabledInstallments": ['2', '3', '6', '9'],
#         'buyer': buyer,
#         'shippingAddress': address,
#         'billingAddress': address,
#         'basketItems': basket_items,
#         'userId': user_cart.id
#         # 'debitCardAllowed': True
#     }
#     request.session['user_id'] = selected_user.id
#
#     try:
#         checkout_form_initialize = iyzipay.CheckoutFormInitialize().create(payment_request, options)
#         content = checkout_form_initialize.read().decode('utf-8')
#         json_content = json.loads(content)
#         print(type(json_content))
#         print(json_content["checkoutFormContent"])
#         print(json_content["token"])
#         token = json_content.get("token")
#         request.session['q'] = token
#         print(token)
#
#         if token:
#             print(token)
#             sozlukToken.append(json_content["token"])
#             order = SessionTokens.objects.create(
#                 user=user,
#                 sepet=user_cart,
#                 token=token
#             )
#             request.session['payment_token'] = json_content["token"]
#             request.session['user_id'] = selected_user.id
#             request.session['cart_id'] = user_cart.id
#             request.session.save()
#             logger.info("Token added to sozlukToken: %s", json_content["token"])
#             return HttpResponse(json_content["checkoutFormContent"])
#         else:
#             # Token alınamadıysa
#             print("Error: Token not found in the response")
#             logger.error("Error: Token not found in the response")
#             # Handle this case as needed, maybe redirect to an error page
#             return HttpResponse("Error: Token not found in the response")
#
#     except json.decoder.JSONDecodeError as e:
#         print("Error decoding JSON:", e)
#         logger.exception("An error occurred during payment")
#         print("Response content:", content)
#         # Handle the error as needed
#         return HttpResponse("Error decoding JSON")
#     except Exception as e:
#         print("An error occurred during payment:", e)
#         # Handle other exceptions as needed
#         return HttpResponseServerError("Internal Server Error during payment")



# @require_http_methods(['POST'])
# @csrf_exempt
# def result(request):
#     context = dict()
#     url = request.META.get('index')
#     token = request.session.get('payment_token')
#     user_id = request.session.get('user_id')
#     cart_id = request.session.get('cart_id')
#     q = request.session.get('q', '')
#     print(q)
#     data = SessionTokens.objects.get(user=request.user, active=True,token=q)
#     print(data)
#     request = {
#         'locale': 'tr',
#         'conversationId': str(conversationId),
#         'token': q
#     }
#     checkout_form_result = iyzipay.CheckoutForm().retrieve(request, options)
#     print("************************")
#     print(type(checkout_form_result))
#     result = checkout_form_result.read().decode('utf-8')
#     print("************************")
#     # print(sozlukToken[0])  # Form oluşturulduğunda
#     print("************************")
#     print("************************")
#     sonuc = json.loads(result, object_pairs_hook=list)
#     # print(sonuc[0][1])  # İşlem sonuç Durumu dönüyor
#     # print(sonuc[5][1])   # Test ödeme tutarı
#     print("************************")
#     for i in sonuc:
#         print(i)
#     print("************************")
#     # print(sozlukToken)
#     print("************************")
#     if sonuc[0][1] == 'success':
#         context['success'] = 'Başarılı İŞLEMLER'
#         success_url = reverse('success') + f'?sonuc={sonuc}'
#         return HttpResponseRedirect(success_url)
#
#
#
#     elif sonuc[0][1] == 'failure':
#         context['failure'] = 'Başarısız'
#         success_url = reverse('failure')
#         return HttpResponseRedirect(success_url)
#
#     return HttpResponse(url)
#
def update_cart_status(user_cart, payment_id):
    user_cart.durum = Sepet.TAMAMLANDI  # Assuming you have a constant like TAMAMLANDI for completed status
    user_cart.guncelleme_tarihi = datetime.now()
    user_cart.order_id = payment_id
    user_cart.save()
    return
def update_token_status(user_cart):
    temp = SessionTokens.objects.get(sepet=user_cart)
    temp.active= False
    temp.save()
    return

def move_cart_items_to_order(user_cart, order):
    cart_items = user_cart.sepetsatiri_set.all()
    for cart_item in cart_items:
        order_item = SiparisSatiri.objects.create(
            siparis=order,
            urun=cart_item.urun,
            adet=cart_item.adet,
            birim_fiyat=cart_item.urun.fiyat,
            durum='H'
        )
        # Adjust stock quantity
        cart_item.urun.stok_durumu -= cart_item.adet
        cart_item.urun.save()
    return


def create_order(user, user_cart, payment_id, tutar):
    odeme_tipi_mapping = {
        'CREDIT_CARD': 'K',
        'Havale': 'H',
        'KAPIDA_ODEME_KREDI_KARTI': 'KK',
        'KAPIDA_ODEME_NAKIT': 'KN',
    }
    sepet_instance = get_object_or_404(Sepet, id=user_cart.id)
    print(sepet_instance)
    order = Siparis.objects.create(
        user=user,
        sepet=sepet_instance,
        tarih=timezone.now(),
        order_id=payment_id,
        durum='S',
        toplam_tutar=tutar,
        kargo_ucreti=50
    )
    return order


def success(request):
    context = dict()
    template = 'payment/ok.html'
    context['success'] = 'İşlem Başarılı'
    user = request.user
    sonuc_str = request.GET.get('sonuc', None)
    if sonuc_str:
        sonuc_str = sonuc_str[1:-1]

        # Tuple'ları içeren string'i ayırın
        tuple_str_list = sonuc_str.split("), (")

        # Her bir tuple'ı bir string olarak ele alıp, uygun bir formata getirin
        for i in range(len(tuple_str_list)):
            tuple_str_list[i] = tuple_str_list[i].replace("(", "").replace(")", "")

        # Her bir tuple string'ini bir tuple nesnesine dönüştürün
        sonuc_list = [tuple(item.split(", ")) for item in tuple_str_list]

        # Şimdi, sonuc_list içinde tuple'lar içeren bir liste elde ettiniz

        user_cart = get_object_or_404(Sepet, user=user, durum=Sepet.HAZIRLIKTA)
        temp =sonuc_list[7][1]
        temp = temp.strip("'")
        temp1 =sonuc_list[5][1]
        temp1 = temp1.strip("'")
        value_float = int(float(temp))
        value_float1 = int(float(temp1))
        order = create_order(user, user_cart, payment_id=value_float, card_type=sonuc_list[13][1],
                             tutar=value_float1, )
        move_cart_items_to_order(user_cart, order)
        update_cart_status(user_cart, payment_id=value_float)
        update_token_status(user_cart)
        return render(request, template, context)
    else:
        return render(request, template, context)


def fail(request):
    context = dict()
    context['fail'] = 'İşlem Başarısız'
    template = 'payment/fail.html'
    return render(request, template, context)
