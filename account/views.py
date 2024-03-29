import base64
import json

from django.conf import settings
from django.contrib.auth.decorators import user_passes_test, login_required
from django.core.mail import EmailMultiAlternatives
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib import messages
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from . import forms
from .forms import UyeKayitFormu, LoginForm, UyeAdresiForm

from .models import Uye, UyeAdresi
from satis.models import Siparis, SiparisSatiri


def anonymous_required(function=None, redirect_url=None):
    if not redirect_url:
        redirect_url = 'index'

    actual_decorator = user_passes_test(
        lambda u: u.is_anonymous,
        login_url=redirect_url
    )
    if function:
        return actual_decorator(function)
    return actual_decorator


# Create your views here.
def anasayfa(request):
    details = "account/index.html"
    adreses = UyeAdresi.objects.filter(user=request.user)
    orders = Siparis.objects.filter(user=request.user)
    print(orders)
    context = {
        'adreses': adreses,
        'orders': orders,
    }
    return render(request, details, context)


def login_request(request):
    message = ''
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        form = LoginForm({
            'email': email,
            'password': password,
        })
        if form.is_valid():
            user = authenticate(
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password'],
            )
            if user is not None:
                login(request, user)
                return redirect('index.html')
            else:
                error_message = "Girilen e-mail veya şifre hatalıdır."
                return render(request, 'index.html', {'error_message': error_message})
        else:
            return render(request, 'index.html', {'error_message': form.errors})
    return render(request, 'index.html', {'error_message': "Hata."})


def authenticate_user(email=None, password=None):
    User = get_user_model()
    try:
        user = User.objects.get(email=email)
        if user.check_password(password):
            return user
    except User.DoesNotExist:
        return None


def yeni_uye_kayit(request):
    if request.method == "POST":
        try:
            email = request.POST.get('email')
            isim = request.POST.get('isim')
            soyisim = request.POST.get('soyisim')
            password = request.POST.get('password')
            form = UyeKayitFormu({
                'email': email,
                'isim': isim,
                'soyisim': soyisim,
                'password': password,
            })
            if form.is_valid():
                form.save()
                user = authenticate_user(email=email, password=password)
                if user is not None:
                    login(request, user)
                    return redirect('index.html')
            else:
                return render(request, 'index.html', {'error_message': form.errors})
        except json.JSONDecodeError:
            return render(request, 'index.html', {'error_message': "geçersiz format"})
    return render(request, 'index.html', {'error_message': "Geçersiz istek."})


@login_required(login_url='/')
def yeni_adres_ekle(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = UyeAdresiForm(request.POST)
            if form.is_valid():
                new_address = form.save(commit=False)

                # Fetch the Uye instance based on the user's email
                uye_instance = Uye.objects.get(email=request.user.email)

                # Associate the fetched Uye instance with the address
                new_address.user = uye_instance
                new_address.save()
                return render(request, "account/index.html")
            else:
                for field, errors in form.errors.items():
                    print(f"Field: {field}, Errors: {', '.join(errors)}")
                # Form is not valid, render the form with errors
                return render(request, 'account/yeni_adres_ekle.html', {'form': form})
        else:
            form = UyeAdresiForm()

        return render(request, 'account/yeni_adres_ekle.html', {'form': form})
    else:
        return redirect('index.html')


def forget_password(request):
    if request.method == "POST":
        uye_email = request.POST.get("email")
        if uye_email:
            try:
                uye = Uye.objects.get(email=uye_email)
            except Uye.DoesNotExist:
                messages.error(request, "Bu email'e sahip kullanıcı bulunamadı...")
                return redirect("forget-password")
        else:
            return redirect("forget-password")

        mail_dict = dict()
        encoded = base64.b64encode(str(uye_email).encode('ascii'))
        formatlama = str(encoded).replace("'", "/")[1:]
        # url = "http://127.0.0.1:8000/account/mail/change-password" + formatlama
        url = "http://localhost:8000/account/mail/change-password" + formatlama
        mail_dict["hashed_url"] = url
        html_content = render_to_string('email-icerikleri/sifre-degistirme-mail.html', mail_dict)
        text_content = strip_tags(html_content)
        email = EmailMultiAlternatives(
            "Şifre Sıfırlama.",
            text_content,
            settings.POSTMARK_SENDER,
            [uye.email]
        )
        email.attach_alternative(html_content, "text/html")
        email.send()
        messages.success(request, "Şifre Sıfırlama Mailiniz Gönderildi...")
        return redirect("forget-password")
    else:
        return render(request, "account/şifremi_unuttum.html")


def mail_change_password(request, code):
    context = dict()

    if request.method == "POST":
        binary_mail = base64.b64decode(code).decode('utf-8')
        mail_str = str(binary_mail)
        form_datas = dict()
        form_datas["email"] = mail_str
        form_datas["password"] = request.POST.get("password")
        form = forms.PasswordChangeForm(form_datas)
        if form.is_valid():
            form.save()
            messages.success(request, "Şifreniz Başarılı Bir Şekilde Değiştirildi.")
            return redirect("index.html")
        else:
            return render(request, 'index.html', {'error_message': "Şifre değiştirilemedi lütfen tekrar deneyiniz..."})

    return render(request, "account/şifre_yenileme.html", context)


@login_required(login_url='/')
def change_password(request):
    if request.method == 'POST':
        new_password = request.POST.get('password')

        # Burada yeni şifrenin güvenlik kontrolleri ve kullanıcıya atanması yapılabilir
        if len(new_password) < 6:
            messages.error(request, 'Parolanız en az 6 karakter olmalıdır.')
            return render(request, "account/index.html")
        else:
            # Yeni şifreyi kullanıcıya atama işlemi burada gerçekleştirilebilir
            request.user.set_password(new_password)
            request.user.save()
            messages.success(request, 'Şifreniz başarıyla güncellendi.')
            return redirect("index.html")
    return redirect('index.html')


def logout_request(request):
    logout(request)
    return redirect('index.html')

def siparis_detay(request, siparis_id):
    siparis = get_object_or_404(Siparis, id=siparis_id)
    siparis_satiri = SiparisSatiri.objects.filter(siparis=siparis)

    context = {
        'siparis': siparis,
        'siparis_satiri': siparis_satiri
    }
    return render(request, 'account/siparis_detay.html', context)
