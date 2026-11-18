import os
import pandas as pd
from sklearn.model_selection import train_test_split, RandomizedSearchCV
from sklearn.ensemble import RandomForestClassifier

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

data = pd.read_csv(os.path.join(BASE, "results", "processed_data.csv"))

X = data[[
    "longitude", "latitude", "time",
    "longitude_change", "latitude_change",
    "speed", "route_length", "node_count"
]]

y = (data["longitude"] > data["longitude"].median()).astype(int)

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

model = RandomForestClassifier(random_state=42, n_jobs=-1)

params = {
    "n_estimators": [20, 30, 50],
    "max_depth": [5, 10, 15],
    "min_samples_split": [2, 5]
}

search = RandomizedSearchCV(
    model,
    params,
    n_iter=5,
    cv=3,
    n_jobs=-1,
    random_state=42
)

search.fit(X_train, y_train)

print("Best parameters:", search.best_params_)
print("Best CV score:", search.best_score_)
print("Test score:", search.score(X_test, y_test))