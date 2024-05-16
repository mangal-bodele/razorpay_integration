from django.urls import path
from .views import *

urlpatterns =[
    path('home/',home_view,name='home'),
    path('success/',success_view,name='success'),
]