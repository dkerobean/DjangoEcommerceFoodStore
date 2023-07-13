from django.urls import path
from . import views


urlpatterns = [
    path('index/', views.admin_dashboard, name="admin-dashboard" ),
]
