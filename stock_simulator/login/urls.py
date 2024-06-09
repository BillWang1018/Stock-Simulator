from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),
    path('members/', views.members_view, name='members'),
    path('stock/', views.stock_list, name='stock_list'),
    path('stock/<int:snum>/', views.stock_detail, name='stock_detail'),
    path('snum/', views.snum_view, name='snum'),
    path('inventory/<str:customer_id>/', views.inventory_view, name='inventory'),
    path('buy/<str:customer_id>/', views.buy, name='buy'),
    path('sell/<str:customer_id>/', views.sell, name='sell'),  # Add this line
]
