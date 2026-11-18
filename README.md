# PathSnap - GPS Route Reconstruction

## Project Overview
PathSnap is a GPS route reconstruction prototype that processes GPS trajectory data and matches GPS points to road-network nodes.

## Features
- GPS dataset inspection
- GPS data preprocessing
- Feature extraction
- Training and comparison of five ML models
- Randomized hyperparameter optimization
- Viterbi-based route reconstruction
- FastAPI backend
- Interactive map visualization using Leaflet
- Automated API tests

## Technologies Used
- Python
- NumPy and Pandas
- Scikit-learn
- SciPy
- FastAPI
- Leaflet.js
- OpenStreetMap

## Project Structure
- data_processing: Data inspection and preprocessing
- models: ML models and route reconstruction
- backend: FastAPI application
- frontend: Interactive map interface
- results: Generated output files
- tests: API tests

## How to Run

Install dependencies:

pip install -r requirements.txt

Run the backend:

python -m uvicorn backend.main:app --reload

Open API documentation:

http://127.0.0.1:8000/docs

Run the frontend in another terminal:

python -m http.server 5500 --directory frontend

Open:

http://127.0.0.1:5500

Run tests:

python tests/test_api.py

## Limitations
The current route reconstruction is an HMM-inspired Viterbi baseline, not a complete road-network HMM implementation.

The initial ML classification experiment uses a temporary longitude-based target and does not measure actual route-matching accuracy.