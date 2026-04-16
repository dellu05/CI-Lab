def activation_function(yin, func_type, theta):
    if func_type == "binary":
        return 1 if yin > theta else 0
    elif func_type == "bipolar":
        if yin > theta: return 1
        elif yin < -theta: return -1
        else: return 0

def manual_gate_calc(inputs, gate):
    bins = [1 if x == 1 else 0 for x in inputs]
    if gate == "and":
        res = 1
        for x in bins:
            if x == 0: res = 0; break
    elif gate == "or":
        res = 0
        for x in bins:
            if x == 1: res = 1; break
    elif gate == "nand":
        res = 1
        for x in bins:
            if x == 0: res = 0; break
        res = 1 - res
    elif gate == "nor":
        res = 0
        for x in bins:
            if x == 1: res = 1; break
        res = 1 - res
    elif gate == "xor":
        res = 1 if sum(bins) % 2 != 0 else 0
    return res

def get_combinations(n, values):
    res = [[]]
    rev_values = values[::-1]
    for _ in range(n):
        res = [prev + [v] for prev in res for v in rev_values]
    return res

def perceptron():
    print("\n--- Perceptron Learning Model ---")
    print("1. Use Logic Gate (Auto-generate)")
    print("2. Use Custom Data (Manual input)")
    mode = input("Select mode (1/2): ")

    input_type = input("Data type (binary/bipolar): ").lower()
    n = int(input("Number of inputs (n): "))
    dataset = []

    if mode == "1":
        gate = input("Enter logic gate (AND/OR/NAND/NOR/XOR): ").lower()
        domain = [0, 1] if input_type == "binary" else [-1, 1]
        combinations = get_combinations(n, domain)
        for xs in combinations:
            out = manual_gate_calc(xs, gate)
            target = 1 if out == 1 else (-1 if input_type == "bipolar" else 0)
            dataset.append((xs, target))
    else:
        num_samples = int(input("How many samples/rows of data? "))
        for i in range(num_samples):
            print(f"Sample {i+1}:")
            xs = [float(input(f"  Input x{j+1}: ")) for j in range(n)]
            target = float(input(f"  Target value: "))
            dataset.append((xs, target))

    print("\n--- Enter Initial Parameters ---")
    weights = [float(input(f"Enter initial weight w{i+1}: ")) for i in range(n)]
    bias = float(input("Enter initial bias b: "))
    alpha = float(input("Learning rate (alpha): "))
    theta = float(input("Threshold (theta): "))
    max_epochs = int(input("Max epochs: "))

    for epoch in range(1, max_epochs + 1):
        x_headers = " ".join([f"x{i+1:<2}" for i in range(n)])
        dw_headers = " ".join([f"dw{i+1:<2}" for i in range(n)])
        w_headers = " ".join([f"w{i+1:<2}" for i in range(n)])

        print(f"\n{'='*105}")
        print(f" EPOCH: {epoch}")
        print(f"{'='*105}")
        print(f"{x_headers} | T  | Yin   | Y  | {dw_headers} | db   | {w_headers} | b")
        print("-" * 105)

        converged = True
        for xs, t in dataset:
            yin = sum(x * w for x, w in zip(xs, weights)) + bias
            y = activation_function(yin, input_type, theta)

            d_ws = [0.0] * n
            d_b = 0.0

            if y != t:
                converged = False
                d_b = alpha * t
                for i in range(n):
                    d_ws[i] = alpha * t * xs[i]
                    weights[i] += d_ws[i]
                bias += d_b

            x_vals = " ".join([f"{val:<3}" for val in xs])
            dw_vals = " ".join([f"{val:<4.1f}" for val in d_ws])
            w_vals = " ".join([f"{val:<4.1f}" for val in weights])

            print(f"{x_vals} | {t:<2.0f} | {yin:<5.1f} | {y:<2.0f} | {dw_vals} | {d_b:<4.1f} | {w_vals} | {bias:.1f}")

        if converged:
            print(f"\nCONVERGED! Final Weights: {weights}, Bias: {bias}")
            break
    else:
        print(f"\nReached {max_epochs} epochs without convergence.")

if __name__ == "__main__":
    perceptron()
