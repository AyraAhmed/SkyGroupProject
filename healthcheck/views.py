from django.shortcuts import render
from .models import ViewSummary 
from accounts.models import UserProfile

# Create your views here.
def session_selection_view(request): 
    return render(request, 'healthcheck/session_selection.html')

def summary_view(request):
    user_profile = UserProfile.objects.get(user=request.user)

    summaries = ViewSummary.objects.filter(
        vote_log__user_profile=user_profile
    ).select_related('vote_log__health_card')

    role = user_profile.role
    return render(request, 'healthcheck/summary.html', {
        'role': role,
        'summaries': summaries
    })


