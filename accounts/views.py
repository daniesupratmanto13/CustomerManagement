from django.shortcuts import render
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    TemplateView,
    UpdateView,
)
# Create your views here.
from .models import (
    CustomerModel,
    ProductModel,
    OrderModel,
)
from .forms import *
from .decorators import *


@method_decorator(unauthenticated, name='dispatch')
class RegistrationView(SuccessMessageMixin, CreateView):
    form_class = CreateUserForm
    template_name = 'accounts/registration_form.html'
    success_url = reverse_lazy('login')
    success_message = "%(username)s was created"
    extra_context = {
        'title': 'Registration'
    }

    def get_context_data(self, **kwargs):
        kwargs = self.kwargs
        context = super().get_context_data(**kwargs)
        context.update(self.extra_context)
        return context


@method_decorator(unauthenticated, name='dispatch')
class LoginPageView(LoginView):
    template_name = 'accounts/login_form.html'
    success_url = reverse_lazy('home')
    extra_context = {
        'title': 'Login'
    }

    def get_context_data(self, **kwargs):
        kwargs = self.kwargs
        context = super().get_context_data(**kwargs)
        context.update(self.extra_context)
        return context


class LogoutUser(LoginRequiredMixin, LogoutView):

    template_name = 'accounts/logout.html'


@method_decorator(login_required(login_url='login'), name='dispatch')
@method_decorator(admin_only, name='dispatch')
class DashboardView(TemplateView):
    template_name = 'accounts/index.html'

    def get_context_data(self, **kwargs):
        kwargs = self.kwargs
        context = super().get_context_data(**kwargs)
        customers = CustomerModel.objects.all()
        orders = OrderModel.objects.all()
        total_order = orders.count()
        total_delivered = orders.filter(status="Delivered").count()
        total_pending = orders.filter(status="Pending").count()
        extra_context = {
            'customers': customers,
            'orders': orders,
            'total_order': total_order,
            'total_delivered': total_delivered,
            'total_pending': total_pending,
        }
        context.update(extra_context)

        return context


@method_decorator(login_required(login_url='login'), name='dispatch')
@method_decorator(allowed_group(allowed=['customer']), name='dispatch')
class UserPageView(TemplateView):
    template_name = 'accounts/user_page.html'

    def get_context_data(self, **kwargs):
        kwargs = self.kwargs
        context = super().get_context_data(**kwargs)
        orders = self.request.user.customermodel.ordermodel_set.all()
        total_orders = orders.count()
        total_delivered = orders.filter(status="Delivered").count()
        total_pending = orders.filter(status="Pending").count()
        extra_context = {
            'orders': orders,
            'total_orders': total_orders,
            'total_delivered': total_delivered,
            'total_pending': total_pending,
        }
        context.update(extra_context)
        return context


@method_decorator(login_required(login_url='login'), name='dispatch')
@method_decorator(allowed_group(allowed=['admin']), name='dispatch')
class CustomerView(DetailView):
    model = CustomerModel
    context_object_name = 'customer'
    template_name = 'accounts/customer.html'

    def get_context_data(self, **kwargs):
        kwargs = self.kwargs
        context = super().get_context_data(**kwargs)
        orders = context['customer'].ordermodel_set.all()
        total_order = orders.count()
        extra_context = {
            'orders': orders,
            'total_order': total_order,
        }
        context.update(extra_context)
        return context


@method_decorator(login_required(login_url='login'), name='dispatch')
@method_decorator(allowed_group(allowed=['admin']), name='dispatch')
class ProductListView(ListView):
    model = ProductModel
    context_object_name = 'product_list'
    template_name = 'accounts/product_list.html'
    ordering = ['name']

    def get_context_data(self, **kwargs):
        kwargs = self.kwargs
        context = super().get_context_data(**kwargs)
        return context


@method_decorator(login_required(login_url='login'), name='dispatch')
@method_decorator(allowed_group(allowed=['admin']), name='dispatch')
class CreateOrderView(CreateView):
    form_class = OrderForm
    template_name = 'accounts/order_form.html'
    extra_context = {
        'title': 'Create Order'
    }

    def get_context_data(self, **kwargs):
        kwargs = self.kwargs
        context = super().get_context_data(**kwargs)
        context.update(self.extra_context)
        return context


@method_decorator(login_required(login_url='login'), name='dispatch')
@method_decorator(allowed_group(allowed=['admin']), name='dispatch')
class UpdateOrderView(UpdateView):
    model = OrderModel
    template_name = 'accounts/order_form.html'
    fields = [
        'product',
        'status',
        'note',
    ]
    extra_context = {
        'title': 'Update Order'
    }

    def get_context_data(self, **kwargs):
        kwargs = self.kwargs
        context = super().get_context_data(**kwargs)
        extra_context = {
            'name': context['object'].customer.name,
        }
        context.update(self.extra_context)
        context.update(extra_context)
        return context


@method_decorator(login_required(login_url='login'), name='dispatch')
@method_decorator(allowed_group(allowed=['admin']), name='dispatch')
class DeleteOrderView(DeleteView):
    model = OrderModel
    template_name = 'accounts/order_delete_confirmation.html'
    success_url = reverse_lazy('home')
    context_object_name = 'order'

    def get_context_data(self, **kwargs):
        kwargs = self.kwargs
        context = super().get_context_data(**kwargs)
        extra_context = {
            'name': context['order'].product.name + " by " + context['order'].customer.name
        }
        context.update(extra_context)
        return context


@method_decorator(login_required(login_url='login'), name='dispatch')
@method_decorator(allowed_group(allowed=['customer']), name='dispatch')
class AccountSetting(UpdateView):
    form_class = CustomerForm
    model = CustomerModel
    template_name = 'accounts/account_setting.html'

    def get_context_data(self, **kwargs):
        kwargs = self.kwargs
        context = super().get_context_data(**kwargs)
        return context
