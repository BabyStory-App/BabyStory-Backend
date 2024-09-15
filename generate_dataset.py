import os
import random
from datetime import datetime, timedelta

# Helper function to create random datetime


def random_datetime(start, end):
    return start + timedelta(seconds=random.randint(0, int((end - start).total_seconds())))

# Random data generators


def random_email(name):
    random_name = random.choice([
        "John", "Jane", "Michael", "Emily", "David", "Sophia",
        "James", "Olivia", "Daniel", "Isabella", "Matthew", "Ava",
        "Andrew", "Mia", "Joseph", "Charlotte", "Samuel", "Amelia",
        "Benjamin", "Harper", "Christopher", "Evelyn", "William",
        "Abigail", "Joshua", "Lily", "Alexander", "Grace", "Noah", "Ella"
    ]).lower()
    return f"{random_name}{random.randint(1, 100)}@example.com"


def random_gender():
    return random.randint(0, 1)


def random_blood_type():
    return random.choice([" A+", " B+", "AB+", " O+", " A-", " B-", "AB-", " O-"])


# Constants
start_date = datetime(2010, 1, 1)
end_date = datetime(2020, 12, 31)


# Modify the baby and parent name lists
baby_names = [
    "이서준", "김하율", "박도윤", "최민서", "강예진",
    "장지호", "한유진", "오은서", "윤지우", "문하린",
    "정서연", "홍수아", "신시윤", "백태윤", "권준혁"
]
parent_nicknames = ['아크하드', '자이언트', '질리탄', '대상혁', '뭐에유']
parent_names = ['김철수', '김근언', '이정원', '장윤정', '정다운']

# Clear previous commands
insert_commands = []

# Adjust the random date generator for baby states to ensure realistic time progression


def generate_baby_states_with_time_progression(baby_id, birth_date):
    baby_cm = random.uniform(30, 50)  # Starting height between 30 and 50 cm
    baby_kg = random.uniform(3, 5)    # Starting weight between 3 and 5 kg
    baby_states = []
    current_time = birth_date  # Start from the baby's birth date

    for k in range(1, 101):
        # Increment time for each entry by adding random days
        time_increment = timedelta(days=random.randint(5, 12), hours=random.randint(
            0, 3), minutes=random.randint(0, 59), seconds=random.randint(0, 59))
        current_time += time_increment

        # Increment height and weight slightly for each entry
        baby_cm += random.uniform(0.1, 0.5)  # Increment between 0.1 and 0.5 cm
        # Increment between 0.05 and 0.3 kg
        baby_kg += random.uniform(0.05, 0.3)

        baby_states.append(
            f"INSERT INTO babystate (baby_id, createTime, cm, kg) VALUES ('{baby_id}', '{current_time}', {round(baby_cm, 2)}, {round(baby_kg, 2)});")

    return baby_states


# Adjusted logic to use birthDate of baby for post, babyState, and other related data
insert_commands = []

# Generate parent data using new parent names and nicknames
for i in range(1, 6):
    name = parent_names[i - 1]
    nickname = parent_nicknames[i - 1]
    email = random_email(name)
    parent_id = f"parent{i}"
    parent_creation_time = random_datetime(start_date, end_date)
    insert_commands.append(
        f"INSERT INTO parent (parent_id, password, email, name, nickname, gender, signInMethod, emailVerified) VALUES ('{parent_id}', 'password{i}', '{email}', '{name}', '{nickname}', {random_gender()}, 'email', TRUE);")

    # Generate posts for each parent with realistic createTime values
    for j in range(1, 6):
        post_id = i * 10 + j
        post_creation_time = parent_creation_time + \
            timedelta(days=random.randint(1, 100))
        insert_commands.append(
            f"INSERT INTO post (post_id, parent_id, reveal, title, createTime) VALUES ({post_id}, 'parent{i}', 1, 'Post Title {post_id}', '{post_creation_time}');")

# Generate baby data using new baby names and baby state data with growth increments
for i in range(1, 6):
    for j in range(1, 4):
        baby_id = f"baby{i}{j}"
        baby_name = baby_names[(i - 1) * 3 + (j - 1)]
        # Ensure the baby is born after the parent account was created
        baby_birth_date = random_datetime(
            parent_creation_time, end_date - timedelta(days=365))
        insert_commands.append(
            f"INSERT INTO baby (baby_id, obn, name, gender, birthDate, bloodType) VALUES ('{baby_id}', 'obn{baby_id}', '{baby_name}', {random_gender()}, '{baby_birth_date}', '{random_blood_type()}');")

        # Generate baby state data with gradual growth for each baby with time progression
        baby_state_entries = generate_baby_states_with_time_progression(
            baby_id, baby_birth_date)
        insert_commands.extend(baby_state_entries)

# Generate SQL insert commands for the updated test data with realistic time progression
test_data_sql_time_corrected = "\n".join(insert_commands)
with open("test_data.sql", "w") as f:
    f.write(test_data_sql_time_corrected)
