from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from datetime import datetime
from .models import UserProfile, Team, Activity, Leaderboard, Workout


class UserProfileModelTest(TestCase):
    """Test cases for UserProfile model"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
    
    def test_user_profile_creation(self):
        """Test creating a user profile"""
        profile = UserProfile.objects.create(
            user=self.user,
            bio='Test bio',
            fitness_level='beginner',
            points=100
        )
        self.assertEqual(profile.user.username, 'testuser')
        self.assertEqual(profile.fitness_level, 'beginner')
        self.assertEqual(profile.points, 100)
    
    def test_user_profile_string_representation(self):
        """Test string representation of user profile"""
        profile = UserProfile.objects.create(user=self.user)
        self.assertEqual(str(profile), "testuser's Profile")


class TeamModelTest(TestCase):
    """Test cases for Team model"""
    
    def setUp(self):
        self.user1 = User.objects.create_user(username='user1', password='pass123')
        self.user2 = User.objects.create_user(username='user2', password='pass123')
    
    def test_team_creation(self):
        """Test creating a team"""
        team = Team.objects.create(
            name='Test Team',
            description='A test team',
            captain=self.user1,
            total_points=0
        )
        team.members.add(self.user1, self.user2)
        
        self.assertEqual(team.name, 'Test Team')
        self.assertEqual(team.members.count(), 2)
        self.assertEqual(team.captain, self.user1)
    
    def test_team_string_representation(self):
        """Test string representation of team"""
        team = Team.objects.create(name='Test Team')
        self.assertEqual(str(team), 'Test Team')


class ActivityModelTest(TestCase):
    """Test cases for Activity model"""
    
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='pass123')
    
    def test_activity_creation(self):
        """Test creating an activity"""
        activity = Activity.objects.create(
            user=self.user,
            activity_type='running',
            duration=30,
            distance=5.0,
            calories=300,
            points_earned=45,
            date=datetime.now()
        )
        
        self.assertEqual(activity.user, self.user)
        self.assertEqual(activity.activity_type, 'running')
        self.assertEqual(activity.duration, 30)
        self.assertEqual(activity.distance, 5.0)


class UserProfileAPITest(APITestCase):
    """Test cases for UserProfile API endpoints"""
    
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.client.force_authenticate(user=self.user)
    
    def test_get_my_profile(self):
        """Test getting current user's profile"""
        response = self.client.get('/api/profiles/my_profile/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TeamAPITest(APITestCase):
    """Test cases for Team API endpoints"""
    
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.client.force_authenticate(user=self.user)
    
    def test_create_team(self):
        """Test creating a team"""
        data = {
            'name': 'Test Team',
            'description': 'A test team'
        }
        response = self.client.post('/api/teams/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Team.objects.count(), 1)
        self.assertEqual(Team.objects.get().name, 'Test Team')
    
    def test_list_teams(self):
        """Test listing teams"""
        Team.objects.create(name='Team 1')
        Team.objects.create(name='Team 2')
        
        response = self.client.get('/api/teams/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)


class ActivityAPITest(APITestCase):
    """Test cases for Activity API endpoints"""
    
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.client.force_authenticate(user=self.user)
        UserProfile.objects.create(user=self.user)
    
    def test_create_activity(self):
        """Test creating an activity"""
        data = {
            'activity_type': 'running',
            'duration': 30,
            'distance': 5.0,
            'calories': 300,
            'date': datetime.now().isoformat()
        }
        response = self.client.post('/api/activities/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Activity.objects.count(), 1)
        
        # Check that points were calculated and added
        activity = Activity.objects.first()
        self.assertGreater(activity.points_earned, 0)
    
    def test_list_my_activities(self):
        """Test listing current user's activities"""
        Activity.objects.create(
            user=self.user,
            activity_type='running',
            duration=30,
            date=datetime.now()
        )
        
        response = self.client.get('/api/activities/my_activities/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class WorkoutAPITest(APITestCase):
    """Test cases for Workout API endpoints"""
    
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.client.force_authenticate(user=self.user)
    
    def test_create_workout(self):
        """Test creating a workout"""
        data = {
            'title': 'Morning Run',
            'description': 'A quick morning run',
            'difficulty': 'beginner',
            'duration': 30,
            'activity_type': 'running',
            'exercises': ['warm up', 'run', 'cool down'],
            'target_muscles': ['legs', 'cardio'],
            'equipment_needed': ['running shoes']
        }
        response = self.client.post('/api/workouts/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Workout.objects.count(), 1)
    
    def test_get_recommended_workouts(self):
        """Test getting recommended workouts"""
        UserProfile.objects.create(user=self.user, fitness_level='beginner')
        
        Workout.objects.create(
            title='Beginner Workout',
            description='Easy workout',
            difficulty='beginner',
            duration=20,
            activity_type='walking',
            created_by=self.user
        )
        
        response = self.client.get('/api/workouts/recommended/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(len(response.data), 0)
