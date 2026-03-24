import pandas as pd
import xgboost as xgb
from sklearn.preprocessing import RobustScaler

# 1. PREPARE THE DATA
v6 = pd.read_csv('master_lithium_v6_ultra_hard.csv')
v7 = pd.read_csv('master_lithium_v7_final.csv')
df = pd.merge(v6, v7[['Site', 'NDVI', 'NDWI']], on='Site')

# Keep the specialist Arid Scope
df_arid = df[df['NDVI'] <= 0.4].copy()

# Core features used in the 80% run
features = ['Elevation', 'BMI', 'Silica_Proxy', 'B11', 'NDSI']
X = df_arid[features]
y = df_arid['Label']

# 2. THE GOLDEN BRAIN (Version 2)
# Locked in with your exact lucky parameters from the screenshot
v2_champion = xgb.XGBClassifier(
    colsample_bytree=0.94657,
    gamma=1.39575,
    learning_rate=0.06072,
    max_depth=2,
    min_child_weight=1,
    n_estimators=941,
    reg_alpha=0.70525,
    reg_lambda=4.35466,
    subsample=0.86041,
    random_state=42
)

v2_champion.fit(X, y)

# 3. SAVE TO DISK
v2_champion.save_model("lithium_hunter_v2_pro.json")

print("✨" * 20)
print("🚀 VERSION 2 (80.25%) DEPLOYED!")
print("💾 File: 'lithium_hunter_v2_pro.json'")
print("✨" * 20)
