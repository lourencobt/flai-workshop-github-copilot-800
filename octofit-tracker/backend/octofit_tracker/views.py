from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.db.models import Sum, Count
from .models import UserProfile, Team, Activity, Leaderboard, Workout
from .serializers import (
    UserSerializer, UserProfileSerializer, TeamSerializer,
    ActivitySerializer, LeaderboardSerializer, WorkoutSerializer
)


class UserViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing users
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=False, methods=['get'])
    def me(self, request):
        """Get current user information"""
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)


class UserProfileViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing user profiles
    """
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """Filter queryset based on user permissions"""
        if self.request.user.is_staff:
            return UserProfile.objects.all()
        return UserProfile.objects.filter(user=self.request.user)

    @action(detail=False, methods=['get'])
    def my_profile(self, request):
        """Get current user's profile"""
        profile, created = UserProfile.objects.get_or_create(user=request.user)
        serializer = self.get_serializer(profile)
        return Response(serializer.data)


class TeamViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing teams
    """
    queryset = Team.objects.all()
    serializer_class = TeamSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=True, methods=['post'])
    def join(self, request, pk=None):
        """Allow a user to join a team"""
        team = self.get_object()
        user = request.user
        
        if user in team.members.all():
            return Response(
                {'detail': 'You are already a member of this team'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        team.members.add(user)
        team.save()
        
        serializer = self.get_serializer(team)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def leave(self, request, pk=None):
        """Allow a user to leave a team"""
        team = self.get_object()
        user = request.user
        
        if user not in team.members.all():
            return Response(
                {'detail': 'You are not a member of this team'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        team.members.remove(user)
        team.save()
        
        return Response({'detail': 'Successfully left the team'})

    @action(detail=True, methods=['get'])
    def stats(self, request, pk=None):
        """Get team statistics"""
        team = self.get_object()
        
        # Calculate team statistics
        team_activities = Activity.objects.filter(user__in=team.members.all())
        stats = team_activities.aggregate(
            total_activities=Count('_id'),
            total_points=Sum('points_earned'),
            total_duration=Sum('duration'),
            total_distance=Sum('distance')
        )
        
        return Response(stats)


class ActivityViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing activities
    """
    queryset = Activity.objects.all()
    serializer_class = ActivitySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """Filter queryset based on user permissions"""
        if self.request.user.is_staff:
            return Activity.objects.all()
        return Activity.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        """Set the user when creating an activity"""
        serializer.save(user=self.request.user)

    @action(detail=False, methods=['get'])
    def my_activities(self, request):
        """Get current user's activities"""
        activities = Activity.objects.filter(user=request.user)
        serializer = self.get_serializer(activities, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def stats(self, request):
        """Get user's activity statistics"""
        activities = Activity.objects.filter(user=request.user)
        stats = activities.aggregate(
            total_activities=Count('_id'),
            total_points=Sum('points_earned'),
            total_duration=Sum('duration'),
            total_distance=Sum('distance')
        )
        return Response(stats)


class LeaderboardViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for viewing leaderboard (read-only)
    """
    queryset = Leaderboard.objects.all()
    serializer_class = LeaderboardSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """Filter leaderboard by period"""
        queryset = Leaderboard.objects.all()
        period = self.request.query_params.get('period', 'all_time')
        
        if period:
            queryset = queryset.filter(period=period)
        
        return queryset.order_by('rank')

    @action(detail=False, methods=['post'])
    def update_rankings(self, request):
        """Update leaderboard rankings (admin only)"""
        if not request.user.is_staff:
            return Response(
                {'detail': 'Permission denied'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Update leaderboard for all users
        users = User.objects.all()
        period = request.data.get('period', 'all_time')
        
        for user in users:
            activities = Activity.objects.filter(user=user)
            
            stats = activities.aggregate(
                total_activities=Count('_id'),
                total_points=Sum('points_earned'),
                total_duration=Sum('duration'),
                total_distance=Sum('distance')
            )
            
            Leaderboard.objects.update_or_create(
                user=user,
                period=period,
                defaults={
                    'total_points': stats['total_points'] or 0,
                    'total_activities': stats['total_activities'] or 0,
                    'total_duration': stats['total_duration'] or 0,
                    'total_distance': stats['total_distance'] or 0,
                }
            )
        
        # Update ranks
        leaderboard_entries = Leaderboard.objects.filter(period=period).order_by('-total_points')
        for index, entry in enumerate(leaderboard_entries, start=1):
            entry.rank = index
            entry.save()
        
        return Response({'detail': 'Leaderboard updated successfully'})


class WorkoutViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing workouts
    """
    queryset = Workout.objects.all()
    serializer_class = WorkoutSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        """Set the creator when creating a workout"""
        serializer.save(created_by=self.request.user)

    @action(detail=False, methods=['get'])
    def recommended(self, request):
        """Get recommended workouts based on user's fitness level"""
        try:
            profile = UserProfile.objects.get(user=request.user)
            fitness_level = profile.fitness_level
        except UserProfile.DoesNotExist:
            fitness_level = 'beginner'
        
        workouts = Workout.objects.filter(difficulty=fitness_level)
        serializer = self.get_serializer(workouts, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def by_difficulty(self, request):
        """Get workouts filtered by difficulty"""
        difficulty = request.query_params.get('difficulty', 'beginner')
        workouts = Workout.objects.filter(difficulty=difficulty)
        serializer = self.get_serializer(workouts, many=True)
        return Response(serializer.data)
