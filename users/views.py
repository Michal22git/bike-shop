from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView, UpdateView, DeleteView

from .forms import UserRegisterForm, AddressForm
from .models import Address


class UserRegisterView(CreateView):
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:login')
    form_class = UserRegisterForm


class UserProfileView(LoginRequiredMixin, DetailView):
    model = User
    template_name = 'users/profile.html'

    def get_object(self):
        return self.request.user


class UserAddressesView(LoginRequiredMixin, ListView):
    model = Address
    template_name = 'users/address.html'
    context_object_name = 'addresses'

    def get_object(self):
        Address.objects.filter(user=self.request.user)


class AddAddressView(LoginRequiredMixin, CreateView):
    template_name = 'users/address_form.html'
    success_url = reverse_lazy('users:addresses')
    form_class = AddressForm

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class UpdateAddressView(LoginRequiredMixin, UpdateView):
    model = Address
    form_class = AddressForm
    template_name = 'users/address_form.html'
    success_url = reverse_lazy('users:addresses')

    def test_func(self):
        address = self.get_object()
        if self.request.user == address.user:
            return True
        return False

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class DeleteAddressView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Address
    success_url = reverse_lazy('users:addresses')

    def test_func(self):
        address = self.get_object()
        if self.request.user == address.user:
            return True
        return False
