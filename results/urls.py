from django.urls import path
from . import views  # Import views from the current app

urlpatterns = [
    path('engineer_results/', views.engineer_results_view, name='engineer_results'),  # URL for the engineer results 
    # Add more URLs for other views here (e.g., team leader, department leader and senior manager)
    path('team_leader_results/', views.team_leader_results_view, name='team_leader_results'),
    path('department_leader_results/',views.department_leader_results_view, name='department_leader_results'),
    path('senior_manager_results/', views.senior_manager_results_view, name='senior_manager_results'),
]