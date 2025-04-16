#initiator

#implement rank algorithm ranksvm
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score

def train_ranksvm(X_train, y_train):
    """
    Train RankSVM model using training data.

    :param X_train: Features of training data.
    :param y_train: Labels of training data.
    :return: Trained RankSVM model.
    """
    # Initialize and train SVM model
    svm = SVC(kernel='linear')
    svm.fit(X_train, y_train)
    return svm


def predict_ranksvm(model, X_test):
    """
    Predict rankings using trained RankSVM model.

    :param model: Trained RankSVM model.
    :param X_test: Features of test data.
    :return: Predicted rankings.
    """
    # Predict rankings using trained model
    rankings = model.decision_function(X_test)
    return rankings

# Example usage
if __name__ == "__main__":
    # Generate synthetic dataset
    X, y = make_classification(n_samples=100, n_features=20, n_classes=2, random_state=42)

    # Split dataset into train and test sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Standardize features
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    # Train RankSVM model
    ranksvm_model = train_ranksvm(X_train_scaled, y_train)

    # Predict rankings
    rankings = predict_ranksvm(ranksvm_model, X_test_scaled)

    # Evaluate the model
    y_pred = (rankings > 0).astype(int)  # Convert rankings to binary predictions
    accuracy = accuracy_score(y_test, y_pred)
    print("Approximate Ranking Accuracy", accuracy)



    

