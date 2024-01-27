from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django import forms
from import_export.admin import ImportExportModelAdmin

from satis.admin import SiparisSatiriInlineAdmin
from satis.models import Siparis
from .models import Uye, Il, Ilce, Mahalle, UyeAdresi
from .resource import IlResource, IlceResource, MahalleResource


class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = Uye
        fields = '__all__'
        # fields = ('email', 'isim', 'soyisim')

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user
class UyeAdresiInline(admin.TabularInline):
    model = UyeAdresi
    extra = 0
    fields = ('id', 'baslik', 'ilce', 'il', 'adres', 'tel')

    def get_readonly_fields(self, request, obj=None):
        return list(set([field.name for field in self.opts.local_fields] +
                        [field.name for field in self.opts.local_many_to_many]))

    def has_delete_permission(self, request, obj=None):
        return False

    def get_queryset(self, request):
        return super(UyeAdresiInline, self).get_queryset(request).filter(silindi=False).all()
    pass

class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField(label=("Password"),
                                         help_text=("Raw passwords are not stored, so there is no way to see "
                                                    "this user's password, but you can change the password "
                                                    "using <a id=\"password\" href=\"#\">this form</a>."))

    class Meta:
        model = Uye
        fields = '__all__'

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]

class SiparisInline(admin.TabularInline):
    model = Siparis
    # fields = ('tarih','odeme_tipi','siparis_tutari', 'durum', )
    inlines = [SiparisSatiriInlineAdmin]
    extra = 0

    def get_readonly_fields(self, request, obj=None):
        return list(set([field.name for field in self.opts.local_fields] +
                        [field.name for field in self.opts.local_many_to_many]))

class UyeAdmin(UserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    model = Uye
    list_display = ('email', 'isim', 'soyisim', 'is_staff', 'is_active')
    list_filter = ('is_staff', 'is_active')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('isim', 'soyisim',)}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'isim', 'soyisim', 'is_staff', 'is_active')}
         ),
    )
    search_fields = ('email', 'isim', 'soyisim')
    ordering = ('email',)
    inlines = [UyeAdresiInline, SiparisInline]

admin.site.register(Uye, UyeAdmin)


class IlAdmin(ImportExportModelAdmin):
    resource_class = IlResource
    pass


class IlceAdmin(ImportExportModelAdmin):
    list_filter = ['il']
    search_fields = ['isim']
    list_display = ['il', 'isim', 'kod']
    resource_class = IlceResource
    pass


class MahalleAdmin(ImportExportModelAdmin):
    list_filter = ['ilce']
    search_fields = ['isim', 'ilce__isim', 'ilce__il__isim']
    list_display = ['kod', 'isim', 'ilce',]
    resource_class = MahalleResource



class UyeAdresiAdmin(admin.ModelAdmin):
    pass

admin.site.register(Il, IlAdmin)
admin.site.register(Ilce, IlceAdmin)
admin.site.register(Mahalle, MahalleAdmin)