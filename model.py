import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, confusion_matrix

# 1. LOAD DATA
df = pd.read_csv('master_lithium_dataset_100_sites.csv')

# 2. SELECT THE "ELITE 8" SURVIVORS
features = ['Iron_Oxide', 'SI1', 'Albedo', 'VegStress', 'Shadow_Proxy', 'Clay_CMR', 'BMI', 'Silica_Proxy']
X = df[features].copy()
y = df['Label']

# 3. THE "SUPER-INTERACTIONS" (The secret to 80%)
# These tell the AI how markers combine in real geology
X['Iron_Salt_Inter'] = X['Iron_Oxide'] * X['SI1']  # High Iron + High Salt = Lithium signature
X['Shadow_Veg_Inter'] = X['Shadow_Proxy'] * X['VegStress'] # Geography + Plant stress
X['Clay_BMI_Ratio'] = X['Clay_CMR'] / (X['BMI'] + 1e-6) # Pure clay vs moisture

# 4. SCALE EVERYTHING
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# 5. SPLIT (Using your preferred Random State 42)
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.3, random_state=42)

# 6. THE "ULTRA-PRECISION" GRADIENT BOOSTER
# We use a very slow learning rate (0.01) to find deep patterns without overfitting
model = GradientBoostingClassifier(
    n_estimators=1000, 
    learning_rate=0.01, 
    max_depth=3,         # Moderate depth
    subsample=0.8,       # Only look at 80% of data per tree to prevent memorizing
    random_state=42
)

print("🧪 Training the 80% PB Crusher Model...")
model.fit(X_train, y_train)

# 7. THE FINAL MOMENT OF TRUTH
y_pred = model.predict(X_test)
test_acc = accuracy_score(y_test, y_pred)

print("\n" + "="*40)
print(f"🎯 FINAL TEST ACCURACY: {test_acc:.4f} ")
print("="*40)

print("\nConfusion Matrix:")
print(confusion_matrix(y_test, y_pred))
