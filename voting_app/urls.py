from django.urls import path
from . import views

urlpatterns = [
    path('api/healthcards/', views.HealthCardList.as_view(), name='healthcard-list'),
    path('api/vote/', views.VoteCreate.as_view(), name='vote-create'),
    path('api/results/', views.ResultsView.as_view(), name='results'),
    path('api/user/profile/', views.UserProfileView.as_view(), name='user-profile'),
]
