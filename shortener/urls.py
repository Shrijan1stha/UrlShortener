from django.urls import path
from .views import home, login, register, urlShortener, urlCreate, shortener, urldelete, logout_view, generate_qrcode, urledit

urlpatterns = [
    path('', home, name = 'home'),
    path('login/', login, name='login'),
    path('register/', register, name='register'),
    path('logout/', logout_view, name='logout'),
    path('url/list/', urlShortener, name='urllist'),
    path('url/create/', urlCreate, name='urlcreate'),
    path('<str:id>/', shortener, name='shortener'),
    path('url/delete/<int:pk>/', urldelete, name='delete'),
    path('url/qrcode/<int:pk>/', generate_qrcode, name='qrcode'),
    path('url/edit/<int:pk>/', urledit, name='edit')
]