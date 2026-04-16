import csv
import math
from collections import Counter

# -------------------------------
# Read CSV (Handles N features)
# -------------------------------
def read_csv(filename):
    data = []
    with open(filename, "r") as file:
        reader = csv.reader(file)
        next(reader)
        for row in reader:

            features = [float(x) for x in row[:-1]]
            label = row[-1]
            data.append(features + [label])
    return data

# -------------------------------
# Normalization (Min-Max)
# -------------------------------
def normalization(dataset):
    num_features = len(dataset[0]) - 1
    bounds = []

    # Logic for Z-Score Normalization (Standardization):
    # mean = sum(values) / len(values)
    # std_dev = math.sqrt(sum((x - mean)**2) / len(values))
    # norm_val = (val - mean) / std_dev

    for i in range(num_features):
        col_values = [row[i] for row in dataset]
        bounds.append((min(col_values), max(col_values)))

    norm_ds = []
    for row in dataset:
        n_row = []
        for i in range(num_features):
            mi, ma = bounds[i]
            n_val = (row[i] - mi) / (ma - mi) if ma != mi else 0
            n_row.append(n_val)
        norm_ds.append(n_row + [row[-1]])

    return norm_ds, bounds

# -------------------------------
# Generic Distance Metric (Minkowski)
# -------------------------------
def distance_metric(point1, point2, r):
    # Works for N dimensions via zip
    sum_diff = sum(abs(p1 - p2)**r for p1, p2 in zip(point1, point2))
    return sum_diff**(1/r)

# -------------------------------
# Process Table
# -------------------------------
def process_table(dataset, norm_ds, u_point, r_val, bounds):

    n_u_point = []
    for i in range(len(u_point)):
        mi, ma = bounds[i]
        n_u_point.append((u_point[i] - mi) / (ma - mi) if ma != mi else 0)

    full_table = []
    for i in range(len(dataset)):
        orig_features = dataset[i][:-1]
        norm_features = norm_ds[i][:-1]
        label = dataset[i][-1]

        dist = distance_metric(norm_features, n_u_point, r_val)
        full_table.append([orig_features, norm_features, dist, label])

    full_table.sort(key=lambda x: x[2])
    for idx, row in enumerate(full_table):
        row.insert(3, idx + 1)
    return full_table

# -------------------------------
# Display Functions
# -------------------------------
def print_intermediate(table):
    print("\nINTERMEDIATE TABLE (All Data)")
    print("-" * 100)
    print(f"{'Original Features':<25} {'Norm Features':<25} {'Dist':<10} {'Rank':<6} {'Class'}")  #:<for space after
    print("-" * 100)
    for r in table:
        orig_str = str([round(x, 2) for x in r[0]])
        norm_str = str([round(x, 2) for x in r[1]])
        print(f"{orig_str:<25} {norm_str:<25} {round(r[2],4):<10} {r[3]:<6} {r[4]}")

def print_final(table, k, knn_type):
    print(f"\nFINAL TABLE (K={k} Neighbors)")
    print("-" * 100)
    neighbors = table[:k]
    for r in neighbors:
        orig_str = str([round(x, 2) for x in r[0]])
        norm_str = str([round(x, 2) for x in r[1]])
        print(f"{orig_str:<25} {norm_str:<25} {round(r[2],4):<10} {r[3]:<6} {r[4]}")

    if knn_type == 1:
        classes = [r[4] for r in neighbors]
        return Counter(classes).most_common(1)[0][0]
    else:
        weights = {}
        for r in neighbors:
            label, d = r[4], r[2]
            w = 1 / (d + 0.0001) # Epsilon added to prevent division by zero
            weights[label] = weights.get(label, 0) + w
        return max(weights, key=weights.get)

# -------------------------------
# Main Program
# -------------------------------
filename = input("Enter CSV file name: ")
orig_dataset = read_csv(filename)
norm_dataset, bounds = normalization(orig_dataset)

num_features = len(orig_dataset[0]) - 1
print(f"Detected {num_features} dimensions.")
u_point = []
for i in range(num_features):
    u_point.append(float(input(f"Enter value for Dimension {i+1}: ")))

r_val = float(input("Enter distance metric r (1: Manhattan, 2: Euclidean): "))

table = process_table(orig_dataset, norm_dataset, u_point, r_val, bounds)
print_intermediate(table)

while True:
    k_input = input("\nEnter value of K (or 'q' to quit): ")
    if k_input.lower() == 'q': break
    k = int(k_input)

    print("KNN Type: 1. Unweighted  2. Weighted")
    knn_type = int(input("Choice: "))

    result = print_final(table, k, knn_type)
    print(f"\nResult: Point {u_point} classified as: {result}")
