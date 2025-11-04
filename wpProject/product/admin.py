from django.contrib import admin
from django.shortcuts import HttpResponse,render
from .models import *
from django.template import loader
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from io import BytesIO
from django_xhtml2pdf.utils import pdf_decorator
from wpProject import views

class productDetails(admin.ModelAdmin):
     list_display=('p_name','price','description','qty','image_url','cat_id')
     @admin.action(description = "Generate Product Report")
     def generate_product_report(self, request, queryset):
          product_obj = queryset
          # pdf_data = views.generate_pdf_report(orders)
          # response = HttpResponse(pdf_data, content_type='application/pdf')
          # response['Content-Disposition'] = 'attachment; filename="order_report.pdf"'
          return render(request,"product_report.html",{'product_obj':queryset})
     actions=[generate_product_report]

class product_catDetails(admin.ModelAdmin):
    list_display=('id','cat_name')

# Register your models here.
admin.site.register(product,productDetails)
admin.site.register(product_category,product_catDetails)
