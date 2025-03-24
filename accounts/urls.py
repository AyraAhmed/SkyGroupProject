from django.urls import path
from . import views  # Import views from the current app

urlpatterns = [
    path('', views.home_view, name='home'),
    path('login/', views.login_view, name='login'),  # URL for the login page
    # Add more URLs for other views here (e.g., register, profile)
    path('register/',views.register_view, name='register'),
    path('profile/', views.profile_view, name='profile'),
]
