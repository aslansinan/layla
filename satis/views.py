from django.shortcuts import render, redirect, get_object_or_404

from account.models import UyeAdresi
from .models import Sepet, SepetSatiri
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib import messages

def get_kullanici_aktif_sepet(request):
    if request.user.is_authenticated:
        try:
            return Sepet.objects.filter(
                siparis__isnull=True, user_id=request.user.id, durum=Sepet.HAZIRLIKTA
            ).order_by('-id')[0]
        except IndexError:
            return None
    else:
        session_name = '__sepet_'
        if session_name in request.session:
            try:
                sepet_id = request.session.get(session_name)
                return Sepet.objects.get(pk=sepet_id)
            except Sepet.DoesNotExist:
                del request.session[session_name]
        return None
# Create your views here.
def sepetim(request):
    sepet = get_kullanici_aktif_sepet(request)
    q = 1
    request.session['q'] = q

    if sepet is not None:
        sepet_satirlari = sepet.sepetsatiri_set.order_by('pk').all()
    else:
        sepet_satirlari = None

    return render(request, 'satis/sepetim.html', {
        'sepet': sepet,
        'user': request.user,
        'sepet_satirlari': sepet_satirlari,
    })

def adres_secim(request):
    total_amount = request.POST.get('totalAmount')
    user = request.user
    adreses = UyeAdresi.objects.filter(user=request.user)
    q = request.session.get('q', '')
    print(q)

    return render(request, 'satis/adres_secim.html', {
        'user': request.user,
        'adreses': adreses,
        'total_amount':total_amount
    })

@login_required()
def sepete_ekle(request, urun_id):
    # Adet değerini request üzerinden al, eğer gelmemişse varsayılan olarak 1 kullan
    adet = int(request.GET.get('adet', 1))

    user_sepet, created = Sepet.objects.get_or_create(user=request.user, durum=Sepet.HAZIRLIKTA)

    sepet_satiri, created = SepetSatiri.objects.get_or_create(sepet=user_sepet, urun_id=urun_id, defaults={'adet': adet})
    if not created:
        sepet_satiri.adet += adet
        sepet_satiri.save()

    user_sepet.save()

    messages.success(request, 'Ürün sepete eklendi!')
    return redirect(request.META['HTTP_REFERER'])

def miktar_degistir(request, sepet_satiri_id, operation):
    try:
        sepet_satiri = get_object_or_404(SepetSatiri, id=sepet_satiri_id)
        if operation == 'arttir':
            sepet_satiri.adet += 1
        elif operation == 'azalt' and sepet_satiri.adet > 1:
            sepet_satiri.adet -= 1
        sepet_satiri.save()

        return JsonResponse({'success': True, 'adet': sepet_satiri.adet})
    except SepetSatiri.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Sepet satırı bulunamadı.'})

def sepetten_kaldir(request, sepet_satiri_id):
    try:
        sepet_satiri = SepetSatiri.objects.get(pk=sepet_satiri_id)
        sepet_satiri.delete()

        return JsonResponse({'success': True})
    except SepetSatiri.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Sepet satırı bulunamadı.'})

def sepeti_temizle(request):
    try:
        sepet = get_kullanici_aktif_sepet(request)
        sepet.sepet_temizle()

        return JsonResponse({'success': True})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})

def sepet_urun_adeti(request):
    try:
        aktif_sepet = get_kullanici_aktif_sepet(request)
        sepet_urun_adeti = aktif_sepet.sepet_urun_adeti() if aktif_sepet else 0
        data = {
            'sepet_urun_adeti': sepet_urun_adeti
        }
        return JsonResponse(data)
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})