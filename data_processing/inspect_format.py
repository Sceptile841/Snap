import os

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

for split, trip in [("train", "00000001"), ("student_test", "00000000")]:

    folder = os.path.join(BASE, split, trip)

    print(f"\n========== {split.upper()} ==========")

    for filename in os.listdir(folder):

        print(f"\n--- {filename} ---")

        with open(os.path.join(folder, filename), "r") as f:
            for i in range(5):
                line = f.readline()
                if not line:
                    break
                print(line.strip())