import account
from django.urls import path
from store import views

app_name = 'store'
urlpatterns = [
    path('', views.HomeProductView.as_view(), name='index'),
    path('product/<int:pk>/', views.ProductDetialsView.as_view(), name='product_detail'),
    path('account/seller/add-new-product/', views.AddNewProductView.as_view(), name='add_new_product'),
    path('account/seller/add-new-category/', views.AddNewCategoryView.as_view(), name='add_new_category'),
    path('account/seller/product-list/', views.SellerDashboardProductView.as_view(), name='product_list'),
    path('account/seller/category-list/', views.SellerCategoryView.as_view(), name='category_list'),
    path('product/seller/<int:pk>/', views.SellerProductView.as_view(), name='seller_product'),
    #export seller product route
    path('account/seller/products/export/', views.export_seller_products, name='export_seller_product'),
]
