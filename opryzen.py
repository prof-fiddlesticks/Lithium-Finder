import pandas as pd
import numpy as np
import xgboost as xgb
from sklearn.model_selection import LeaveOneOut, GridSearchCV
from sklearn.preprocessing import RobustScaler
from tqdm import tqdm

# 1. LOAD PLAN C DATA
df = pd.read_csv('master_lithium_v3_context.csv')

# The 14 Contextual Features
features = [
    'Clay_CMR', 'Hydroxyl_OHI', 'Silica_Proxy', 'Borate_Proxy', 'SI1', 'BMI', 
    'Albedo', 'Iron_Oxide', 'Ferrous_Idx', 'NDSI', 
    'B11', 'B12', 'Elevation', 'Slope'
]

X = df[features].copy()
y = df['Label']

scaler = RobustScaler()
X_scaled = scaler.fit_transform(X)

# 2. SEARCH GRID
param_grid = {
    'max_depth': [3, 4, 5],         # Letting it think a bit deeper for topography
    'learning_rate': [0.01, 0.05], 
    'n_estimators': [300, 500,1000],
    'subsample': [0.7, 0.85],       
    'colsample_bytree': [0.7, 0.8], 
    'reg_alpha': [0.1, 1.0],        
    'reg_lambda': [5, 20]          
}

print("🏔️ Plan C: Running Topographical & Spectral Search...")
print("Engaging all Ryzen threads. Looking for Basin/Pegmatite signatures...")

grid_search = GridSearchCV(
    estimator=xgb.XGBClassifier(tree_method='hist', n_jobs=-1, random_state=42),
    param_grid=param_grid,
    cv=5, 
    scoring='accuracy'
)

grid_search.fit(X_scaled, y)
best_model = grid_search.best_estimator_

# 3. TRUTH TEST (LOOCV)
loo = LeaveOneOut()
loo_scores = []

for train_idx, test_idx in tqdm(loo.split(X_scaled), total=len(X_scaled)):
    X_train, X_test = X_scaled[train_idx], X_scaled[test_idx]
    y_train, y_test = y.iloc[train_idx], y.iloc[test_idx]
    
    best_model.fit(X_train, y_train)
    pred = best_model.predict(X_test)
    loo_scores.append(1 if pred[0] == y_test.iloc[0] else 0)

final_acc = np.mean(loo_scores)
print(f"\n🏁 PLAN C VERIFIED ACCURACY: {final_acc:.4f}")

# 4. NEW FEATURE IMPORTANCE
feat_imp = pd.Series(best_model.feature_importances_, index=features).sort_values(ascending=False)
print("\n📊 PLAN C TOP 5 MARKERS (Topography Included):")
print(feat_imp.head(5))
