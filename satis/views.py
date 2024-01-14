from django.shortcuts import render

from satis.models import Sepet


def get_kullanici_aktif_sepet(request):
    if request.user.is_authenticated:
        try:
            return Sepet.objects.filter(
                siparis__isnull=True, user_id=request.user.id
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

    if sepet is not None:
        sepet_satirlari = sepet.sepetsatiri_set.order_by('pk').all()
    else:
        sepet_satirlari = None

    return render(request, 'satis/sepetim.html', {
        'sepet': sepet,
        'user': request.user,
        'sepet_satirlari': sepet_satirlari,
    })
