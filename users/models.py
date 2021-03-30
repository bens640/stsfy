from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from PIL import Image

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')

    def __str__(self):
        return f'{self.user.username}s Profile'


class Group(models.Model):
    name = models.CharField(max_length=128)
    members = models.ManyToManyField(User, through='Membership')
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')
    about = models.CharField(default="", max_length=200)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('library-home')


class Membership(models.Model):
    person = models.ForeignKey(User, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    date_joined = models.DateField()

