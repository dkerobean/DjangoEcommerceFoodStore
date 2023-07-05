from django.shortcuts import render

def index_page(request):
    
    
    return render(request, 'frontend/ui/index.html')


def shop_page(request):
    
    
    return render(request, 'frontend/ui/shop.html')


def about_page(request):
    
    return render(request, 'frontend/ui/about.html')


def contact_page(request):
    
    return render(request, 'frontend/ui/contact.html')