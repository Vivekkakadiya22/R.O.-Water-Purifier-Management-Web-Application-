from django.db import models
from django.core.exceptions import ValidationError
# Create your models here.
class product_category(models.Model):
    id=models.AutoField(primary_key=True)
    cat_name=models.CharField(max_length=50)
    def __str__(self):
        return self.cat_name

   


class product(models.Model):
    p_name=models.CharField(max_length=100, unique=True)
    price=models.IntegerField()
    description=models.TextField()
    cat_id=models.ForeignKey(product_category,on_delete=models.CASCADE)
    qty=models.IntegerField(default=0)
    image_url=models.FileField(upload_to="product_images/",max_length=250,null=True,default=None)

    def clean(self):
        if self.price <= 0 or self.qty < 0:
            raise ValidationError("Price or Quantity must be greater than 0.")
        super().clean()

    @staticmethod
    def get_products_by_id(ids):
        ids = [id for id in ids if id.isdigit()]
        return product.objects.filter(id__in=ids)
   
    def __str__(self):
       return self.p_name
   