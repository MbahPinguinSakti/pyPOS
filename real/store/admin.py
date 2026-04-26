from django.contrib import admin
from .models import Product, Transaction, TransactionItem


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'buy_price', 'stock_eceran', 'stock_lusinan', 'conversion_rate')
    search_fields = ('name',)


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('id', 'total_amount', 'payment_amount', 'change_amount', 'timestamp')
    list_filter = ('timestamp',)


@admin.register(TransactionItem)
class TransactionItemAdmin(admin.ModelAdmin):
    list_display = ('transaction', 'product', 'quantity', 'sale_type', 'price_at_sale', 'subtotal')
    list_filter = ('sale_type',)
