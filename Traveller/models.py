from django.db import models
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField
class User(AbstractUser):
    email = models.EmailField("email",unique=True)
    profile_picture = models.ImageField(upload_to='profile_pics', blank=True, null=True)
    
class Contact(models.Model):
    msg= models.TextField(max_length=3000)
    name=models.CharField(max_length=50)
    email=models.EmailField()
    sub=models.TextField(max_length=500)

class TripQueries(models.Model):
    name=models.CharField(max_length=50)
    phno=PhoneNumberField()
    query=models.TextField()

class destination(models.Model):
    name = models.CharField(max_length=100)
    cont = models.CharField(max_length=200)
    short_desc = models.CharField(max_length=255,default="")
    brief_desc = models.TextField(default="")
    img = models.ImageField(upload_to='imgs')
    price = models.PositiveIntegerField()
    flag = models.BooleanField(default=False)
    reviews = models.PositiveIntegerField()
    days = models.PositiveIntegerField()
    def __str__(self):
        return self.name

class DestinationDay(models.Model):
    name = models.ForeignKey(destination, on_delete=models.CASCADE)
    day_number = models.IntegerField()
    day_info = models.TextField()
    
class pop_dest(models.Model):
    cimg=models.ImageField(upload_to='cimgs')
    coun_name=models.CharField(max_length=25)
    no_places=models.PositiveIntegerField()

class testimonial(models.Model):
    comment = models.TextField()
    author = models.CharField(max_length=20)
    timg= models.ImageField(upload_to='timgs')

class BookTrip(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    destination= models.ForeignKey(destination,on_delete=models.CASCADE)
    tourist_name=models.CharField(max_length=50)
    tourist_email=models.EmailField()
    tourist_phone=PhoneNumberField()
    start_date=models.DateField()
    special_requests=models.TextField(blank=True)
    def __str__(self):
        return f"{self.tourist_name}-{self.destination.name}"