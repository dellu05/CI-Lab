import csv

print("--- Joint Probability (A, B, C) ---")
p = {}

# Take CSV file path from user
file_path = input("Enter CSV file path: ")

with open(file_path, 'r') as file:
    reader = csv.DictReader(file)
    for row in reader:
        a = int(row['A'])
        b = int(row['B'])
        c = int(row['C'])
        prob = float(row['P'])
        p[(a, b, c)] = prob

while True:
    print("\n--- Extended Menu ---")
    print("1. Find Joint Probability P(A,B,C)")
    print("2. Find Marginal Probability (e.g., P(A), P(B), or P(C))")
    print("3. Find Conditional Probability P(A | B,C)")
    print("4. Find Conditional Probability P(B | A,C)")
    print("5. Exit")

    choice = input("Enter choice (1-5): ")

    if choice == '1':
        ta, tb, tc = map(int, input("Enter values for A, B, C (e.g., 1 0 1): ").split())
        print(f"Result: P(A={ta}, B={tb}, C={tc}) = {p[(ta, tb, tc)]}")

    elif choice == '2':
        var = input("Which variable's marginal probability? (A/B/C): ").upper()
        val = int(input(f"Value for {var} (0 or 1): "))

        if var == 'A':
            components = [p[(val, b, c)] for b in [0, 1] for c in [0, 1]]
            res = sum(components)
            detail_str = " + ".join([str(v) for v in components])
            print(f"\nFormula: P(A={val}) = Summation P(A={val}, B, C)")
            print(f"Calculation: {detail_str}")
        elif var == 'B':
            components = [p[(a, val, c)] for a in [0, 1] for c in [0, 1]]
            res = sum(components)
            detail_str = " + ".join([str(v) for v in components])
            print(f"\nFormula: P(B={val}) = Summation P(A, B={val}, C)")
            print(f"Calculation: {detail_str}")
        else:
            components = [p[(a, b, val)] for a in [0, 1] for b in [0, 1]]
            res = sum(components)
            detail_str = " + ".join([str(v) for v in components])
            print(f"\nFormula: P(C={val}) = Summation P(A, B, C={val})")
            print(f"Calculation: {detail_str}")

        print(f"Result: Marginal P({var}={val}) = {res:.4f}")

    elif choice == '3':
        ta, tb, tc = map(int, input("Enter target A, B, C (e.g., 1 1 0): ").split())
        p_abc = p[(ta, tb, tc)]
        v1, v2 = p[(0, tb, tc)], p[(1, tb, tc)]
        p_bc = v1 + v2

        print(f"\nFormula: P(A|B,C) = P(A,B,C) / P(B,C)")
        print(f"Step 1: Numerator P(A={ta}, B={tb}, C={tc}) = {p_abc}")
        print(f"Step 2: Denominator P(B={tb}, C={tc}) = {v1} + {v2} = {p_bc}")
        print(f"Step 3: {p_abc} / {p_bc}")
        print(f"Result: P(A={ta}|B={tb},C={tc}) = {p_abc/p_bc if p_bc > 0 else 0:.4f}")

    elif choice == '4':
        ta, tb, tc = map(int, input("Enter values for A, B, C (e.g., 0 1 1): ").split())
        p_abc = p[(ta, tb, tc)]
        v1, v2 = p[(ta, 0, tc)], p[(ta, 1, tc)]
        p_ac = v1 + v2

        print(f"\nFormula: P(B|A,C) = P(A,B,C) / P(A,C)")
        print(f"Step 1: Numerator P(A={ta}, B={tb}, C={tc}) = {p_abc}")
        print(f"Step 2: Denominator P(A={ta}, C={tc}) = {v1} + {v2} = {p_ac}")
        print(f"Step 3: {p_abc} / {p_ac}")
        print(f"Result: P(B={tb}|A={ta},C={tc}) = {p_abc/p_ac if p_ac > 0 else 0:.4f}")

    elif choice == '5':
        print("Bye!")
        break
    else:
        print("Invalid Choice!")
