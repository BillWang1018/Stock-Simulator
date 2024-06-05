import logging
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.template import loader
from django.contrib import messages
from .forms import RegisterForm
from django.db import connection
from .forms import LoginForm
logger = logging.getLogger(__name__)

def login_view(request):
    # Load the login template
    login_page = loader.get_template('login.html')

    if request.method == 'GET':
        # If it's a GET request, render the login form
        login_form = LoginForm()
        context = {
            'user': request.user,
            'login_form': login_form,
        }
        return HttpResponse(login_page.render(context, request))

    elif request.method == 'POST':
        # If it's a POST request, process the login form
        login_form = LoginForm(request.POST)

        if login_form.is_valid():
            # If the form is valid, attempt to authenticate the user
            account = login_form.cleaned_data['account']
            password = login_form.cleaned_data['password']

            # Securely authenticate the user
            user = authenticate(request, account=account, password=password)

            if user is not None:
                # If authentication succeeds, fetch stock data and log in the user
                with connection.cursor() as cursor:
                    cursor.execute("SELECT * FROM stock;")
                    columns = [col[0] for col in cursor.description]
                    rows = cursor.fetchall()
                stocks = [dict(zip(columns, row)) for row in rows]

                auth_login(request, user)
                return render(request, 'stocks.html', {'stocks': stocks})
            else:
                # If authentication fails, return an error message
                message = 'Login failed (invalid credentials)'
                return HttpResponse(message)
        else:
            # If the form is not valid, return an error message
            return HttpResponse("Login form is not valid")

    else:
        # Return an error if the request method is neither GET nor POST
        return HttpResponse("Error: Unsupported request method")
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

def stock_detail(request, snum):
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM quotations WHERE Snum = %s", [snum])
        columns = [col[0] for col in cursor.description]
        row = cursor.fetchone()
    stock = dict(zip(columns, row)) if row else None
    return render(request, 'stock_detail.html', {'stock': stock})
