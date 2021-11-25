from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import auth

def create_user(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']

        if empty(name):
            #messages.error(request, 'O nome não pode ser vazio')
            return redirect('create_user')
        if empty(email):
            #messages.error(request, 'O email não pode ser vazio')
            return redirect('create_user')
        if empty(password) or empty(password2):
            #messages.error(request, 'A senha não pode ser vazia')
            return redirect('create_user')
        if not_equal_passwords(password, password2):
            #messages.error(request, 'As senhas não são iguais')
            return redirect('create_user')
        if User.objects.filter(email=email).exists():
            #messages.error(request, 'Usuário já cadastrado')
            return redirect('create_user')
        if User.objects.filter(username=name).exists():
            #messages.error(request, 'Usuário já cadastrado')
            return redirect('create_user')
            
        user = User.objects.create_user(username=name, email=email, password=password)
        user.save()
        #messages.success(request, 'Cadastro realizado com sucesso')
        return redirect('index')
        
    return render(request, 'users/create_user.html')

def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password_user']
        if empty(email) or empty(password):
            #messages.error(request, 'Os campos email e password não podem ficar em branco')
            return redirect('login')
        print(email, password)
        if User.objects.filter(email=email).exists():
            name = User.objects.filter(email=email).values_list('username', flat=True).get()
            user = auth.authenticate(request, username=name, password=password)
            if user is not None:
                auth.login(request, user)
                #messages.success(request, 'Login realizado com sucesso')
                return redirect('index')
            #else:
                #messages.error(request, 'Usuário ou senha incorreto, por favor tente novamente')
    return render(request, 'users/login.html')

def empty(campo):
    return not campo.strip()

def not_equal_passwords(senha, senha2):
    return senha != senha2