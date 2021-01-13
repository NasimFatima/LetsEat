from django.db import models
from user.models import User
from menu.models import ItemSize


class Common(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)
    deleted_at = models.DateTimeField(auto_now=False, null=True, blank=True)
    disabled_at = models.DateTimeField(auto_now=False, null=True, blank=True)
    order_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,
                                 related_name='customer')

    class Meta:
        abstract = True


class Orders(Common):
    CASH_ON_DELIVERY = 1
    CARD = 2
    Other = 3

    PAYMENT_METHOD_CHOICES = [
        (CASH_ON_DELIVERY, 'CASH_ON_DELIVERY'),
        (CARD, 'CARD'),
        (Other, 'Other')
    ]

    order_number = models.IntegerField(default=0)
    total_bill = models.IntegerField()
    payment_method = models.IntegerField(
        choices=PAYMENT_METHOD_CHOICES, null=True)

    def save(self, *args, **kwargs):
        self.order_number = self.order_number + 1
        super().save(*args, **kwargs)


class OrderItems(models.Model):

    item_category = models.ForeignKey(ItemSize, on_delete=models.CASCADE, null=True, blank=True,
                                      related_name='product')
    price = models.IntegerField()
    quantity = models.IntegerField(default=1)
    order = models.ForeignKey(Orders, on_delete=models.CASCADE, null=True, blank=True,
                              related_name='order')
