from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render,redirect
from product.models import *
from signup.models import *
from orders.models import *
from django.utils import timezone
from datetime import timedelta
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from middlewares.auth import auth_middleware
from django.db.models import Max
from django.template import loader
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from io import BytesIO
from django.template.loader import get_template
import uuid
from django.urls import reverse
from django.contrib import messages
from django.conf import settings
from django.core.mail import send_mail


def otpPage(request):
    return render(request,"otpverify.html")

def profile_page(request):
    customer_obj=signupAction.objects.get(id=request.session['customer_id'])
    return render(request,"profile.html",{'customer_obj':customer_obj})

def profile_edit_page(request):
    customer_obj=signupAction.objects.get(id=request.session['customer_id'])
    return render(request,"edit.html",{'customer_obj':customer_obj})

def resetotpPage(request):
    return render(request,"resetotp.html")

def insertProduct(request):
    return render(request,"insert_product.html")

def header(request):
    return render(request,'header.html')

def footer(request):
    return render(request,'footer.html')

def forgotpassPage(request):
    return render(request,'forgotpassword.html')

def emailPage(request):
    return render(request,"email.html")

def home(request):
    return render(request,'index.html')

def aboutUs(request):
    feedback_obj=feedback_rating.objects.all()[1:8]
    return render(request,'about.html',{'feedback_obj':feedback_obj})

def amc(request):
    amc_obj=amc_plans.objects.all()
    return render(request,'amc.html',{'amc_obj':amc_obj})

def amc_detail_page(request):
    return render(request,"amc_detail.html")

def offer(request):
    return render(request,'offer.html')

def search(request):
    return render(request,'searchbar.html')

def feedback_page(request):
    return render(request,"feedback.html")

def feedback_action(request):
    if request.method == "POST":
        rating=request.POST.get('star')
        feedback_message=request.POST.get('feedback')
        # print("rating = ",rating)
        user_obj=signupAction.objects.get(id=request.session['customer_id'])
        feedback_obj=feedback_rating.objects.create(rating=rating,message=feedback_message,user_id=user_obj)
        feedback_obj.save()
        fname=user_obj.firstname
        lname=user_obj.lastname
        subject="Feedback and rating"
        email_message=f"Thank You {fname} {lname} for giving your valuable feedback and ratings! Keep touch with us."
        from_email=settings.EMAIL_HOST_USER
        recipient_list=[user_obj.email]
        send_mail(subject,email_message,from_email,recipient_list,fail_silently=False)
        message="Your feedback and rating sent successfully!!"
        return render(request,"feedback.html",{'message':message})
    return render(request,"feedback.html")

def contact(request):
    if request.session.get('islogin', False):
        customer_obj=signupAction.objects.get(id=request.session['customer_id'])
        return render(request,'contact.html',{'customer_obj':customer_obj})
    return render(request,'contact.html')

def paymentPage(request):
    return render(request,'payment.html')

def invoice_page(request):
    return render(request,"invoice.html")

def select_time_range_page(request):
    return render(request,"select_time_range.html")

def reportPage(request):
    return render(request,"report.html")

def customer_reportPage(request):
    return render(request,"customer_report.html")

def inquiry_reportPage(request):
    return render(request,"inquiry_report.html")

def feedback_reportPage(request):
    return render(request,"feedback_report.html")

def product_reportPage(request):
    return render(request,"product_report.html")

def paymentsuccessfullPage(request):
    return render(request,"paymentsuccessfull.html")

def searchPage(request):
    return render(request,"search.html")

def login(request):
    msg1 = request.GET.get('msg1', None)
    return render(request,'login.html',{'msg1':msg1})

def registration(request):
    getCity=city.objects.all()
    cityDetails={
        'getCity':getCity
    }
    return render(request,'registration.html',cityDetails)

def cancle_confirm_page(request):
    order_id=request.POST.get('order_id')
    # print("order id === ",order_id)
    return render(request,"cancle_confirm.html",{'order_id':order_id})

def cancel_reason_page(request,order_id):
    return render(request,"cancel_reason.html",{'order_id':order_id})

def confirm_msg_page(request): #Confirm msg for cancel order
    order_id=request.POST.get('order_id')
    order_obj=order.objects.get(id=order_id)
    order_obj.is_canceled=True
    order_obj.save()
    sendEmail(request.session['email'],order_id)
    return render(request,"confirm_msg.html")

