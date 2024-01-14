import datetime

from django.db.models import Count, DecimalField, F, Sum, Value
from django.db.models.functions import Coalesce
from import_export import fields, resources
from satis.models import Siparis, SiparisSatiri

class SiparisSatiriResource(resources.ModelResource):
    email = fields.Field(column_name='email', readonly=True)
    odeme_tipi = fields.Field(column_name='odeme_tipi', readonly=True)
    banka = fields.Field(column_name='banka', readonly=True)
    banka_id = fields.Field(column_name='banka_id', readonly=True)
    kdv_haric_fiya = fields.Field(column_name='kdv_haric_fiyat', readonly=True)
    kdv_dahil_fiyat = fields.Field(column_name='kdv_dahil_fiyat', readonly=True)
    kdv_tutari = fields.Field(column_name='kdv_tutari', readonly=True)

    def dehydrate_kdv_haric_fiyat(self, siparissatiri):
        return '%s' % (siparissatiri.kdv_haric_fiyat())

    def dehydrate_kdv_dahil_fiyat(self, siparissatiri):
        return '%s' % (siparissatiri.kdv_dahil_fiyat())

    def dehydrate_kdv_tutari(self, siparissatiri):
        return '%s' % (siparissatiri.kdv_tutari())

    def dehydrate_email(self, siparissatiri):
        return '%s' % (siparissatiri.siparis.user.email)

    def dehydrate_odeme_tipi(self, siparissatiri):
        return '%s' % (siparissatiri.siparis.get_odeme_tipi_display())

    def dehydrate_banka(self, siparissatiri):
        banka = ''
        if siparissatiri.siparis.odeme_tipi == 'H':
            banka = siparissatiri.siparis.havale_yapilacak_hesap.isim
        if siparissatiri.siparis.odeme_tipi == 'K':
            banka = siparissatiri.siparis.kredi_karti_pos.isim
        return banka

    def dehydrate_banka_id(self, siparissatiri):
        return '%s' % (siparissatiri.siparis.order_id)

    def get_queryset(self):
        return super(SiparisSatiriResource, self).queryset().filter(self.email == 'test').all()

    class Meta:
        model = SiparisSatiri
        fields = ('siparis', 'sira', 'urun__isim', 'adet',
                  'kalan_adet', 'ogrenci_ismi', 'ogrenci_cinsiyet')


class SiparisResource(resources.ModelResource):
    siparis_id = fields.Field(column_name='siparis_id', readonly=True)
    # ogrenci=fields.Field(column_name='ogrenci', readonly=True)
    uye = fields.Field(column_name='uye', readonly=True)
    email = fields.Field(column_name='email', readonly=True)
    # teslimat_adresi=fields.Field(column_name='teslimat_adresi', readonly=True)
    # fatura_adresi=fields.Field(column_name='fatura_adresi', readonly=True)
    odeme_tipi = fields.Field(column_name='odeme_tipi', readonly=True)
    banka = fields.Field(column_name='banka', readonly=True)
    banka_id = fields.Field(column_name='banka_id', readonly=True)
    vade = fields.Field(column_name='vade', readonly=True)
    tutar = fields.Field(column_name='tutar', readonly=True)
    durum = fields.Field(column_name='durum', readonly=True)
    tarih = fields.Field(column_name='tarih', readonly=True)
    satir_sayisi = fields.Field(column_name='satir_sayisi', readonly=True)
    toplam_adet = fields.Field(column_name='toplam_adet', readonly=True)
    aciklama = fields.Field(column_name='aciklama', readonly=True)

    def dehydrate_siparis_id(self, siparis):
        return '%s' % (siparis['id'])


    # def dehydrate_ogrenci(self, siparis):
    #     satirlar=siparis.siparissatiri_set.filter(sinif_ismi__isnull=False).all()
    #     ogrenciler=satirlar.values('ogrenci_ismi','ogrenci_cinsiyet').order_by().annotate(Count('ogrenci_ismi'),Count('ogrenci_cinsiyet'))
    #     return "<br />".join(["%s - (%s)" % (item['ogrenci_ismi'],item['ogrenci_cinsiyet']) for item in ogrenciler])

    def dehydrate_uye(self, siparis):
        return '%s %s' % (siparis['user__isim_soyisim'])

    def dehydrate_email(self, siparis):
        return '%s' % (siparis['user__email'])

    # def dehydrate_teslimat_adresi(self, siparis):
    #     return '%s' % (siparis.teslimat_adresi.adres)
    #
    # def dehydrate_fatura_adresi(self, siparis):
    #     return '%s' % (siparis.fatura_adresi.adres)

    def dehydrate_odeme_tipi(self, siparis):
        odeme_tipi = "Yok"
        for k, v in Siparis.ODEME_TIPLERI:
            if k == siparis['odeme_tipi']:
                odeme_tipi = v
                break
        return odeme_tipi

    def dehydrate_banka(self, siparis):
        banka = siparis['kredi_karti_pos__isim']
        if siparis['odeme_tipi'] == 'H':
            banka = siparis['havale_yapilacak_hesap__isim']
        return banka

    def dehydrate_banka_id(self, siparis):
        return '%s' % (siparis['order_id'])

    def dehydrate_vade(self, siparis):
        return '%s' % (
            siparis['kredi_karti_vade_secenegi__vade'] if siparis['kredi_karti_vade_secenegi__vade'] else '')

    def dehydrate_tutar(self, siparis):
        return '%s' % (siparis['tutar'])

    def dehydrate_durum(self, siparis):
        durum = "Yok"
        for k, v in Siparis.SIPARIS_DURUMLARI:
            if k == siparis['durum']:
                durum = v
                break
        return '%s' % (durum)

    def dehydrate_tarih(self, siparis):
        return '%s' % (siparis['tarih'])

    def dehydrate_satir_sayisi(self, siparis):
        return '%s' % (siparis['satir_sayisi'])

    def dehydrate_toplam_adet(self, siparis):
        return '%s' % (siparis['adet'])

    def dehydrate_aciklama(self, siparis):
        return '%s' % (siparis['kargo_notu'])

    def export(self, queryset=None, *args, **kwargs):
        queryset = queryset or Siparis.objects.filter(tarih__gte=datetime.date(2021, 5, 31))
        queryset = queryset\
            .select_related('user')\
            .values('id',)\

        return super(SiparisResource, self).export(queryset, *args, **kwargs)

    class Meta:
        export_order = ('siparis_id', 'uye', 'email',
                        'toplam_adet',)
