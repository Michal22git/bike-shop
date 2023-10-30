from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.urls import reverse_lazy
from django.views.generic import ListView, DeleteView, CreateView, View, DetailView

from .models import Product, Category, Cart, CartedItem, Order
from users.models import Address


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


class ItemView(DetailView):
    model = Product
    template_name = 'shop/item.html'
    context_object_name = 'item'


class AddToCartView(LoginRequiredMixin, View):

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

        return redirect('shop:cart')


class CartView(LoginRequiredMixin, ListView):
    model = CartedItem
    template_name = 'shop/cart.html'
    context_object_name = 'carted_items'

    def get_queryset(self):
        user = self.request.user
        carted_items = CartedItem.objects.filter(cart__user=user)
        return carted_items

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        cart, created = Cart.objects.get_or_create(user=user)

        context['total_items'] = cart.total_items
        context['total_price'] = cart.total_price

        return context


class DeleteItemView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = CartedItem
    success_url = reverse_lazy('shop:cart')

    def test_func(self):
        item = self.get_object()
        if self.request.user == item.cart.user:
            return True
        return False


class CartAddressView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Address
    template_name = 'shop/order_address.html'
    context_object_name = 'addresses'

    def get_queryset(self):
        user = self.request.user
        return Address.objects.filter(user=user)

    def test_func(self):
        user = self.request.user
        return CartedItem.objects.filter(cart__user=user).exists()

    def handle_no_permission(self):
        return redirect('shop:cart')


class SummaryView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Cart
    template_name = 'shop/summary.html'
    context_object_name = 'cart'

    def get_object(self):
        user = self.request.user
        cart = Cart.objects.filter(user=user).first()
        if not cart:
            return redirect('shop:home')
        return cart

    def test_func(self):
        user = self.request.user
        address_id = self.kwargs['pk']
        return Address.objects.filter(id=address_id, user=user).exists()

    def handle_no_permission(self):
        return redirect('shop:cart')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart = self.object
        carted_items = CartedItem.objects.filter(cart=cart)
        address_id = self.kwargs['pk']
        address = get_object_or_404(Address, id=address_id)

        context['address'] = address
        context['carted_items'] = carted_items
        context['total_items'] = cart.total_items
        context['total_price'] = cart.total_price

        return context


class PlaceOrderView(LoginRequiredMixin, UserPassesTestMixin, View):

    def test_func(self):
        address_id = self.kwargs.get('pk')
        try:
            address = Address.objects.get(id=address_id, user=self.request.user)
        except Address.DoesNotExist:
            return False
        return True

    def get(self, request, *args, **kwargs):
        address_id = kwargs.get('pk')

        if address_id is None:
            return redirect('shop:cart')

        user = request.user
        cart = Cart.objects.filter(user=user).first()

        if cart is None:
            return redirect('shop:cart')

        address = get_object_or_404(Address, id=address_id)
        carted_items = CartedItem.objects.filter(cart=cart)
        total_items = cart.total_items
        total_price = cart.total_price

        order = Order(
            user=user,
            address=address,
            status='accepted',
            total_items=total_items,
            total_price=total_price
        )

        order.save()

        for carted_item in carted_items:
            for _ in range(carted_item.quantity):
                order.items.add(carted_item.product)

        carted_items.delete()

        cart.total_items = 0
        cart.total_price = 0
        cart.save()

        return redirect('users:profile')
