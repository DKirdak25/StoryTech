from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

class Post(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    image = models.FileField(upload_to="blog_images/", blank=True, null=True)

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('blog_detail', args=[str(self.id)])

class PostBlock(models.Model):
    TYPE_CHOICES = [
        ('text', 'Text'),
        ('code', 'Code'),
    ]

    post = models.ForeignKey(Post, related_name='blocks', on_delete=models.CASCADE)
    type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    value = models.TextField()
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']