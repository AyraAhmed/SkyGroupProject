from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from rest_framework import generics, permissions
from .models import UserProfile
from .serializers import UserProfileSerializer

def home_view(request):
    return render(request, 'accounts/home.html')

def login_view(request): 
    return render(request, 'accounts/login.html')

def register_view(request):
    return render(request, 'accounts/register.html')

@login_required
def profile_view(request):
    profile = request.user.userprofile

    if request.method == 'POST':
        profile.role = request.POST.get('role', profile.role)
        profile.phone_number = request.POST.get('phone_number', profile.phone_number)
        profile.save()

        user = request.user
        user.first_name = request.POST.get('first_name', user.first_name)
        user.last_name = request.POST.get('last_name', user.last_name)
        user.email = request.POST.get('email', user.email)
        if request.POST.get('password'):
            user.set_password(request.POST['password'])
        user.save()

        return redirect('profile')

    return render(request, 'accounts/profile.html', {'profile': profile})

def custom_logout_view(request):
    logout(request)
    return redirect('home')

class EditOwnProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user.userprofile
