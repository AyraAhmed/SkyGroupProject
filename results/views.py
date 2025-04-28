from django.shortcuts import render  # For showing your HTML page.

# Create your views here.
def team_leader_results_view(request):
    return render(request, 'results/team_leader_results.html')

def engineer_results_view(request):
    return render(request, 'results/engineer_results.html')

def department_leader_results_view(request):
    return render(request, 'results/department_leader_results.html')



import plotly.graph_objs as go
from plotly.offline import plot

def senior_manager_results_view(request):
    # Get values from GET request or set default
    team = request.GET.get('team', 'Team Alpha')
    department = request.GET.get('department', 'Department 1')
    progress = request.GET.get('progress', '3')

    # Dummy data (change as needed)
    labels = ['Red', 'Yellow', 'Green']
    values = [30, 10, 60]

    # Generate the Plotly bar chart
    bar_chart = go.Bar(x=labels, y=values, marker_color=['red', 'yellow', 'green'])
    layout = go.Layout(
        title=f'Traffic Signal Distribution for {team} - {department} ({progress} Months)',
        xaxis=dict(title='Traffic Signal'),
        yaxis=dict(title='Count')
    )
    fig = go.Figure(data=[bar_chart], layout=layout)
    graph_div = plot(fig, output_type='div', include_plotlyjs=True)

    # Pass values back to HTML for selection persistence
    return render(request, 'results/senior_manager_results.html', {
        'graph_div': graph_div,
        'team': team,
        'department': department,
        'progress': progress
    })
