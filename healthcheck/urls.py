# AUTHOR OF THIS PAGE AYRA AHMED W1947450
from django.urls import path
from . import views  # Import views from the current app

urlpatterns = [
    # URLs for selecting a session and summary 
    path('session_selection/', views.session_selection_view, name='session_selection'), 
    path('summary/',views.summary_view, name='summary'),
]