from django.shortcuts import render, get_object_or_404
from django.http import Http404

# Create your views here.
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

#imports of current app
from .serializerhelper import *
from .serialisers import *
from .models import *


class ProductsList(APIView):

    def get(self, request, format=None):
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProductsDetail(APIView):
    """
        Retrieve, update or delete a product instance.
    """

    def get_object(self, pk):
        try:
            return Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        product = self.get_object(pk)
        serializer = ProductSerializer(product)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        product = self.get_object(pk)
        serializer = ProductSerializer(product, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        product = self.get_object(pk)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class Rating(APIView):

    def get_product_id(self, pk):
        try:
            return Product.objects.get(productId=pk)
        except Product.DoesNotExist:
            return None

    def get_purchase_id(self,pk):
        try:
            return PurchaseOrder.objects.get(purchaseId=pk)
        except Product.DoesNotExist:
            return None


    def get(self, request, format=None):
        try:
            if self.request.query_params.get('pid'):
                productObj = self.get_product_id(self.request.query_params.get('pid'))
                if productObj is None:
                    response = {'pid': 'bad product Id'}
                    return Response(response, status=status.HTTP_400_BAD_REQUEST)
                obj = RatingSerialiszerHelper(productObj)
                serializer = RatingSerializer(obj)
                return Response(serializer.data)
            else:
                response = {'pid': 'product id is missing in query'}
                return Response(response, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print('Exception:', str(e))
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request, format=None):
        try:
            data = request.data
            print(data)
            if 'puid' not in data:
                return Response({'puid: purchaseId is missing'}, status=status.HTTP_400_BAD_REQUEST)
            if 'pid' not in data:
                return Response({'pid': 'productId is missing'}, status=status.HTTP_400_BAD_REQUEST)
            if 'rating' not in data:
                return Response({'rating': 'rating is missing'}, status=status.HTTP_400_BAD_REQUEST)

            productObj = self.get_product_id(data['pid'])

            if productObj is None:
                response = {'pid': 'bad product Id'}
                return Response(response, status=status.HTTP_400_BAD_REQUEST)

            purchaseOrderObj = self.get_purchase_id(data['puid'])

            if purchaseOrderObj is None:
                response = {'pid': 'bad purchase Id'}
                return Response(response, status=status.HTTP_400_BAD_REQUEST)

            pod = PurchaseOrderDetails.objects.get(productId=productObj, purchaseId=purchaseOrderObj)
            ratingobj = Ratings(purchaseOrderDetailsId=pod, ratings=data['rating'])
            ratingobj.save()
            return Response(status=status.HTTP_201_CREATED)

        except Exception as e:
            print('Exception:',str(e))
            return Response(status=status.HTTP_400_BAD_REQUEST)
        # uid validation using JWT
        # is valid purchase id and product Id
