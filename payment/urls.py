from django.urls import path
from payment import views

app_name = 'payment'
urlpatterns = [
    path('checkout/', views.CheckoutView.as_view(), name='checkout'),
]
