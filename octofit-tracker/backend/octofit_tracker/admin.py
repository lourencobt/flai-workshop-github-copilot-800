from django.contrib import admin
from .models import UserProfile, Team, Activity, Leaderboard, Workout


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'fitness_level', 'points', 'created_at', 'updated_at']
    list_filter = ['fitness_level', 'created_at']
    search_fields = ['user__username', 'user__email']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('User Information', {
            'fields': ('user', 'bio', 'fitness_level')
        }),
        ('Statistics', {
            'fields': ('points',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ['name', 'captain', 'total_points', 'member_count', 'created_at']
    list_filter = ['created_at']
    search_fields = ['name', 'description', 'captain__username']
    filter_horizontal = ['members']
    readonly_fields = ['created_at', 'updated_at']
    
    def member_count(self, obj):
        return obj.members.count()
    member_count.short_description = 'Members'
    
    fieldsets = (
        ('Team Information', {
            'fields': ('name', 'description', 'captain')
        }),
        ('Members', {
            'fields': ('members',)
        }),
        ('Statistics', {
            'fields': ('total_points',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    list_display = ['user', 'activity_type', 'duration', 'distance', 'points_earned', 'date', 'created_at']
    list_filter = ['activity_type', 'date', 'created_at']
    search_fields = ['user__username', 'activity_type', 'notes']
    readonly_fields = ['created_at']
    date_hierarchy = 'date'
    
    fieldsets = (
        ('User Information', {
            'fields': ('user',)
        }),
        ('Activity Details', {
            'fields': ('activity_type', 'duration', 'distance', 'calories', 'date')
        }),
        ('Points & Notes', {
            'fields': ('points_earned', 'notes')
        }),
        ('Timestamps', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )


@admin.register(Leaderboard)
class LeaderboardAdmin(admin.ModelAdmin):
    list_display = ['user', 'rank', 'total_points', 'total_activities', 'total_duration', 'period', 'updated_at']
    list_filter = ['period', 'updated_at']
    search_fields = ['user__username']
    readonly_fields = ['updated_at']
    ordering = ['period', 'rank']
    
    fieldsets = (
        ('User Information', {
            'fields': ('user', 'period')
        }),
        ('Statistics', {
            'fields': ('rank', 'total_points', 'total_activities', 'total_duration', 'total_distance')
        }),
        ('Timestamps', {
            'fields': ('updated_at',),
            'classes': ('collapse',)
        }),
    )


@admin.register(Workout)
class WorkoutAdmin(admin.ModelAdmin):
    list_display = ['title', 'difficulty', 'duration', 'activity_type', 'created_by', 'created_at']
    list_filter = ['difficulty', 'activity_type', 'created_at']
    search_fields = ['title', 'description', 'activity_type']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Workout Information', {
            'fields': ('title', 'description', 'difficulty', 'duration', 'activity_type')
        }),
        ('Details', {
            'fields': ('exercises', 'target_muscles', 'equipment_needed')
        }),
        ('Creator', {
            'fields': ('created_by',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
