print("--- Bayes Theorem ---")
pa = float(input("Enter P(A): "))
pbgna = float(input("Enter P(B|A): "))
pb = float(input("Enter P(B): "))

if pb == 0:
    print("Error: Division by zero is not possible.")
else:
    # Step 1: Logic
    p_a_given_b = (pbgna * pa) / pb

    print(f"\nStep 1: Calculate P(A|B)")
    print(f"Formula: P(A|B) = (P(B|A) * P(A)) / P(B)")
    print(f"Calculation: ({pbgna} * {pa}) / {pb}")
    print(f"Result: P(A|B) = {p_a_given_b:.4f}")
