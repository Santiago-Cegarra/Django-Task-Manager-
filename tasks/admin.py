from django.contrib import admin
from .models import Task


class taskAdmin(admin.ModelAdmin):
    readonly_fields = ('created_date', )


admin.site.register(Task, taskAdmin)
# Register your models here.
