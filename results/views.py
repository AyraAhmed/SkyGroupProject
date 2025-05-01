from django.shortcuts import render
from .models import DepartmentLeaderResult
import matplotlib
matplotlib.use('Agg') 
import matplotlib.pyplot as plt
import io
import urllib, base64


# Team Leader View
def team_leader_results_view(request):
    return render(request, 'results/team_leader_results.html')

# Engineer View
def engineer_results_view(request):
    return render(request, 'results/engineer_results.html')


def department_leader_results_view(request):
    context = {}

    if request.method == 'POST':
        team = request.POST.get('team')
        department = request.POST.get('department')
        healthcard = request.POST.get('healthcard')
        progress = request.POST.get('progress')

        if team and department and healthcard and progress:
            results = DepartmentLeaderResult.objects.filter(
                team=team,
                department=department,
                healthcard=healthcard,
                progress_month=int(progress)
            )

           
            data = {'Red': 0, 'Yellow': 0, 'Green': 0}
            for result in results:
                if result.traffic_signal in data:
                    data[result.traffic_signal] += result.count

           
            labels = list(data.keys())
            values = list(data.values())
            plt.figure(figsize=(6, 4))
            plt.bar(labels, values, color='orange')
            plt.title('Traffic Signal Distribution')
            plt.xlabel('Traffic Signal')
            plt.ylabel('Count')

            buf = io.BytesIO()
            plt.savefig(buf, format='png')
            buf.seek(0)
            string = base64.b64encode(buf.read()).decode()
            uri = f'data:image/png;base64,{string}'
            plt.close()

            context['chart'] = uri
            print("Generated chart URI:", uri[:100]) 

        context.update({
            'selected_team': team,
            'selected_department': department,
            'selected_healthcard': healthcard,
            'selected_progress': progress,
        })

    return render(request, 'results/department_leader_results.html', context)









def senior_manager_results_view(request):
    import plotly.graph_objs as go
    from plotly.offline import plot

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
