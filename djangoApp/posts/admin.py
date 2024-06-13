from django.contrib import admin

from .models import Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created_at', 'status')
    list_filter = ('status',)
    search_fields = ('title', 'content', 'author__username')
    actions = ['accept_posts', 'reject_posts']

    def accept_posts(self, request, queryset):
        queryset.update(status='ACCEPTED')

    accept_posts.short_description = 'Accept selected posts'

    def reject_posts(self, request, queryset):
        queryset.update(status='REJECTED')

    reject_posts.short_description = 'Reject selected posts'
