import pandas as pd
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
import joblib
import os

df = pd.read_csv("chatapp/data/food_dataset.csv")  # must exist
X, y = df["dish"], df["label"]

model = Pipeline([
    ("tfidf", TfidfVectorizer(ngram_range=(1, 2))),
    ("clf", LogisticRegression(max_iter=1000))
])
model.fit(X, y)

# Save to classifier path
output_path = os.path.join("chatapp", "classifier", "food_classifier.pkl")
joblib.dump(model, output_path)
print(f"✅ Model saved to {output_path}")
