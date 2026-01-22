from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from datetime import datetime, timedelta
import random
from octofit_tracker.models import Team, Activity, Leaderboard, Workout, UserProfile


class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Starting database population...'))

        # Clear existing data
        self.stdout.write('Clearing existing data...')
        Activity.objects.all().delete()
        Leaderboard.objects.all().delete()
        Workout.objects.all().delete()
        Team.objects.all().delete()
        UserProfile.objects.all().delete()
        User.objects.all().delete()

        # Insert Teams
        self.stdout.write('Inserting teams...')
        team_marvel = Team.objects.create(
            name="Team Marvel",
            description="Earth's Mightiest Heroes"
        )
        
        team_dc = Team.objects.create(
            name="Team DC",
            description="The Justice League"
        )

        # Insert Users (Superheroes)
        self.stdout.write('Inserting users...')
        
        # Team Marvel users
        user1 = User.objects.create_user(
            username='ironman',
            email='tony.stark@marvel.com',
            password='test123',
            first_name='Tony',
            last_name='Stark'
        )
        UserProfile.objects.create(user=user1, fitness_level='advanced', points=1250)
        team_marvel.members.add(user1)
        team_marvel.captain = user1
        team_marvel.save()
        
        user2 = User.objects.create_user(
            username='captainamerica',
            email='steve.rogers@marvel.com',
            password='test123',
            first_name='Steve',
            last_name='Rogers'
        )
        UserProfile.objects.create(user=user2, fitness_level='advanced', points=1180)
        team_marvel.members.add(user2)
        
        user3 = User.objects.create_user(
            username='blackwidow',
            email='natasha.romanoff@marvel.com',
            password='test123',
            first_name='Natasha',
            last_name='Romanoff'
        )
        UserProfile.objects.create(user=user3, fitness_level='advanced', points=1150)
        team_marvel.members.add(user3)
        
        user4 = User.objects.create_user(
            username='thor',
            email='thor.odinson@marvel.com',
            password='test123',
            first_name='Thor',
            last_name='Odinson'
        )
        UserProfile.objects.create(user=user4, fitness_level='advanced', points=1320)
        team_marvel.members.add(user4)
        
        user5 = User.objects.create_user(
            username='hulk',
            email='bruce.banner@marvel.com',
            password='test123',
            first_name='Bruce',
            last_name='Banner'
        )
        UserProfile.objects.create(user=user5, fitness_level='intermediate', points=1100)
        team_marvel.members.add(user5)
        
        # Team DC users
        user6 = User.objects.create_user(
            username='superman',
            email='clark.kent@dc.com',
            password='test123',
            first_name='Clark',
            last_name='Kent'
        )
        UserProfile.objects.create(user=user6, fitness_level='advanced', points=1400)
        team_dc.members.add(user6)
        team_dc.captain = user6
        team_dc.save()
        
        user7 = User.objects.create_user(
            username='batman',
            email='bruce.wayne@dc.com',
            password='test123',
            first_name='Bruce',
            last_name='Wayne'
        )
        UserProfile.objects.create(user=user7, fitness_level='advanced', points=1350)
        team_dc.members.add(user7)
        
        user8 = User.objects.create_user(
            username='wonderwoman',
            email='diana.prince@dc.com',
            password='test123',
            first_name='Diana',
            last_name='Prince'
        )
        UserProfile.objects.create(user=user8, fitness_level='advanced', points=1280)
        team_dc.members.add(user8)
        
        user9 = User.objects.create_user(
            username='flash',
            email='barry.allen@dc.com',
            password='test123',
            first_name='Barry',
            last_name='Allen'
        )
        UserProfile.objects.create(user=user9, fitness_level='intermediate', points=1200)
        team_dc.members.add(user9)
        
        user10 = User.objects.create_user(
            username='aquaman',
            email='arthur.curry@dc.com',
            password='test123',
            first_name='Arthur',
            last_name='Curry'
        )
        UserProfile.objects.create(user=user10, fitness_level='intermediate', points=1050)
        team_dc.members.add(user10)
        
        users = [user1, user2, user3, user4, user5, user6, user7, user8, user9, user10]

        # Insert Activities
        self.stdout.write('Inserting activities...')
        activity_types = ['running', 'walking', 'cycling', 'swimming', 'strength_training', 'yoga']
        
        activities_count = 0
        for user in users:
            for i in range(random.randint(5, 15)):
                activity_date = datetime.now() - timedelta(days=random.randint(0, 30))
                activity_type = random.choice(activity_types)
                duration = random.randint(20, 120)
                distance = round(random.uniform(1, 20), 2) if activity_type in ['running', 'walking', 'cycling', 'swimming'] else None
                
                Activity.objects.create(
                    user=user,
                    activity_type=activity_type,
                    duration=duration,
                    distance=distance,
                    calories=random.randint(100, 800),
                    points_earned=random.randint(50, 200),
                    date=activity_date,
                    notes="Great workout session!"
                )
                activities_count += 1

        # Insert Workouts (Suggested workout plans)
        self.stdout.write('Inserting workouts...')
        workouts_data = [
            {
                "title": "Hero Strength Training",
                "description": "Build superhuman strength with this intensive workout. Includes bench press, squats, deadlifts, and pull-ups.",
                "difficulty": "advanced",
                "duration": 60,
                "activity_type": "strength_training"
            },
            {
                "title": "Speedster Cardio",
                "description": "Train like the fastest heroes alive. Sprint intervals, jump rope, burpees, and high knees.",
                "difficulty": "intermediate",
                "duration": 45,
                "activity_type": "running"
            },
            {
                "title": "Warrior Endurance",
                "description": "Build stamina for long battles. Long distance run, plank hold, mountain climbers.",
                "difficulty": "intermediate",
                "duration": 90,
                "activity_type": "running"
            },
            {
                "title": "Flexibility & Recovery",
                "description": "Maintain agility and prevent injuries. Yoga flow, dynamic stretching, foam rolling.",
                "difficulty": "beginner",
                "duration": 30,
                "activity_type": "yoga"
            },
            {
                "title": "Combat Training",
                "description": "Master hand-to-hand combat techniques. Shadow boxing, heavy bag work, speed bag, grappling drills.",
                "difficulty": "advanced",
                "duration": 60,
                "activity_type": "strength_training"
            }
        ]
        
        for workout_data in workouts_data:
            Workout.objects.create(**workout_data)

        # Calculate and insert Leaderboard entries
        self.stdout.write('Calculating leaderboard...')
        
        leaderboard_count = 0
        for user in users:
            user_activities = Activity.objects.filter(user=user)
            total_points = sum(a.points_earned for a in user_activities)
            total_activities = user_activities.count()
            total_duration = sum(a.duration for a in user_activities)
            total_distance = sum(a.distance for a in user_activities if a.distance)
            
            Leaderboard.objects.create(
                user=user,
                total_points=total_points,
                total_activities=total_activities,
                total_duration=total_duration,
                total_distance=total_distance,
                period='all_time'
            )
            leaderboard_count += 1
        
        # Update ranks
        leaderboard_entries = Leaderboard.objects.filter(period='all_time').order_by('-total_points')
        for rank, entry in enumerate(leaderboard_entries, start=1):
            entry.rank = rank
            entry.save()
        
        # Update team points
        team_marvel.total_points = sum(Activity.objects.filter(user__in=team_marvel.members.all()).values_list('points_earned', flat=True))
        team_marvel.save()
        
        team_dc.total_points = sum(Activity.objects.filter(user__in=team_dc.members.all()).values_list('points_earned', flat=True))
        team_dc.save()

        self.stdout.write(self.style.SUCCESS('\n=== Database Population Complete ==='))
        self.stdout.write(self.style.SUCCESS(f'Teams created: 2'))
        self.stdout.write(self.style.SUCCESS(f'Users created: {len(users)}'))
        self.stdout.write(self.style.SUCCESS(f'Activities created: {activities_count}'))
        self.stdout.write(self.style.SUCCESS(f'Workouts created: {len(workouts_data)}'))
        self.stdout.write(self.style.SUCCESS(f'Leaderboard entries created: {leaderboard_count}'))
        self.stdout.write(self.style.SUCCESS('\nDatabase successfully populated with superhero test data!'))
