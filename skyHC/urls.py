"""
URL configuration for skyHealthCheck project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include  # Use include to link to app URLs
from accounts.views import custom_logout_view 
from results import views
#from results.views import get_record_data  # import it manually
#from results.views import senior_manager_results_view  # import it manually

urlpatterns = [
    path('admin/', admin.site.urls),            # Admin page
    path('', include('accounts.urls')),  # Include the accounts app URLs here
    path('healthcheck/', include('healthcheck.urls')),
    path('results/', include('results.urls')),
    path('voting/', include('voting.urls')), 
    path('logout/', custom_logout_view, name='logout'),
    path('api/accounts/', include('accounts.urls')),
    path('results/', include('results.urls')),  # include results app urls
    path('senior_manager_results/', views.senior_manager_results_view, name='senior_manager_results'),

]

