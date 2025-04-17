def addition(numbers: list) -> float:
    return sum(numbers)
def show_code():
    code = '''
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score, classification_report
from sklearn.model_selection import train_test_split

X = ["I love this movie", "This movie is terrible", "Great movie, highly recommended",
     "Waste of time, not worth watching", "Amazing performance by the actors"]

y = ["Positive", "Negative", "Positive", "Negative", "Positive"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

X_train_tfidf = TfidfVectorizer().fit_transform(X_train)
X_test_tfidf = TfidfVectorizer().fit(X_train).transform(X_test)

y_pred = SVC(kernel='linear').fit(X_train_tfidf, y_train).predict(X_test_tfidf)

accuracy = accuracy_score(y_test, y_pred)
print("Accuracy:", accuracy)

print("Classification Report:")
print(classification_report(y_test, y_pred, zero_division=0))

    '''
    print(code)