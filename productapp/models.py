from django.db import models
from django.contrib.auth.models import User

class FitFusionAICategory(models.Model):
    fitfusionai_category_id = models.AutoField(primary_key=True)
    fitfusionai_category_name = models.CharField(max_length=100, unique=True)

    # Boolean Fields
    fitfusionai_category_isactive = models.BooleanField(default=True)
    fitfusionai_category_isstatus = models.BooleanField(default=True)
    fitfusionai_category_ispopular = models.BooleanField(default=False)
    fitfusionai_category_istrending = models.BooleanField(default=False)
    fitfusionai_category_isnewarrival = models.BooleanField(default=False)

    def __str__(self):
        return self.fitfusionai_category_name

    class Meta:
        db_table = "fitfusionai_category"

class FitFusionAIProduct(models.Model):
    fitfusionai_product_id = models.AutoField(primary_key=True)
    fitfusionai_product_name = models.CharField(max_length=255)
    fitfusionai_product_description = models.TextField()

    # ForeignKey Link to Category
    fitfusionai_category = models.ForeignKey(FitFusionAICategory, on_delete=models.CASCADE, related_name="products")

    fitfusionai_product_price = models.DecimalField(max_digits=10, decimal_places=2)
    fitfusionai_product_stock = models.IntegerField()

    # Product Images
    fitfusionai_product_image1 = models.ImageField(upload_to='product_images/', null=True, blank=True)
    fitfusionai_product_image2 = models.ImageField(upload_to='product_images/', null=True, blank=True)
    fitfusionai_product_image3 = models.ImageField(upload_to='product_images/', null=True, blank=True)
    fitfusionai_product_image4 = models.ImageField(upload_to='product_images/', null=True, blank=True)
    fitfusionai_product_image5 = models.ImageField(upload_to='product_images/', null=True, blank=True)

    # Boolean Fields
    fitfusionai_product_active = models.BooleanField(default=True)
    fitfusionai_product_status = models.BooleanField(default=True)
    fitfusionai_product_popular = models.BooleanField(default=False)
    fitfusionai_product_trending = models.BooleanField(default=False)
    fitfusionai_product_newarrival = models.BooleanField(default=False)

    # Pricing Fields
    fitfusionai_product_discount = models.IntegerField(default=0)
    fitfusionai_product_actual_price = models.DecimalField(max_digits=10, decimal_places=2)
    fitfusionai_product_current_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.fitfusionai_product_name

    class Meta:
        db_table = "fitfusionai_product"

class FitFusionAIcart(models.Model):
    fitfusionai_cart_id = models.AutoField(primary_key=True)
    fitfusionai_product = models.ForeignKey(FitFusionAIProduct, on_delete=models.CASCADE, related_name="cart_items")
    fitfusionai_cart_quantity = models.IntegerField(default=1)
    fitfusionai_cart_user_id = models.IntegerField()
    fitfusionai_cart_date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "fitfusionai_cart"

class Order(models.Model):
    fitfusionai_order_cart_id = models.CharField(max_length=255, unique=True)
    fitfusionai_order_customer_email = models.EmailField()
    fitfusionai_order_amount_total_inr = models.DecimalField(max_digits=10, decimal_places=2)
    fitfusionai_order_currency = models.CharField(max_length=10)
    fitfusionai_order_payment_status = models.CharField(max_length=20)
    fitfusionai_order_payment_intent = models.CharField(max_length=255, blank=True, null=True)
    fitfusionai_order_customer_id = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)  # optional but recommended
    updated_at = models.DateTimeField(auto_now=True)      # optional but recommended

    class Meta:
        db_table = "fitfusionai_order"

    
    