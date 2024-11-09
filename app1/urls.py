# urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),  # Home page for coffee orders
    path('success/', views.success_view, name='success'),  # Success page after payment
]