def sendEmail(e_mail,order_id):
    order_obj=order.objects.get(id=order_id)
    if order_obj.payment_mode == "Online" or order_obj.payment_mode == "online":
        subject="Order Cancellation!!"
        message = f"Dear customer, This is from RO WALA PVT. LTD., Your order has been canceled successfully! You will get your refunds as soon as possible. Order id was {order_id}."
        from_email=settings.EMAIL_HOST_USER
        recipient_list = [e_mail]
    else:
        subject="Order Cancellation!!"
        message = f"Dear customer, This is from RO WALA PVT. LTD., Your order has been canceled successfully! Order id was {order_id}."
        from_email=settings.EMAIL_HOST_USER
        recipient_list = [e_mail]
    send_mail(subject,message,from_email,recipient_list,fail_silently=False)

def contactUs_action(request):
    if request.method == 'POST':
        if request.session.get('islogin', False):
            user_id=request.POST.get('user_id')
            customer_obj=signupAction.objects.get(id=user_id)
            name=request.POST.get('name')
            email=request.POST.get('email')
            phone=request.POST.get('phone')
            message=request.POST.get('message')
            subject="Customer inquiry"
            from_email=email
            recipient_list = [settings.EMAIL_HOST_USER]
            contact_obj=contactUs.objects.create(name=name,email=email,phone=phone,message=message,customer=customer_obj)
            contact_obj.save()
            send_mail(subject,message,from_email,recipient_list,fail_silently=False)
            messages.success(request, "Your inquiry sent successfully!")
            data={
                'message': messages.get_messages(request)
            }
            return render(request,"index.html",data)
        else:
            name=request.POST.get('name')
            email=request.POST.get('email')
            phone=request.POST.get('phone')
            message=request.POST.get('message')
            subject="Customer inquiry"
            from_email=email
            recipient_list = [settings.EMAIL_HOST_USER]
            contact_obj=contactUs.objects.create(name=name,email=email,phone=phone,message=message)
            contact_obj.save()
            send_mail(subject,message,from_email,recipient_list,fail_silently=False)
            messages.success(request, "Your inquiry sent successfully!")
            data={
                'message': messages.get_messages(request)
            }
            return render(request,"index.html",data)

def invoice_action(request):
    if request.method == "POST":
        invoice_cntr=0
        order_id=request.POST.get('order_id')
        order_obj=order.objects.get(id=order_id)
        current_date=datetime.datetime.today
        customer_obj=signupAction.objects.get(id=request.session['customer_id'])
        data={
            'order_obj':order_obj,
            'current_date':current_date,
            'customer_obj':customer_obj
        }
        return render(request,"invoice.html",data)

# def save_pdf(params:dict):
#     template=get_template("templates/invoice.html")
#     html=template.render(params)
#     response=BytesIO()
#     pdf=pisa.pisaDocument(BytesIO(html.encode('UTF-8')), response)
#     file_name=uuid.uuid4()


# def generate_report(request):
#     orders = order.objects.all()
#     template = loader.get_template('report_template.html')
#     context = {'orders': orders}
#     html = template.render(context)
#     return HttpResponse(html)

def edit_action(request):
    fname=request.POST.get('fname')
    lname=request.POST.get('lname')
    email=request.POST.get('email')
    phone=request.POST.get('phone')
    address=request.POST.get('address')

    customer_obj=signupAction.objects.get(id=request.session['customer_id'])
    customer_obj.firstname=fname
    customer_obj.lastname=lname
    customer_obj.phoneNo=phone
    customer_obj.address=address
    customer_obj.save()
    request.session['fname']=fname
    request.session['lname']=lname
    request.session['phone']=phone
    request.session['address']=address
    message="Your profile has been edited!"
    return render(request,"profile.html",{'customer_obj':customer_obj,'msg':message})

def generate_pdf_report(orders):
          buffer = BytesIO()

          # Create a new PDF
          pdf = SimpleDocTemplate(buffer, pagesize=letter)
          elements = []

          # Define table data
          data = [["Order Number", "Order Date", "Customer Name","Quantity","Price"]]
          for order in orders:
               data.append([order.id, order.date, f"{order.customer.firstname} {order.customer.lastname}",order.quantity,order.price])

          # Create table
          table = Table(data)
          table.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#007bff')),
                                        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                                        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                                        ('FONTNAME', (0, 0), (-1, 0), 'Times-Roman'),
                                        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                                        ('BACKGROUND', (0, 1), (-1, -1), colors.lightgrey),
                                        ]))
          table.setStyle(TableStyle([
                ('LINEABOVE', (0, 0), (-1, -1), 0, colors.white),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
                ('LEFTPADDING', (0, 0), (-1, -1), 10),
                ('RIGHTPADDING', (0, 0), (-1, -1), 10),
                ('TOPPADDING', (0, 0), (-1, -1), 10),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
                ('SIZE', (0, 0), (-1, -1), 12),
            ]))
          elements.append(table)

          # Write PDF to buffer
          pdf.build(elements)
          pdf_data = buffer.getvalue()
          buffer.close()

          return pdf_data
     
