from django.views.generic import ListView, DetailView

from .models import Project

class ProjectList(ListView):
				model = Project
				template_name = "projects/project_list.html"
				context_object_name = 'projects'

class ProjectDetailView(DetailView):
				model = Project
				template_name = "projects/project_detail.html"
