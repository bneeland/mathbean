from django.contrib import admin
from . import models

class DocumentAdmin(admin.ModelAdmin):
    list_display = ("name", "user", "created_at", )

admin.site.register(models.Document, DocumentAdmin)
