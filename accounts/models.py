from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

# Create your models here.


class CustomerModel(models.Model):
    user = models.OneToOneField(
        User, blank=True, null=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, null=True)
    email = models.EmailField(max_length=255, null=True)
    phone = models.CharField(max_length=200, null=True)
    profile_pic = models.ImageField(default='blank.png', null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    update = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return "{}. {}".format(self.id, self.name)

    def get_absolute_url(self):
        pk = {'pk': self.id}
        return reverse('account_setting', kwargs=pk)


class TagModel(models.Model):
    name = models.CharField(max_length=255, null=True)

    def __str__(self):
        return self.name


class ProductModel(models.Model):
    CATEGORY = (
        ('Indoor', 'Indoor'),
        ('Outdoor', 'Outdoor'),
        ('Both', 'Both'),
    )

    name = models.CharField(max_length=255, null=True)
    price = models.CharField(max_length=255, null=True)
    category = models.CharField(max_length=255, null=True, choices=CATEGORY)
    tag = models.ManyToManyField(TagModel)
    description = models.CharField(max_length=255, null=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return "{}. {}".format(self.id, self.name)


class OrderModel(models.Model):
    STATUS = (
        ('Pending', 'Pending'),
        ('Delivered', 'Delivered'),
        ('Out of Delivery', 'Out of Delivery'),
    )

    customer = models.ForeignKey(
        CustomerModel, null=True, on_delete=models.SET_NULL)
    product = models.ForeignKey(
        ProductModel, null=True, on_delete=models.SET_NULL)
    status = models.CharField(max_length=255, null=True, choices=STATUS)
    note = models.CharField(max_length=900, null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return "{}. {} by {}".format(self.id, self.product.name, self.customer.name)

    def get_absolute_url(self):
        pk = {'pk': self.customer.id}
        return reverse('customer', kwargs=pk)
