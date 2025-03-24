from django.shortcuts import render

# Create your views here.
def department_leader_results_view(request): 
    return render(request, 'results/department_leader_results.html')

def engineer_results_view(request):
    return render(request, 'results/engineer_results.html')

def senior_manager_results_view(request):
    return render(request, 'results/senior_manager_results.html')

def team_leader_results_view(request):
    return render(request, 'results/team_leader_results.html')
