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

'''     SCHEMA
Item
MEDIA_TYPES = [
    ("F", "Movie"),
    ("T", "TV"),
    ("M", "Music"),
]
-> item_Name charfield
-> item_Type = models.Charfield(max_length = 1, choices = MEDIA_TYPES)
-> owned_by foreignkey to User
-> genres many to many field to Genre

UserItem
-> item foreignkey to Item
-> owned_by foreignkey to User null true
-> group foreignkey to Group null true
-> consumed boolean
-> date_added datefield

Genre
-> name charfield
-> media_type charfield
-> number int


TODO

show who added media in media card

create media
Add media to user
show users in detail page

create group
add user to group
show groups in detail page

'''