# AUTHOR OF THIS PAGE AYRA AHMED W1947450
from django.shortcuts import render
from .models import ViewSummary 
from accounts.models import UserProfile
from django.contrib.auth.decorators import login_required

# views for healthcheck app
# display session selection html and summary html
def session_selection_view(request): 
    return render(request, 'healthcheck/session_selection.html')

@login_required
def summary_view(request):
    # get the logged in user's profile
    user_profile = UserProfile.objects.get(user=request.user)

    # get summaries related to the user's votes 
    summaries = ViewSummary.objects.filter(
        vote_log__user_profile=user_profile
    ).select_related('vote_log__health_card') # optimise related object queries

    role = user_profile.role
    return render(request, 'healthcheck/summary.html', {
        'role': role,
        'summaries': summaries
    })


