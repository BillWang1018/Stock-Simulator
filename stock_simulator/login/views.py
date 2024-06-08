from datetime import timezone
import logging
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import redirect, render
from django.template import loader
from django.contrib import messages
from datetime import timedelta
from members.models import Customer
from .forms import InventoryForm, RegisterForm, LoginForm
from django.contrib.auth.models import User
from django.utils import timezone 
from django.db import connection
from .forms import SellForm

from django.db import connection
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.db import connection
logger = logging.getLogger(__name__)

def sell(request, customer_id):
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT ctfc FROM customer WHERE account = %s", [customer_id])
            flag = cursor.fetchone()
        
        if flag is None:
            return HttpResponse(f"Customer with account {customer_id} does not exist")
        
        ctfc = flag[0]

        # 存储第一个查询的结果
        first_result = (ctfc,)

    except Exception as e:
        return HttpResponse(f"Error executing query for customer ID {customer_id}: {e}")

    if request.method == 'POST':
        form = SellForm(request.POST)
        if form.is_valid():
            snum = form.cleaned_data['snum']
            amount = form.cleaned_data['amount']
            price = form.cleaned_data['price']
            
            # 使用存储的结果执行第二个查询
            try:
                with connection.cursor() as cursor:
                    cursor.execute("""
                        SELECT Amount FROM inventory 
                        WHERE Cid = %s AND Snum = %s
                        FOR UPDATE
                    """, [first_result[0], snum])
                    row = cursor.fetchone()
                    
                    if row is None:
                        return HttpResponse(f"Customer does not have stock item with Snum {snum}")
                    
                    current_amount = row[0]
                    if amount > current_amount:
                        return HttpResponse("Insufficient stock to sell")
                    
                    new_amount = current_amount - amount

                    cursor.execute("""
                        UPDATE inventory 
                        SET Amount = %s 
                        WHERE Cid = %s AND Snum = %s
                    """, [new_amount, first_result[0], snum])

                    # 删除原表格中的行
                    cursor.execute("""
                        DELETE FROM inventory
                        WHERE Cid = %s AND Snum = %s AND Amount = 0
                    """, [first_result[0], snum])

                return HttpResponseRedirect(request.path_info)
            except Exception as e:
                return HttpResponse(f"Error updating inventory: {e}")
    else:
        form = SellForm()

    # Fetch inventory data excluding the sold items
    try:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT inventory.Snum, inventory.Amount, inventory.Price, inventory.Tstmp
                FROM inventory
                JOIN stock ON inventory.Snum = stock.Number
                WHERE inventory.Cid = %s;
                """, [first_result[0]]
            )
            result = cursor.fetchall()
    except Exception as e:
        return HttpResponse(f"Error fetching inventory data: {e}")

    return render(request, 'sell.html', {'inventory': result, 'form': form})
def buy(request, customer_id):
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT ctfc FROM customer WHERE account = %s", [customer_id])
            flag = cursor.fetchone()
        
        if flag is None:
            return HttpResponse(f"Customer with account {customer_id} does not exist")
        
        ctfc = flag[0]

    except Exception as e:
        return HttpResponse(f"Error executing query for customer ID {customer_id}: {e}")

    if request.method == 'POST':
        form = InventoryForm(request.POST)
        if form.is_valid():
            snum = form.cleaned_data['snum']
            amount = form.cleaned_data['amount']
            price = form.cleaned_data['price']
            
            # Check if the stock item exists
            try:
                with connection.cursor() as cursor:
                    cursor.execute("SELECT Number FROM stock WHERE Number = %s", [snum])
                    stock_item = cursor.fetchone()
                    
                    if stock_item is None:
                        return HttpResponse(f"Stock item with Snum {snum} does not exist")
            except Exception as e:
                return HttpResponse(f"Error checking stock item: {e}")
            
            # Insert into inventory and update quotations
            tstmp = timezone.now() + timedelta(hours=8)
            try:
                with connection.cursor() as cursor:
                    # 插入库存数据
                    cursor.execute(
                        """
                        INSERT INTO inventory (Cid, Snum, Amount, Price, Tstmp)
                        VALUES (%s, %s, %s, %s, %s)
                        ON DUPLICATE KEY UPDATE Amount = Amount + VALUES(Amount);
                        """, [ctfc, snum, amount, price, tstmp]
                    )

                    # 删除旧的行情记录
                    cursor.execute("DELETE FROM quotations WHERE snum = %s", [snum])

                    # 插入新的行情记录到行情表
                    cursor.execute(
                        """
                        INSERT INTO quotations (snum, buyamt, sellamt, tstmp, sprice)
                        VALUES (%s, %s, %s, %s, %s)
                        """, [snum, amount, 0, tstmp, price]
                    )

                return HttpResponseRedirect(request.path_info)
            except Exception as e:
                return HttpResponse(f"Error inserting data into inventory or quotations: {e}")
    else:
        form = InventoryForm()

    # Fetch inventory data
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
        return HttpResponse(f"Error fetching inventory data: {e}")

    return render(request, 'buy.html', {'inventory': result, 'form': form})

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
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM customer WHERE account = %s", [account])
                row = cursor.fetchone()
                if row:
                    db_password = row[4]
                else:
                    db_password = None

            if row and password == db_password:
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