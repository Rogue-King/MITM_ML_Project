import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report

# 1. Prepare your features (X) and labels (y)
# Assume you have already extracted and processed your features.
# X should be a 2D array (or DataFrame) with shape (n_samples, n_features).
# y should be a 1D array with shape (n_samples,) containing binary labels.

# 2. Split your data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# 3. Create an instance of the Logistic Regression model
model = LogisticRegression()

# 4. Train the model on the training data
model.fit(X_train, y_train)

# 5. Make predictions on the test set
y_pred = model.predict(X_test)

# 6. Evaluate the model's performance
accuracy = accuracy_score(y_test, y_pred)
print(f"Accuracy: {accuracy}")

# Generate a classification report for more detailed metrics
report = classification_report(y_test, y_pred)
print(report)
