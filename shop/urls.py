from django.urls import path

from .views import HomeView, ProductListView, ItemView, AddToCartView, CartView, DeleteItemView, CartAddressView, SummaryView, PlaceOrderView

app_name = 'shop'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('products/<str:category_name>/', ProductListView.as_view(), name='product-list'),
    path('item/<int:pk>/', ItemView.as_view(), name='item'),
    path('add/<int:item_id>/', AddToCartView.as_view(), name='add-item'),
    path('cart/', CartView.as_view(), name='cart'),
    path('cart/remove/<int:pk>', DeleteItemView.as_view(), name='remove-item'),
    path('cart/address/', CartAddressView.as_view(), name='cart-address'),
    path('cart/address/<int:pk>/summary/', SummaryView.as_view(), name='summary'),
    path('cart/address/<int:pk>/order/', PlaceOrderView.as_view(), name='order')
]
