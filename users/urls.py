from django.urls import path
from . import views

urlpatterns = [
    path('register-user/', views.UserRegistration.as_view()),
    path('delete-user/<int:pk>/', views.UserDeletion.as_view()),
    path('login-user/', views.UserLogin.as_view()),
    path('login-user/<int:pk>/', views.UserLoginByID.as_view()),

    path('authorization/', views.CheckAuthenticated.as_view()),
    path('csrf_cookie', views.GetCSRFToken.as_view())
]