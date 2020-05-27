from django.contrib import admin
from .models import Todo

#specifying created as read only file

class TodoAdmin(admin.ModelAdmin):
      readonly_fields=('created',)


admin.site.register(Todo,TodoAdmin)
