import csv
import math
from collections import Counter

# -------------------------------
# Read CSV
# -------------------------------
def read_csv(filename):
    data = []
    with open(filename, "r") as file:
        reader = csv.reader(file)
        next(reader)
        for row in reader:
            data.append([float(row[0]), float(row[1]), row[2]])
    return data

# -------------------------------
# Normalization (Min-Max)
# -------------------------------
def normalization(dataset):
    x_coords = [row[0] for row in dataset]
    y_coords = [row[1] for row in dataset]

    min_x, max_x = min(x_coords), max(x_coords)
    min_y, max_y = min(y_coords), max(y_coords)

    # Logic for Z-Score Normalization (Standardization):
    # mean_x = sum(x_coords) / len(x_coords)
    # std_x = math.sqrt(sum((xi - mean_x)**2 for xi in x_coords) / len(x_coords))
    # normalized_x = (x - mean_x) / std_x

    norm_ds = []
    for row in dataset:
        nx = (row[0] - min_x) / (max_x - min_x) if max_x != min_x else 0
        ny = (row[1] - min_y) / (max_y - min_y) if max_y != min_y else 0
        norm_ds.append([nx, ny, row[2]])

    return norm_ds, (min_x, max_x, min_y, max_y)

# -------------------------------
# Generic Distance Metric (Minkowski)
# -------------------------------
def distance_metric(x1, y1, x2, y2, r):
    # Generic Minkowski formula: (sum(|xi - yi|^r))^(1/r)
    # r=1 is Manhattan, r=2 is Euclidean
    return (abs(x1 - x2)**r + abs(y1 - y2)**r)**(1/r)

# -------------------------------
# Core Logic
# -------------------------------
def process_table(dataset, norm_ds, ux, uy, r_val, bounds):
    min_x, max_x, min_y, max_y = bounds
    n_ux = (ux - min_x) / (max_x - min_x) if max_x != min_x else 0
    n_uy = (uy - min_y) / (max_y - min_y) if max_y != min_y else 0

    full_table = []
    for i in range(len(dataset)):
        orig = dataset[i]
        norm = norm_ds[i]
        dist = distance_metric(norm[0], norm[1], n_ux, n_uy, r_val)
        # Table structure: [Orig X, Orig Y, Norm X, Norm Y, Distance, Class]
        full_table.append([orig[0], orig[1], norm[0], norm[1], dist, orig[2]])

    full_table.sort(key=lambda x: x[4])
    for idx, row in enumerate(full_table):
        row.insert(5, idx + 1) # Insert Rank
    return full_table

# -------------------------------
# Printing Functions
# -------------------------------
def print_intermediate(table):
    print("\nINTERMEDIATE TABLE")
    print("-" * 80)
    print(f"{'X':<6} {'Y':<6} {'NX':<8} {'NY':<8} {'Dist':<10} {'Rank':<6} {'Class'}")
    print("-" * 80)
    for r in table:
        print(f"{r[0]:<6} {r[1]:<6} {round(r[2],3):<8} {round(r[3],3):<8} "
              f"{round(r[4],4):<10} {r[5]:<6} {r[6]}")

def print_final(table, k, knn_type):
    print(f"\nFINAL TABLE (K={k} Neighbors)")
    print("-" * 80)
    print(f"{'X':<6} {'Y':<6} {'NX':<8} {'NY':<8} {'Dist':<10} {'Rank':<6} {'Class'}")
    print("-" * 80)

    neighbors = table[:k]
    for r in neighbors:
        print(f"{r[0]:<6} {r[1]:<6} {round(r[2],3):<8} {round(r[3],3):<8} "
              f"{round(r[4],4):<10} {r[5]:<6} {r[6]}")

    if knn_type == 1:
        classes = [r[6] for r in neighbors]
        return Counter(classes).most_common(1)[0][0]
    else:
        weights = {}
        for r in neighbors:
            label, d = r[6], r[4]
            w = 1 / (d + 0.0001)
            weights[label] = weights.get(label, 0) + w
        return max(weights, key=weights.get)

# -------------------------------
# Main Program
# -------------------------------
filename = input("Enter CSV file name: ")
orig_dataset = read_csv(filename)
norm_dataset, bounds = normalization(orig_dataset)

ux = float(input("Enter X value of unknown data: "))
uy = float(input("Enter Y value of unknown data: "))
r_val = float(input("Enter distance metric r (1: Manhattan, 2: Euclidean): "))

table = process_table(orig_dataset, norm_dataset, ux, uy, r_val, bounds)
print_intermediate(table)

while True:
    k_input = input("\nEnter value of K (or 'q' to quit): ")
    if k_input.lower() == 'q': break
    k = int(k_input)

    print("KNN Type: 1. Unweighted  2. Weighted")
    knn_type = int(input("Choice: "))

    result = print_final(table, k, knn_type)
    print(f"\nResult: Point ({ux}, {uy}) classified as: {result}")
