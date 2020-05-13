
from .models import Product,PurchaseOrderDetails,Ratings
import math

class RatingSerialiszerHelper():

    def __init__(self,Product):
        self.productId = Product.productId
        hashMap = [0 for i in range(6)]
        pods = PurchaseOrderDetails.objects.filter(productId=Product)
        for pod in pods:
            rating = Ratings.objects.filter(purchaseOrderDetailsId=pod).values()
            hashMap[rating[0]['ratings']] += hashMap[rating[0]['ratings']] + 1
        self.noRating = hashMap[0]
        self.poor = hashMap[1]
        self.average = hashMap[2]
        self.good = hashMap[3]
        self.veryGood = hashMap[4]
        self.excellent = hashMap[5]
        total_sum = 1 * hashMap[1] + 2 * hashMap[2] \
                    + 3 * hashMap[3] + 4 * hashMap[4] \
                    + 5 * hashMap[5]
        total = sum(hashMap)
        RATINGS = (
            (0, 'NO Rating'),
            (1, 'Poor'),
            (2, 'Average'),
            (3, 'Good'),
            (4, 'Very Good'),
            (5, 'Excellent'),
        )

        self.averageRatings =str(math.floor(total_sum / total))+' out of 5'