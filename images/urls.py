from django.urls import path
from . import views

urlpatterns = [
    path('upload-image/', views.ImagePost.as_view())
]