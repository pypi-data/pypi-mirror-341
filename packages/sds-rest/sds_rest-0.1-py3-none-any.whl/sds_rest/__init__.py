import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.tree import DecisionTreeClassifier, export_text
import matplotlib.pyplot as plt
from sklearn.tree import plot_tree
data = pd.read_csv("decision_tree.csv")
df = pd.DataFrame(data)
label_encoders = {}
for column in df.columns:
    if column != 'Price':
        le = LabelEncoder()
        df[column] = le.fit_transform(df[column])
        label_encoders[column] = le
X = df.drop('Wait', axis=1)
y = df['Wait']
clf = DecisionTreeClassifier(criterion='entropy', random_state=42)
clf.fit(X, y)
tree_rules = export_text(clf, feature_names=X.columns.tolist())
print("Decision Tree Rules:\n")
print(tree_rules)
plt.figure(figsize=(16, 8))
plot_tree(clf, feature_names=X.columns, class_names=label_encoders['Wait'].classes_, filled=True)
plt.title("Decision Tree")
plt.show()
test_input_raw = {
    'Alt': 'Yes',
    'Bar': 'No',
    'Fri': 'Yes',
    'Hun': 'Yes',
    'Pat': 'Full',
    'Price': 3000,
    'Rain': 'No',
    'Res': 'Yes',
    'Type': 'Thai',
    'Est': '30-60'
}

test_input_encoded = []
for feature in X.columns:
    value = test_input_raw[feature]
    if feature in label_encoders:
        value = label_encoders[feature].transform([value])[0]
    test_input_encoded.append(value)
test_df = pd.DataFrame([test_input_encoded], columns=X.columns)
prediction = clf.predict(test_df)[0]
wait_result = label_encoders['Wait'].inverse_transform([prediction])[0]
print("\nPrediction for test input:", wait_result)
