from django.urls import path
from . import views  # Import views from the current app
#from .views import EditOwnProfileView # Import the API view for editing profile 

urlpatterns = [
    # URLs for home page, login page, registration page, user profile page
    path('', views.home_view, name='home'),
     path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('profile/', views.profile_view, name='profile'),
    path('edit-profile/', views.edit_profile_view, name='edit-profile'),
    path('change-password/', views.changePassword_view, name='change-password'),
    path('logout/', views.custom_logout_view, name='logout'),
    
    # API endpoint for editing own profile 
    #path('edit-profile/', EditOwnProfileView.as_view(), name='edit-profile'),
]
