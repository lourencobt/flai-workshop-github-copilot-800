from djongo import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    _id = models.ObjectIdField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(blank=True, null=True)
    fitness_level = models.CharField(max_length=50, default='beginner')
    points = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'user_profiles'

    def __str__(self):
        return f"{self.user.username}'s Profile"


class Team(models.Model):
    _id = models.ObjectIdField(primary_key=True)
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    members = models.ManyToManyField(User, related_name='teams')
    captain = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='captained_teams')
    total_points = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'teams'

    def __str__(self):
        return self.name


class Activity(models.Model):
    ACTIVITY_TYPES = [
        ('running', 'Running'),
        ('walking', 'Walking'),
        ('cycling', 'Cycling'),
        ('swimming', 'Swimming'),
        ('strength_training', 'Strength Training'),
        ('yoga', 'Yoga'),
        ('other', 'Other'),
    ]

    _id = models.ObjectIdField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='activities')
    activity_type = models.CharField(max_length=50, choices=ACTIVITY_TYPES)
    duration = models.IntegerField(help_text='Duration in minutes')
    distance = models.FloatField(null=True, blank=True, help_text='Distance in kilometers')
    calories = models.IntegerField(null=True, blank=True)
    points_earned = models.IntegerField(default=0)
    notes = models.TextField(blank=True, null=True)
    date = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'activities'
        ordering = ['-date']

    def __str__(self):
        return f"{self.user.username} - {self.activity_type} - {self.date}"


class Leaderboard(models.Model):
    _id = models.ObjectIdField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='leaderboard_entries')
    total_points = models.IntegerField(default=0)
    total_activities = models.IntegerField(default=0)
    total_duration = models.IntegerField(default=0, help_text='Total duration in minutes')
    total_distance = models.FloatField(default=0, help_text='Total distance in kilometers')
    rank = models.IntegerField(default=0)
    period = models.CharField(max_length=20, default='all_time')  # daily, weekly, monthly, all_time
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'leaderboard'
        ordering = ['rank']
        unique_together = ['user', 'period']

    def __str__(self):
        return f"{self.user.username} - Rank {self.rank} ({self.period})"


class Workout(models.Model):
    DIFFICULTY_LEVELS = [
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
    ]

    _id = models.ObjectIdField(primary_key=True)
    title = models.CharField(max_length=200)
    description = models.TextField()
    difficulty = models.CharField(max_length=20, choices=DIFFICULTY_LEVELS)
    duration = models.IntegerField(help_text='Duration in minutes')
    activity_type = models.CharField(max_length=50)
    exercises = models.JSONField(default=list)
    target_muscles = models.JSONField(default=list)
    equipment_needed = models.JSONField(default=list)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_workouts')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'workouts'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} ({self.difficulty})"
