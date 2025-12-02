from django.contrib import admin
from .models import Post, PostBlock

class PostBlockInline(admin.TabularInline):
    model = PostBlock
    extra = 1
    fields = ('order', 'type', 'value')
    ordering = ('order',)
       
class PostAdmin(admin.ModelAdmin):
				list_display = (
				    "title",
				    "author",
				    "image",
				)

class PostBlockAdmin(admin.ModelAdmin):
    list_display = ('post', 'type', 'order')
    ordering = ('post', 'order')

admin.site.register(Post, PostAdmin)
admin.site.register(PostBlock, PostBlockAdmin)