from django.urls import path

from .views import HomeView, ProductListView

app_name = 'shop'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('products/<str:category_name>/', ProductListView.as_view(), name='product-list'),
]
