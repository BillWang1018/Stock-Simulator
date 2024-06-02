import logging
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.template import loader
from django.contrib import messages

from members.models import Customer
from .forms import RegisterForm
from django.contrib.auth.models import User

from django.db import connection

from django.db import connection

from django.shortcuts import render
from django.db import connection

def stock(request):
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM stock;")
        columns = [col[0] for col in cursor.description]
        rows = cursor.fetchall()
    members = []
    for row in rows:
        member_dict = dict(zip(columns, row))
        members.append(member_dict)
    return render(request, 'stock.html', {'members': members})

def members_view(request):
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM customer;")
        columns = [col[0] for col in cursor.description]
        rows = cursor.fetchall()

    members = []
    for row in rows:
        member_dict = dict(zip(columns, row))
        members.append(member_dict)

    return render(request, 'members.html', {'members': members})

logger = logging.getLogger(__name__)

def login_view(request):
    login_page = loader.get_template('login.html')
    if request.method == 'GET':
        login_form = RegisterForm()
        context = {
            'user': request.user,
            'login_form': login_form,
        }
        return HttpResponse(login_page.render(context, request))
    elif request.method == "POST":
        login_form = RegisterForm(request.POST)
        if login_form.is_valid():
            account = login_form.cleaned_data['account']
            password = login_form.cleaned_data['password']
            user = authenticate(request, username=account, password=password)
            if user is not None:
                auth_login(request, user)
                main_page = loader.get_template('main.html')
                context = {'user': request.user, 'message': 'login ok'}
                return HttpResponse(main_page.render(context, request))
            else:
                message = 'Login failed (auth fail)'
                return HttpResponse(message)
        else:                    
            print('Login error (login form is not valid)')
            return HttpResponse("Login form is not valid")
    else:
        print('Error on request (not GET/POST)')
        return HttpResponse("Error on request (not GET/POST)")

def logout_view(request):
    auth_logout(request)
    main_html = loader.get_template('main.html')
    context = {'user': request.user}
    return HttpResponse(main_html.render(context, request))

logger = logging.getLogger(__name__)

def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            try:
                name = form.cleaned_data['name']
                identity = form.cleaned_data['identity']
                account = form.cleaned_data['account']
                password = form.cleaned_data['password']
                ctfc = form.cleaned_data['ctfc']
                
                # 使用原始的 SQL 语句将数据插入到数据库中
                with connection.cursor() as cursor:
                    cursor.execute(
                        "INSERT INTO customer (Name, Identity, Account, Ctfc,password) VALUES (%s, %s, %s, %s, %s);",
                        [name, identity, account, password, ctfc]
                    )
                messages.success(request, 'Account created successfully!')
                return redirect('/')  # 替换为您的成功URL
            except Exception as e:
                # 记录错误信息
                logger.error(f"Error during user registration: {e}")
                messages.error(request, 'An error occurred during registration. Please try again later.')
        else:
            logger.error(f"Form is not valid: {form.errors}")
            messages.error(request, 'Form is not valid. Please correct the errors and try again.')
    else:
        form = RegisterForm()
    
    return render(request, 'register.html', {'form': form})