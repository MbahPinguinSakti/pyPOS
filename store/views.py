from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.db import transaction as db_transaction
from django.db.models import Sum, F
from decimal import Decimal

from .models import Product, Transaction, TransactionItem


# ---------------------------------------------------------------------------
# Helper: get dashboard context
# ---------------------------------------------------------------------------
def _get_dashboard_context():
    """Return common context data used across multiple views."""
    products = Product.objects.all()
    total_sales = (
        Transaction.objects.aggregate(total=Sum('total_amount'))['total']
        or Decimal('0.00')
    )
    total_buy_price = (
        Product.objects.aggregate(total=Sum('buy_price'))['total']
        or Decimal('0.00')
    )
    newest_transactions = Transaction.objects.order_by('-timestamp')[:10]

    return {
        'products': products,
        'total_sales': total_sales,
        'total_buy_price': total_buy_price,
        'newest_transactions': newest_transactions,
    }


# ---------------------------------------------------------------------------
# Views
# ---------------------------------------------------------------------------
def index(request):
    """Dashboard / landing page for the store app."""
    ctx = _get_dashboard_context()
    return render(request, 'store/index.html', {
        'products': ctx['products'],
        'newest_transactions': ctx['newest_transactions'],
    })


def product_create(request):
    """Create a new product (restock page)."""
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        stock_eceran = request.POST.get('stock_eceran', '0')
        stock_lusinan = request.POST.get('stock_lusinan', '0')
        conversion_rate = request.POST.get('conversion_rate', '12')
        buy_price = request.POST.get('buy_price', '0')
        sell_price = request.POST.get('sell_price', '0')

        if name and sell_price:
            try:
                Product.objects.create(
                    name=name,
                    stock_eceran=int(stock_eceran),
                    stock_lusinan=int(stock_lusinan),
                    conversion_rate=int(conversion_rate),
                    buy_price=Decimal(buy_price),
                    price=Decimal(sell_price),
                )
                return redirect('store_index')
            except Exception as e:
                pass  # TODO: add error message via Django messages

    ctx = _get_dashboard_context()
    return render(request, 'store/restock.html', {
        'products': ctx['products'],
        'newest_transactions': ctx['newest_transactions'],
    })


def transactions(request):
    """Process a new sale transaction."""
    if request.method == 'POST':
        total = Decimal('0.00')
        item_data = []

        product_ids = request.POST.getlist('product')
        quantities = request.POST.getlist('quantity')
        sale_types = request.POST.getlist('sale_type')

        for product_id, qty, sale_type in zip(product_ids, quantities, sale_types):
            product = get_object_or_404(Product, id=product_id)
            quantity = int(qty)
            price = product.price
            subtotal = price * quantity
            total += subtotal
            item_data.append({
                'product': product,
                'quantity': quantity,
                'price': price,
                'subtotal': subtotal,
                'sale_type': sale_type,
            })

        payment_raw = request.POST.get('payment', '0').replace('.', '').replace(',', '.')
        payment_amount = Decimal(payment_raw)
        change_amount = payment_amount - total

        with db_transaction.atomic():
            trx = Transaction.objects.create(
                total_amount=total,
                payment_amount=payment_amount,
                change_amount=change_amount,
            )

            for item in item_data:
                product = item['product']
                quantity = item['quantity']
                sale_type = item['sale_type']

                # ---------- Stock adjustment logic ----------
                if sale_type == 'lusinan':
                    # Jual lusinan: kurangi stok lusinan
                    if product.stock_lusinan >= quantity:
                        product.stock_lusinan -= quantity
                    else:
                        raise ValueError(
                            f"Stok lusinan {product.name} tidak cukup "
                            f"(tersedia: {product.stock_lusinan}, diminta: {quantity})"
                        )
                else:
                    # Jual eceran: kurangi stok eceran.
                    # Jika stok eceran tidak cukup, bongkar box/lusin.
                    remaining = quantity
                    if product.stock_eceran >= remaining:
                        product.stock_eceran -= remaining
                    else:
                        remaining -= product.stock_eceran
                        product.stock_eceran = 0
                        # Bongkar box secukupnya
                        boxes_needed = -(-remaining // product.conversion_rate)  # ceil division
                        if product.stock_lusinan >= boxes_needed:
                            product.stock_lusinan -= boxes_needed
                            product.stock_eceran += (boxes_needed * product.conversion_rate) - remaining
                        else:
                            raise ValueError(
                                f"Stok {product.name} tidak cukup untuk menjual {quantity} eceran."
                            )

                product.save()

                TransactionItem.objects.create(
                    transaction=trx,
                    product=product,
                    quantity=quantity,
                    price_at_sale=item['price'],
                    subtotal=item['subtotal'],
                    sale_type=sale_type,
                )

        return redirect('transaksi_detail', trx.id)

    products = Product.objects.all()
    return render(request, 'store/make.html', {'products': products})


def transaksi_detail(request, id):
    """Show transaction receipt."""
    trx = get_object_or_404(Transaction, id=id)
    items = trx.items.select_related('product').all()
    return render(request, 'store/detail.html', {'trx': trx, 'items': items})


def transactions_history(request):
    """Show all past transactions."""
    ctx = _get_dashboard_context()
    profit = ctx['total_sales'] - ctx['total_buy_price']

    return render(request, 'store/history.html', {
        'transactions': Transaction.objects.order_by('-timestamp'),
        'total_sales': ctx['total_sales'],
        'profit': profit,
        'products': ctx['products'],
    })
