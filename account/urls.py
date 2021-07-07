from django.urls import path
from account import views

app_name = 'account'
urlpatterns = [
    path('register/', views.CreateAnAccountView.as_view(), name='register'),
    path('login/', views.CustomerLoginView.as_view(), name='login'),
    path('customer-profile/', views.CustomerProfileView.as_view(), name='customer_profile'),
    path('dashboard/', views.SellerProfileView.as_view(), name='dashboard'),
    path('become-seller/', views.BecomeSellerView.as_view(), name='becomeseller'),
]
