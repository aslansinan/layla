from django.shortcuts import render


# Create your views here.
def indexaccount(request):
    return render(request, 'account/index.html')
