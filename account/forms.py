from django import forms
from django.core.exceptions import ValidationError
from .models import Uye, UyeAdresi
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

    isim = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
    }))

    soyisim = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
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

    def clean_password(self):
        password = self.cleaned_data["password"]
        if len(password) < 6:
            raise ValidationError("Parolanız en az 6 karakter olmalıdır.")
        return password

    def __uye_kaydi(self):
        uye = Uye.objects.create_user(
            email=self.cleaned_data['email'],
            isim=self.cleaned_data['isim'],
            soyisim=self.cleaned_data['soyisim'],
            password=self.cleaned_data["password"],
        )
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
    isim = forms.CharField(widget=forms.TextInput())
    soyisim = forms.CharField(widget=forms.TextInput())
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
        uye.isim = (self.data["isim"])
        uye.soyisim = (self.data["soyisim"])
        uye.cep_telefonu = (self.data["cep_telefonu"])
        uye.save()
        return uye

class UyeAdresiForm(forms.ModelForm):
    class Meta:
        model = UyeAdresi  # Specify the model class
        exclude = ['user']

    baslik = forms.CharField(max_length=10, help_text=u'Ev, İş vb ..', label=u'Adres Başlığı')
    isim = forms.CharField(max_length=255, label=u'Alıcı İsmi')
    il = forms.CharField(max_length=1024, label=u'İl')
    ilce = forms.CharField(max_length=1024, label=u'İlçe')
    mahalle = forms.CharField(max_length=1024, label=u'Mahalle')
    tel = forms.CharField(max_length=16)
    posta_kodu = forms.CharField(max_length=5, required=False)
    adres = forms.CharField(widget=forms.Textarea, min_length=5)

    def clean_adres(self):
        data = self.cleaned_data['adres']
        data = ' '.join(data.split())
        return data

    def clean(self):
        cleaned_data = super().clean()
        isim = cleaned_data.get('isim')

        if len(isim) < 2:
            raise forms.ValidationError('Alıcı ismi çok kısa.')

        return cleaned_data
    def clean_tel(self):
        tel = self.cleaned_data['tel']
        no = tel.replace(' ', '').replace('(', '').replace(')', '').replace('_', '')
        if len(no) < 10 or no.startswith('0') or no.startswith('9'):
            raise forms.ValidationError(u"Lütfen telefon numaranızı doğru ve eksiksiz giriniz.")
        return tel

