import re
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score, classification_report

# Function to extract hexadecimal patterns from a text
def extract_hex_patterns(text):
    hex_patterns = re.findall(r'\b[0-9A-Fa-f]+\b', text)
    return hex_patterns

# Function to classify hex patterns
def classify_hex_patterns(hex_patterns):
    labels = []
    for pattern in hex_patterns:
        # Define your classification logic here
        # For this example, we classify patterns with length > 4 as 'hexadecimal' and others as 'non-hexadecimal'
        if len(pattern) > 4:
            labels.append('hexadecimal')
        else:
            labels.append('non-hexadecimal')
    return labels

# Load the text file
file_path = 'output.csv'
with open(file_path, 'r') as file:
    file_content = file.read()

# Extract hexadecimal patterns from the file content
hex_patterns = extract_hex_patterns(file_content)

# Classify the hex patterns
labels = classify_hex_patterns(hex_patterns)

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(hex_patterns, labels, test_size=0.2, random_state=42)

# Vectorize the text data
vectorizer = CountVectorizer()
X_train = vectorizer.fit_transform(X_train)
X_test = vectorizer.transform(X_test)

# Train a Multinomial Naive Bayes classifier
classifier = MultinomialNB()
classifier.fit(X_train, y_train)

# Make predictions on the test data
y_pred = classifier.predict(X_test)

# Evaluate the model
accuracy = accuracy_score(y_test, y_pred)
print(f'Accuracy: {accuracy:.2f}')

# Display classification report
report = classification_report(y_test, y_pred)
print(report)
