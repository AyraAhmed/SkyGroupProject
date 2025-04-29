from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from rest_framework import generics, permissions
from .models import UserProfile
#from .serializers import UserProfileSerializer

# html pages for home, login, register and profile 
def home_view(request):
    return render(request, 'accounts/home.html')

def login_view(request): 
    return render(request, 'accounts/login.html')

def register_view(request):
    return render(request, 'accounts/register.html')

def change_password_view(request):
    return render(request, 'accounts/change-password.html')

# view and update user profile (only for logged in users)
@login_required
def profile_view(request):
    profile = request.user.userprofile # get the logged in user's profile 

    if request.method == 'POST':
        # update basic UserProfile fields 
        profile.role = request.POST.get('role', profile.role)
        profile.phone_number = request.POST.get('phone_number', profile.phone_number)
        profile.save()

        # update basic user fields 
        user = request.user
        user.first_name = request.POST.get('first_name', user.first_name)
        user.last_name = request.POST.get('last_name', user.last_name)
        user.email = request.POST.get('email', user.email)
        if request.POST.get('password'):
            user.set_password(request.POST['password']) # securely set new password
        user.save()

        return redirect('profile') # redirect after saving changes 

    return render(request, 'accounts/profile.html', {'profile': profile})

# log out the current user 
def custom_logout_view(request):
    logout(request)
    return redirect('home')

# # API view to retrieve and update the logged in user profile via DRF (Django REST framework)
# class EditOwnProfileView(generics.RetrieveUpdateAPIView):
#     serializer_class = UserProfileSerializer
#     permission_classes = [permissions.IsAuthenticated]

#     # limit access to own profile only 
#     def get_object(self):
#         return self.request.user.userprofile 

# View to edit profile
@login_required
def edit_profile_view(request):
    profile = request.user.userprofile  # Get the logged-in user's profile

    if request.method == 'POST':
        # Update profile details
        profile.role = request.POST.get('role', profile.role)
        profile.phone_number = request.POST.get('phone_number', profile.phone_number)
        profile.save()

        # Update user details like first name, last name, and email
        user = request.user
        user.first_name = request.POST.get('first_name', user.first_name)
        user.last_name = request.POST.get('last_name', user.last_name)
        user.email = request.POST.get('email', user.email)
        if request.POST.get('password'):
            user.set_password(request.POST['password'])  # Securely set the new password
        user.save()

        return redirect('profile')  # Redirect to the profile page after saving

    return render(request, 'accounts/editProfile.html', {'profile': profile})