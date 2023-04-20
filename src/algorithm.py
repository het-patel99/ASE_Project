import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score
from sklearn.ensemble import RandomForestRegressor
from options import options

class MultiObjectiveModel:
    def __init__(self):
        self.rf_mpg = RandomForestRegressor(n_estimators=100, random_state=42)
        self.rf_hp = RandomForestRegressor(n_estimators=100, random_state=42)
        
    def fit(self, X, y):
        self.rf_mpg.fit(X, y['Mpg+'])
        self.rf_hp.fit(X, y['HpX'])
        
    def predict(self, X):
        y_mpg = self.rf_mpg.predict(X)
        y_hp = self.rf_hp.predict(X)
        return np.column_stack((y_mpg, y_hp))

# Load dataset and split into labeled and unlabeled examples
data = pd.read_csv("../etc/data/auto93.csv", na_values='?')
data = data.dropna()
X = data.drop(columns=['Mpg+', 'HpX'])
y = data[['Mpg+', 'HpX']]
X_labeled, X_unlabeled, y_labeled, y_unlabeled = train_test_split(X, y, test_size=0.8, random_state=42)

# Set algorithm parameters
B0 = 10  # initial subset size
budget = 50  # total number of times Y values can be accessed
m = 5  # number of examples to select in each iteration

# Train initial model on labeled examples
scaler = StandardScaler()
X_labeled_scaled = scaler.fit_transform(X_labeled)
model = MultiObjectiveModel()
model.fit(X_labeled_scaled, y_labeled)

# Loop until desired performance is achieved or budget is exhausted
while True:
    # Rank unlabeled examples based on predicted scores
    X_unlabeled_scaled = scaler.transform(X_unlabeled)
    scores = model.predict(X_unlabeled_scaled)
    ranked_examples = np.argsort(scores, axis=0)[::-1]
    
    # Extract summary of top m examples
    summary = ranked_examples[:m]
    
    # Evaluate model on selected examples
    X_selected = X_unlabeled.iloc[summary]
    y_selected = y_unlabeled.iloc[summary]
    X_combined = pd.concat([X_labeled, X_selected])
    y_combined = pd.concat([y_labeled, y_selected])
    X_combined_scaled = scaler.transform(X_combined)
    model.fit(X_combined_scaled, y_combined)
    y_pred = model.predict(X_labeled_scaled)
    performance = accuracy_score(y_labeled['Mpg+'], y_pred[:,0] > np.median(y_labeled['Mpg+']))
    
    # Update budget and check stopping condition
    budget -= m
    if budget <= 0 or performance > 0.9:
        break
    X_unlabeled = X_unlabeled.drop(index=X_selected.index)
    y_unlabeled = y_unlabeled.drop(index=X_selected.index)

# Output final model and selected examples
print(f"Final performance: {performance}")
