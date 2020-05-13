# CasaOneAssignment
CasaOne Assignment

Installation:

1. Download the code into your local repository.
2. Create a virtual environment using 'virutalenv -p python3 .'
3. install the dependencies using pip install -r requirements.txt
4. Activate virtualenvironment and run python manage.py runserver.


API's List are available in postman docs.
Below are api that are developed.

1.AddDerived Attributes:
  
     http://127.0.0.1:8000/products/addattributes/
   
    It is POST Request. Json Body format is
     [
        {
            "productId": 2,
            "derivedAttributes": [
                {
                    "key": "time to assemble",
                    "value": "8 hours"
                },
                {
                    "key": "speed of delivery",
                    "value": "24 hours"
                }
            ]
        }
    ]



2. UpdateDerived Attribute API:
    
    
     http://127.0.0.1:8000/products/updateattribute/
     
     It is an PUT request. Json Body format will be
     {
        "productId": 2,
        "derivedAttributes": [
            {
                "key": "time to assemble",
                "value": "45 hours"
            },
            {
                "key": "speed of delivery",
                "value": "30 minutes"
            }
        ]
    }
    
 3. FetchRatingsAPI :
 
        http://127.0.0.1:8000/ratings/?pid=3
        It is a GET request. pid means productId it is mandatory field for 
        fetching product rating.
        
        Output Json be like:
        {
            "productId": 3,
            "averageRatings": "4 out of 5",
            "poor": 0,
            "average": 0,
            "good": 0,
            "veryGood": 1,
            "excellent": 1
        }
     
 4. RecordRatingsAPI:
 
        http://127.0.0.1:8000/ratings/
        It is a POST request. It is for recording the ratings for 
        the purchase products.
        Json Body Format be like:
         {
           "uid":2,
           "puid":1,
           "pid":2,
           "rating":5
        }
        Here is uid means userid it is redundant. puid means purchaseid
        pid means productid and ratings is between 1-5.