import os
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]
FILE_PATH = PROJECT_ROOT / "data" / "Ad_Spend_Budget_Performance_Analytics.xlsx"
OUTPUT_DIR = PROJECT_ROOT / "outputs"
OUTPUT_DIR.mkdir(exist_ok=True)

MONTH_PATTERN = r"^(Jan|Feb|Mar|Apr|May|Jun)-26$"
VALID_CATEGORIES = ["Headcount", "Media / Ad Spend", "Programs", "Tools & Licensing"]
VALID_CHANNELS = ["Search", "Social", "Display", "Video"]


def load_data():
    """Load only the monthly transaction-level records from the workbook."""
    budget_df = pd.read_excel(FILE_PATH, sheet_name="Budget vs Actual", header=3)
    budget_df = budget_df[
        budget_df["Cost Category"].isin(VALID_CATEGORIES)
        & budget_df["Month"].astype(str).str.match(MONTH_PATTERN)
    ].copy()

    ads_df = pd.read_excel(FILE_PATH, sheet_name="Ad Channel Performance", header=3)
    ads_df = ads_df[
        ads_df["Channel"].isin(VALID_CHANNELS)
        & ads_df["Month"].astype(str).str.match(MONTH_PATTERN)
    ].copy()
    return budget_df, ads_df


def analyze_budget(budget_df):
    budget_df["Variance ($000s)"] = budget_df["Actual ($000s)"] - budget_df["Budget ($000s)"]
    budget_df["Variance %"] = budget_df["Variance ($000s)"] / budget_df["Budget ($000s)"]
    budget_df["Review Flag"] = budget_df["Variance %"].abs().ge(0.10).map({True: "REVIEW", False: "OK"})

    category_summary = budget_df.groupby("Cost Category").agg(
        Total_Budget=("Budget ($000s)", "sum"),
        Total_Actual=("Actual ($000s)", "sum"),
    )
    category_summary["Variance"] = category_summary["Total_Actual"] - category_summary["Total_Budget"]
    category_summary["Variance %"] = category_summary["Variance"] / category_summary["Total_Budget"]
    return budget_df, category_summary


def analyze_ads(ads_df):
    channel_summary = ads_df.groupby("Channel").agg(
        Total_Spend=("Spend ($000s)", "sum"),
        Total_Revenue=("Revenue ($000s)", "sum"),
        Total_Conversions=("Conversions", "sum"),
        Avg_CTR=("CTR", "mean"),
        Avg_CPC=("CPC ($)", "mean"),
        Avg_CVR=("CVR", "mean"),
    )
    channel_summary["ROAS"] = channel_summary["Total_Revenue"] / channel_summary["Total_Spend"]
    channel_summary["CPA ($)"] = channel_summary["Total_Spend"] * 1000 / channel_summary["Total_Conversions"]
    return channel_summary


def create_visualizations(category_summary, channel_summary):
    category_summary[["Total_Budget", "Total_Actual"]].plot(kind="bar", figsize=(10, 6))
    plt.title("Budget vs Actual Spending by Cost Category")
    plt.xlabel("Cost Category")
    plt.ylabel("Amount ($000s)")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "budget_vs_actual.svg")
    plt.close()

    channel_summary[["Total_Spend", "Total_Revenue"]].plot(kind="bar", figsize=(10, 6))
    plt.title("Advertising Spend vs Revenue by Channel")
    plt.xlabel("Advertising Channel")
    plt.ylabel("Amount ($000s)")
    plt.xticks(rotation=0)
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "ad_spend_vs_revenue.svg")
    plt.close()

    channel_summary["ROAS"].sort_values(ascending=False).plot(kind="bar", figsize=(8, 5))
    plt.title("Return on Ad Spend (ROAS) by Channel")
    plt.xlabel("Advertising Channel")
    plt.ylabel("ROAS")
    plt.xticks(rotation=0)
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "channel_roas.svg")
    plt.close()


def main():
    if not FILE_PATH.exists():
        raise FileNotFoundError(f"Excel file not found: {FILE_PATH}")

    budget_df, ads_df = load_data()
    budget_df, category_summary = analyze_budget(budget_df)
    channel_summary = analyze_ads(ads_df)

    total_budget = budget_df["Budget ($000s)"].sum()
    total_actual = budget_df["Actual ($000s)"].sum()
    total_variance = total_actual - total_budget

    print(f"Total Budget: ${total_budget:,.0f}K")
    print(f"Total Actual Spend: ${total_actual:,.0f}K")
    print(f"Total Variance: ${total_variance:,.0f}K")
    print(f"Overall Variance %: {total_variance / total_budget:.2%}")
    print(f"Best Performing Channel: {channel_summary['ROAS'].idxmax()}")
    print(f"Best ROAS: {channel_summary['ROAS'].max():.2f}x")

    category_summary.to_csv(OUTPUT_DIR / "budget_summary.csv")
    channel_summary.to_csv(OUTPUT_DIR / "channel_performance_summary.csv")
    create_visualizations(category_summary, channel_summary)


if __name__ == "__main__":
    main()
