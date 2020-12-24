from django.db import models
from .menu_item import MenuItems
from .common import Common


class ItemsCategory(Common):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=300)
    menu_item = models.ForeignKey(MenuItems, on_delete=models.CASCADE, null=True, blank=True,
                                  related_name='item')

    class Meta:
        db_table = "item_category"
