from django.db import models
from user.models import User
from menu.models import ItemSize


class Common(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)
    deleted_at = models.DateTimeField(auto_now=False, null=True, blank=True)
    disabled_at = models.DateTimeField(auto_now=False, null=True, blank=True)

    class Meta:
        abstract = True


class Orders(Common):
    CASH_ON_DELIVERY = 1
    CARD = 2
    Other = 3

    PAYMENT_METHOD_CHOICES_DICT = {
        1: 'Cash On Delivery',
        2: 'Card',
        3: 'None'
    }
    PAYMENT_METHOD_CHOICES = (
        (CASH_ON_DELIVERY, 'CASH_ON_DELIVERY'),
        (CARD, 'CARD'),
        (Other, 'Other')
    )

    PENDING = 1
    COMPLETE = 2

    STATUS_CHOICES_DICT = {
        1: 'Pending',
        2: 'Complete'
    }

    STATUS_CHOICES = (
        (PENDING, 'PENDING'),
        (COMPLETE, 'COMPLETE')
    )

    total_bill = models.IntegerField()
    payment_method = models.IntegerField(
        choices=PAYMENT_METHOD_CHOICES, null=True)
    status = models.IntegerField(choices=STATUS_CHOICES, default=PENDING)
    is_checkedout = models.BooleanField(default=False)
    customer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,
                                 related_name='customer')


class OrderItems(Common):

    item_category = models.ForeignKey(ItemSize, on_delete=models.CASCADE, null=True, blank=True,
                                      related_name='product')
    price = models.IntegerField()
    quantity = models.IntegerField(default=1)
    order = models.ForeignKey(Orders, on_delete=models.CASCADE, null=True, blank=True,
                              related_name='order')
