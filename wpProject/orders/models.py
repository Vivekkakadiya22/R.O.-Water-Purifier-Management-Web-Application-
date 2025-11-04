from django.db import models
from product.models import product
from signup.models import signupAction
import datetime
from django.core.exceptions import ValidationError

# Create your models here.
class order(models.Model):
    product=models.ForeignKey(product,on_delete=models.CASCADE)
    customer=models.ForeignKey(signupAction,on_delete=models.CASCADE)
    quantity=models.IntegerField(default=1)
    price=models.IntegerField()
    address=models.TextField(default='',blank=True)
    phone=models.CharField(max_length=50,default='',blank=True)
    payment_mode=models.CharField(max_length=15,default='Online')
    date=models.DateField(default=datetime.datetime.today)
    payment_status=models.BooleanField(default=False)
    delivery_status=models.BooleanField(default=False)
    is_canceled=models.BooleanField(default=False)

    def placeorder(self):
        self.save()

    @staticmethod
    def get_orders_by_customer(customer_id):
        return order.objects.filter(customer=customer_id).order_by('-date')
    
    def __str__(self) -> str:
        return self.product.p_name

class amc_plans(models.Model):
    plan_name=models.CharField(max_length=40,unique=True)
    plan_description=models.TextField()
    price=models.IntegerField()
    service=models.BooleanField(default=True)
    filter=models.BooleanField(default=False)
    membrane=models.BooleanField(default=False)
    electric_parts=models.BooleanField(default=False)
    faulty_parts=models.BooleanField(default=False)

    def clean(self):
        if self.price <= 0:
            raise ValidationError("Price or Quantity must be greater than 0.")
        super().clean()

    def __str__(self) -> str:
        return self.plan_name

class amc_orders(models.Model):
    phone=models.CharField(max_length=10,blank=False)
    address=models.TextField(blank=False)
    amc_plan=models.ForeignKey(amc_plans,on_delete=models.CASCADE)
    customer=models.ForeignKey(signupAction,on_delete=models.CASCADE)
    date=models.DateField(default=datetime.datetime.today)

class payment(models.Model):
    order=models.ForeignKey(order,on_delete=models.CASCADE,null=True)
    amc_plan=models.ForeignKey(amc_orders,on_delete=models.CASCADE,null=True)
    note=models.CharField(max_length=50,default='',blank=True,null=True)
    total_amount=models.IntegerField()
    payment_date=models.DateField(default=datetime.datetime.today)
    payment_status=models.BooleanField(default=False)