import csv
import math
from collections import Counter

filename = input("Enter CSV file name (with .csv): ")

try:
    with open(filename, "r") as f:
        csv_reader = csv.reader(f)
        dataset = list(csv_reader)
except FileNotFoundError:
    print("File not found!")
    exit()

header = dataset[0]
rows = dataset[1:]
class_col_index = len(header) - 1

# --- Entropy Function with Step Display ---
def find_entropy_with_steps(class_list, val_name):
    freq = Counter(class_list)
    total_count = sum(freq.values())
    if total_count == 0: return 0

    ent = 0
    terms = []
    for label, count in freq.items():
        prob = count / total_count
        term = prob * math.log2(prob)
        ent -= term
        terms.append("-({}/{} * log2({}/{}))".format(count, total_count, count, total_count))

    print(f"    > Entropy({val_name}): {' + '.join(terms)} = {round(ent, 4)}")
    return ent

# --- Function to calculate Information Gain for all features ---
def get_best_feature(current_rows, current_features):
    dataset_entropy = find_entropy_with_steps([r[class_col_index] for r in current_rows], "Current Subset")

    best_gain = -1
    best_feat_idx = -1

    for feat_idx in current_features:
        column_name = header[feat_idx]
        print(f"\n  Analyzing Feature: {column_name}")

        unique_vals = sorted(set(r[feat_idx] for r in current_rows))
        weighted_entropy = 0

        for val in unique_vals:
            subset = [r[class_col_index] for r in current_rows if r[feat_idx] == val]
            ent_subset = find_entropy_with_steps(subset, val)
            weighted_entropy += (len(subset) / len(current_rows)) * ent_subset

        gain = dataset_entropy - weighted_entropy
        print(f"  IG({column_name}) = {round(dataset_entropy,4)} - {round(weighted_entropy,4)} = {round(gain, 4)}")

        if gain > best_gain:
            best_gain = gain
            best_feat_idx = feat_idx

    return best_feat_idx

# --- Recursive Function to Build the Tree ---
def build_tree(current_rows, current_features, depth=0):
    classes = [r[class_col_index] for r in current_rows]

    # Stop Case 1: All instances have the same class
    if len(set(classes)) == 1:
        return classes[0]

    # Stop Case 2: No more features to split
    if not current_features:
        return Counter(classes).most_common(1)[0][0]

    print(f"\n{'='*20} DEPTH {depth}: CALCULATING BEST SPLIT {'='*20}")
    best_feat_idx = get_best_feature(current_rows, current_features)
    best_feat_name = header[best_feat_idx]

    print(f"\n>>> Best Feature for this node: {best_feat_name}")

    tree = {best_feat_name: {}}
    remaining_features = [f for f in current_features if f != best_feat_idx]

    feature_values = sorted(set(r[best_feat_idx] for r in current_rows))

    for val in feature_values:
        sub_rows = [r for r in current_rows if r[best_feat_idx] == val]
        print(f"\n--- Branching: {best_feat_name} == {val} ---")
        tree[best_feat_name][val] = build_tree(sub_rows, remaining_features, depth + 1)

    return tree

def print_tree(tree, indent=""):
    if not isinstance(tree, dict):
        print(" -> Result: " + tree)
        return

    for feature, branches in tree.items():
        print(f"\n{indent}[ {feature} ]")
        for val, subtree in branches.items():
            print(f"{indent}  |-- {val}", end="")
            print_tree(subtree, indent + "      ")

initial_features = list(range(len(header) - 1))
print("\n--- STARTING FULL TREE CONSTRUCTION ---")
final_tree = build_tree(rows, initial_features)

print("\n" + "="*50)
print("FINAL DECISION TREE STRUCTURE")
print("="*50)
print_tree(final_tree)
