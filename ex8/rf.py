import pandas as pd
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix

data = load_iris()
X = data.data
y = data.target

print("\nDataset: Iris Dataset (UCI Repository)")
print("Features:", data.feature_names)
print("Classes:", data.target_names)

n_trees = int(input("\nEnter number of Decision Trees: "))
crit = input("Enter criterion (gini or entropy): ").lower()

if crit not in ['gini', 'entropy']:
    print("Invalid criterion! Defaulting to 'gini'.")
    crit = 'gini'

splits = [(0.7, 0.3), (0.6, 0.4), (0.75, 0.25)]
results = []

for train_size, test_size in splits:
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=42
    )

    split_name = f"{int(train_size*100)}-{int(test_size*100)}"

    print(f"\n{'='*50}")
    print(f" ANALYSIS FOR SPLIT: {split_name} ")
    print(f"{'='*50}")
    print(f"Train Samples  : {len(X_train)}")
    print(f"Test Samples   : {len(X_test)}")

    model = RandomForestClassifier(n_estimators=n_trees, criterion=crit, random_state=42)
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)

    acc = accuracy_score(y_test, y_pred)
    prec = precision_score(y_test, y_pred, average='weighted')
    rec = recall_score(y_test, y_pred, average='weighted')
    f1 = f1_score(y_test, y_pred, average='weighted')

    results.append([split_name, acc, prec, rec, f1])

    print(f"\nConfusion Matrix for {split_name}:")
    cm = confusion_matrix(y_test, y_pred)
    cm_df = pd.DataFrame(cm,
                         index=[f"Actual {name}" for name in data.target_names],
                         columns=[f"Predicted {name}" for name in data.target_names])
    print(cm_df)

df = pd.DataFrame(results, columns=["Split", "Accuracy", "Precision", "Recall", "F1 Score"])

print(f"\n{'='*60}")
print(f" FINAL RESULTS TABLE (Criterion: {crit.upper()}) ")
print(f"{'='*60}")
print(df.to_string(index=False))

