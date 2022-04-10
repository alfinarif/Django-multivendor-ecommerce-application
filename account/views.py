from django.shortcuts import render, redirect
from django.urls import reverse

from account.forms import CreateAnAccountForm, ProfileInfoForm, BecomeSellerForm

from account.models import User, Profile
from order.models import Cart
from store.models import Category, Product

from django.views.generic import View, TemplateView

from django.contrib import messages

from django.contrib.auth import login, authenticate

# create qr code 
import qrcode
from io import BytesIO
from django.core.files import File
from PIL import Image, ImageDraw


# anyone can create account from this class view
class CreateAnAccountView(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('account:login')
        else:
            form = CreateAnAccountForm()
            context = {
                'form': form
            }
            return render(request, 'customer/register.html', context)

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('account:login')
        else:
            form = CreateAnAccountForm()
            if request.method == 'post' or request.method == 'POST':
                form = CreateAnAccountForm(request.POST)
                if form.is_valid():
                    form.save()
                    return redirect('account:login')
                else:
                    return redirect('account:register')
            else:
                messages.info(request, "Sorry for our server error! please try again!")
                return redirect('account:register')
    
# customers and seller login class
class CustomerLoginView(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user.user_type == 1:
                return redirect('account:customer_profile')
            if request.user.user_type == 2:
                return redirect('account:dashboard')
        else:
            return render(request, 'customer/login.html')

    def post(self, request, *args, **kwargs):
        if request.method == 'post' or request.method == 'POST':
            email = request.POST.get('email')
            password = request.POST.get('password')
            user = authenticate(email=email, password=password)
            if user is not None:
                login(request, user)
                if request.user.user_type == 1:
                    return redirect('account:customer_profile')
                if request.user.user_type == 2:
                    return redirect('account:dashboard')       
            else:
                messages.warning(request, "Please try again!")
                return redirect('account:login')


# normal customer profile class
class CustomerProfileView(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user.user_type == 1:
                return render(request, 'customer/customer-profile.html')

            if request.user.user_type == 2:
                return redirect('account:dashboard')
        else:
            return redirect('account:login')


# seller dashboard class
class SellerProfileView(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user.user_type == 1:
                return redirect('account:customer_profile')

            if request.user.user_type == 2:
                carts = Cart.objects.filter(item__user=request.user, purchased=True)
                total = 0
                for cart in carts:
                    if cart.variation_total():
                        total += float(cart.variation_total())
                    elif cart.variation_single_price():
                        total += float(cart.variation_single_price())
                    else:
                        total += float(cart.get_total())

                seller_qr = request.user.profile.qr_code
                
                context = {
                    'qr_code': seller_qr,
                    'total_sales_amount': total
                }
                return render(request, 'customer/index.html', context)
            else:
                return redirect('/')
        else:
            return redirect('account:login')


# become a seller view class 
class BecomeSellerView(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user.user_type == 1:
                form = BecomeSellerForm()
                context = {
                    'form': form
                }
                return render(request, 'customer/becomeseller.html', context)

            if request.user.user_type == 2:
                return redirect('account:dashboard')
        else:
            return redirect('account:login')
    
    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user.user_type == 2:
                return redirect('account:dashboard')
            if request.user.user_type == 1:
                form = BecomeSellerForm()
                if request.method == 'post' or request.method == 'POST':
                    form = BecomeSellerForm(request.POST, request.FILES)
                    if form.is_valid():
                        form.save() 
                        get_user_id = request.user.id
                        current_user = User.objects.get(id=get_user_id)
                        current_user.user_type = 2
                        current_user.save()
                        return redirect('account:dashboard')
                else:
                    return redirect('account:customer_profile')
        else:
            return redirect('account:login')




# if request.user.user_type == 1:
#     return redirect('account:customer_profile')
# if request.user.user_type == 2:
#     return redirect('account:dashboard')








