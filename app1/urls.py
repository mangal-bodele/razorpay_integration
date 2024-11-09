from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', views.home_view, name='home'),  # Home page with the order form
    path('create-order/', views.create_order, name='create_order'),  # Endpoint to create a new order
    path('success/', views.success_view, name='success'),  # Payment success confirmation page
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
