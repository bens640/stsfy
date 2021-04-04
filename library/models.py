from datetime import datetime

from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from users.models import Group


class Item(models.Model):
    MEDIA_TYPES = [
        ("F", "Movie"),
        ("T", "TV"),
        ("M", "Music"),
    ]
    name = models.CharField(max_length=100)
    item_id = models.CharField(max_length=100)
    item_type = models.CharField(max_length=1, choices=MEDIA_TYPES)
    image_path = models.CharField(max_length=100, blank=True, null=True)
    owned_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.name


class UserItem(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    owned_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, null=True, blank=True)
    consumed = models.BooleanField(default=False)
    date_added = models.DateTimeField(default=datetime.now())

    def __str__(self):
        if self.owned_by is True:
            return f"{self.owned_by}'s {self.item.name}"
        elif self.group is True:
            return f"{self.group.name}'s {self.item.name}"
        else:
            return self.item.name

