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

class signupUser(admin.ModelAdmin):
    list_display=('firstname','lastname','email','password','gender','phoneNo','state','city','is_created')
    list_filter = ('is_created',)
    @admin.action(description = "Generate Customer Report")
    def generate_customer_report(self, request, queryset):
          customer_obj = queryset
          # pdf_data = views.generate_pdf_report(orders)
          # response = HttpResponse(pdf_data, content_type='application/pdf')
          # response['Content-Disposition'] = 'attachment; filename="order_report.pdf"'
          return render(request,"customer_report.html",{'customer_obj':customer_obj})
    actions=[generate_customer_report]

class getCity(admin.ModelAdmin):
    list_display=('id','c_name')

class display_contactUs(admin.ModelAdmin):
    list_display=['name','email','phone','message','customer','date','is_replied']
    list_filter = ('date',)
    @admin.action(description = "Generate Inquiry Report")
    def generate_inquiry_report(self, request, queryset):
          inquiry_obj = queryset
          # pdf_data = views.generate_pdf_report(orders)
          # response = HttpResponse(pdf_data, content_type='application/pdf')
          # response['Content-Disposition'] = 'attachment; filename="order_report.pdf"'
          return render(request,"inquiry_report.html",{'inquiry_obj':inquiry_obj})
    actions=[generate_inquiry_report]

class display_feedbackRating(admin.ModelAdmin):
    list_display=['id','rating','message','feedback_date','user_id']
    list_filter = ('feedback_date',)
    @admin.action(description = "Generate Feedback Report")
    def generate_feedback_report(self, request, queryset):
          feedback_obj = queryset
          # pdf_data = views.generate_pdf_report(orders)
          # response = HttpResponse(pdf_data, content_type='application/pdf')
          # response['Content-Disposition'] = 'attachment; filename="order_report.pdf"'
          return render(request,"feedback_report.html",{'feedback_obj':feedback_obj})
    actions=[generate_feedback_report]

# # class productDetails(admin.ModelAdmin):
# #     list_display=('p_name','price','description','image_url')
# # Register your models here.
admin.site.register(signupAction,signupUser)
admin.site.register(city,getCity)
admin.site.register(contactUs,display_contactUs)
admin.site.register(feedback_rating,display_feedbackRating)