from django.urls import path
from .views import BlogPostList, BlogDetailView

urlpatterns = [
    path("post/<int:pk>/", BlogDetailView.as_view(), name="blog_detail"),
    path("", BlogPostList.as_view(), name="blog_list"),
]

   