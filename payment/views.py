from datetime import datetime

from django.utils import timezone
from django.core.serializers.json import DjangoJSONEncoder
from django.shortcuts import render, get_object_or_404
import iyzipay
import json
# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
import requests
from django.contrib import messages
import pprint

from account.models import UyeAdresi, Uye
from pages.models import Kategori
from satis.models import Sepet, Siparis, SiparisSatiri

api_key = 'sandbox-etkBOaBAec7Zh6jLDL59Gng0xJV2o1tV'
secret_key = 'sandbox-uC9ysXfBn2syo7ZMOW2ywhYoc9z9hTHh'
base_url = 'sandbox-api.iyzipay.com'

options = {
    'api_key': api_key,
    'secret_key': secret_key,
    'base_url': base_url
}
sozlukToken = list()


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
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def payment(request):
    if request.method == 'POST':
        selected_address_id = request.POST.get('selectedAddress')

        # Do something with the selected_address_id, such as retrieving the address from the database
        selected_address = UyeAdresi.objects.get(id=selected_address_id)
        user = request.user
        selected_user = Uye.objects.get(email=user.email)
        user_ip = get_client_ip(request)
        # Rest of your payment logic goes here
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
        request = {
            'locale': 'tr',
            'conversationId': str(user_cart.id),
            'price': total_amount,
            'paidPrice': total_amount,
            'currency': 'TRY',
            'basketId': user_cart.id,
            'paymentGroup': 'PRODUCT',
            "callbackUrl": "http://localhost:8000/payment/result/",
            "enabledInstallments": ['2', '3', '6', '9'],
            'buyer': buyer,
            'shippingAddress': address,
            'billingAddress': address,
            'basketItems': basket_items,
            # 'debitCardAllowed': True
        }
    #
    try:
        checkout_form_initialize = iyzipay.CheckoutFormInitialize().create(request, options)
        content = checkout_form_initialize.read().decode('utf-8')
        json_content = json.loads(content)
        print(type(json_content))
        print(json_content["checkoutFormContent"])
        print("************************")
        print(json_content["token"])
        print("************************")
        sozlukToken.append(json_content["token"])
        return HttpResponse(json_content["checkoutFormContent"])

    except json.decoder.JSONDecodeError as e:
        print("Error decoding JSON:", e)
        print("Response content:", content)
        # Handle the error as needed
        return HttpResponse("Error decoding JSON")


@require_http_methods(['POST'])
@csrf_exempt
def result(request):
    user = request.user
    if user.is_authenticated:
        user_cart = get_object_or_404(Sepet, user=user, durum=Sepet.HAZIRLIKTA)

        context = dict()
        url = request.META.get('index')

        request = {
            'locale': 'tr',
            'conversationId': str(user_cart.id),
            'token': sozlukToken[0]
        }
        checkout_form_result = iyzipay.CheckoutForm().retrieve(request, options)
        print("************************")
        print(type(checkout_form_result))
        result = checkout_form_result.read().decode('utf-8')
        print("************************")
        print(sozlukToken[0])  # Form oluşturulduğunda
        print("************************")
        print("************************")
        sonuc = json.loads(result, object_pairs_hook=list)
        # print(sonuc[0][1])  # İşlem sonuç Durumu dönüyor
        # print(sonuc[5][1])   # Test ödeme tutarı
        print("************************")
        for i in sonuc:
            print(i)
        print("************************")
        print(sozlukToken)
        print("************************")
        if sonuc[0][1] == 'success':
            print(sonuc[7][1])
            user_cart = get_object_or_404(Sepet, user=user, durum=Sepet.HAZIRLIKTA)
            order = create_order(user, user_cart, payment_id=sonuc[7][1], card_type=sonuc[13][1], tutar=sonuc[5][1], )
            move_cart_items_to_order(user_cart, order)
            update_cart_status(user_cart, payment_id=sonuc[7][1])
            context['success'] = 'Başarılı İŞLEMLER'
            return HttpResponseRedirect(reverse('success'), context)

        elif sonuc[0][1] == 'failure':
            context['failure'] = 'Başarısız'
            return HttpResponseRedirect(reverse('failure'), context)

        return HttpResponse(url)
    else:
        return render(request, "index.html")


def update_cart_status(user_cart, payment_id):
    user_cart.durum = Sepet.TAMAMLANDI  # Assuming you have a constant like TAMAMLANDI for completed status
    user_cart.guncelleme_tarihi = datetime.now()
    user_cart.order_id = payment_id
    user_cart.save()
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


def create_order(user, user_cart, payment_id, card_type, tutar):
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
        odeme_tipi=odeme_tipi_mapping.get(card_type, ''),
        durum='S',
        toplam_tutar=tutar,
        kargo_ucreti=50
    )
    return order


def success(request):
    context = dict()
    context['success'] = 'İşlem Başarılı'

    template = 'payment/ok.html'
    return render(request, template, context)


def fail(request):
    context = dict()
    context['fail'] = 'İşlem Başarısız'

    template = '/fail.html'
    return render(request, template, context)
