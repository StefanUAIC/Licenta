from django.contrib import admin

from .models import Class, Membership


@admin.register(Class)
class ClassAdmin(admin.ModelAdmin):
    list_display = ('name', 'teacher', 'created_at', 'join_code')
    search_fields = ('name', 'teacher__username')


@admin.register(Membership)
class MembershipAdmin(admin.ModelAdmin):
    list_display = ('student', 'class_instance')
    search_fields = ('student__username', 'class_instance__name')
