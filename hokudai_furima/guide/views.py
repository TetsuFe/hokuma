from django.shortcuts import render

# Create your views here.
def sell_guide(request):
    return render(request, 'guide/sell_guide.html')


def buy_guide(request):
    return render(request, 'guide/buy_guide.html')
