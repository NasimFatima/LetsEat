from django.db import models
from .item_categories import ItemsCategory
from .common import Common


class ItemSize(models.Model):
    item_category = models.ForeignKey(ItemsCategory, on_delete=models.CASCADE, null=True, blank=True,
                                      related_name='item_category')
    price = models.IntegerField(null=True)
    size = models.CharField(null=False, max_length=100)

    class Meta:
        db_table = "item_size"
