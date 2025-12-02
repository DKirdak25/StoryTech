from django.contrib import admin
from .models import Project, ProjectBlock


class ProjectBlockInline(admin.TabularInline):
    model = ProjectBlock
    extra = 1
    fields = ('order', 'type', 'value')
    ordering = ('order',)


class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'image', 'discription')
    inlines = [ProjectBlockInline]


class ProjectBlockAdmin(admin.ModelAdmin):
    list_display = ('project', 'type', 'order')
    ordering = ('project', 'order')


admin.site.register(Project, ProjectAdmin)
admin.site.register(ProjectBlock, ProjectBlockAdmin)