# def generate_report(request):
#     # Assuming you have a form to select the time range
#     if request.method == 'POST':
#         start_date = request.POST.get('start_date')
#         end_date = request.POST.get('end_date')
        
#         # Query orders based on the selected time range
#         orders = order.objects.filter(date__range=[start_date, end_date])

#         # Pass orders to the template for rendering
#         return render(request, 'report.html', {'orders': orders})
#     else:
#         # Render form to select time range
#         return render(request, 'select_time_range.html')

# def product_search(request):
#     query = request.GET.get('query')
#     if query:
#         filtered_products = product.objects.filter(p_name__icontains=query)
#     else:
#         filtered_products = product.objects.all()
#     return render(request, 'products.html', {'filtered_products': filtered_products,'search':True})

def product_filter(request):
    if request.GET.get('range1'):
        rangevalue1=request.GET['rangevalue1']
        rangevalue2=request.GET['rangevalue2']
        if rangevalue1 and rangevalue2:
            filter_products=product.objects.filter(price__gte=rangevalue1, price__lte=rangevalue2)
        else:
            filter_products=product.objects.all()
        return render(request,"products.html",{'filter_products':filter_products}) 
    
    elif request.GET.get('range2'):
        rangevalue3=request.GET['rangevalue3']
        rangevalue4=request.GET['rangevalue4']
        if rangevalue3 and rangevalue4:
            filter_products=product.objects.filter(price__gte=rangevalue3, price__lte=rangevalue4)
        else:
            filter_products=product.objects.all()
        return render(request,"products.html",{'filter_products':filter_products})
    
    elif request.GET.get('range3'):
        rangevalue5=request.GET['rangevalue5']
        rangevalue6=request.GET['rangevalue6']
        if rangevalue5 and rangevalue6:
            filter_products=product.objects.filter(price__gte=rangevalue5, price__lte=rangevalue6)
        else:
            filter_products=product.objects.all()
        return render(request,"products.html",{'filter_products':filter_products})
    
    elif request.GET.get('range4'):
        rangevalue7=request.GET['rangevalue7']
        rangevalue8=request.GET['rangevalue8']
        if rangevalue7 and rangevalue8:
            filter_products=product.objects.filter(price__gte=rangevalue7, price__lte=rangevalue8)
        else:
            filter_products=product.objects.all()
        return render(request,"products.html",{'filter_products':filter_products})
    
    elif request.GET.get('range5'):
        rangevalue9=request.GET['rangevalue9']
        if rangevalue9:
            filter_products=product.objects.filter(price__gte=rangevalue9)
        else:
            filter_products=product.objects.all()
        return render(request,"products.html",{'filter_products':filter_products})
    
    elif request.GET.get('range6'):
        min_price=product.objects.order_by('price').first()
        return render(request,"products.html",{'min_price':min_price})
    
    elif request.GET.get('range7'):
        max_price = product.objects.aggregate(max_price=Max('price'))['max_price']
        max_price=product.objects.filter(price=max_price).first()
        return render(request,"products.html",{'max_price':max_price})
    
    

def product_search(request):
    query=request.GET['query']
    allproducts=product.objects.filter(p_name__icontains=query)
    data={'allproducts':allproducts}
    # print("data == ",data)
    return render(request,"search.html",data)
    # return HttpResponse("This is search page")

def products(request):
    pro_id=request.POST.get('product')
    remove=request.POST.get('remove')
    cart=request.session.get('cart')

    proDetails=product.objects.all()
    procatDetails=product_category.objects.all()  
    
    if not cart:
        request.session['cart']={}
    if cart:
        quantity=cart.get(pro_id)
        if quantity:
            product_instance = product.objects.get(id=pro_id)
            if remove:
                if quantity<=1:
                    cart.pop(pro_id)
                else:
                    cart[pro_id]=quantity-1
            else:
                if quantity + 1 <= product_instance.qty:
                    cart[pro_id] = quantity + 1
                else:
                    messages.error(request, f"Stock is limited. You cannot add more than {product_instance.qty} items.")
        else:
            cart[pro_id]=1
    else:
        cart={}
        cart[pro_id]=1
    
    request.session['cart']={key: value for key, value in cart.items() if key not in ['null', None]}
    print('cart = ',request.session['cart'])
    details={
         'proDetails':proDetails,
         'procatDetails':procatDetails,
         'message': messages.get_messages(request),
     }
    return render(request,'products.html',details)

