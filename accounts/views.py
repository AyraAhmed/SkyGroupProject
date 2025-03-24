from django.shortcuts import render

# Create your views here.
def home_view(request):
    return render(request,'accounts/home.html' )

def login_view(request): 
    return render(request, 'accounts/login.html')

def register_view(request):
    return render(request, 'accounts/register.html')

def profile_view(request):
    return render(request, 'accounts/profile.html')
