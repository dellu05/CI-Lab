def dice_probability():
    print("--- Dice Probability ---")
    t = int(input("Enter target sum (2-12): "))
    total_outcomes = 36
    favorable = []

    # Simple nested loop for 2 dice
    for i in range(1, 7):
        for j in range(1, 7):
            if i + j == t:
                favorable.append((i, j))

    p = len(favorable) / total_outcomes

    print(f"\nStep 1: Identify Favorable Outcomes")
    print(f"Outcomes: {favorable}")
    print(f"Count (n): {len(favorable)}")

    print(f"\nStep 2: Calculate Probability")
    print(f"Formula: P = Favorable Outcomes / Total Outcomes (36)")
    print(f"Calculation: {len(favorable)} / {total_outcomes}")
    print(f"Result: Probability = {p:.4f}")

dice_probability()
