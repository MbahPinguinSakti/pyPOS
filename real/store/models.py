from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=100, unique=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, help_text="Harga jual satuan/eceran")
    buy_price = models.DecimalField(max_digits=10, decimal_places=2, help_text="Harga beli satuan")
    stock_eceran = models.PositiveIntegerField(default=0, help_text="Stok eceran (satuan)")
    stock_lusinan = models.PositiveIntegerField(default=0, help_text="Stok lusinan/box")
    conversion_rate = models.PositiveIntegerField(
        default=12,
        help_text="Jumlah eceran per 1 lusin/box (misal: 12)"
    )

    def __str__(self):
        return self.name

    @property
    def total_stock_eceran(self):
        """Total seluruh stok dalam satuan eceran."""
        return self.stock_eceran + (self.stock_lusinan * self.conversion_rate)


class Transaction(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    total_amount = models.DecimalField(max_digits=12, decimal_places=2)
    payment_amount = models.DecimalField(max_digits=12, decimal_places=2)
    change_amount = models.DecimalField(max_digits=12, decimal_places=2)

    def __str__(self):
        return f"Transaction #{self.id} - {self.timestamp.strftime('%Y-%m-%d %H:%M')}"


class TransactionItem(models.Model):
    SALE_TYPE_CHOICES = [
        ('eceran', 'Eceran'),
        ('lusinan', 'Lusinan/Box'),
    ]

    transaction = models.ForeignKey(Transaction, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField()
    price_at_sale = models.DecimalField(max_digits=10, decimal_places=2)
    subtotal = models.DecimalField(max_digits=12, decimal_places=2)
    sale_type = models.CharField(max_length=10, choices=SALE_TYPE_CHOICES, default='eceran')

    def __str__(self):
        return f"{self.quantity} x {self.product.name} ({self.sale_type}) in Transaction #{self.transaction.id}"
