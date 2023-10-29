from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.views.generic import ListView, DeleteView, CreateView, View

from .models import Product, Category, Cart, CartedItem


class HomeView(ListView):
    model = Product
    template_name = 'shop/home.html'


class ProductListView(ListView):
    model = Product
    template_name = 'shop/products.html'
    context_object_name = 'products'

    def get_queryset(self):
        category_name = self.kwargs['category_name'].lower()
        category = Category.objects.get(name__iexact=category_name)
        return Product.objects.filter(category=category)


class ItemView(DeleteView):
    model = Product
    template_name = 'shop/item.html'
    context_object_name = 'item'


class AddToCartView(View):

    def get(self, request, item_id):
        item = get_object_or_404(Product, pk=item_id)
        cart, created = Cart.objects.get_or_create(user=request.user)

        carted_item, created = CartedItem.objects.get_or_create(cart=cart, product=item)

        if not created:
            carted_item.quantity += 1
            carted_item.save()
        else:
            carted_item.quantity = 1
            carted_item.save()

        cart.calculate_total()

        return redirect('shop:home')
