from django.db import models
from .common import Common


class MenuItems(Common):

    name = models.CharField(max_length=50)

    class Meta:
        db_table = "menu_items"

    def __str__(self):

        return "{}".format(self.name)
