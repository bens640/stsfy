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
-> media_id charfield
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



'''