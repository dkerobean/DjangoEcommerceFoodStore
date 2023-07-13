from django.shortcuts import render


def admin_dashboard(request):
    
    return render(request, 'admin_dashboard/index.html')



def admin_login(request):
    
    return render(request, 'admin_dashboard/auth/login.html')
