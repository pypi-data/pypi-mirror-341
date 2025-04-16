#svm classi

from sklearn.datasets import fetch_20newsgroups
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.metrics import classification_report, accuracy_score

# Selected categories
categories = ['alt.atheism', 'soc.religion.christian', 'comp.graphics', 'sci.med']

# 1. Load dataset
newsgroups = fetch_20newsgroups(subset='all', categories=categories, remove=('headers', 'footers', 'quotes'))

# 2. Vectorize
vectorizer = TfidfVectorizer(stop_words='english', max_df=0.5)
X = vectorizer.fit_transform(newsgroups.data)
y = newsgroups.target

# 3. Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42)

# 4. Train SVM
svm = SVC(kernel='linear')
svm.fit(X_train, y_train)

# 5. Evaluate
y_pred = svm.predict(X_test)
print("Accuracy:", accuracy_score(y_test, y_pred))
print("\nClassification Report:\n", classification_report(y_test, y_pred, target_names=newsgroups.target_names))

# 6. Predict on custom examples
example_texts = [
    "There is no scientific evidence for the existence of a god.",
    "Graphics design and 3D rendering are essential in video games.",
    "I have been taking antibiotics for my infection.",
    "Jesus Christ is central to Christianity and its teachings."
]

example_vectors = vectorizer.transform(example_texts)
predicted = svm.predict(example_vectors)

print("Classification on custom examples:")
for text, category in zip(example_texts, predicted):
    print(f"\nText: {text}\nPredicted Category: {newsgroups.target_names[category]}")
