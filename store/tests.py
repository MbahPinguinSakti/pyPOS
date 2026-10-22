from decimal import Decimal
from django.test import TestCase, Client
from django.urls import reverse
from .models import Product, Transaction, TransactionItem


class ProductModelTest(TestCase):
    def setUp(self):
        self.product = Product.objects.create(
            name="Indomie Goreng",
            price=Decimal("3500.00"),
            buy_price=Decimal("2800.00"),
            stock_eceran=10,
            stock_lusinan=2,
            conversion_rate=12,
        )

    def test_product_str(self):
        self.assertEqual(str(self.product), "Indomie Goreng")

    def test_total_stock_eceran_calculation(self):
        # 10 eceran + (2 lusinan * 12 conversion) = 34
        self.assertEqual(self.product.total_stock_eceran, 34)


class TransactionModelTest(TestCase):
    def setUp(self):
        self.product = Product.objects.create(
            name="Kopi Kapal Api",
            price=Decimal("2000.00"),
            buy_price=Decimal("1500.00"),
            stock_eceran=50,
            stock_lusinan=5,
            conversion_rate=10,
        )
        self.transaction = Transaction.objects.create(
            total_amount=Decimal("10000.00"),
            payment_amount=Decimal("15000.00"),
            change_amount=Decimal("5000.00"),
        )
        self.item = TransactionItem.objects.create(
            transaction=self.transaction,
            product=self.product,
            quantity=5,
            price_at_sale=Decimal("2000.00"),
            subtotal=Decimal("10000.00"),
            sale_type="eceran",
        )

    def test_transaction_str(self):
        self.assertIn(f"Transaction #{self.transaction.id}", str(self.transaction))

    def test_transaction_item_str(self):
        expected_str = f"5 x Kopi Kapal Api (eceran) in Transaction #{self.transaction.id}"
        self.assertEqual(str(self.item), expected_str)


class StoreViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.product = Product.objects.create(
            name="Teh Botol Sosro",
            price=Decimal("5000.00"),
            buy_price=Decimal("4000.00"),
            stock_eceran=5,
            stock_lusinan=3,
            conversion_rate=12,
        )

    def test_root_redirect(self):
        response = self.client.get(reverse('index'))
        self.assertRedirects(response, reverse('store_index'))

    def test_dashboard_view(self):
        response = self.client.get(reverse('store_index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'store/index.html')
        self.assertIn('products', response.context)
        self.assertIn('newest_transactions', response.context)

    def test_product_create_get(self):
        response = self.client.get(reverse('product_create'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'store/restock.html')

    def test_product_create_post(self):
        data = {
            'name': 'Susu Ultra Milk',
            'stock_eceran': '20',
            'stock_lusinan': '5',
            'conversion_rate': '24',
            'buy_price': '5500',
            'sell_price': '7000',
        }
        response = self.client.post(reverse('product_create'), data)
        self.assertRedirects(response, reverse('store_index'))

        created = Product.objects.filter(name='Susu Ultra Milk').first()
        self.assertIsNotNone(created)
        self.assertEqual(created.stock_eceran, 20)
        self.assertEqual(created.stock_lusinan, 5)
        self.assertEqual(created.conversion_rate, 24)
        self.assertEqual(created.price, Decimal('7000.00'))

    def test_sale_transaction_eceran_direct(self):
        data = {
            'product': [str(self.product.id)],
            'quantity': ['3'],
            'sale_type': ['eceran'],
            'payment': '20000',
        }
        response = self.client.post(reverse('transaksi'), data)
        trx = Transaction.objects.latest('id')
        self.assertRedirects(response, reverse('transaksi_detail', args=[trx.id]))

        self.product.refresh_from_db()
        self.assertEqual(self.product.stock_eceran, 2)  # 5 - 3 = 2
        self.assertEqual(self.product.stock_lusinan, 3)
        self.assertEqual(trx.total_amount, Decimal('15000.00'))
        self.assertEqual(trx.change_amount, Decimal('5000.00'))

    def test_sale_transaction_eceran_unpack_box(self):
        # Product has 5 eceran and 3 lusinan (conv rate: 12)
        # Sell 10 eceran -> need 5 from loose + 5 from 1 box.
        # Box unpacked: 1 box removed, 12 added - 5 used = 7 eceran left.
        data = {
            'product': [str(self.product.id)],
            'quantity': ['10'],
            'sale_type': ['eceran'],
            'payment': '50000',
        }
        response = self.client.post(reverse('transaksi'), data)
        trx = Transaction.objects.latest('id')
        self.assertRedirects(response, reverse('transaksi_detail', args=[trx.id]))

        self.product.refresh_from_db()
        self.assertEqual(self.product.stock_lusinan, 2)  # 3 - 1
        self.assertEqual(self.product.stock_eceran, 7)   # (12 - 5)

    def test_sale_transaction_lusinan(self):
        data = {
            'product': [str(self.product.id)],
            'quantity': ['2'],
            'sale_type': ['lusinan'],
            'payment': '10000',
        }
        response = self.client.post(reverse('transaksi'), data)
        trx = Transaction.objects.latest('id')
        self.assertRedirects(response, reverse('transaksi_detail', args=[trx.id]))

        self.product.refresh_from_db()
        self.assertEqual(self.product.stock_lusinan, 1)  # 3 - 2
        self.assertEqual(self.product.stock_eceran, 5)

    def test_transaction_history_view(self):
        response = self.client.get(reverse('history_transactions'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'store/history.html')
        self.assertIn('transactions', response.context)
        self.assertIn('total_sales', response.context)
        self.assertIn('profit', response.context)

    def test_transaction_detail_view(self):
        trx = Transaction.objects.create(
            total_amount=Decimal("5000.00"),
            payment_amount=Decimal("10000.00"),
            change_amount=Decimal("5000.00"),
        )
        TransactionItem.objects.create(
            transaction=trx,
            product=self.product,
            quantity=1,
            price_at_sale=Decimal("5000.00"),
            subtotal=Decimal("5000.00"),
            sale_type="eceran",
        )
        response = self.client.get(reverse('transaksi_detail', args=[trx.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'store/detail.html')
        self.assertEqual(response.context['trx'], trx)
