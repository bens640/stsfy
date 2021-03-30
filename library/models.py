from django.contrib.auth.models import User
from django.db import models

# Create your models here.

class Item(models.Model):

    name = models.CharField(max_length=100)


    def __str__(self):
        return self.name


'''     SCHEMA
Item
MEDIA_TYPES = [
    ("F", "Movie"),
    ("T", "TV"),
    ("M", "Music"),
]
-> item_Name charfield
-> media_type charfield
-> item_Type = models.Charfield(max_length = 1, choices = MEDIA_TYPES)
-> owned_by foreignkey to User
-> genres many to many field to Genre

UserItem
-> item foreignkey to Item
-> owned_by foreignkey to User
-> consumed boolean
-> date_added datefield

Genre
-> name charfield
-> media_type charfield
-> number int


TODO
Fix music detail
add tv filter
add music filter

show who added media in media card

create media
Add media to user
show users in detail page

create group
add user to group
show groups in detail page




'''