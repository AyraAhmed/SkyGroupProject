from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.db.models import Sum
from accounts.models import UserProfile
from healthcheck.models import ViewSummary, VoteLog, HealthCard
from datetime import timedelta, date

#html pages for department leader, engineer, senior manager and team leader
def department_leader_results_view(request): 
    return render(request, 'results/department_leader_results.html')

def engineer_results_view(request):
    return render(request, 'results/engineer_results.html')

def senior_manager_results_view(request):
    return render(request, 'results/senior_manager_results.html')

def team_leader_results_view(request):
    return render(request, 'results/team_leader_results.html')

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