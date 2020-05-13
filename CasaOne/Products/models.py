from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Product(models.Model):
    productId = models.AutoField(primary_key=True)
    productName = models.CharField(max_length=250, unique=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    available = models.PositiveIntegerField(null=True)


class DerivedProduct(models.Model):
    derivedProductId = models.AutoField(primary_key=True)
    key = models.CharField(max_length=250)
    value = models.CharField(max_length=250)
    productId = models.ForeignKey(Product, models.SET_NULL, blank=True, null=True, related_name='derivedAttributes')


class PurchaseOrder(models.Model):
    purchaseId = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, models.SET_NULL, blank=True, null=True)
    purchaseDate = models.DateTimeField(editable=False, auto_now_add=True)


class PurchaseOrderDetails(models.Model):
    purchaseOrderDetailsId = models.AutoField(primary_key=True)
    productId = models.ForeignKey(Product, models.SET_NULL, blank=True, null=True)
    purchaseId = models.ForeignKey(PurchaseOrder, models.SET_NULL, blank=True, null=True)
    quantity = models.PositiveIntegerField(default=0)


class Ratings(models.Model):
    RATINGS = (
        (0, 'NO Rating'),
        (1, 'Poor'),
        (2, 'Average'),
        (3, 'Good'),
        (4, 'Very Good'),
        (5, 'Excellent'),
    )
    ratingId = models.AutoField(primary_key=True)
    purchaseOrderDetailsId = models.ForeignKey(PurchaseOrderDetails, models.SET_NULL, blank=True, null=True)
    ratings = models.IntegerField(choices=RATINGS, default=0)
