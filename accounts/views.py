from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from rest_framework import generics, permissions
from .models import UserProfile
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.views.decorators.csrf import csrf_exempt

#from .serializers import UserProfileSerializer

# html pages for home, login, register and profile 
def home_view(request):
    return render(request, 'accounts/home.html')

# Login Page and Logic
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'accounts/login.html', {'error': 'Invalid username or password.'})

    return render(request, 'accounts/login.html')

@csrf_exempt
def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
        first_name = request.POST.get('first_name')
        role = request.POST.get('role')

        # Basic validation
        if not username or not password or not email or not first_name:
            return render(request, 'accounts/register.html', {
                'error': 'All fields are required.'
            })

        # Check if user already exists
        if User.objects.filter(username=username).exists():
            return render(request, 'accounts/register.html', {
                'error': 'Username already exists.'
            })

        # Create user
        user = User.objects.create_user(
            username=username,
            password=password,
            email=email,
            first_name=first_name
        )

        UserProfile.objects.create(
            user=user,
            email=email,
            first_name=first_name,
            role=role
        )

        # Log in the user
        login(request, user)

        return redirect('home')

    return render(request, 'accounts/register.html')
# Change Password Page
def changePassword_view(request):
    return render(request, 'accounts/changePassword.html')

# View and Update Profile
@login_required
def profile_view(request):
    profile = request.user.userprofile  # Get the logged-in user's profile

    if request.method == 'POST':
        # Update profile details
        profile.role = request.POST.get('role', profile.role)
        profile.phone_number = request.POST.get('phone_number', profile.phone_number)
        profile.save()

        # Update basic user details
        user = request.user
        user.first_name = request.POST.get('first_name', user.first_name)
        user.last_name = request.POST.get('last_name', user.last_name)
        user.email = request.POST.get('email', user.email)
        if request.POST.get('password'):
            user.set_password(request.POST['password'])  # securely update password
        user.save()

        return redirect('profile')

    return render(request, 'accounts/profile.html', {'profile': profile})

# Edit Profile Page (Separate view)
@login_required
def edit_profile_view(request):
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

    return render(request, 'accounts/editProfile.html', {'profile': profile})

# Logout View
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