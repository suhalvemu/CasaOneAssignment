from .models import *


def get_product_id(pk):
    try:
        return Product.objects.get(productId=pk)
    except Product.DoesNotExist:
        return None


def get_purchase_id(pk):
    try:
        return PurchaseOrder.objects.get(purchaseId=pk)
    except Product.DoesNotExist:
        return None