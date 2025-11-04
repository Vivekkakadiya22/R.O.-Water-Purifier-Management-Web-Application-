from django.db import models
from django.utils import timezone
from datetime import datetime
import datetime

# Create your models here.
class signupAction(models.Model):
    firstname=models.CharField(max_length=40)
    lastname=models.CharField(max_length=40)
    email=models.EmailField(max_length=50)
    password=models.CharField(max_length=255)
    gender=models.CharField(max_length=10)
    phoneNo=models.CharField(max_length=10)
    address=models.TextField()
    state=models.CharField(max_length=20)
    city=models.CharField(max_length=20)
    zipcode=models.CharField(max_length=6)
    is_created=models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f'{self.firstname} {self.lastname}'
   
class city(models.Model):
    c_name=models.CharField(max_length=40)

class contactUs(models.Model):
    name=models.CharField(max_length=40)
    email=models.CharField(max_length=50)
    phone=models.CharField(max_length=10)
    message=models.TextField()
    customer=models.ForeignKey(signupAction,on_delete=models.CASCADE,default='',blank=True,null=True)
    date=models.DateField(default=datetime.datetime.today)
    is_replied=models.BooleanField(default=False)

class feedback_rating(models.Model):
    rating=models.IntegerField()
    message=models.TextField()
    feedback_date=models.DateTimeField(default=datetime.datetime.today)
    user_id=models.ForeignKey(signupAction,on_delete=models.CASCADE,default='',null=True)