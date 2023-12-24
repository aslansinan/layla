from django.contrib import admin
from django import forms
from django.contrib.auth.admin import UserAdmin
from import_export.admin import ExportMixin
from account.models import Uye
from django.contrib.auth.forms import ReadOnlyPasswordHashField


# Register your models here.
class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = Uye
        fields = ('email', 'isim_soyisim', 'cep_telefonu')

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField(label=("Password"),
                                         help_text=("Raw passwords are not stored, so there is no way to see "
                                                    "this user's password, but you can change the password "
                                                    "using <a id=\"password\" href=\"#\">this form</a>."))

    class Meta:
        model = Uye
        fields = '__all__'

    def clean_password(self):
        return self.initial["password"]

class UyeAdmin(ExportMixin, UserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    list_display = ['email', 'isim_soyisim', 'cep_telefonu', 'olusturma_tarihi']
    search_fields = ['email', 'isim_soyisim', 'cep_telefonu']
    list_filter = ['email', 'is_active', 'olusturma_tarihi']
    ordering = ('email',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Kişisel Bilgileri', {'fields': ('isim_soyisim', 'cep_telefonu')}),
        ('Yetkilendirme', {'fields': ('is_staff', 'is_superuser', 'is_active')}),
        ('Önemli Tarihler', {'fields': ('last_login',)}),
    )
    exclude = ('username',)

    class Media:
        js = [
            '/static/js/uyelik.js',
        ]


admin.site.register(Uye, UyeAdmin)