from django.urls import path
from .views import HomeView,ContactView,ContactSuccessView

urlpatterns = [
     path('', HomeView.as_view(), name="home"),
     path('contact/', ContactView.as_view(), name="contact"),
    path("contact/success/", ContactSuccessView.as_view(), name="contact_success"),
   ]