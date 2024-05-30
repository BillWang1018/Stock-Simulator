from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.template import loader
from django.contrib import messages
from .forms import RegisterForm, LoginForm
from django.contrib.auth.models import User

def login_view(request):
    login_page = loader.get_template('login.html')
    if request.method == 'GET':
        login_form = LoginForm()
        context = {
            'user': request.user,
            'login_form': login_form,
        }
        return HttpResponse(login_page.render(context, request))
    elif request.method == "POST":
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                auth_login(request, user)
                main_page = loader.get_template('main.html')
                context = {'user': request.user, 'message': 'login ok'}
                return HttpResponse(main_page.render(context, request))
            else:
                message = 'Login failed (auth fail)'
        else:                    
            print('Login error (login form is not valid)')
    else:
        print('Error on request (not GET/POST)')

def logout_view(request):
    auth_logout(request)
    main_html = loader.get_template('main.html')
    context = {'user': request.user}
    return HttpResponse(main_html.render(context, request))

def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        if not User.objects.filter(username=username).exists():
            user = User.objects.create_user(username=username, password=password)
            messages.success(request, f'Account created for {username}!')
            return redirect('members:main') 
        else:
            messages.error(request, f'Username {username} already exists!')
    return render(request, 'register.html')