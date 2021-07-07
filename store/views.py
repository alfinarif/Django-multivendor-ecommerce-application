from django.db import models
from django.shortcuts import render, redirect
from django.urls import resolve

from account.models import User
from store.forms import CategoryForm, ProductForm
from store.models import Product, Category
from order.models import Cart

from django.views.generic import View, ListView, DetailView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin


class AddNewProductView(LoginRequiredMixin, View):
    login_url = 'account:login'
    redirect_field_name = 'redirect_to'
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user.user_type == 1:
                return redirect('account:customer_profile')
            if request.user.user_type == 2:
                user_categories = request.user.user_base_category.all()
                form = ProductForm()
                context = {
                    'form': form,
                    'user_categories': user_categories
                }
                return render(request, 'customer/add_new_product.html', context)
        else:
            return redirect('account:login')

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user.user_type == 1:
                return redirect('account:customer_profile')
            if request.user.user_type == 2:
                form = ProductForm()
                if request.method == 'post' or request.method == 'POST':
                    form = ProductForm(request.POST, request.FILES)
                    user_category_id = request.POST.get('category')
                    user_category = Category.objects.get(id=user_category_id)
                    if form.is_valid():
                        product = form.save(commit=False)
                        product.user = request.user
                        product.category = user_category
                        product.save()
                        return redirect('account:dashboard')
                else:
                    return redirect('account:dashboard')
        else:
            return redirect('account:login')





class AddNewCategoryView(LoginRequiredMixin, View):
    login_url = 'account:login'
    redirect_field_name = 'redirect_to'
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user.user_type == 1:
                return redirect('account:customer_profile')
            if request.user.user_type == 2:
                user_categories = request.user.user_base_category.all()
                form = CategoryForm()
                
                context = {
                    'form': form,
                    'user_categories': user_categories
                }
                return render(request, 'customer/add_new_product _category.html', context)
        else:
            return redirect('account:login')

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user.user_type == 1:
                return redirect('account:customer_profile')
            if request.user.user_type == 2:
                form = CategoryForm()
                if request.method == 'post' or request.method == 'POST':
                    form = CategoryForm(request.POST, request.FILES)
                    user_category_id = request.POST.get('category')
                    if user_category_id != '':
                        user_category = Category.objects.get(id=user_category_id)
                        if form.is_valid():
                            category = form.save(commit=False)
                            category.user = request.user
                            category.parent = user_category
                            category.save()
                            return redirect('account:dashboard')
                    else:
                        if form.is_valid():
                            category = form.save(commit=False)
                            category.user = request.user
                            category.save()
                            return redirect('account:dashboard')
                else:
                    return redirect('store:add_new_category')
        else:
            return redirect('account:login')




class SellerDashboardProductView(LoginRequiredMixin, View):
    login_url = 'account:login'
    redirect_field_name = 'redirect_to'
    
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user.user_type == 1:
                return redirect('account:customer_profile')
            if request.user.user_type == 2:
                my_products = Product.objects.filter(user=request.user)
                context = {
                    'products': my_products
                }
                return render(request, 'customer/product_list.html', context)
        else:
            return redirect('account:login')



class SellerCategoryView(LoginRequiredMixin, View):
    login_url = 'account:login'
    redirect_field_name = 'redirect_to'
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            if request.user.user_type == 1:
                return redirect('account:customer_profile')
            if request.user.user_type == 2:
                my_category = Category.objects.filter(user=request.user)
                context = {
                    'categories': my_category
                }
                return render(request, 'customer/category_list.html', context)
        else:
            return redirect('account:login')




# if request.user.user_type == 1:
#     return redirect('account:customer_profile')
# if request.user.user_type == 2:
#     return redirect('account:dashboard')





class HomeProductView(ListView):
    model = Product
    template_name = 'store/index.html'
    context_object_name = 'products'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sellers'] = User.objects.filter(user_type=2).order_by('-id')
        return context




class ProductDetialsView(DetailView):
    model = Product
    template_name = 'store/product.html'
    context_object_name = 'product'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        get_cat_id = self.object.category_id
        get_category = Category.objects.get(id=get_cat_id)
        context['releted_products'] = Product.objects.filter(category=get_category)[::-2]
        return context



# seller product page view
class SellerProductView(TemplateView):
    def get(self, request, pk, *args, **kwargs):
        seller_products = Product.objects.filter(user=pk)
        context = {
            'seller_products': seller_products
        }
        return render(request, 'store/seller_product.html', context)

