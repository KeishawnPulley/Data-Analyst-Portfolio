# Personal Budget & Spending Analysis

Goal:
I wanted to see where money is actually going month to month, whether spending is trending in a good or bad direction, and how income compares to expenses over time.

Code:
synthetic_budget_data.py

Description:
Since I didn't want to use my real bank data, I wrote a Python script to generate a realistic fake dataset of 803 transactions spanning two years (2024-2026). I built in patterns you'd actually see in real life: fixed costs like rent and subscriptions that repeat every month, variable spending like groceries and dining out that happens more on weekends, a spending spike around the holidays, and biweekly paycheck income. Then I brought that into Power BI to build a dashboard summarizing income vs. expenses, spending by category, and overall trends.

Skills used:
Generating synthetic data with Python, building simple DAX formulas in Power BI (for example, a measure to calculate net savings as income minus expenses), designing KPI cards, and building category-based charts.

Tools:
Python (pandas, numpy), Power BI

What I found:
Over the two-year period, total income was $137.80K against $76.84K in expenses, leaving about $60.96K in net savings. Rent was by far the biggest expense at 45% of total spending, followed by groceries at 19% and dining out at about 7.5%. Having both a bar chart and a donut chart lets you see the ranked list and the overall proportions at the same time.

Dashboard includes:
- KPI cards showing total income, total expenses, and net savings
- Bar chart of spending by category, highest to lowest
- Donut chart showing each category's share of total spending

What I'd improve with more time:
I'd add a line chart showing income vs. expenses by month, so the seasonal spending spike I built into the data would actually be visible, and a category-by-month table to pinpoint exactly when certain categories spiked.
