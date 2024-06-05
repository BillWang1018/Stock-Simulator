import logging
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.template import loader
from django.contrib import messages
from .forms import RegisterForm
from django.db import connection

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
            return HttpResponse("Login form is not valid")
    else:
        return HttpResponse("Error on request (not GET/POST)")

def logout_view(request):
    auth_logout(request)
    main_html = loader.get_template('main.html')
    context = {'user': request.user}
    return HttpResponse(main_html.render(context, request))

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

                with connection.cursor() as cursor:
                    cursor.execute(
                        "INSERT INTO customer (Name, Identity, Account, Ctfc, password) VALUES (%s, %s, %s, %s, %s);",
                        [name, identity, account, password, ctfc]
                    )
                messages.success(request, 'Account created successfully!')
                return redirect('/')
            except Exception as e:
                logger.error(f"Error during user registration: {e}")
                messages.error(request, 'An error occurred during registration. Please try again later.')
        else:
            messages.error(request, 'Form is not valid. Please correct the errors and try again.')
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})

def members_view(request):
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM customer;")
        columns = [col[0] for col in cursor.description]
        rows = cursor.fetchall()
    members = [dict(zip(columns, row)) for row in rows]
    return render(request, 'members.html', {'members': members})

def snum_view(request):
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM quotations;")
        columns = [col[0] for col in cursor.description]
        rows = cursor.fetchall()
    members = [dict(zip(columns, row)) for row in rows]
    return render(request, 'snum.html', {'members': members})

def stock_list(request):
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM quotations;")
        columns = [col[0] for col in cursor.description]
        rows = cursor.fetchall()
    members = [dict(zip(columns, row)) for row in rows]
    return render(request, 'stock_list.html', {'members': members})

def stock_detail(request, pk):
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM quotations WHERE Snum = %s", [pk])
        columns = [col[0] for col in cursor.description]
        row = cursor.fetchone()
    stock = dict(zip(columns, row)) if row else None
    return render(request, 'stock_detail.html', {'stock': stock})
