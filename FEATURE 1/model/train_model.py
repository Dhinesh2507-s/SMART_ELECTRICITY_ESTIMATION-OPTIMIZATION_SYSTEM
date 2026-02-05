import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestRegressor
import pickle

# 1. Load dataset
df = pd.read_csv("C:\\Users\\Hema V\\Downloads\\electricity_project\\data\\synthetic_electricity_dataset_5000.csv")

# 2. Encode categorical columns
le = LabelEncoder()
df["lighting_type"] = le.fit_transform(df["lighting_type"])
df["tariff_type"] = le.fit_transform(df["tariff_type"])
df["season"] = le.fit_transform(df["season"])

# 3. Split input & output
X = df.drop("predicted_bill", axis=1)
y = df["predicted_bill"]

# 4. Train-test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# 5. Train ML model
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# 6. Save model
with open("model/electricity_model.pkl", "wb") as f:
    pickle.dump(model, f)

print("✅ Model trained and saved successfully")
