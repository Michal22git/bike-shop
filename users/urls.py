from django.contrib.auth import views as auth_views
from django.urls import path
from django.urls import reverse_lazy

from .views import UserRegisterView, UserProfileView, UserAddressesView, AddAddressView, UpdateAddressView, DeleteAddressView, OrdersView

app_name = 'users'

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name="users/login.html"), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page=reverse_lazy('shop:home')), name='logout'),
    path('register/', UserRegisterView.as_view(), name='register'),
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('profile/orders/', OrdersView.as_view(), name='orders'),
    path('profile/addresses/', UserAddressesView.as_view(), name='addresses'),
    path('profile/addresses/add', AddAddressView.as_view(), name='addresses-add'),
    path('profile/addresses/<int:pk>/', UpdateAddressView.as_view(), name='addresses-update'),
    path('profile/addresses/<int:pk>/delete', DeleteAddressView.as_view(), name='addresses-delete'),
]
