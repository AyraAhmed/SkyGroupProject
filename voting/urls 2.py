from django.urls import path
from . import views  # Import views from the current app

urlpatterns = [
    path('voting/', views.voting_view, name='voting'),  # URL for the engineer results
]