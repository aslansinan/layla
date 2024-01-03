import base64
import json

from django.conf import settings
from django.contrib.auth.decorators import user_passes_test
from django.core.mail import EmailMultiAlternatives
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib import messages
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from . import forms
from .forms import UyeKayitFormu
from django.http import JsonResponse
from http import HTTPStatus

from .models import Uye


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
def indexaccount(request):
    return render(request, 'account/index.html')


def login_request(request):
    message = ''
    if request.method == 'POST':
        datas = json.load(request)
        form = forms.LoginForm(datas["data"])
        if form.is_valid():
            user = authenticate(
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password'],
            )
            if user is not None:
                login(request, user)
                return JsonResponse({'success': '.'})
            else:
                return JsonResponse({"error": "Girilen e-mail veya şifre hatalıdır."},
                                    status=HTTPStatus.INTERNAL_SERVER_ERROR)
        else:
            return JsonResponse({"error": form.errors}, status=HTTPStatus.INTERNAL_SERVER_ERROR)
    return JsonResponse({"error": "Hata."}, status=HTTPStatus.INTERNAL_SERVER_ERROR)


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
            isim_soyisim = request.POST.get('isim_soyisim')
            password = request.POST.get('password')
            form = UyeKayitFormu({
                'email': email,
                'isim_soyisim': isim_soyisim,
                'password': password,
            })
            if form.is_valid():
                form.save()
                user = authenticate_user(email=email, password=password)
                print(user)
                if user is not None:
                    login(request, user)
                    return JsonResponse({'success': 'Kayıt başarılı bir şekilde yapıldı.'})
            else:
                return JsonResponse({"errors": form.errors}, status=HTTPStatus.INTERNAL_SERVER_ERROR)
        except json.JSONDecodeError:
            return JsonResponse({"errors": "Geçersiz JSON formatı"}, status=HTTPStatus.BAD_REQUEST)

    return JsonResponse({'error': 'Geçersiz istek'}, status=HTTPStatus.BAD_REQUEST)


@anonymous_required
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
        url = "https://penfest.com.tr/account/mail/change-password" + formatlama
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
        return redirect("index")
    else:
        return render(request, "account/sifremi_unuttum.html")


def logout_request(request):
    logout(request)
    return redirect("index")
