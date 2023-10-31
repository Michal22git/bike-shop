from django.contrib.auth import views as auth_views
from django.urls import path
from django.urls import reverse_lazy

from .views import HomeView, CustomLoginView, OrdersView, OrderView

app_name = 'staff'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page=reverse_lazy('staff:home')), name='logout'),
    path('orders/', OrdersView.as_view(), name='orders'),
    path('order/<int:pk>', OrderView.as_view(), name='order'),
]
