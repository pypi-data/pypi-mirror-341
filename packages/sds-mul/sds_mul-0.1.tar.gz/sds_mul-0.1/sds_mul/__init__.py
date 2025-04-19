import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score, classification_report
from sklearn.preprocessing import KBinsDiscretizer
import seaborn as sns
import matplotlib.pyplot as plt
url = "https://raw.githubusercontent.com/jbrownlee/Datasets/master/pima-indians-diabetes.data.csv"
columns = ["Pregnancies", "Glucose", "BloodPressure", "SkinThickness", "Insulin",
           "BMI", "DiabetesPedigreeFunction", "Age", "Outcome"]
df = pd.read_csv(url, names=columns)
X = df.drop(['Glucose'], axis=1)
y = df['Glucose']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
model = LinearRegression()
model.fit(X_train, y_train)
y_pred = model.predict(X_test)
mse = mean_squared_error(y_test, y_pred)
rmse = np.sqrt(mse)
r2 = r2_score(y_test, y_pred)

print("Multiple Linear Regression Evaluation:")
print(f"Mean Squared Error (MSE): {mse:.2f}")
print(f"Root Mean Squared Error (RMSE): {rmse:.2f}")
print(f"R-squared (R²): {r2:.4f}")

bin_encoder = KBinsDiscretizer(n_bins=3, encode='ordinal', strategy='quantile')
y_test_bins = bin_encoder.fit_transform(y_test.values.reshape(-1, 1)).astype(int).flatten()
y_pred_bins = bin_encoder.transform(y_pred.reshape(-1, 1)).astype(int).flatten()

print("\nClassification-style Evaluation:")
print(classification_report(y_test_bins, y_pred_bins, zero_division=0))

new_patient = pd.DataFrame([{
    'Pregnancies': 2,
    'BloodPressure': 70,
    'SkinThickness': 25,
    'Insulin': 80,
    'BMI': 28.5,
    'DiabetesPedigreeFunction': 0.45,
    'Age': 33,
    'Outcome': 1
}])

predicted_glucose = model.predict(new_patient)[0]
print(f"\nPredicted Glucose Level for New Patient: {predicted_glucose:.2f}")
