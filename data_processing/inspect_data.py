import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

for split in ["train", "student_test"]:

    folder = os.path.join(BASE_DIR, split)

    print(f"\n========== {split.upper()} ==========")

    trips = os.listdir(folder)
    print("Total trips:", len(trips))

    for trip in trips[:3]:

        trip_path = os.path.join(folder, trip)

        print(f"\nTrip: {trip}")

        for file in os.listdir(trip_path):

            filepath = os.path.join(trip_path, file)

            with open(filepath, "r") as f:
                lines = f.readlines()

            print(file, " | Records:", len(lines))