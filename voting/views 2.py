from django.shortcuts import render

# Create your views here.
def voting_view(request): 
    return render(request, 'voting/voting.html')
