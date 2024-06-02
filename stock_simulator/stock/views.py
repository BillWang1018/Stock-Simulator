from django.shortcuts import render
from .models import Stock, Quotations, Inventory

def stock_view(request):
    stocks = Stock.objects.all()
    return render(request, 'stock.html', {'stocks': stocks})

