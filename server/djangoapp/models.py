from django.db import models
from django.utils.timezone import now


# Create your models here.

class CarMake(models.Model):
    name = models.CharField(null=False, max_length=50)
    description = models.CharField(max_length=1000)
    
    def __str__(self):
        return "Name: " + self.name + "," + \
               "Description: " + self.description


class CarModel(models.Model):
    car_make = models.ForeignKey(CarMake, on_delete=models.CASCADE)
    dealer_id = models.IntegerField()
    SEDAN = 'Sedan'
    SUV = 'suv'
    WAGON = 'wagon'
    CAR_TYPE = [
    (SEDAN, 'Sedan'),
    (SUV, 'suv'),
    (WAGON, 'wagon')
    ]
    type = models.CharField(max_length=5, choices=CAR_TYPE, default=SEDAN)
    year = models.DateDield(default=now)
    
    def __str__(self):
        return "Name: " + self.name + "," + \
               "Description: " + self.description


# <HINT> Create a plain Python class `CarDealer` to hold dealer data


# <HINT> Create a plain Python class `DealerReview` to hold review data
