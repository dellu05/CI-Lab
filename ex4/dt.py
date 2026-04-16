import csv
import math
from collections import Counter

# --------- Get File Name From User ---------
filename = input("Enter CSV file name (with .csv): ")

with open(filename, "r") as f:
    csv_reader = csv.reader(f)
    dataset = list(csv_reader)

# --- Calculate Maximum Width for Each Column ---
col_widths = []

for col in zip(*dataset):   # transpose rows -> columns
    max_len = max(len(str(value)) for value in col)
    col_widths.append(max_len)

# --- Print Dataset with Proper Alignment ---
print("\n--- CSV FILE DATA ---")

for row in dataset:
    for i, value in enumerate(row):
        print(f"{value:<{col_widths[i]}}", end=" | ")
    print()

print("----------------------\n")

header = dataset[0]
rows = dataset[1:]
class_col = len(header) - 1

# --------- Entropy Function with Step Display ---------
def find_entropy_with_steps(class_list, val_name):
    freq = Counter(class_list)
    total_count = sum(freq.values())
    if total_count == 0: return 0

    ent = 0
    # Replaced Sigma symbol with "Sum" to avoid UnicodeEncodeError
    steps_str = "    Formula: -Summation(p * log2(p))\n    Calculation: "
    terms = []

    for label, count in freq.items():
        prob = count / total_count
        # Using math.log2() for entropy
        term = prob * math.log2(prob)
        ent -= term
        terms.append("-({}/{} * log2({}/{}))".format(count, total_count, count, total_count))

    print("\n  > Entropy({}):".format(val_name))
    print("{} {}".format(steps_str, " + ".join(terms)))
    print("    Result: {}".format(round(ent, 4)))
    return ent

# --------- Total Dataset Entropy ---------
class_values = [r[class_col] for r in rows]
dataset_entropy = find_entropy_with_steps(class_values, "Entire Dataset")
classes = sorted(set(class_values))

# --------- Main Processing ---------
info_gain_dict = {}

for col in range(len(header) - 1):
    column_name = header[col]
    unique_vals = sorted(set(r[col] for r in rows))

    print("\n" + "="*60)
    print("ANALYZING FEATURE: {}".format(column_name))
    print("="*60)

    # --- STEP 1: Frequency Table ---
    print("Step 1: Frequency Table")
    print("{:<15}".format("Value"), end="")
    for c in classes:
        print(" | {:<8}".format(c), end="")
    print("\n" + "-" * (25 + len(classes)*11))

    subset_info = []
    weighted_entropy_parts = []
    column_totals = {c: 0 for c in classes}

    for val in unique_vals:
        filtered_rows = [r for r in rows if r[col] == val]
        filtered_classes = [r[class_col] for r in filtered_rows]

        counts = Counter(filtered_classes)
        print("{:<15}".format(val), end="")
        for c in classes:
            count_val = counts[c]
            print(" | {:<8}".format(count_val), end="")
            column_totals[c] += count_val
        print()
        subset_info.append((val, filtered_classes))

    print("{:<15}".format("Total"), end="")
    for c in classes:
        print(" | {:<8}".format(column_totals[c]), end="")
    print("\n")

    # --- STEP 2: Entropy Calculation ---
    print("Step 2: Entropy Calculation for each subset")
    total_weighted_entropy = 0
    for val, f_classes in subset_info:
        ent_subset = find_entropy_with_steps(f_classes, val)
        weight = len(f_classes) / len(rows)
        weighted_val = weight * ent_subset
        total_weighted_entropy += weighted_val
        weighted_entropy_parts.append("({}/{} * {})".format(len(f_classes), len(rows), round(ent_subset,4)))

    # --- STEP 3: Information Gain ---
    print("\nStep 3: Information Gain (IG)")
    print("  Weighted Entropy = {}".format(" + ".join(weighted_entropy_parts)))
    print("  Total Weighted Entropy = {}".format(round(total_weighted_entropy, 4)))

    gain = dataset_entropy - total_weighted_entropy
    info_gain_dict[column_name] = gain
    print("  IG = Total Entropy - Weighted Entropy")
    print("  IG = {} - {} = {}".format(round(dataset_entropy, 4), round(total_weighted_entropy, 4), round(gain, 4)))

# --- STEP 4: Final Result ---
print("\n" + "="*60)
print("Step 4: Final Result & Root Node Selection")
print("="*60)
for feat, val in info_gain_dict.items():
    print("{:<15} : IG = {}".format(feat, round(val, 4)))

best_feature = max(info_gain_dict, key=info_gain_dict.get)
print("\n>>> Best Feature (Root Node): {}".format(best_feature))
