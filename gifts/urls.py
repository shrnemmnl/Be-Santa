from django.urls import path
from . import views

app_name = 'gifts'

urlpatterns = [
    path('be-santa/', views.be_santa_view, name='be_santa'),
    path('success/', views.gift_success_view, name='gift_success'),
    path('receive-gift/', views.receive_gift_view, name='receive_gift'),
]
