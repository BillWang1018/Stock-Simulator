from django.urls import path
from . import views

urlpatterns = [
   path('stock_list/', views.stock_list, name='stock_list'),  
   path('stock_detail/<int:pk>/', views.stock_detail, name='stock_detail'),
]

