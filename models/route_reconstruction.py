import numpy as np
import pandas as pd
from pathlib import Path
from scipy.spatial import cKDTree

# Paths
BASE = Path(__file__).resolve().parent.parent
DATA = BASE / "train"
OUTPUT = BASE / "results"
OUTPUT.mkdir(exist_ok=True)

# Select a training trip
trip = DATA / "00000001"

# Load data
track = pd.read_csv(
    trip / "00000001.track",
    sep=r"\s+",
    header=None,
    names=["lon", "lat", "time"]
)

nodes = pd.read_csv(
    trip / "00000001.nodes",
    sep=r"\s+",
    header=None,
    names=["lon", "lat"]
)

arcs = pd.read_csv(
    trip / "00000001.arcs",
    sep=r"\s+",
    header=None,
    names=["source", "target"]
)

# Limit GPS points to keep processing manageable
if len(track) > 300:
    indices = np.linspace(0, len(track) - 1, 300).astype(int)
    track = track.iloc[indices].reset_index(drop=True)

# Build road-network graph connections
edges = set()

for source, target in arcs.itertuples(index=False):
    edges.add((int(source), int(target)))
    edges.add((int(target), int(source)))

# Find nearest candidate road nodes for every GPS point
node_coordinates = nodes[["lon", "lat"]].to_numpy()
gps_coordinates = track[["lon", "lat"]].to_numpy()

tree = cKDTree(node_coordinates)

k = min(5, len(nodes))
distances, candidates = tree.query(gps_coordinates, k=k)

if k == 1:
    distances = distances.reshape(-1, 1)
    candidates = candidates.reshape(-1, 1)

# HMM-inspired Viterbi route selection
emission_weight = 100
transition_weight = 100

n = len(track)

cost = np.full((n, k), np.inf)
previous = np.zeros((n, k), dtype=int)

# Initial emission costs
cost[0] = distances[0] * emission_weight

# Viterbi algorithm
for i in range(1, n):

    gps_distance = np.linalg.norm(
        gps_coordinates[i] - gps_coordinates[i - 1]
    )

    for current in range(k):

        current_node = candidates[i, current]

        emission = distances[i, current] * emission_weight

        for previous_state in range(k):

            previous_node = candidates[i - 1, previous_state]

            road_distance = np.linalg.norm(
                node_coordinates[current_node] -
                node_coordinates[previous_node]
            )

            transition = abs(road_distance - gps_distance)

            # Small penalty if nodes are not directly connected
            if current_node != previous_node:
                if (int(previous_node), int(current_node)) not in edges:
                    transition += 0.05

            total = (
                cost[i - 1, previous_state]
                + emission
                + transition * transition_weight
            )

            if total < cost[i, current]:
                cost[i, current] = total
                previous[i, current] = previous_state

# Backtrack to find the best sequence
best_state = np.argmin(cost[-1])

route = [candidates[-1, best_state]]

for i in range(n - 1, 0, -1):
    best_state = previous[i, best_state]
    route.append(candidates[i - 1, best_state])

route.reverse()

# Save reconstructed route
result = pd.DataFrame({
    "gps_longitude": gps_coordinates[:, 0],
    "gps_latitude": gps_coordinates[:, 1],
    "matched_node": route,
    "matched_longitude": node_coordinates[route, 0],
    "matched_latitude": node_coordinates[route, 1]
})

result.to_csv(OUTPUT / "reconstructed_route.csv", index=False)

print("Route reconstruction completed!")
print("GPS points processed:", n)
print("Reconstructed route points:", len(route))
print("Output saved to results/reconstructed_route.csv")