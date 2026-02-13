from django.db import models
from cloudinary.models import CloudinaryField
from django.contrib.auth.models import User

# ---------------- Brand ----------------
class Brand(models.Model):
    brandName = models.CharField(max_length=255)
    brandImg = CloudinaryField('image')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.brandName

# ---------------- Category ----------------
class Category(models.Model):
    categoryName = models.CharField(max_length=255)
    categoryImg = CloudinaryField('image')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.categoryName

# ---------------- Product ----------------
class Product(models.Model):
    REMARK_CHOICES = [
        ('popular', 'Popular'),
        ('new', 'New'),
        ('top', 'Top'),
        ('special', 'Special'),
    ]
    title = models.CharField(max_length=255)
    short_des = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount = models.PositiveSmallIntegerField(default=0)
    discount_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    image = CloudinaryField('image')
    stock = models.PositiveIntegerField(default=0)
    star = models.FloatField(default=0)
    remark = models.CharField(max_length=20, choices=REMARK_CHOICES, blank=True)

    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

# ---------------- Product Slider ----------------
class ProductSlider(models.Model):
    title = models.CharField(max_length=255)
    short_des = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = CloudinaryField('image')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

# ---------------- Product Details ----------------
class ProductDetail(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    img1 = CloudinaryField('image')
    img2 = CloudinaryField('image', blank=True, null=True)
    img3 = CloudinaryField('image', blank=True, null=True)
    img4 = CloudinaryField('image', blank=True, null=True)
    des = models.TextField()
    color = models.CharField(max_length=255, blank=True)
    size = models.CharField(max_length=255, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

# ---------------- Cart ----------------
class ProductCart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    color = models.CharField(max_length=255, blank=True)
    size = models.CharField(max_length=255, blank=True)
    qty = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

# ---------------- Invoice ----------------
class Invoice(models.Model):
    DELIVERY_STATUS = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('delivered', 'Delivered'),
    ]
    total = models.DecimalField(max_digits=10, decimal_places=2)
    vat = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    payable = models.DecimalField(max_digits=10, decimal_places=2)
    cus_details = models.CharField(max_length=255)
    ship_details = models.CharField(max_length=255)
    tran_id = models.CharField(max_length=255, blank=True)
    val_id = models.CharField(max_length=255, blank=True)
    delivery_status = models.CharField(max_length=20, choices=DELIVERY_STATUS, default='pending')
    payment_status = models.CharField(max_length=50, default='Pending')
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

# ---------------- Invoice Products ----------------
class InvoiceProduct(models.Model):
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    qty = models.PositiveIntegerField(default=1)
    sale_price = models.DecimalField(max_digits=10, decimal_places=2)

# ---------------- SSLCommerz ----------------
class SSLCommerzAccount(models.Model):
    store_id = models.CharField(max_length=255)
    store_passwd = models.CharField(max_length=255)
    currency = models.CharField(max_length=50)
    success_url = models.CharField(max_length=255)
    fail_url = models.CharField(max_length=255)
    cancel_url = models.CharField(max_length=255)
    ipn_url = models.CharField(max_length=255)
    init_url = models.CharField(max_length=255)

# ---------------- Policy ----------------
class Policy(models.Model):
    POLICY_TYPES = [
        ('about', 'About'),
        ('refund', 'Refund'),
        ('privacy', 'Privacy'),
        ('terms', 'Terms'),
    ]
    type = models.CharField(max_length=20, choices=POLICY_TYPES)
    des = models.TextField()
