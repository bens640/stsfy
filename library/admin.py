from django.contrib import admin
import django.apps
from library.models import Item

# admin.site.unregister(django.contrib.auth.models.Group)

# models = django.apps.apps.get_models()
#
# print(models)
#
# for model in models:
#
#     try:
#         admin.site.register(model)
#     except admin.sites.AlreadyRegistered:
#         pass


admin.site.register(Item)





# @admin.register(Item)
# class ItemAdmin(admin.ModelAdmin):
#     fields = []


# admin.site.register(Item, ItemAdmin)