from django.views.generic import ListView, DetailView

from .models import Post

class BlogPostList(ListView):
				model = Post
				template_name = "blog/blog_list.html"
				context_object_name = 'posts'

class BlogDetailView(DetailView):
				model = Post
				template_name = "blog/blog_detail.html"