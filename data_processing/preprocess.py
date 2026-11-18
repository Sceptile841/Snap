import os
import numpy as np
import pandas as pd

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

all_data = []

for trip in os.listdir(os.path.join(BASE, "train")):

    folder = os.path.join(BASE, "train", trip)

    track_file = os.path.join(folder, trip + ".track")
    nodes_file = os.path.join(folder, trip + ".nodes")
    route_file = os.path.join(folder, trip + ".route")

    track = pd.read_csv(
        track_file, sep=r"\s+", header=None,
        names=["longitude", "latitude", "time"]
    )

    nodes = pd.read_csv(
        nodes_file, sep=r"\s+", header=None,
        names=["longitude", "latitude"]
    )

    route = pd.read_csv(route_file, header=None, names=["node_id"])

    track = track.replace([np.inf, -np.inf], np.nan).dropna()

    track["trip_id"] = trip

    track["longitude_change"] = track["longitude"].diff().fillna(0)
    track["latitude_change"] = track["latitude"].diff().fillna(0)

    track["speed"] = np.sqrt(
        track["longitude_change"]**2 +
        track["latitude_change"]**2
    )

    track["route_length"] = len(route)
    track["node_count"] = len(nodes)

    all_data.append(track)

data = pd.concat(all_data, ignore_index=True)

os.makedirs(os.path.join(BASE, "results"), exist_ok=True)

data.to_csv(os.path.join(BASE, "results", "processed_data.csv"), index=False)

print("Preprocessing completed!")
print("Total GPS records:", len(data))
print("Total training trips:", data["trip_id"].nunique())
print(data.head())