def getCat(request,cat_id):
    cats=product_category.objects.get(id=cat_id)
    request.session['c_id']=cats.id
    selected_cat=request.session.get('c_id')
    getProduct=product.objects.filter(cat_id=selected_cat)
    #print(getProduct)
    procatDetails=product_category.objects.all()
    details={
        'procatDetails':procatDetails,
        'getProduct':getProduct
    }
    return render(request,'product_cat.html',details)


def cart(request):
    cart_data = request.session.get('cart', {})
    ids = list(cart_data.keys())
    filtered_list=[item for item in ids if item is not None and item != 'null']
    print("list = ",filtered_list)
    products=product.get_products_by_id(filtered_list)
    print("products = ",products)
    return render(request,'cart.html',{'products':products,'filtered_list':filtered_list})

def productDetails_page(request,p_id):
    productDetail=product.objects.filter(id=p_id)
    pro_id=request.POST.get('productDetail')
    remove=request.POST.get('remove')
    cart=request.session.get('cart')
    # print("p_id = ",pro_id)
    
    if not cart:
        request.session['cart']={}
    if cart:
        quantity=cart.get(pro_id)
        if quantity:
            if remove:
                if quantity<=1:
                    cart.pop(pro_id)
                else:
                    cart[pro_id]=quantity-1
            else:
                cart[pro_id]=quantity+1
        else:
            cart[pro_id]=1
    else:
        cart={}
        cart[pro_id]=1

    request.session['cart']=cart
    data={
        'productDetail':productDetail
    }
    # print(request.session['cart'])
    return render(request,"product_details.html",data)

def remove_from_cart(request,p_id):
    if 'cart' in request.session:
        cart = request.session['cart']

        # Check if the product is in the cart
        if str(p_id) in cart:
            # Remove the product from the cart
            del cart[str(p_id)]
            
            # Save the updated cart in the session
            request.session['cart'] = cart
    return render(request,"cart.html")

def change_password(request):
    return render(request,"change_password.html")

def checkout_page(request):#checkout_page from cart
    cart=request.session['cart']
    customer=signupAction.objects.get(id=request.session['customer_id'])
    # print("check cart = ",cart)
    products=product.get_products_by_id(list(cart.keys()))
    return render(request,"checkout.html",{'products':products,'customer':customer,'cart':True})

def checkout_buynow(request):#checkout_page from buynow
    p_id=request.POST.get('product')
    products=product.objects.get(id=p_id)
    customer=signupAction.objects.get(id=request.session['customer_id'])
    # print("buy now product = ",products)
    return render(request,"checkout_buynow.html",{'products':products,'customer':customer,})

def checkout_buynow_action(request):#action for buynow
    phone=request.POST.get('phone')
    address=request.POST.get('address') 
    pro_id=request.POST.get('product_id')
    qty = int(request.POST.get('qty'))
    totalamount=request.POST.get('totalamount')
    totalamount=int(totalamount)
    paymentmode=request.POST.get('paymentmode')
    customer=request.session.get('customer_id')
    products = product.objects.get(id=pro_id)
    # print("pidd=",pro_id)
    p_qty=products.qty
    p_status=True
    d_status=False
    if qty > p_qty:
            customer=signupAction.objects.get(id=request.session['customer_id'])
            # Display error message
            message=f"Sorry, only {p_qty} quantity available in stock for this product."
            return render(request,"checkout_buynow.html",{'products':products,'customer':customer,'message':message})

    # print(phone, address, customer, cart, products)
    if paymentmode=="COD":
        p_status=False
            
        orders=order(customer=signupAction(id=customer),
                            product=products,
                            price=products.price,
                            address=address,
                            phone=phone,
                            payment_mode=paymentmode,
                            payment_status=p_status,
                            delivery_status=d_status,
                            quantity=qty)
        orders.placeorder()
        product_obj=product.objects.get(id=pro_id)
        product_obj.qty=product_obj.qty-qty
        product_obj.save()
        return render(request, "order_confirmation.html")
    else:
        p_status=True
            
        orders=order(customer=signupAction(id=customer),
                            product=products,
                            price=products.price,
                            address=address,
                            phone=phone,
                            payment_mode=paymentmode,
                            payment_status=p_status,
                            delivery_status=d_status,
                            quantity=qty)
        orders.placeorder()
        product_obj=product.objects.get(id=pro_id)
        product_obj.qty=product_obj.qty-qty
        product_obj.save()
        return render(request,"payment.html",{'totalamount':totalamount,'orders':orders})


