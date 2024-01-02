from django import forms
from django.core.exceptions import ValidationError
from .models import Uye
from django.core.validators import EmailValidator


class LoginForm(forms.Form):
    email = forms.EmailField(max_length=100)
    password = forms.CharField(max_length=63, widget=forms.PasswordInput)

    def clean(self):
        # User Active Check
        try:
            uye = Uye.objects.get(email=self.cleaned_data["email"])
        except Uye.DoesNotExist:
            raise ValidationError("E-mail kaydı bulunamadı.")

        if uye.is_active:
            return self.cleaned_data
        else:
            raise ValidationError("Hesabınız aktif değildir. Lütfen iletişime geçiniz....")


class UyeKayitFormu(forms.Form):
    email = forms.CharField(widget=forms.EmailInput(attrs={
        'class': 'form-control',
        'placeholder': 'E-mail',
    }))

    isim_soyisim = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
    }))

    # dogum_gunu = forms.DateField(required=True)

    # cinsiyet = forms.CharField(required=True)

    cep_telefonu = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Cep Telefonu',
    }))

    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Parola',
    }))

    def clean_email(self):
        email = self.cleaned_data["email"]
        email_validator = EmailValidator()

        if Uye.objects.filter(email=email).exists():
            raise ValidationError("Bu e-mail ile önceden kayıt olunmuş.")

        try:
            email_validator(email)
        except ValidationError:
            raise ValidationError("Lütfen geçerli bir e-posta adresi girin.")

        return email

    def clean_cep_telefonu(self):
        cep_telefonu = self.cleaned_data["cep_telefonu"]
        if Uye.objects.filter(cep_telefonu=cep_telefonu).exists():
            raise ValidationError("Bu cep_telefonu ile önceden kayıt olunmuş.")
        return cep_telefonu

    def clean_password(self):
        password = self.cleaned_data["password"]
        if len(password) < 6:
            raise ValidationError("Parolanız en az 6 karakter olmalıdır.")
        return password

    def __uye_kaydi(self):
        uye = Uye.objects.create_user(
            email=self.cleaned_data['email'],
            isim_soyisim=self.cleaned_data['isim_soyisim'],
            password=self.cleaned_data["password"],
        )
        uye.cep_telefonu = self.cleaned_data["cep_telefonu"]
        return uye

    def save(self, commit=True):
        uye = self.__uye_kaydi()
        uye.save()
        return uye


class PasswordChangeForm(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput())

    def clean_password(self):
        password = self.cleaned_data["password"]
        if len(password) < 6:
            raise ValidationError("Parolanız en az 6 karakter olmalıdır.")
        return password

    def clean(self):
        try:
            uye = Uye.objects.get(email=self.data["email"])
        except Uye.DoesNotExist:
            raise ValidationError("Bu email'e sahip bir kullanıcı bulunamadı...")

    def save(self, commit=True):
        uye = Uye.objects.get(email=self.data["email"])
        uye.set_password(self.data["password"])
        uye.save()
        return uye


class AccountInfoChangeForm(forms.Form):
    isim_soyisim = forms.CharField(widget=forms.TextInput())
    cep_telefonu = forms.CharField(widget=forms.TextInput())

    # giren üyenin cep telefonu kendisinin ki ise kontrole girmeyecek farklı ise diğerleri ile karşılaştırılıcak
    def clean_cep_telefonu(self):
        uye = Uye.objects.get(email=self.data["email"])
        cep_telefonu = self.cleaned_data["cep_telefonu"]
        if uye.cep_telefonu != cep_telefonu:
            if Uye.objects.filter(cep_telefonu=cep_telefonu).exists():
                raise ValidationError("Bu cep_telefonu ile önceden kayıt olunmuş.")
        return cep_telefonu

    def clean(self):
        try:
            uye = Uye.objects.get(email=self.data["email"])
        except Uye.DoesNotExist:
            raise ValidationError("Bu email'e sahip bir kullanıcı bulunamadı...")

    def save(self, commit=True):
        uye = Uye.objects.get(email=self.data["email"])
        uye.isim_soyisim = (self.data["isim_soyisim"])
        uye.cep_telefonu = (self.data["cep_telefonu"])
        uye.save()
        return uye
