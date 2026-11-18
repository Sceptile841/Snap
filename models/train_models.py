import os
import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline
from sklearn.metrics import accuracy_score

from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, ExtraTreesClassifier, GradientBoostingClassifier, HistGradientBoostingClassifier

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

data = pd.read_csv(os.path.join(BASE, "results", "processed_data.csv"))

features = [
    "longitude",
    "latitude",
    "time",
    "longitude_change",
    "latitude_change",
    "speed",
    "route_length",
    "node_count"
]

X = data[features]

# Temporary demonstration target, NOT actual road-node labels.
y = (data["longitude"] > data["longitude"].median()).astype(int)

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

models = {
    "Decision Tree": DecisionTreeClassifier(max_depth=10),
    "Random Forest": RandomForestClassifier(n_estimators=30, max_depth=10, n_jobs=-1),
    "Extra Trees": ExtraTreesClassifier(n_estimators=30, max_depth=10, n_jobs=-1),
    "Gradient Boosting": GradientBoostingClassifier(n_estimators=30, max_depth=3),
    "Histogram Gradient Boosting": HistGradientBoostingClassifier(max_iter=30, max_leaf_nodes=15)
}

os.makedirs(os.path.join(BASE, "models", "saved"), exist_ok=True)

for name, model in models.items():

    model.fit(X_train, y_train)

    predictions = model.predict(X_test)

    accuracy = accuracy_score(y_test, predictions)

    filename = name.lower().replace(" ", "_") + ".joblib"

    joblib.dump(model, os.path.join(BASE, "models", "saved", filename))

    print(f"{name}: {accuracy:.4f}")

print("\nTraining completed!")