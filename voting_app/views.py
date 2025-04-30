from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import HealthCard, Vote, UserProfile
from .serializers import HealthCardSerializer, VoteSerializer, UserProfileSerializer
from django.db.models import Count, Q

class HealthCardList(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        health_cards = HealthCard.objects.all()
        serializer = HealthCardSerializer(health_cards, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = HealthCardSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class VoteCreate(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        print(f"Request user: {request.user}, User ID: {request.user.id}, Authenticated: {request.user.is_authenticated}")
        if not request.user.is_authenticated:
            return Response({"error": "User not authenticated"}, status=status.HTTP_401_UNAUTHORIZED)
        data = request.data.copy()
        data['user'] = request.user.id
        print(f"Serializer data: {data}")
        serializer = VoteSerializer(data=data)
        if serializer.is_valid():
            try:
                vote = serializer.save()
                print(f"Vote saved: {vote}")
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except Exception as e:
                print(f"Exception during save: {str(e)}")
                return Response({"error": f"Failed to save vote: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)
        print(f"Serializer errors: {serializer.errors}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ResultsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        role = request.query_params.get('role')
        health_cards = HealthCard.objects.all()
        if role:
            if role not in ['engineer', 'team_leader', 'department_leader']:
                return Response({"error": "Invalid role"}, status=status.HTTP_400_BAD_REQUEST)
            user_ids = UserProfile.objects.filter(role=role).values_list('user_id', flat=True)
            health_cards = health_cards.annotate(
                red_count=Count('vote', filter=Q(vote__rating='red', vote__user_id__in=user_ids)),
                amber_count=Count('vote', filter=Q(vote__rating='amber', vote__user_id__in=user_ids)),
                green_count=Count('vote', filter=Q(vote__rating='green', vote__user_id__in=user_ids))
            )
        else:
            health_cards = health_cards.annotate(
                red_count=Count('vote', filter=Q(vote__rating='red')),
                amber_count=Count('vote', filter=Q(vote__rating='amber')),
                green_count=Count('vote', filter=Q(vote__rating='green'))
            )
        data = [
            {
                'name': card.name,
                'red_count': card.red_count,
                'amber_count': card.amber_count,
                'green_count': card.green_count
            } for card in health_cards
        ]
        return Response(data)

class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            profile = UserProfile.objects.get(user=request.user)
            serializer = UserProfileSerializer(profile)
            return Response(serializer.data)
        except UserProfile.DoesNotExist:
            return Response({"error": "User profile not found"}, status=status.HTTP_404_NOT_FOUND)
