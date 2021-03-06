from rest_framework import serializers
from .models import *
from django.db.models import Avg, Sum


class DerivedProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = DerivedProduct
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    derivedAttributes = DerivedProductSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = ('productId', 'productName', 'price', 'available', 'derivedAttributes')


class RatingSerializer(serializers.Serializer):
    productId = serializers.SerializerMethodField('get_ProductId')
    averageRatings = serializers.SerializerMethodField('get_averageRatings')
    poor = serializers.SerializerMethodField('get_poor')
    average = serializers.SerializerMethodField('get_average')
    good = serializers.SerializerMethodField('get_good')
    veryGood = serializers.SerializerMethodField('get_verygood')
    excellent = serializers.SerializerMethodField('get_excellent')

    def get_ProductId(self, obj):
        return obj.productId

    def get_noRating(self, obj):
        return obj.noRating

    def get_poor(self, obj):
        return obj.poor

    def get_average(self, obj):
        return obj.average

    def get_good(self, obj):
        return obj.good

    def get_verygood(self, obj):
        return obj.veryGood

    def get_excellent(self, obj):
        return obj.excellent

    def get_averageRatings(self, obj):
        return obj.averageRatings
