from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth import login as login_django
from django.contrib.auth.decorators import login_required
from django.core.validators import validate_email
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError


# Create your views here.
def cad(request):
    if request.method == 'GET':
        return render(request, 'cadastro.html')
    elif request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        try:
            validate_email(email)
        except ValidationError:
            return HttpResponse('ERRO AQUI HEIN (email)')
        try:
            validate_password(password)
        except ValidationError:
            return HttpResponse('ERRO AQUI HEIN (password)')

        user = User.objects.filter(username = username).first()
        if user:
            return HttpResponse('Já existe um usuario com esse nome')
        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()
        return HttpResponse('Cadastrado com sucesso')

def login(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    elif request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username = username, password = password)

        if user:
            login_django(request, user)
            return HttpResponse('Logado com sucesso!')
        else:
            return HttpResponse('Email ou senha inválidos')
    
@login_required(login_url='/acesso/login/')
def plataforma(request):
    return HttpResponse('Entrou na plataforma')