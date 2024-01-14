from django.contrib import admin
from django.db.models import Count
from django.utils.safestring import mark_safe
from import_export.admin import ImportExportModelAdmin
from satis.models import SiparisSatiri, SepetSatiri, Siparis, Sepet
from satis.resource import SiparisSatiriResource, SiparisResource
import datetime
from django.urls import reverse
# Register your models here.
class SiparisSatiriInlineAdmin(admin.StackedInline):
    model = SiparisSatiri
    extra = 0
    readonly_fields = ('urun', 'sira', 'adet', 'kalan_adet', 'birim_fiyat',
                       'ogrenci_ismi', 'tc_kimlik_no',
                       'durum')
    can_delete = False

    def get_queryset(self, request):
        return super(SiparisSatiriInlineAdmin, self) \
            .get_queryset(request) \
            .select_related('urun', 'fatura') \
            .order_by('-durum').all()

class SiparisAdmin(ImportExportModelAdmin):
    list_filter = ['durum', 'odeme_tipi',]
    list_display = ['id']
    search_fields = ['id',
                     'user__isim_soyisim']

    resource_class = SiparisResource
    inlines = [SiparisSatiriInlineAdmin]

    @mark_safe
    def musteri(self, obj):
        return '<a href="%s">%s</a>' % (
            reverse('admin:uyelik_uye_change', args=(obj.user.id,), current_app=self.admin_site.name),
            obj.user.get_full_name())

    musteri.short_description = u'Müşteri İsmi'
    musteri.allow_tags = True

    @mark_safe
    def kargo_takip_numaralari(self, obj):
        return "<br />".join(['<a target="_blank" href="%s">%s</a>' % (
            siparis_faturasi.kargo_url.replace("('", "").replace("',)", ""),
            siparis_faturasi.kargo_takip_no.replace("('", "").replace("',)", "")
        ) if siparis_faturasi.kargo_takip_no else "--" for siparis_faturasi in obj.siparisfaturasi_set.all()])

    kargo_takip_numaralari.allow_tags = True

    @mark_safe
    def ogrenci_ismi(self, obj):
        satirlar = obj.siparissatiri_set.all()
        ogrenciler = satirlar.values().order_by().annotate(
            Count('ogrenci_ismi'))
        return "<br />".join(["%s - (%s)" % (item['ogrenci_ismi']) for item in ogrenciler])

    ogrenci_ismi.allow_tags = True

    def siparis_durumu(self, obj):
        return obj.get_durum_display()

    class Media:
        css = {
            'all': [
                '/static/admin/css/collapse.css',
                '/static/admin/css/admindatefilter.css',
            ]
        }
        js = [
            '/static/admin/js/siparis.js',
            '/static/admin/js/collapse.js',
        ]

    def suit_row_attributes(self, obj, request):
        satirlar = obj.siparissatiri_set.all()
        if len(satirlar.filter(durum='T')) == len(satirlar):
            return {'class': 'success'}

        if len(satirlar.filter(durum='F')) == len(satirlar):
            return {'class': 'warning'}

        if len(satirlar.filter(durum='K')) == len(satirlar):
            return {'class': 'info'}

        if len(satirlar.filter(durum='I')) == len(satirlar) or obj.durum == 'I':
            return {'class': 'error'}

    def get_queryset(self, request):
        return super().get_queryset(request).filter(tarih__gte=datetime.date.today() - datetime.timedelta(days=90)) \
            .select_related('sepet', 'user',).all()

    def has_delete_permission(self, request, obj=None):
        return False

    def save_model(self, request, obj, form, change):
        obj.save()
        # if obj.odeme_tipi == 'H' and form.cleaned_data['durum'] == 'G':
        #     subject = 'Havale Ödemesi'
        #     from_email = 'bilgi@okulsepeti.com.tr'
        #     to = 'siparis@okulsepeti.com.tr'
        #     text_content = u'%s nolu siparişin ödemesi gelmiştir.' % (unicode(obj.pk))
        #     msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
        #     msg.send()

    pass


class SiparisSatiriAdmin(ImportExportModelAdmin):
    list_display = [
        'sira', 'siparis', 'get_user', 'urun', 'adet',
        'kalan_adet', 'birim_fiyat', 'durum', 'ogrenci_ismi',

    ]

    def get_user(self, obj):
        return obj.siparis.user

    get_user.short_description = 'Muşteri'


    search_fields = [
        'siparis__pk', 'urun__kod', 'urun__isim',
        'ogrenci_ismi', 'urun__pk'
    ]

    list_filter = [
        'siparis__durum',
        'siparis__odeme_tipi',
    ]
    sortable_field_name = "siparis"
    resource_class = SiparisSatiriResource

    def has_delete_permission(self, request, obj=None):
        return False

    def get_queryset(self, request):
        return super(SiparisSatiriAdmin, self).get_queryset(request).filter(
            siparis__tarih__gt=datetime.date.today() - datetime.timedelta(days=90),
            siparis__isnull=False) \
            .select_related('siparis', 'siparis__user').all()

    pass

class SepetSatiriInlineAdmin(admin.StackedInline):
    model = SepetSatiri
    extra = 0


class SepetAdmin(ImportExportModelAdmin):
    list_display = ['id', 'user', 'tarih', 'degisim']
    raw_id_fields = ('user',)
    readonly_fields = ('vade_ucreti', 'order_id', 'trans_id', 'banka_3d_onay_tarihi', 'banka_odeme_tarihi')
    search_fields = ['id',
                     'user__isim_soyisim',]

    inlines = [SepetSatiriInlineAdmin]

admin.site.register(Siparis, SiparisAdmin)
admin.site.register(SiparisSatiri, SiparisSatiriAdmin)
admin.site.register(Sepet, SepetAdmin)