from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Product, ProductDetail, ProductCart, Invoice, InvoiceProduct, SSLCommerzAccount, ProductSlider, Category
from django.contrib.auth.models import User

# ---------------- Home ----------------
def home(request):
    products = Product.objects.all()
    sliders = ProductSlider.objects.all()
    categories = Category.objects.all()
    context = {'products': products, 'sliders': sliders, 'categories': categories}
    return render(request, 'index.html', context)

# ---------------- Product List ----------------
def product_list(request, category_id=None):
    products = Product.objects.all()
    if category_id:
        products = products.filter(category_id=category_id)
    categories = Category.objects.all()
    return render(request, 'shop/product_list.html', {'products': products, 'categories': categories})

# ---------------- Product Detail ----------------
def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    details = ProductDetail.objects.filter(product=product).first()
    return render(request, 'shop/product_detail.html', {'product': product, 'details': details})

# ---------------- Add to Cart ----------------
def add_to_cart(request, product_id):
    user = request.user if request.user.is_authenticated else User.objects.get(id=1)  # dummy admin fallback
    product = get_object_or_404(Product, id=product_id)
    color = request.POST.get('color', '')
    size = request.POST.get('size', '')
    qty = int(request.POST.get('qty', 1))

    cart_item, created = ProductCart.objects.get_or_create(
        user=user,
        product=product,
        color=color,
        size=size,
        defaults={'qty': qty, 'price': product.price}
    )
    if not created:
        cart_item.qty += qty
        cart_item.save()

    messages.success(request, 'Product added to cart!')
    return redirect('cart_view')

# ---------------- Cart View ----------------
def cart_view(request):
    user = request.user if request.user.is_authenticated else User.objects.get(id=1)
    cart_items = ProductCart.objects.filter(user=user)
    subtotal = sum(item.price * item.qty for item in cart_items)
    shipping = 0  # Update if you have shipping calculation
    tax = 0       # Update if you have tax calculation
    total = subtotal + shipping + tax
    context = {
        'cart_items': cart_items,
        'subtotal': subtotal,
        'shipping': shipping,
        'tax': tax,
        'total': total
    }
    return render(request, 'shop/cart.html', context)

# ---------------- Direct SSLCommerz Checkout ----------------
def ssl_checkout(request):
    user = request.user if request.user.is_authenticated else User.objects.get(id=1)
    cart_items = ProductCart.objects.filter(user=user)
    ssl_account = SSLCommerzAccount.objects.first()

    if not cart_items.exists():
        messages.warning(request, "Your cart is empty.")
        return redirect('cart_view')

    total = sum(item.price * item.qty for item in cart_items)

    # Create invoice
    invoice = Invoice.objects.create(
        total=total,
        vat=0,
        payable=total,
        cus_details="Billing Details",  # You can fetch from user profile
        ship_details="Shipping Details",
        tran_id="",
        val_id="",
        delivery_status="pending",
        payment_status="Pending",
        user=user
    )

    # Add products to invoice
    for item in cart_items:
        InvoiceProduct.objects.create(
            invoice=invoice,
            product=item.product,
            qty=item.qty,
            sale_price=item.price
        )

    # Clear the cart
    cart_items.delete()

    messages.success(request, "Order placed! Redirecting to payment.")
    return redirect('ssl_payment', invoice_id=invoice.id)

# ---------------- SSLCommerz Payment ----------------
def ssl_payment(request, invoice_id):
    invoice = get_object_or_404(Invoice, id=invoice_id)
    ssl_account = SSLCommerzAccount.objects.first()
    return render(request, 'shop/ssl_payment.html', {'invoice': invoice, 'ssl_account': ssl_account})
