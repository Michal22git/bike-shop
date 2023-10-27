from django.views.generic import ListView, DeleteView

from .models import Product, Category


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
