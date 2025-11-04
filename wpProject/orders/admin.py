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

# def download_pdf(self, request, queryset):
#      model_name = self.model.__name__
#      response=HttpResponse(content_type='application/pdf')
#      response['content-Disposition']='attachment; filename={model_name}.pdf'

#      pdf=canvas.Canvas(response, pagesize=letter)
#      pdf.setTitle('PDF Report')

#      headers=[field.verbose_name for field in self.model._meta.fields]
#      data=[headers]

#      for obj in queryset:
#           data_row=[str(getattr(obj, field.name)) ]

admin.site.site_header = "RO WALA"
# Register your models here.
class display_orders(admin.ModelAdmin):
     list_display=('id','product','customer','quantity','price','date','payment_mode','payment_status','delivery_status','is_canceled')
     list_filter = ('date','is_canceled')

     @admin.action(description = "Generate Order Report")
     def generate_order_report(self, request, queryset):
          orders = queryset
          # pdf_data = views.generate_pdf_report(orders)
          # response = HttpResponse(pdf_data, content_type='application/pdf')
          # response['Content-Disposition'] = 'attachment; filename="order_report.pdf"'
          return render(request,"report.html",{'orders':queryset})

     @admin.action(description = "Generate Cancel Order Report")
     def generate_cancelOrder_report(self, request, queryset):
          orders = queryset
          # pdf_data = views.generate_pdf_report(orders)
          # response = HttpResponse(pdf_data, content_type='application/pdf')
          # response['Content-Disposition'] = 'attachment; filename="order_report.pdf"'
          return render(request,"report.html",{'orders':queryset,'cancel':True})
     actions=[generate_cancelOrder_report,generate_order_report]


     # generate_report.short_description = "Generate Order Report"

class payment_diplay(admin.ModelAdmin):
     list_display=['order','amc_plan','note','total_amount','payment_date','payment_status']

class amc_display(admin.ModelAdmin):
     list_display=['plan_name','plan_description','price','service','filter','membrane','electric_parts','faulty_parts']

class amc_orders_display(admin.ModelAdmin):
     list_display=['phone','address','amc_plan','customer','date']
     list_filter = ('date',)
     @admin.action(description = "Generate AMC Order Report")
     def generate_amc_report(self, request, queryset):
          orders = queryset
         
          # pdf_data = views.generate_pdf_report(orders)
          # response = HttpResponse(pdf_data, content_type='application/pdf')
          # response['Content-Disposition'] = 'attachment; filename="order_report.pdf"'
          return render(request,"amc_order_report.html",{'orders':queryset})
     actions=[generate_amc_report]


# admin.site.register(order,display_orders)
admin.site.register(payment,payment_diplay)
# admin.site.register(amc_plans,amc_display)
# admin.site.register(amc_orders,amc_orders_display)