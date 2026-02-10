from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from rest_framework.response import Response
from .models import User, urlShort
import random
from django.db.models import F
from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny
from django.db import IntegrityError

# Create your views here.

@permission_classes([AllowAny])
def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(username=email, password=password)

        if user is not None:
            auth_login(request, user)
            # messages.success(request, 'Logged in successfully')
            return redirect('urllist')
        else:
            messages.error(request, 'Invalid credentials')
            return render(request, 'login.html')
    return render(request, 'login.html')

def register(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        if not email or not password:
            messages.error(request, 'Email and password are required')
            return render(request, 'register.html')

        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already registered')
            return render(request, 'register.html')

        user = User.objects.create_user(username=email, email=email, password=password)
        auth_login(request, user)
        return redirect("home")
    return render(request, 'register.html')

def logout_view(request):
    logout(request)
    return redirect('login')

def home(request):
    return render(request, 'home.html')

@login_required
def urlShortener(request):
    urls = urlShort.objects.filter(owner=request.user)
    data = {'urls':urls}
    return render(request, 'listurl.html', context=data )

@login_required
def urlCreate(request):
    if request.method == 'POST':
        long_url = request.POST.get('long_url')
        existing_url = urlShort.objects.filter(original_url=long_url, owner=request.user).first()
        short_link = ""
        a = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9']

        if existing_url:
            short_link=existing_url.short
        else:
                for i in range(1,7):
                    letters = random.randint(0, len(a) - 1)
                    let = a[letters]
                    short_link += let

                url = urlShort( original_url=long_url, short=short_link, owner=request.user)
                url.save()

        new_url = 'http://127.0.0.1:8000/' + short_link
        return render(request, 'create.html', {'newurl':new_url})
        
    return render(request, 'create.html')


def shortener(request, id):
    url_obj = get_object_or_404(urlShort, short=id)
    url_obj.click += 1
    url_obj.save()
    return redirect(url_obj.original_url)

@login_required
def urldelete(request,pk):
    url_obj = get_object_or_404(urlShort, id=pk, owner=request.user)
    url_obj.delete()
    return redirect('urllist')

@login_required
def generate_qrcode(request,pk):
    tree = urlShort.objects.filter(owner=request.user, id=pk)
    data = {'tree': tree}
    return render(request, 'qrcode.html', context=data)

def urledit(request,pk):
    url_obj = get_object_or_404(urlShort, id=pk)
    if request.method == 'POST':
        short = request.POST.get('short')
        try:
            url_obj.short = short
            url_obj.save()
            return redirect('urllist')
        except IntegrityError:
            messages.error(request, f'The short url {short} already exists')
    data = {'urls': url_obj}
    return render(request, 'edit.html', context=data)