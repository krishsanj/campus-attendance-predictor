
# train_model.py

import pandas as pd
import pickle

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
    classification_report
)

# 1. Load the sample dataset.
df = pd.read_csv("sample_students.csv")

# 2. Select the input columns.
# These are the factors the model uses to make a prediction.
X = df[
    [
        "Attendance",
        "Internal_Marks",
        "Assignment_Completion",
        "Previous_Performance"
    ]
]

# 3. Select the target column.
# This is the outcome the model tries to learn.
y = df["Dropped_Out"]

# 4. Split data into training and testing sets.
# 80% is used for training and 20% for testing.
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)

# 5. Create the Logistic Regression model.
model = LogisticRegression(max_iter=1000)

# 6. Train the model using the training data.
model.fit(X_train, y_train)

# 7. Predict outcomes for unseen test rows.
y_pred = model.predict(X_test)

# 8. Calculate evaluation metrics.
print("Accuracy:", accuracy_score(y_test, y_pred))

print(
    "Precision:",
    precision_score(y_test, y_pred, zero_division=0)
)

print(
    "Recall:",
    recall_score(y_test, y_pred, zero_division=0)
)

print(
    "F1 Score:",
    f1_score(y_test, y_pred, zero_division=0)
)

print("\nConfusion Matrix:")
print(confusion_matrix(y_test, y_pred))

print("\nClassification Report:")
print(classification_report(y_test, y_pred, zero_division=0))

# 9. Save the trained model for later use.
with open("dropout_model.pkl", "wb") as file:
    pickle.dump(model, file)

print("\nModel saved as dropout_model.pkl")
