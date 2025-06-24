import numpy as np

def calculate_std(prices):

    prices = np.array(prices, dtype=float)
    mean = prices.mean()
    std = prices.std(ddof=1)
    rails = {
        "mean": mean,
        "std": std,
        "+1σ": mean + std,
        "-1σ": mean - std,
        "+2σ": mean + 2 * std,
        "-2σ": mean - 2 * std,
        "+3σ": mean + 3 * std,
        "-3σ": mean - 3 * std
    }
    return rails

# Example usage:
closes = [1.15211, 1.14935, 1.14791, 1.14793, 1.15593,
          1.15510, 1.15804, 1.14873, 1.14202, 1.14175]

rails = calculate_std(closes)
for label, value in rails.items():
    print(f"{label}: {value:.8f}")
