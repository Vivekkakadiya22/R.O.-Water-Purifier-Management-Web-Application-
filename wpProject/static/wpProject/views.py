from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render,redirect

def header(request):
    return render(request,'header.html')

def home(request):
    return render(request,'index.html')

def aboutUs(request):
    return render(request,'about.html')

def blog(request):
    return render(request,'blog.html')

def contact(request):
    return render(request,'contact.html')

def login(request):
    return render(request,'login.html')

def registration(request):
    return render(request,'registration.html')

def products(request):
    return render(request,'products.html')