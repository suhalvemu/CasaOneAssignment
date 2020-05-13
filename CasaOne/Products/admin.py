from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(Product)
admin.site.register(PurchaseOrder)
admin.site.register(PurchaseOrderDetails)
admin.site.register(Ratings)
admin.site.register(DerivedProduct)
