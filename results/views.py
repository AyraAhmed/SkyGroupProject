from django.shortcuts import render  # For showing your HTML page.
from django.shortcuts import render  # For showing your HTML page.
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.db.models import Sum
from accounts.models import UserProfile
from healthcheck.models import ViewSummary, VoteLog, HealthCard
from datetime import timedelta, date
from django.http import JsonResponse
from .models import Record
from django.views.decorators.csrf import csrf_exempt

#html pages for department leader, engineer, senior manager and team leader
def team_leader_results_view(request):
    return render(request, 'results/team_leader_results.html')

def engineer_results_view(request):
    return render(request, 'results/engineer_results.html')

def department_leader_results_view(request):
    return render(request, 'results/department_leader_results.html')
def senior_manager_results_view(request):
    return render(request, 'results/senior_manager_results.html')



@csrf_exempt
def get_record_data(request):
    team = request.GET.get('team')
    department = request.GET.get('department')
    progress = request.GET.get('progress')

    try:
        record = Record.objects.get(team=team, department=department, progress_month=progress)
        data = {
            'red': record.red_count,
            'yellow': record.yellow_count,
            'green': record.green_count,
        }
        return JsonResponse({'success': True, 'data': data})
    except Record.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'No record found for this combination.'})


# import plotly.graph_objs as go
# from plotly.offline import plot

# def senior_manager_results_view(request):
#     # Get values from GET request or set default
#     team = request.GET.get('team', 'Team Alpha')
#     department = request.GET.get('department', 'Department 1')
#     progress = request.GET.get('progress', '3')

#     # Dummy data (change as needed)
#     labels = ['Red', 'Yellow', 'Green']
#     values = [30, 10, 60]

#     # Generate the Plotly bar chart
#     bar_chart = go.Bar(x=labels, y=values, marker_color=['red', 'yellow', 'green'])
#     layout = go.Layout(
#         title=f'Traffic Signal Distribution for {team} - {department} ({progress} Months)',
#         xaxis=dict(title='Traffic Signal'),
#         yaxis=dict(title='Count')
#     )
#     fig = go.Figure(data=[bar_chart], layout=layout)
#     graph_div = plot(fig, output_type='div', include_plotlyjs=True)

#     # Pass values back to HTML for selection persistence
#     return render(request, 'results/senior_manager_results.html', {
#         'graph_div': graph_div,
#         'team': team,
#         'department': department,
#         'progress': progress
#     })

# using api GET method to test 
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def engineer_results_data_view(request):
    user_profile = request.user.userprofile

# individual or team results 
    view_type = request.GET.get('view_type')
    healthcard_name = request.GET.get('healthcard')
    timeframe = request.GET.get('quarter')

# checking if all filters are provided 
    if not view_type or not healthcard_name or not timeframe:
        return Response({
            "error": "Missing filters. Please select view type, healthcard, and time frame"
        }, status=400)
    
# clean and convert the timeframe into a real date 
    timeframe_clean = timeframe.replace("Progress after ", "").strip().lower()

    if timeframe_clean == "3 months":
        cutoff_date = date.today() - timedelta(days=90)
    elif timeframe_clean == "6 months": 
        cutoff_date = date.today() - timedelta(days=180)
    elif timeframe_clean == "9 months":
        cutoff_date = date.today() - timedelta(days=270)
    else:
        return Response({"error": "Invalid timeframe selected."}, status=400)

# Getting the selected HealthCard 
    try:
        healthcard = HealthCard.objects.get(name=healthcard_name)
    except HealthCard.DoesNotExist:
        return Response({"error": "Invalid healthcard selected."}, status=400)
    
# Filter ViewSummary records based on healthcard + timeframe 
    view_summaries = ViewSummary.objects.filter(
        vote_log__health_card = healthcard,
        view_date__gte=cutoff_date
    )
# filter by view type: individual or team 
    if view_type == 'individual':
        view_summaries = view_summaries.filter(vote_log__user_profile=user_profile)
    elif view_type == 'team':
        view_summaries = view_summaries.filter(vote_log__user_profile__team=user_profile.team)
    else:
        return Response({"error": "Invalid view type."}, status=400)
    
# Sum progress grouped by vote status
    progress_data = view_summaries.values('vote_log__status').annotate(total_progress=Sum('progress'))

# formatting the data foe JSON response 
    formatted = []
    for entry in progress_data:
        formatted.append({
            "status": entry['vote_log__status'],
            "progress": entry['total_progress']
        })

# return the full data for chart 
    return Response({
        "user": request.user.username,
        "team": user_profile.team.name if user_profile.team else None,
        "view_type": view_type,
        "healthcard": healthcard_name,
        "quarter": timeframe_clean, 
        "data": formatted
    })

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def team_leader_results_data_view(request):
    """
    API endpoint to fetch team leader results data based on filters.
    """
    user_profile = request.user.userprofile

    # Get filters from the request
    team_name = request.GET.get('team')
    healthcard_name = request.GET.get('healthcard')
    timeframe = request.GET.get('quarter')

    # Validate filters
    if not team_name or not healthcard_name or not timeframe:
        return Response({
            "error": "Missing filters. Please select team, healthcard, and time frame."
        }, status=400)

    # Convert timeframe into a date range
    timeframe_clean = timeframe.replace("Progress over ", "").strip().lower()
    if timeframe_clean == "3 months":
        cutoff_date = date.today() - timedelta(days=90)
    elif timeframe_clean == "6 months":
        cutoff_date = date.today() - timedelta(days=180)
    elif timeframe_clean == "9 months":
        cutoff_date = date.today() - timedelta(days=270)
    else:
        return Response({"error": "Invalid timeframe selected."}, status=400)

    # Get the selected HealthCard
    try:
        healthcard = HealthCard.objects.get(name=healthcard_name)
    except HealthCard.DoesNotExist:
        return Response({"error": "Invalid healthcard selected."}, status=400)

    # Filter ViewSummary records based on healthcard, timeframe, and team
    view_summaries = ViewSummary.objects.filter(
        vote_log__health_card=healthcard,
        view_date__gte=cutoff_date,
        vote_log__user_profile__team__name=team_name
    )

    # Sum progress grouped by vote status
    progress_data = view_summaries.values('vote_log__status').annotate(total_progress=Sum('progress'))

    # Format the data for JSON response
    formatted = []
    for entry in progress_data:
        formatted.append({
            "status": entry['vote_log__status'],
            "progress": entry['total_progress']
        })

    # Return the full data for the chart
    return Response({
        "team": team_name,
        "healthcard": healthcard_name,
        "quarter": timeframe_clean,
        "data": formatted
    })

