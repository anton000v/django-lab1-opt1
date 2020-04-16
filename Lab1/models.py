from django.db import models
from django.contrib.auth.models import User
from .choices import THE_STATUS_CHOICES, NOT_PAID
from phonenumber_field.modelfields import PhoneNumberField

class Product(models.Model):
    name = models.CharField(max_length=150, verbose_name="Название", unique=True)
    price = models.FloatField(verbose_name='Цена')
    product_image = models.ImageField(verbose_name='Фото', blank=True, null=True, editable=True)

    def __str__(self):
        return "{} - {}".format(self.name,self.price)


class BasketElement(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='be_user')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='BEProduct')
    amount = models.PositiveSmallIntegerField(verbose_name=u"Колличество")

    class Meta:
        unique_together = ('user', 'product')

    def __str__(self):
        return '{} - {} - {}'.format(self.user, self.product, self.amount)

class Basket(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='b_user')
    products = models.ManyToManyField(BasketElement, related_name="BProduct",null=True, blank=True)
    in_order = models.BooleanField(verbose_name='Заказ оформлен', default=False)
    def __str__(self):
        return 'Basket of {}'.format(self.user)

    def calculate_common_price(self):
        common_price = 0
        for basket_item in self.products.all():
            common_price += basket_item.product.price * basket_item.amount
        return common_price

class Order(models.Model):
    basket = models.ForeignKey(Basket, on_delete=models.CASCADE, related_name='o_basket', blank=True, unique=True)
    phone_number = PhoneNumberField()
    dont_call = models.BooleanField(verbose_name='Не перезванивать',default=False)
    status = models.CharField(max_length=2, choices=THE_STATUS_CHOICES,default=NOT_PAID)
    wishes = models.CharField(max_length=100, null=True, blank=True)
