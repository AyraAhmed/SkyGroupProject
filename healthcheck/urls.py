from django.urls import path
from . import views  # Import views from the current app

urlpatterns = [
    path('session_selection/', views.session_selection_view, name='session_selection'),  # URL for the selecting a session
    # Add more URLs for other views here (e.g., summary page)
    path('summary/',views.summary_view, name='summary'),
]