def checkout_action(request):
    phone=request.POST.get('phone')
    address=request.POST.get('address')  
    paymentmode=request.POST.get('paymentmode')
    totalamount=request.POST.get('totalAmount')
    totalamount=int(totalamount)
    customer=request.session.get('customer_id')
    cart=request.session.get('cart')
    products=product.get_products_by_id(list(cart.keys()))
    p_status=False
    d_status=False
    # print("product id == ", products)
    if paymentmode=="COD":
        p_status=False
        for product1 in products:
            
            
            orders=order(customer=signupAction(id=customer),
                     product=product1,
                     price=product1.price,
                     address=address,
                     phone=phone,
                     payment_mode=paymentmode,
                     payment_status=p_status,
                     delivery_status=d_status,
                     quantity=cart.get(str(product1.id)))
            orders.placeorder()
            product1.qty=product1.qty-cart.get(str(product1.id))
            product1.save()
        request.session['cart']={}
        return render(request, "order_confirmation.html")
    else:
        p_status=True
        for product1 in products:
            orders=order(customer=signupAction(id=customer),
                     product=product1,
                     price=product1.price,
                     address=address,
                     phone=phone,
                     payment_mode=paymentmode,
                     payment_status=p_status,
                     delivery_status=d_status,
                     quantity=cart.get(str(product1.id)))
            orders.placeorder()
            product1.qty=product1.qty-cart.get(str(product1.id))
            product1.save()
        request.session['cart']={}
        return render(request,"payment.html",{'totalamount':totalamount,'orders':orders})

def payment_process(request):
    
        totalamount=request.POST.get('totalamount')
        order_id=request.POST.get('order_id')
        note=request.POST.get('note')
        price=request.POST.get('price')
        amc_orderid=request.POST.get('amc_orderid')
        note1=request.POST.get('note1')

        if order_id:
            orders=order.objects.get(id=order_id)
        
            paymentstatus=True
            payment_object=payment.objects.create(order=orders,note=note,total_amount=totalamount,payment_status=paymentstatus)
            payment_object.save()

        if amc_orderid:
            amc_order=amc_orders.objects.get(id=amc_orderid)
            paymentstatus=True
            payment_object=payment.objects.create(amc_plan=amc_order,note=note1,total_amount=price,payment_status=paymentstatus)
            payment_object.save()
        return render(request,"paymentsuccessfull.html")
# def checkout_action(request):
#     phone=request.POST.get('phone')
#     address=request.POST.get('address')  
#     paymentmode=request.POST.get('paymentmode')
#     customer=request.session.get('customer_id')
#     cart=request.session.get('cart')
#     products=product.get_products_by_id(list(cart.keys()))
#     status=True
#     # print(phone, address, customer, cart, products)
#     if paymentmode=="COD":
#         status=False
#     else:
#         status=True

#     for product1 in products:
#         orders=order(customer=signupAction(id=customer),
#                      product=product1,
#                      price=product1.price,
#                      address=address,
#                      phone=phone,
#                      payment_mode=paymentmode,
#                      status=status,
#                      quantity=cart.get(str(product1.id)))
#         orders.placeorder()
#     request.session['cart']={}
#     return render(request, "order_confirmation.html")

def buy_now(request):
    p_id=request.POST['product']
    products=product.objects.get(id=p_id)
    print("buy now product = ",products)
    return render(request,"checkout.html")

def orders_page(request):
    customer=request.session.get('customer_id')
    orders=order.get_orders_by_customer(customer)
    # cancel_order=cancelOrder.objects.filter(order__in=orders)
    # print("cancle order = ",cancel_order)
    # print("orders=",orders)
    # orders=orders.reverse()
    return render(request,'orders.html',{'orders':orders})

def amc_detail_action(request,plan_id):
    plan_obj=amc_plans.objects.get(id=plan_id)
    customer=request.session['customer_id']
    customer_obj=signupAction.objects.get(id=customer)
    # print("customer is == ",customer_obj)
    return render(request,"amc_detail.html",{'plan_obj':plan_obj,'customer_obj':customer_obj})

def amc_purchase_action(request):
    plan_id=request.POST.get('plan_id')
    phone=request.POST.get('phone')
    address=request.POST.get('address')
    price=request.POST.get('price')
    amc_plan=amc_plans.objects.get(id=plan_id)
    customer=signupAction.objects.get(id=request.session['customer_id'])
    amc_obj=amc_orders.objects.create(phone=phone,address=address,amc_plan=amc_plan,customer=customer)
    amc_obj.save()
    return render(request,"payment.html",{'price':price,'amc_obj':amc_obj})