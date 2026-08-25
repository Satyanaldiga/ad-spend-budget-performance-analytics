# Ad Spend & Budget Performance Analytics

## Project Overview

This project analyzes budget performance and digital advertising efficiency using Microsoft Excel and Python. The analysis compares planned budgets with actual spending and evaluates advertising channels using key marketing metrics such as CTR, CPC, CVR, and ROAS.

The goal is to demonstrate an end-to-end analytics workflow relevant to FP&A, business analytics, and marketing analytics.

## What Was Done

### 1. Budget vs. Actual Variance Analysis

The project compares budgeted spending with actual spending across categories including:

- Headcount
- Media / Ad Spend
- Programs
- Tools & Licensing

Key calculations include:

- **Variance ($)** = Actual Spend - Budgeted Spend
- **Variance (%)** = (Actual Spend - Budgeted Spend) / Budgeted Spend

A variance threshold is used to identify spending areas that may require management review.

### 2. Advertising Channel Performance Analysis

Advertising channels are evaluated using:

- Click-Through Rate (CTR)
- Cost Per Click (CPC)
- Conversion Rate (CVR)
- Return on Ad Spend (ROAS)
- Cost Per Acquisition (CPA)

**ROAS = Revenue / Advertising Spend**

These metrics help determine which channels generate stronger returns relative to the money invested.

### 3. Excel Dashboard

The Excel workbook provides a management-level view of:

- Budget versus actual spending
- Spending variances
- Categories requiring attention
- Advertising spend and revenue
- Channel performance

### 4. Python Analysis

Python is used to reproduce and extend the Excel analysis. The script:

1. Loads the Excel datasets with pandas.
2. Calculates budget variances.
3. Flags significant deviations.
4. Aggregates advertising performance by channel.
5. Calculates ROAS and CPA.
6. Identifies the strongest channel by ROAS.
7. Generates charts and CSV summaries.

## Why This Analysis Matters

Organizations need to understand both whether they are spending according to plan and whether their investments are producing results. This project connects financial variance analysis with marketing performance analysis to support questions such as:

- Where is spending above or below budget?
- Which cost categories need additional review?
- Which advertising channels generate stronger returns?
- Where could future budgets potentially be reallocated?

The resulting analysis supports more data-driven financial planning and marketing investment decisions.

## Tools and Technologies

- Microsoft Excel
- Python
- pandas
- matplotlib
- openpyxl

## Project Structure

```text
ad-spend-budget-performance-analytics/
├── data/
│   └── Ad_Spend_Budget_Performance_Analytics.xlsx
├── analysis/
│   └── ad_spend_analysis.py
├── outputs/
│   └── .gitkeep
├── README.md
├── requirements.txt
└── .gitignore
```

## How to Run the Python Analysis

### 1. Clone the repository

```bash
git clone https://github.com/Satyanaldiga/ad-spend-budget-performance-analytics.git
cd ad-spend-budget-performance-analytics
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Add the Excel workbook

Place the workbook in the `data/` directory with this exact name:

`Ad_Spend_Budget_Performance_Analytics.xlsx`

### 4. Run the analysis

```bash
python analysis/ad_spend_analysis.py
```

The script will generate charts and summary CSV files inside the `outputs/` directory.

## Skills Demonstrated

- Financial Analysis
- FP&A
- Budgeting
- Variance Analysis
- Marketing Analytics
- KPI Analysis
- Data Cleaning
- Data Aggregation
- Python
- pandas
- Data Visualization
- Excel Dashboard Development

## Conclusion

This project demonstrates how Excel and Python can be combined in an end-to-end analytics workflow. Budget variance analysis helps identify deviations from financial plans, while advertising metrics help evaluate the efficiency and return of marketing investments.

The project is designed as a practical portfolio example for FP&A, Business Analyst, Data Analyst, and Marketing Analyst roles.
