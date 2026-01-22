from rest_framework import serializers
from django.contrib.auth.models import User
from bson import ObjectId
from .models import UserProfile, Team, Activity, Leaderboard, Workout


class ObjectIdField(serializers.Field):
    """Custom field to serialize ObjectId to string"""
    def to_representation(self, value):
        return str(value)
    
    def to_internal_value(self, data):
        try:
            return ObjectId(data)
        except Exception:
            raise serializers.ValidationError('Invalid ObjectId')


class UserSerializer(serializers.ModelSerializer):
    team_name = serializers.SerializerMethodField()
    team_id = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'team_name', 'team_id', 'date_joined']
        read_only_fields = ['id', 'date_joined']
    
    def get_team_name(self, obj):
        team = obj.teams.first()
        return team.name if team else None
    
    def get_team_id(self, obj):
        team = obj.teams.first()
        return str(team._id) if team else None


class UserProfileSerializer(serializers.ModelSerializer):
    _id = ObjectIdField(read_only=True)
    user = UserSerializer(read_only=True)
    username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = UserProfile
        fields = ['_id', 'user', 'username', 'bio', 'fitness_level', 'points', 'created_at', 'updated_at']
        read_only_fields = ['_id', 'points', 'created_at', 'updated_at']


class TeamSerializer(serializers.ModelSerializer):
    _id = ObjectIdField(read_only=True)
    members = UserSerializer(many=True, read_only=True)
    captain = UserSerializer(read_only=True)
    member_count = serializers.SerializerMethodField()
    member_ids = serializers.ListField(
        child=serializers.IntegerField(),
        write_only=True,
        required=False
    )
    captain_id = serializers.IntegerField(write_only=True, required=False)

    class Meta:
        model = Team
        fields = ['_id', 'name', 'description', 'members', 'captain', 'member_count', 'total_points', 
                  'created_at', 'updated_at', 'member_ids', 'captain_id']
        read_only_fields = ['_id', 'member_count', 'total_points', 'created_at', 'updated_at']
    
    def get_member_count(self, obj):
        return obj.members.count()

    def create(self, validated_data):
        member_ids = validated_data.pop('member_ids', [])
        captain_id = validated_data.pop('captain_id', None)
        
        team = Team.objects.create(**validated_data)
        
        if member_ids:
            team.members.set(User.objects.filter(id__in=member_ids))
        
        if captain_id:
            team.captain = User.objects.get(id=captain_id)
            team.save()
        
        return team


class ActivitySerializer(serializers.ModelSerializer):
    _id = ObjectIdField(read_only=True)
    user = UserSerializer(read_only=True)
    username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = Activity
        fields = ['_id', 'user', 'username', 'activity_type', 'duration', 'distance', 
                  'calories', 'points_earned', 'notes', 'date', 'created_at']
        read_only_fields = ['_id', 'user', 'points_earned', 'created_at']

    def create(self, validated_data):
        # Calculate points based on duration and activity type
        duration = validated_data.get('duration', 0)
        activity_type = validated_data.get('activity_type', '')
        
        # Points calculation logic
        base_points = duration * 1  # 1 point per minute
        
        # Bonus points for different activity types
        activity_multipliers = {
            'running': 1.5,
            'cycling': 1.3,
            'swimming': 1.6,
            'strength_training': 1.4,
            'walking': 1.0,
            'yoga': 1.2,
            'other': 1.0,
        }
        
        multiplier = activity_multipliers.get(activity_type, 1.0)
        points = int(base_points * multiplier)
        validated_data['points_earned'] = points
        
        activity = Activity.objects.create(**validated_data)
        
        # Update user points
        user = validated_data.get('user')
        if user:
            profile = UserProfile.objects.get_or_create(user=user)[0]
            profile.points += points
            profile.save()
        
        return activity


class LeaderboardSerializer(serializers.ModelSerializer):
    _id = ObjectIdField(read_only=True)
    user = UserSerializer(read_only=True)
    username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = Leaderboard
        fields = ['_id', 'user', 'username', 'total_points', 'total_activities', 
                  'total_duration', 'total_distance', 'rank', 'period', 'updated_at']
        read_only_fields = ['_id', 'rank', 'updated_at']


class WorkoutSerializer(serializers.ModelSerializer):
    _id = ObjectIdField(read_only=True)
    created_by = UserSerializer(read_only=True)

    class Meta:
        model = Workout
        fields = ['_id', 'title', 'description', 'difficulty', 'duration', 
                  'activity_type', 'exercises', 'target_muscles', 'equipment_needed',
                  'created_by', 'created_at', 'updated_at']
        read_only_fields = ['_id', 'created_by', 'created_at', 'updated_at']
