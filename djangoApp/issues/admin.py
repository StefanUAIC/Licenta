from django.contrib import admin

from .models import Issue


@admin.register(Issue)
class IssueAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'description', 'created_at')
    search_fields = ('title', 'description', 'author__username')
    list_filter = ('created_at',)
    ordering = ('-created_at',)
