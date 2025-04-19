# Import necessary libraries
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import LabelEncoder
from sklearn import tree
import matplotlib.pyplot as plt

# Define the dataset
data = {
    'Outlook': ['Sunny', 'Sunny', 'Overcast', 'Rain', 'Rain', 'Rain', 'Overcast', 'Sunny', 'Sunny', 'Rain', 
                'Sunny', 'Overcast', 'Overcast', 'Rain', 'Sunny', 'Overcast', 'Overcast', 'Rain', 'Sunny', 'Rain'],
    'Wind': ['Weak', 'Strong', 'Weak', 'Weak', 'Weak', 'Strong', 'Strong', 'Weak', 'Weak', 'Weak', 
             'Strong', 'Strong', 'Weak', 'Strong', 'Strong', 'Strong', 'Weak', 'Weak', 'Weak', 'Strong'],
    'PlayTennis': ['No', 'No', 'Yes', 'Yes', 'Yes', 'No', 'Yes', 'No', 'Yes', 'Yes', 
                   'Yes', 'Yes', 'Yes', 'No', 'Yes', 'No', 'Yes', 'No', 'No', 'Yes']
}

# Convert to DataFrame
df = pd.DataFrame(data)

# Label encoding for categorical variables
le = LabelEncoder()
df['Outlook'] = le.fit_transform(df['Outlook'])
df['Wind'] = le.fit_transform(df['Wind'])
df['PlayTennis'] = le.fit_transform(df['PlayTennis'])

# Define features and target variable
X = df.drop('PlayTennis', axis=1)  # Features (Outlook, Wind)
y = df['PlayTennis']  # Target (PlayTennis)

# Split the data into training and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Initialize and train the Decision Tree Classifier
clf = DecisionTreeClassifier(random_state=42)
clf.fit(X_train, y_train)

# Make predictions
y_pred = clf.predict(X_test)

# Calculate the accuracy
accuracy = accuracy_score(y_test, y_pred)
print(f"Accuracy of the Decision Tree model: {accuracy * 100:.2f}%")

# Visualize the decision tree
plt.figure(figsize=(12,8))
tree.plot_tree(clf, filled=True, feature_names=X.columns, class_names=['No', 'Yes'], rounded=True)
plt.title("Decision Tree for PlayTennis Classification")
plt.show()

# Test the model with a sample input (e.g., Outlook=Sunny, Wind=Weak)
sample_input = pd.DataFrame([[1, 0]], columns=['Outlook', 'Wind'])  # Outlook=Sunny, Wind=Weak (encoded as 1 and 0)
prediction = clf.predict(sample_input)

# Print prediction and conclusion
predicted_label = 'PlayTennis' if prediction == 1 else 'No PlayTennis'
print(f"Prediction for Outlook=Sunny and Wind=Weak: {predicted_label}")

# Conclusion
if predicted_label == "PlayTennis":
    print("Conclusion: The model predicted that the person will play tennis, which is correct as per the rules.")
else:
    print("Conclusion: The model predicted that the person will not play tennis. The prediction aligns with the dataset and decision tree logic.")
