#initiator
from sklearn.datasets import fetch_20newsgroups
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.svm import SVC
from sklearn.pipeline import make_pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import seaborn as sns
import matplotlib.pyplot as plt

# Load dataset (filtered categories)
categories = ['alt.atheism', 'soc.religion.christian', 'comp.graphics', 'sci.med']
data = fetch_20newsgroups(subset='all', categories=categories, remove=('headers', 'footers', 'quotes'))

# Split data
X_train, X_test, y_train, y_test = train_test_split(data.data, data.target, test_size=0.2, random_state=42)

# Pipeline: TF-IDF + SVM + Scaling
pipeline = make_pipeline(
    TfidfVectorizer(stop_words='english', max_df=0.7, max_features=5000, ngram_range=(1, 2), min_df=2),
    StandardScaler(with_mean=False),  # Scaling for sparse matrices
    SVC(class_weight='balanced')
)

# Hyperparameter grid search
params = {
    'svc__C': [0.1, 1, 10, 100, 1000],
    'svc__gamma': ['scale', 'auto', 0.01, 0.001],
    'svc__kernel': ['linear', 'rbf', 'poly'],
    'svc__degree': [3, 4, 5]  # For 'poly' kernel
}

# Grid Search with 10-fold cross-validation
grid = GridSearchCV(pipeline, params, cv=10, n_jobs=-1, verbose=1)
grid.fit(X_train, y_train)

# Best parameters
print(f"Best Parameters: {grid.best_params_}")

# Predictions
y_pred = grid.predict(X_test)

# Evaluation
print(f"Accuracy: {accuracy_score(y_test, y_pred):.4f}")
print("\nClassification Report:\n", classification_report(y_test, y_pred, target_names=categories))

# Confusion Matrix
cm = confusion_matrix(y_test, y_pred)
plt.figure(figsize=(10, 7))
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', xticklabels=categories, yticklabels=categories)
plt.xlabel('Predicted')
plt.ylabel('Actual')
plt.show()

# Predict for new review
new_review = ["The latest graphics processing units are optimized for gaming"]
new_pred = grid.predict(new_review)
predicted_category = categories[new_pred[0]]
print(f"\nPredicted category for the new review: {predicted_category}")
