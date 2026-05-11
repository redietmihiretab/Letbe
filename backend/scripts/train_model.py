import pandas as pd
import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
import os

def train_baseline_model(data_path):
    if not os.path.exists(data_path):
        print(f"Data not found at {data_path}. Please run ingest_historical.py first.")
        return
    
    df = pd.read_csv(data_path)
    
    # Define Target: 1 (Home Win), 0 (Draw), 2 (Away Win)
    def label_outcome(row):
        if row['FTHG'] > row['FTAG']: return 1 # Home
        if row['FTHG'] == row['FTAG']: return 0 # Draw
        return 2 # Away
    
    df['target'] = df.apply(label_outcome, axis=1)
    
    # Feature Selection (Basic form/strength features)
    # For a real model, we'd use rolling averages here.
    # For this baseline, we'll just use a few match-day stats (though this is "leaky" for prediction, it's for demo)
    features = ['HS', 'AS', 'HST', 'AST', 'HC', 'AC']
    X = df[features]
    y = df['target']
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    print("Training XGBoost Classifier...")
    model = xgb.XGBClassifier(objective='multi:softprob', num_class=3)
    model.fit(X_train, y_train)
    
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    
    print(f"\nModel Accuracy: {accuracy:.2f}")
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred))
    
    # Save model
    os.makedirs("backend/models", exist_ok=True)
    model.save_model("backend/models/baseline_1x2.json")
    print("\nModel saved to backend/models/baseline_1x2.json")

if __name__ == "__main__":
    train_baseline_model("backend/data/E0_2324_processed.csv")
