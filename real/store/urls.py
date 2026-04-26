from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='store_index'),
    path('tambah/', views.product_create, name='product_create'),
    path('history/', views.transactions_history, name='history_transactions'),
    path('jual/', views.transactions, name='transaksi'),
    path('transaksi/<int:id>/', views.transaksi_detail, name='transaksi_detail'),
]