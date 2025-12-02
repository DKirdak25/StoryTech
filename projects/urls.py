from django.urls import path
from .views import ProjectList, ProjectDetailView

urlpatterns = [
    path("project/<int:pk>/", ProjectDetailView.as_view(), name="project_detail"),
    path("", ProjectList.as_view(), name="project_list"),
]
