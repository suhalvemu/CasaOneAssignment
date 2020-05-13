from django.urls import path
from .views import *

urlpatterns = [
    path('products/', ProductsList.as_view(), name='ProductsList'),
    # path('products/<int:pk>/', ProductsDetail.as_view()),
    # path('purchase/',PurchaseDetail.as_view()),
    path('ratings/',Rating.as_view())
]