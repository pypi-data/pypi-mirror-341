from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.utils import to_categorical
from tqdm import tqdm
import numpy as np
import warnings

model = None
X_train = None
X_test = None
y_train = None
y_test = None
accuracy = None


def train(model_type="auto"):
    global model, X_train, X_test, y_train, y_test, accuracy
    from emon.core.cleaner import X, y

    if X is None or y is None:
        raise RuntimeError("[emon.train] Please run emon.clean() first.")

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    if model_type == "auto":
        model_type = "keras" if len(np.unique(y)) > 2 else "rf"

    print(f"\n[emon.train] Training model: {model_type}")

    if model_type == "rf":
        model = RandomForestClassifier(n_estimators=100, random_state=42)
        model.fit(X_train, y_train)
    elif model_type == "lr":
        model = LogisticRegression(max_iter=1000)
        model.fit(X_train, y_train)
    elif model_type == "keras":
        model = Sequential([
            Dense(64, activation='relu', input_shape=(X_train.shape[1],)),
            Dense(64, activation='relu'),
            Dense(len(np.unique(y_train)), activation='softmax')
        ])
        model.compile(optimizer=Adam(), loss='sparse_categorical_crossentropy', metrics=['accuracy'])
        for _ in tqdm(range(1), desc="Training Keras model"):
            model.fit(X_train, y_train, epochs=10, verbose=0)
    else:
        raise ValueError("[emon.train] Unsupported model type. Choose 'auto', 'rf', 'lr', or 'keras'.")

    y_pred = model.predict(X_test)
    if model_type == "keras":
        y_pred = np.argmax(y_pred, axis=1)

    accuracy = accuracy_score(y_test, y_pred)
    print("\n[emon.train] Model trained.")
    print(f"Accuracy: {accuracy:.2f}\n")
    print(classification_report(y_test, y_pred))


def get_accuracy():
    global accuracy
    return accuracy


def evaluate():
    from sklearn.metrics import confusion_matrix
    y_pred = model.predict(X_test)
    if hasattr(y_pred, 'argmax'):
        y_pred = y_pred.argmax(axis=1)
    cm = confusion_matrix(y_test, y_pred)
    print("Confusion Matrix:\n", cm)