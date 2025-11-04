"""
URL configuration for wpProject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from wpProject import views
from django.views.generic import RedirectView
from signup import views as sn
from django.conf import settings
from django.conf.urls.static import static
from middlewares.auth import auth_middleware

urlpatterns = [
    path('admin-panel/', admin.site.urls),
    path('logout/', RedirectView.as_view(url='/admin-panel/logout/')),
    path('admin/generate-report/', views.generate_pdf_report, name='generate_report'),
    path('',views.home,name="index"),
    path('aboutus/',views.aboutUs),
    path('header/',views.header,name='header'),
    path('cancle_confirm_page/',views.cancle_confirm_page,name='cancle_confirm_page'),
    path('confirm_msg_page/',views.confirm_msg_page,name='confirm_msg_page'),
    path('cancel_reason_page/<int:order_id>/',views.cancel_reason_page,name='cancel_reason_page'),
    path('profile_page/',views.profile_page,name='profile_page'),
    path('profile_edit_page/',views.profile_edit_page,name='profile_edit_page'),
    path('edit_action/',views.edit_action,name='edit_action'),
    path('footer/',views.footer,name='footer'),
    path('invoice_action/',views.invoice_action,name='invoice_action'),
    path('select_time_range_page/',views.select_time_range_page,name='select_time_range_page'),
    path('reportPage/',views.reportPage,name='reportPage'),
    path('generate_report/',views.generate_pdf_report,name='generate_report'),
    path('offer/',views.offer),
    path('amc/',auth_middleware(views.amc)),
    path('contact/',views.contact,name="contact/"),
    path('login/',views.login,name="login"),
    path('amc_detail_page/',views.amc_detail_page,name="amc_detail_page"),
    path('amc_detail_action/<int:plan_id>',views.amc_detail_action,name="amc_detail_action"),
    path('amc_purchase_action/',views.amc_purchase_action,name="amc_purchase_action"),
    path('searchbar/',views.search),
    path('registration/',views.registration),
    path('feedback_page/',auth_middleware(views.feedback_page),name="feedback_page"),
    path('feedback_action/',views.feedback_action,name='feedback_action'),
    path('registerUser/',sn.registerUser,name='registerUser'),
    path('loginUser/',sn.loginUser,name='loginUser'),
    path('logoutUser/',sn.logoutUser,name='logoutUser'),
    path('otpPage/',views.otpPage,name='otpPage'),
    path('resetotpPage/',views.resetotpPage,name='resetotpPage'),
    path('customer_reportPage/',views.customer_reportPage,name='customer_reportPage'),
    path('product_reportPage/',views.product_reportPage,name='product_reportPage'),
    path('inquiry_reportPage/',views.inquiry_reportPage,name='inquiry_reportPage'),
    path('feedback_reportPage/',views.feedback_reportPage,name='feedback_reportPage'),
    path('product_search/', views.product_search, name='product_search'),
    path('change_password/',views.change_password,name='change_password'),
    path('emailPage/',views.emailPage,name='emailPage'),
    path('paymentPage/',views.paymentPage,name='paymentPage'),
    path('payment_process/',views.payment_process,name='payment_process'),
    path('paymentsuccessfullPage/',views.paymentsuccessfullPage,name='paymentsuccessfullPage'),
    path('forgotpassPage/',views.forgotpassPage,name='forgotpassPage'),
    path('searchPage/',views.searchPage,name='searchPage'),
    path('forgotpassword_action/',sn.forgotpassword_action,name='forgotpassword_action'),
    path('change_password_action/',sn.change_password_action,name='change_password_action'),
    path('otpverify/',sn.optVerify,name='otpverify'),
    path('verify_resetotp/',sn.verify_resetotp,name='verify_resetotp'),
    path('forgot_password/',sn.forgot_password,name='forgot_password'),
    path('products/',views.products,name='products'),
    path('product_filter/',views.product_filter,name='product_filter'),
    path('productDetails/<int:p_id>',views.productDetails_page,name='productDetails'),
    path('remove_from_cart/<int:p_id>',views.remove_from_cart,name="remove_from_cart"),
    path('getCat/<int:cat_id>/',views.getCat,name='getCat'),
    path('checkout/',auth_middleware(views.checkout_page),name='checkout'),
    path('checkout_action/',views.checkout_action,name='checkout_action'),
    path('contactUs_action/',views.contactUs_action,name='contactUs_action'),
    path('checkout_buynow/',auth_middleware(views.checkout_buynow),name='checkout_buynow'),
    path('checkout_buynow_action/',views.checkout_buynow_action,name='checkout_buynow_action'),
    path('buy_now/',views.buy_now,name='buy_now'),
    path('invoice_page/',views.invoice_page,name='invoice_page'),
    path('orders_page/',auth_middleware(views.orders_page),name='orders_page'),
    path('cart/',auth_middleware(views.cart),name="cart")
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)