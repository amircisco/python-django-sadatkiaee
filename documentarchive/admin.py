from django.contrib import admin
from .models import DocumentArchive,DocType


class DocumentArchiveAdmin(admin.ModelAdmin):
    fields = [
        'user',
        'file',
        'doctype',
    ]
    list_display = [
        'user',
        'doctype',
    ]


class DocTypeAdmin(admin.ModelAdmin):
    fields = [
        'name',
    ]
    list_display = [
        'name',
    ]


admin.site.register(DocumentArchive,DocumentArchiveAdmin)
admin.site.register(DocType,DocTypeAdmin)