import json
import random
from datetime import datetime, timedelta


def save_cry_state_sample_data_to_file(start_date, end_date, baby_id, file_path):
    # Constants
    types = ['sad', 'hug', 'diaper', 'hungry',
             'sleepy', 'awake', 'uncomfortable']
    intensities = ['low', 'medium', 'high']
    audio_id_counter = 1

    def generate_predict_map():
        # Randomly select 4 types to have a probability of 0
        zero_probability_types = random.sample(types, 4)

        # Remaining types will have probabilities of 0.8, 0.1, and 0.1
        remaining_types = [t for t in types if t not in zero_probability_types]
        probabilities = [0.85, 0.1, 0.05]
        uniform = random.uniform(-0.07, 0.07)
        half_uniform = uniform / 2
        probabilities[0] -= uniform
        probabilities[1] += half_uniform
        probabilities[2] += half_uniform
        # Shuffle to assign these probabilities randomly
        random.shuffle(probabilities)

        # Combine into a single dictionary
        predict_map = {t: 0.0 for t in zero_probability_types}
        for t, p in zip(remaining_types, probabilities):
            predict_map[t] = round(p, 3)

        return predict_map

    # Writing data to the file
    with open(file_path, 'w') as file:
        current_date = start_date
        while current_date <= end_date:
            # Random number of records for the day
            num_records = random.randint(1, 4)
            for _ in range(num_records):
                # Generate random time for the current date
                random_time = current_date + timedelta(hours=random.randint(
                    0, 23), minutes=random.randint(0, 59), seconds=random.randint(0, 59))
                # Randomly select intensity and duration
                intensity = random.choice(intensities)
                duration = round(random.uniform(2.0, 17.0), 2)
                # Generate predictMap and select type with the largest probability
                predict_map = generate_predict_map()
                selected_type = max(predict_map, key=predict_map.get)
                # Create the SQL INSERT statement
                insert_statement = f"INSERT INTO cry_state (babyId, time, type, audioId, predictMap, intensity, duration) VALUES ('{baby_id}', '{random_time.strftime('%Y-%m-%d %H:%M:%S')}', '{selected_type}', 'audioId{audio_id_counter}', '{json.dumps(predict_map)}', '{intensity}', {duration});\n"
                file.write(insert_statement)
                audio_id_counter += 1
            current_date += timedelta(days=1)

    return file_path


# Example usage
if __name__ == '__main__':
    file_path = 'cry_state_sample_data.txt'
    start_date = datetime(2023, 9, 12)
    end_date = datetime(2023, 12, 4)
    baby_id = "0204eb99-35de-4a30-b6fc-9590a176985c"
    save_cry_state_sample_data_to_file(
        start_date, end_date, baby_id, file_path)
