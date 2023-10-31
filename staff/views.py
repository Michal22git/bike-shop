from django.contrib import messages
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.views import LoginView
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView, DetailView

from shop.models import Order
from .forms import OrderStatusForm


class HomeView(TemplateView):
    template_name = 'staff/home.html'


class CustomLoginView(LoginView):
    template_name = 'staff/login.html'
    next_page = reverse_lazy('staff:home')

    def form_valid(self, form):
        user = form.get_user()
        if user.is_staff:
            response = super().form_valid(form)
            messages.success(self.request, f"Welcome back {self.request.user.username}!")
            return response
        else:
            messages.error(self.request, "You do not have staff status to log in")
            return self.form_invalid(form)


class OrdersView(LoginView, UserPassesTestMixin, ListView):
    model = Order
    template_name = 'staff/orders.html'
    context_object_name = 'orders'

    def test_func(self):
        return self.request.user.is_staff

    def get_queryset(self):
        return Order.objects.all()


class OrderView(LoginView, UserPassesTestMixin, DetailView):
    model = Order
    template_name = 'staff/order.html'
    context_object_name = 'order'

    def test_func(self):
        return self.request.user.is_staff

    def get_queryset(self):
        pk = self.kwargs['pk']
        return Order.objects.filter(pk=pk)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = OrderStatusForm(instance=self.object)
        return context

    def post(self, request, *args, **kwargs):
        pk = self.kwargs['pk']
        order = get_object_or_404(Order, pk=pk)
        form = OrderStatusForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('staff:orders')
        else:
            return self.render_to_response(self.get_context_data(form=form))