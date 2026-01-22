from django.core.management.base import BaseCommand
from pymongo import MongoClient
from datetime import datetime, timedelta
import random


class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data'

    def handle(self, *args, **options):
        # Connect to MongoDB
        client = MongoClient('localhost', 27017)
        db = client['octofit_db']

        self.stdout.write(self.style.SUCCESS('Starting database population...'))

        # Clear existing data
        self.stdout.write('Clearing existing data...')
        db.users.delete_many({})
        db.teams.delete_many({})
        db.activities.delete_many({})
        db.leaderboard.delete_many({})
        db.workouts.delete_many({})

        # Create unique index on email field
        self.stdout.write('Creating unique index on email field...')
        db.users.create_index([("email", 1)], unique=True)

        # Insert Teams
        self.stdout.write('Inserting teams...')
        teams = [
            {
                "_id": 1,
                "name": "Team Marvel",
                "description": "Earth's Mightiest Heroes",
                "created_at": datetime.now()
            },
            {
                "_id": 2,
                "name": "Team DC",
                "description": "The Justice League",
                "created_at": datetime.now()
            }
        ]
        db.teams.insert_many(teams)

        # Insert Users (Superheroes)
        self.stdout.write('Inserting users...')
        users = [
            # Team Marvel
            {
                "_id": 1,
                "username": "ironman",
                "email": "tony.stark@marvel.com",
                "password": "pbkdf2_sha256$260000$test",
                "first_name": "Tony",
                "last_name": "Stark",
                "team_id": 1,
                "total_points": 1250,
                "created_at": datetime.now()
            },
            {
                "_id": 2,
                "username": "captainamerica",
                "email": "steve.rogers@marvel.com",
                "password": "pbkdf2_sha256$260000$test",
                "first_name": "Steve",
                "last_name": "Rogers",
                "team_id": 1,
                "total_points": 1180,
                "created_at": datetime.now()
            },
            {
                "_id": 3,
                "username": "blackwidow",
                "email": "natasha.romanoff@marvel.com",
                "password": "pbkdf2_sha256$260000$test",
                "first_name": "Natasha",
                "last_name": "Romanoff",
                "team_id": 1,
                "total_points": 1150,
                "created_at": datetime.now()
            },
            {
                "_id": 4,
                "username": "thor",
                "email": "thor.odinson@marvel.com",
                "password": "pbkdf2_sha256$260000$test",
                "first_name": "Thor",
                "last_name": "Odinson",
                "team_id": 1,
                "total_points": 1320,
                "created_at": datetime.now()
            },
            {
                "_id": 5,
                "username": "hulk",
                "email": "bruce.banner@marvel.com",
                "password": "pbkdf2_sha256$260000$test",
                "first_name": "Bruce",
                "last_name": "Banner",
                "team_id": 1,
                "total_points": 1400,
                "created_at": datetime.now()
            },
            # Team DC
            {
                "_id": 6,
                "username": "superman",
                "email": "clark.kent@dc.com",
                "password": "pbkdf2_sha256$260000$test",
                "first_name": "Clark",
                "last_name": "Kent",
                "team_id": 2,
                "total_points": 1500,
                "created_at": datetime.now()
            },
            {
                "_id": 7,
                "username": "batman",
                "email": "bruce.wayne@dc.com",
                "password": "pbkdf2_sha256$260000$test",
                "first_name": "Bruce",
                "last_name": "Wayne",
                "team_id": 2,
                "total_points": 1450,
                "created_at": datetime.now()
            },
            {
                "_id": 8,
                "username": "wonderwoman",
                "email": "diana.prince@dc.com",
                "password": "pbkdf2_sha256$260000$test",
                "first_name": "Diana",
                "last_name": "Prince",
                "team_id": 2,
                "total_points": 1380,
                "created_at": datetime.now()
            },
            {
                "_id": 9,
                "username": "flash",
                "email": "barry.allen@dc.com",
                "password": "pbkdf2_sha256$260000$test",
                "first_name": "Barry",
                "last_name": "Allen",
                "team_id": 2,
                "total_points": 1220,
                "created_at": datetime.now()
            },
            {
                "_id": 10,
                "username": "aquaman",
                "email": "arthur.curry@dc.com",
                "password": "pbkdf2_sha256$260000$test",
                "first_name": "Arthur",
                "last_name": "Curry",
                "team_id": 2,
                "total_points": 1100,
                "created_at": datetime.now()
            }
        ]
        db.users.insert_many(users)

        # Insert Activities
        self.stdout.write('Inserting activities...')
        activities = []
        activity_types = ['Running', 'Cycling', 'Swimming', 'Weightlifting', 'Yoga', 'Boxing', 'CrossFit']
        
        for user in users:
            for i in range(random.randint(5, 15)):
                activity_date = datetime.now() - timedelta(days=random.randint(0, 30))
                activity = {
                    "user_id": user["_id"],
                    "activity_type": random.choice(activity_types),
                    "duration_minutes": random.randint(20, 120),
                    "calories_burned": random.randint(100, 800),
                    "distance_km": round(random.uniform(1, 20), 2) if random.choice(activity_types) in ['Running', 'Cycling', 'Swimming'] else 0,
                    "points_earned": random.randint(50, 200),
                    "date": activity_date,
                    "notes": f"Great workout session!"
                }
                activities.append(activity)
        
        db.activities.insert_many(activities)

        # Insert Workouts (Suggested workout plans)
        self.stdout.write('Inserting workouts...')
        workouts = [
            {
                "_id": 1,
                "name": "Hero Strength Training",
                "description": "Build superhuman strength with this intensive workout",
                "category": "Strength",
                "difficulty": "Advanced",
                "duration_minutes": 60,
                "exercises": [
                    {"name": "Bench Press", "sets": 4, "reps": 10},
                    {"name": "Squats", "sets": 4, "reps": 12},
                    {"name": "Deadlifts", "sets": 4, "reps": 8},
                    {"name": "Pull-ups", "sets": 3, "reps": 15}
                ],
                "created_at": datetime.now()
            },
            {
                "_id": 2,
                "name": "Speedster Cardio",
                "description": "Train like the fastest heroes alive",
                "category": "Cardio",
                "difficulty": "Intermediate",
                "duration_minutes": 45,
                "exercises": [
                    {"name": "Sprint Intervals", "sets": 6, "duration": "30 seconds"},
                    {"name": "Jump Rope", "sets": 3, "duration": "2 minutes"},
                    {"name": "Burpees", "sets": 3, "reps": 20},
                    {"name": "High Knees", "sets": 3, "duration": "1 minute"}
                ],
                "created_at": datetime.now()
            },
            {
                "_id": 3,
                "name": "Warrior Endurance",
                "description": "Build stamina for long battles",
                "category": "Endurance",
                "difficulty": "Intermediate",
                "duration_minutes": 90,
                "exercises": [
                    {"name": "Long Distance Run", "duration": "60 minutes"},
                    {"name": "Plank Hold", "sets": 3, "duration": "2 minutes"},
                    {"name": "Mountain Climbers", "sets": 4, "reps": 30},
                    {"name": "Jump Squats", "sets": 3, "reps": 20}
                ],
                "created_at": datetime.now()
            },
            {
                "_id": 4,
                "name": "Flexibility & Recovery",
                "description": "Maintain agility and prevent injuries",
                "category": "Flexibility",
                "difficulty": "Beginner",
                "duration_minutes": 30,
                "exercises": [
                    {"name": "Yoga Flow", "duration": "15 minutes"},
                    {"name": "Dynamic Stretching", "duration": "10 minutes"},
                    {"name": "Foam Rolling", "duration": "5 minutes"}
                ],
                "created_at": datetime.now()
            },
            {
                "_id": 5,
                "name": "Combat Training",
                "description": "Master hand-to-hand combat techniques",
                "category": "Combat",
                "difficulty": "Advanced",
                "duration_minutes": 60,
                "exercises": [
                    {"name": "Shadow Boxing", "sets": 5, "duration": "3 minutes"},
                    {"name": "Heavy Bag Work", "sets": 4, "duration": "3 minutes"},
                    {"name": "Speed Bag", "sets": 3, "duration": "2 minutes"},
                    {"name": "Grappling Drills", "sets": 3, "duration": "5 minutes"}
                ],
                "created_at": datetime.now()
            }
        ]
        db.workouts.insert_many(workouts)

        # Calculate and insert Leaderboard entries
        self.stdout.write('Calculating leaderboard...')
        leaderboard_entries = []
        
        # Individual leaderboard
        for user in sorted(users, key=lambda x: x['total_points'], reverse=True):
            rank = len(leaderboard_entries) + 1
            leaderboard_entries.append({
                "user_id": user["_id"],
                "username": user["username"],
                "team_id": user["team_id"],
                "total_points": user["total_points"],
                "rank": rank,
                "leaderboard_type": "individual",
                "updated_at": datetime.now()
            })
        
        # Team leaderboard
        team_scores = {}
        for user in users:
            team_id = user["team_id"]
            if team_id not in team_scores:
                team_scores[team_id] = {"total": 0, "count": 0}
            team_scores[team_id]["total"] += user["total_points"]
            team_scores[team_id]["count"] += 1
        
        team_rank = 1
        for team in sorted(teams, key=lambda x: team_scores[x["_id"]]["total"], reverse=True):
            team_id = team["_id"]
            leaderboard_entries.append({
                "team_id": team_id,
                "team_name": team["name"],
                "total_points": team_scores[team_id]["total"],
                "member_count": team_scores[team_id]["count"],
                "average_points": round(team_scores[team_id]["total"] / team_scores[team_id]["count"], 2),
                "rank": team_rank,
                "leaderboard_type": "team",
                "updated_at": datetime.now()
            })
            team_rank += 1
        
        db.leaderboard.insert_many(leaderboard_entries)

        # Summary
        self.stdout.write(self.style.SUCCESS('\n=== Database Population Complete ==='))
        self.stdout.write(self.style.SUCCESS(f'Teams created: {db.teams.count_documents({})}'))
        self.stdout.write(self.style.SUCCESS(f'Users created: {db.users.count_documents({})}'))
        self.stdout.write(self.style.SUCCESS(f'Activities created: {db.activities.count_documents({})}'))
        self.stdout.write(self.style.SUCCESS(f'Workouts created: {db.workouts.count_documents({})}'))
        self.stdout.write(self.style.SUCCESS(f'Leaderboard entries created: {db.leaderboard.count_documents({})}'))
        self.stdout.write(self.style.SUCCESS('\nDatabase successfully populated with superhero test data!'))
        
        client.close()
