import logging
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.template import loader
from django.contrib import messages

from members.models import Customer
from .forms import RegisterForm, LoginForm
from django.contrib.auth.models import User

from django.db import connection

from django.db import connection
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.db import connection
logger = logging.getLogger(__name__)

def login_view(request):
    login_page = loader.get_template('login.html')
    if request.method == 'GET':
        login_form = LoginForm()
        context = {
            'login_form': login_form,
            'user': request.user,
        }
        return HttpResponse(login_page.render(context, request))
    elif request.method == "POST":
        login_form = LoginForm(request.POST)

        if login_form.is_valid():
            account = login_form.cleaned_data['account']
            password = login_form.cleaned_data['password']
            user = None
            aa = 0
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM customer WHERE account = %s", [account])
                row = cursor.fetchone()
                if row:
                    db_password = row[4]
                else:
                    db_password = None

            if row and password == db_password:
                aa = 1
                user, created = User.objects.get_or_create(username=account)
                if created:
                    user.set_password(password)
                    user.save()
                else:
                    user = authenticate(username=account, password=password)

                if user:
                    auth_login(request, user)
                    with connection.cursor() as cursor:
                        cursor.execute("SELECT * FROM stock;")
                        columns = [col[0] for col in cursor.description]
                        rows = cursor.fetchall()
                    members = [dict(zip(columns, row)) for row in rows]
                    return render(request, 'stocks.html', {'members': members})

                    #return redirect('stocks')

            message = f'Login failed for account: {account}.'
            return HttpResponse(message)
        else:
            message = 'Login form is not valid'
            return HttpResponse(message)
    else:
        message = 'Error on request (not GET/POST)'
        return HttpResponse(message)
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

def inventory_view(request, customer_id):
    try:
        with connection.cursor() as cursor:
            # 直接通过 account 获取 ctfc
            cursor.execute("SELECT ctfc FROM customer WHERE account = %s", [customer_id])
            flag = cursor.fetchone()
        
        if flag is None:
            return HttpResponse(f"Customer with account {customer_id} does not exist")
        
        ctfc = flag[0]  # 提取 ctfc 的实际值

    except Exception as e:
        return HttpResponse(f"Error executing query for customer ID {customer_id}: {e}")

    # 执行 SQL 查询
    try:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT inventory.Snum, inventory.Amount, inventory.Price, inventory.Tstmp
                FROM inventory
                JOIN stock ON inventory.Snum = stock.Number
                WHERE inventory.Cid = %s;
                """, [ctfc]
            )
            result = cursor.fetchall()
    except Exception as e:
        return HttpResponse(f"Error executing query: {e}")

    return render(request, 'inventory.html', {'inventory': result})