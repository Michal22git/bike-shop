from django.urls import path

from .views import HomeView, ProductListView, ItemView, AddToCartView

app_name = 'shop'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('products/<str:category_name>/', ProductListView.as_view(), name='product-list'),
    path('item/<int:pk>/', ItemView.as_view(), name='item'),
    path('add/<int:item_id>/', AddToCartView.as_view(), name='add-item'),
]
