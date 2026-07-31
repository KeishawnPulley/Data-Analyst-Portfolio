"""
Generates a realistic synthetic personal budget/spending dataset.
Simulates 2 years of transactions with realistic patterns:
- Recurring fixed costs (rent, subscriptions)
- Variable discretionary spending with seasonal/weekend patterns
- A few "spending spike" months to make trend analysis meaningful
- Slight month-over-month category drift so growth analysis has something real to find

pip install pandas numpy
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

np.random.seed(42)
random.seed(42)

START_DATE = datetime(2024, 1, 1)
END_DATE = datetime(2026, 1, 1)

# Category definitions: (category, avg_amount, std_dev, frequency_per_month, is_fixed)
CATEGORIES = {
    "Rent":            (1450, 0,    1,  True),
    "Utilities":       (140,  25,   1,  True),
    "Subscriptions":   (45,   5,    1,  True),
    "Groceries":       (65,   20,   8,  False),
    "Dining Out":      (35,   15,   10, False),
    "Transportation":  (40,   15,   6,  False),
    "Entertainment":   (30,   20,   4,  False),
    "Shopping":        (55,   40,   3,  False),
    "Health/Fitness":  (50,   30,   2,  False),
    "Travel":          (300,  200,  0.3,False),  # rare, occasional big spikes
}

# Months where discretionary spending spikes (e.g. holidays, birthday month)
SPIKE_MONTHS = {12: 1.6, 11: 1.2, 7: 1.15}  # Dec, Nov, July multipliers

def generate_transactions():
    rows = []
    txn_id = 1
    current = START_DATE

    while current < END_DATE:
        month = current.month
        spike_multiplier = SPIKE_MONTHS.get(month, 1.0)

        for category, (avg, std, freq_per_month, is_fixed) in CATEGORIES.items():
            if is_fixed:
                # One transaction per month, low variance
                amount = round(max(avg + np.random.normal(0, std), 0), 2)
                day = random.randint(1, 5)  # fixed costs early in month
                date = current.replace(day=day)
                rows.append([txn_id, date.strftime("%Y-%m-%d"), category, amount])
                txn_id += 1
            else:
                # Variable number of transactions this month
                num_txns = np.random.poisson(freq_per_month)
                for _ in range(num_txns):
                    base_amount = max(np.random.normal(avg, std), 5)
                    amount = round(base_amount * spike_multiplier, 2)
                    day = random.randint(1, 28)
                    date = current.replace(day=day)
                    # Weekend bias for dining/entertainment
                    if category in ("Dining Out", "Entertainment") and date.weekday() < 5:
                        if random.random() < 0.4:
                            continue  # skip some weekday discretionary txns
                    rows.append([txn_id, date.strftime("%Y-%m-%d"), category, amount])
                    txn_id += 1

        # move to next month
        if current.month == 12:
            current = current.replace(year=current.year + 1, month=1)
        else:
            current = current.replace(month=current.month + 1)

    df = pd.DataFrame(rows, columns=["transaction_id", "date", "category", "amount"])
    df["date"] = pd.to_datetime(df["date"])
    df = df.sort_values("date").reset_index(drop=True)
    return df

def add_income(df):
    """Add biweekly paycheck income as separate rows (category = Income, negative convention optional)."""
    income_rows = []
    txn_id = df["transaction_id"].max() + 1
    current = START_DATE
    paycheck = 2600  # biweekly take-home

    while current < END_DATE:
        income_rows.append([txn_id, current.strftime("%Y-%m-%d"), "Income", paycheck])
        txn_id += 1
        current += timedelta(days=14)

    income_df = pd.DataFrame(income_rows, columns=["transaction_id", "date", "category", "amount"])
    income_df["date"] = pd.to_datetime(income_df["date"])
    return pd.concat([df, income_df], ignore_index=True).sort_values("date").reset_index(drop=True)

if __name__ == "__main__":
    transactions = generate_transactions()
    full_data = add_income(transactions)

    # Add helper columns useful for dashboarding
    full_data["month"] = full_data["date"].dt.to_period("M").astype(str)
    full_data["day_of_week"] = full_data["date"].dt.day_name()
    full_data["type"] = full_data["category"].apply(lambda c: "Income" if c == "Income" else "Expense")

    output_path = "budget_transactions.csv"
    full_data.to_csv(output_path, index=False)

    print(f"Generated {len(full_data)} transactions from {START_DATE.date()} to {END_DATE.date()}")
    print(f"Saved to {output_path}")
    print("\nSample:")
    print(full_data.head(10))
    print("\nCategory summary:")
    print(full_data.groupby("category")["amount"].agg(["count", "sum", "mean"]).round(2))
