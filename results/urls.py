
from django.urls import path
from . import views  # Import your views here

urlpatterns = [

    # URL for the html results pages for engineer, team leader, department leader, senior manager
    path('engineer_results/', views.engineer_results_view, name='engineer_results'),   
    path('team_leader_results/', views.team_leader_results_view, name='team_leader_results'),
    path('department_leader_results/',views.department_leader_results_view, name='department_leader_results'),
    path('senior_manager_results/', views.senior_manager_results_view, name='senior_manager_results'),
    
    # API view to return JSON chart data 
    path('api/engineer_results/',views.engineer_results_data_view, name= 'engineer_results_data' ),
]

