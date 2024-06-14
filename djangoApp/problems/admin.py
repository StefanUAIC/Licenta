from django.contrib import admin

from .models import Problem, TestCase


@admin.register(Problem)
class ProblemAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_by', 'created_at', 'status')
    list_filter = ('status',)
    search_fields = ('title', 'description', 'created_by__username')
    actions = ['accept_problems', 'reject_problems']

    def accept_problems(self, request, queryset):
        for problem in queryset:
            problem.status = 'ACCEPTED'
            problem.save()
            message = f'Your problem "{problem.title}" has been accepted.'

    accept_problems.short_description = 'Accept selected problems'

    def reject_problems(self, request, queryset):
        for problem in queryset:
            problem.status = 'REJECTED'
            problem.save()
            message = f'Your problem "{problem.title}" has been rejected.'

    reject_problems.short_description = 'Reject selected problems'


admin.site.register(TestCase)
