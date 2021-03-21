from django.apps import AppConfig
from django.contrib.admin.apps import AdminConfig


class LibraryAdminConfig(AdminConfig):
    default_site = 'library.admin.LibraryAdminArea'

class LibraryConfig(AppConfig):
    name = 'library'
