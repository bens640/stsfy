from django.db import models

# Create your models here.


'''    SCHEMA

Profile
-> img charfield
-> 

Group
-> name charfield
-> description charfield
-> tags many to many field 

Membership
-> group foreignkey to Group null =true
-> user foreignkey to User null =true
-> item foreignkey to UserItem
ItemType
-> name charfield

Tag
-> name charfield


'''
