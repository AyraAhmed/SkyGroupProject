from django.shortcuts import render

# Create your views here.
def session_selection_view(request): 
    return render(request, 'healthcheck/session_selection.html')

def summary_view(request):
    return render(request, 'healthcheck/summary.html')


