from django.shortcuts import render, get_object_or_404
from django.http import Http404

# Create your views here.
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

# imports of current app
from .serializerhelper import *
from .serialisers import *
from .models import *
from .viewhelper import *


class ProductsList(APIView):

    def get(self, request, format=None):
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True,read_only=True)
        return Response(serializer.data)
    #
    # def post(self, request, format=None):
    #     serializer = ProductSerializer(data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DerivedProductView(APIView):

    def post(self,request, format=None):
        try:
            data = request.data
            for dat in data:
                if 'productId' in dat:
                    productobj = get_product_id(dat['productId'])

                if 'derivedAttributes' in dat:
                    for attribute in  dat['derivedAttributes']:
                        if 'key' in attribute and 'value' in attribute and productobj is not None:
                            dpobj = DerivedProduct(productId= productobj, key=attribute['key'], value=attribute['value'])
                            print(type(dpobj))
                            dpobj.save()
                        else:
                            return Response({'msg':'please check json format'},status=status.HTTP_400_BAD_REQUEST)

            return Response(status=status.HTTP_201_CREATED)

        except Exception as e:
            print('Exception:',str(e))
            return Response(status= status.HTTP_500_INTERNAL_SERVER_ERROR)

    def put(self,request,format=None):
        try:
            data = request.data
            if 'productId' in data:
                productobj = get_product_id(data['productId'])
            if productobj is None:
                response = {'pid': 'bad product Id'}
                return Response(response, status=status.HTTP_400_BAD_REQUEST)

            if 'derivedAttributes' in data:
                for attribute in data['derivedAttributes']:
                    if 'key' in attribute and 'value' in attribute and productobj is not None:
                        DerivedProduct.objects.filter(productId=productobj,key=attribute['key']).update(value=attribute['value'])

                    else:
                        return Response({'msg': 'please check json format'}, status=status.HTTP_400_BAD_REQUEST)

            return Response(status=status.HTTP_201_CREATED)

        except Exception as e:
            print('Exception:',str(e))


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

    def get(self, request, format=None):
        """
        API for getting rating for given product Id
        :param request:
        :param format:
        :return:
        """

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
        """
            API for storing the rating for purchased product
        :param request:
        :param format: {'uid':'','puid':'','pid':''}
        :return:
        """
        # uid validation using JWT
        # is valid purchase id and product Id
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
            print('Exception:', str(e))
            return Response(status=status.HTTP_400_BAD_REQUEST)
