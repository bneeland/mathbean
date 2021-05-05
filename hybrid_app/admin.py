from django.contrib import admin
from . import models

class DocumentAdmin(admin.ModelAdmin):
    list_display = ("name", "user", "created_at", "pk", )

class BlockAdmin(admin.ModelAdmin):
    list_display = ("document", "type", "created_at", "pk", )

admin.site.register(models.Document, DocumentAdmin)
admin.site.register(models.Block, BlockAdmin)
