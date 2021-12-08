from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.models import User
from django.contrib import auth, messages
from .models import Client

def create_user(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']

        if empty(name):
            messages.error(request, 'O nome não pode ser vazio')
            return redirect('create_user')
        if empty(email):
            messages.error(request, 'O email não pode ser vazio')
            return redirect('create_user')
        if empty(password) or empty(password2):
            messages.error(request, 'A senha não pode ser vazia')
            return redirect('create_user')
        if not_equal_passwords(password, password2):
            messages.error(request, 'As senhas não são iguais')
            return redirect('create_user')
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Usuário já cadastrado')
            return redirect('create_user')
        if User.objects.filter(username=name).exists():
            messages.error(request, 'Usuário já cadastrado')
            return redirect('create_user')
            
        user = User.objects.create_user(username=name, email=email, password=password)
        client = Client.objects.create(client_id=user.id, fund=100)
        user.save()
        client.save()
        messages.success(request, 'Cadastro realizado com sucesso')
        return redirect('index')
        
    return render(request, 'users/create_user.html')

def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password_user']
        if empty(email) or empty(password):
            messages.error(request, 'Os campos email e password não podem ficar em branco')
            return redirect('login')
        print(email, password)
        if User.objects.filter(email=email).exists():
            name = User.objects.filter(email=email).values_list('username', flat=True).get()
            user = auth.authenticate(request, username=name, password=password)
            if user is not None:
                auth.login(request, user)
                messages.success(request, 'Login realizado com sucesso')
                return redirect('index')
            else:
                messages.error(request, 'Usuário ou senha incorreto, por favor tente novamente')
                return redirect('login')
        else:
            messages.error(request, 'Usuário inexistente')
    return render(request, 'users/login.html')

def logout(request):
    """Realiza o logout"""
    auth.logout(request)
    return redirect('index')

def perfil(request, user_id):
    user = get_object_or_404(User, pk=user_id)

    data = {
        'user':user
    }

    return render(request, 'users/perfil.html', data)

def change_information(request, user_id):
    if request.method == "POST":
        user = User.objects.get(pk=user_id)

        new_name = request.POST['username']
        if not information_user_equal_information_form(user.username, new_name) and User.objects.filter(username=new_name).exists():
            messages.error(request, 'Esse nome de usuário já existe.')
            return redirect('perfil', user_id)
        user.username = new_name

        new_email = request.POST['email']
        if not information_user_equal_information_form(user.email, new_email) and User.objects.filter(email=new_email).exists():
            messages.error(request, 'Esse email já está cadastrado')
            return redirect('perfil', user_id)
        user.email = new_email

        new_password = request.POST['new_password']
        confirm_new_password = request.POST['confirm_new_password']
        if empty(new_password) or not_equal_passwords(new_password, confirm_new_password):
            print('passei aqui')
            messages.error(request, 'As senhas estão diferentes.')
            return redirect('perfil', user_id)
            
        user.set_password(new_password)
        user.save()
        return redirect('index')

def empty(field):
    return not field.strip()

def information_user_equal_information_form(information_user, information_form):
    return information_user == information_form

def not_equal_passwords(password, password2):
    return password != password2