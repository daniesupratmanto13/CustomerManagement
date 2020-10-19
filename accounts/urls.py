from django.urls import path
from .views import *


urlpatterns = [
    path("customer/<str:pk>/", CustomerView.as_view(), name='customer'),
    path("delete/<str:pk>", DeleteOrderView.as_view(), name='delete_order'),
    path("update/<str:pk>/", UpdateOrderView.as_view(), name='update_order'),
    path("account_setting/<str:pk>/",
         AccountSetting.as_view(), name='account_setting'),
    path("registration/", RegistrationView.as_view(), name='registration'),
    path("login/", LoginPageView.as_view(), name='login'),
    path("logout/", LogoutUser.as_view(), name='logout'),
    path("user_page", UserPageView.as_view(), name='user_page'),
    path("create/", CreateOrderView.as_view(), name='create_order'),
    path("product_list/", ProductListView.as_view(), name='product_list'),
    path("", DashboardView.as_view(), name='home'),
]
