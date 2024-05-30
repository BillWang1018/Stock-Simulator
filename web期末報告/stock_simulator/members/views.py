from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

def main(request):
    return render(request, 'main.html')
