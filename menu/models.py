from django.db import models
from user.models import User


class Common(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)
    deleted_at = models.DateTimeField(auto_now=False, null=True, blank=True)
    disabled_at = models.DateTimeField(auto_now=False, null=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,
                                   related_name='user')

    class Meta:
        abstract = True


class MenuItems(Common):

    name = models.CharField(max_length=50)

    class Meta:
        db_table = "menu_items"

    def __str__(self):

        return "{}".format(self.name)


class ItemsCategory(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=300)
    menu_item = models.ForeignKey(MenuItems, on_delete=models.CASCADE, null=True, blank=True,
                                  related_name='item')

    class Meta:
        db_table = "item_category"


class ItemSize(models.Model):
    item_category = models.ForeignKey(ItemsCategory, on_delete=models.CASCADE, null=True, blank=True,
                                      related_name='item_category')
    price = models.IntegerField(null=True)
    size = models.CharField(null=False, max_length=100)

    class Meta:
        db_table = "item_size"
