from django.shortcuts import render,redirect,HttpResponseRedirect
from .models import *
from random import randint
from django.contrib.auth.hashers import make_password,check_password
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import authenticate,login,logout
from django.conf import settings
from django.core.mail import send_mail
from django.contrib import messages
from django.urls import reverse
# Create your views here.

def registerUser(request):
    if request.method=="POST":
        fname=request.POST['fname']
        lname=request.POST['lname']
        email=request.POST['email']
        password=request.POST['password']
        cpassword=request.POST['cpassword']
        gender=request.POST['gender']
        phoneNo=request.POST['phone']
        address=request.POST['address']
        state=request.POST['state']
        city=request.POST['city']
        zipcode=request.POST['zipcode']

        request.session['fname']=fname
        request.session['lname']=lname
        request.session['email']=email
        request.session['phone']=phoneNo
        request.session['gender']=gender
        request.session['address']=address
        request.session['state']=state
        request.session['city']=city
        request.session['zipcode']=zipcode

        user=signupAction.objects.filter(email=email)

        if user:
            message="User already exist"
            return render(request,"registration.html",{'msg':message,'error':True})
        else:
            if password == cpassword:
                otp=sendOtp(request.session["email"])
                request.session['otp']=otp
                hash_password=make_password(password)
                request.session['password']=hash_password
                return render(request,"otpverify.html",{'email':email})
            else:
                message="Passwords do not match, please enter same passowrd in both password field"
                return render(request,"registration.html",{'msg':message,'error':True})
    
    return render(request,"registration.html")

def sendOtp(e_mail):
    subject="OTP Verification!!"
    otp=randint(1000,9999)
    message = f"Dear customer, This is from RO WALA PVT. LTD., Thank you for registering in our website!!Your one-time verification code is {otp}."
    from_email=settings.EMAIL_HOST_USER
    recipient_list = [e_mail]
    send_mail(subject,message,from_email,recipient_list,fail_silently=False)
    return otp

def optVerify(request):
    uotp=int(request.POST['otp'])
    if int(request.session["otp"]) == uotp:
        newUser=signupAction.objects.create(firstname=request.session['fname'],lastname=request.session['lname'],email=request.session['email'],password=request.session['password'],gender=request.session['gender'],phoneNo=request.session['phone'],address=request.session['address'],state=request.session['state'],city=request.session['city'],zipcode=request.session['zipcode'])
        newUser.save()
        message1="OTP Verify successfully!"
        return render(request,"login.html",{'msg1':message1})
    else:
        message2="OTP is incorrect"
        return render(request,"otpverify.html",{'msg2':message2})
    # else:
    #     return render(request,"registration.html")
    
def loginUser(request):
    if request.method=="POST":
        email=request.POST['email']
        password=request.POST['password']

        try:
            user=signupAction.objects.get(email=email)
            # print(user)
            # print('in try')
            if user:
                 hash_password=check_password(password,user.password)
                 if hash_password:
                    request.session['customer_id']=user.id
                    request.session['fname']=user.firstname
                    request.session['lname']=user.lastname
                    request.session['email']=user.email
                    request.session["islogin"]=True
                    message="Login Successfull!"
                    return render(request,"index.html",{'msg1':message,'user':user})
                 else:
                    message="Password does not match"
                    return render(request,"login.html",{'msg1':message,'error':True})
        except ObjectDoesNotExist:
            print('in except')
            message="User does not exist"
            return render(request,"login.html",{'msg1':message,'error':True})
        
    return render(request,"login.html")

def logoutUser(request):
    logout(request)
    return render(request,"login.html")

def change_password_action(request):
    current_pass=request.POST.get('currentpassword')
    new_pass=request.POST.get('newpassword')
    confirm_pass=request.POST.get('confirmpassword')
    userid=request.session.get('customer_id')
    getUser=signupAction.objects.get(id=userid)
    checkpassword=check_password(current_pass,getUser.password)
    if checkpassword:
        if new_pass == current_pass:
            messages="New password must be different from your old password!"
            return render(request,"change_password.html",{'msg':messages,'error':True})

        elif new_pass == confirm_pass:
            hash_password=make_password(new_pass)
            getUser.password=hash_password
            getUser.save()
            messages="Your Password changed successfully!"
            logout(request)
            return HttpResponseRedirect(reverse('login') + f'?msg1={messages}')
        else:
            messages="New password and confirm password should be same!"
            return render(request,"change_password.html",{'msg':messages,'error':True})
    else:
        messages="Your old password is wrong! Please try again."
        return render(request,"change_password.html",{'msg':messages,'error':True})


def resetOtp(email):
    subject = "OTP Verification!!!"
    otp = randint(1000,9999)
    message = f"dear customer, Your one-time verification code for reset password is {otp}."
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject,message,from_email,recipient_list,fail_silently=False)
    return otp

def forgotpassword_action(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        request.session['email']=email
        # print("user email = ",email)
        try:
            user = signupAction.objects.get(email = request.session['email'])
            if user:
                otp = resetOtp(email)
                request.session["otp"] = otp
                return render(request, 'resetotp.html',{'email':email})
        except ObjectDoesNotExist:
            message = 'email does not exist.'
            return render(request, 'email.html', {'msg2': message}) 

def verify_resetotp(request):
    uotp = int(request.POST.get('otp'))
    if int(request.session["otp"]) == uotp:
        return render(request,'forgotpassword.html')
    else:
        massage='OTP is invalid.'
        return render(request,'resetotp.html',{'msg2':massage})

def forgot_password(request):
    password=request.POST.get('newpassword')
    c_password=request.POST.get('confirmpassword')
    if password==c_password:
        user = signupAction.objects.get(email = request.session['email'])
        hash_pass=make_password(password)
        user.password=hash_pass
        user.save()
        message="Password reset successfully!"
        return render(request,'login.html',{'msg1':message})
    else:
        message='password and confirm password must be same'
        return render(request,'forgotpassword.html',{'msg':message,'error':True})