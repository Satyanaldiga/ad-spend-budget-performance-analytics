import os
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


# --------------------------------------------------
# CONFIGURATION
# --------------------------------------------------
PROJECT_ROOT = Path(__file__).resolve().parents[1]
FILE_PATH = PROJECT_ROOT / "data" / "Ad_Spend_Budget_Performance_Analytics.xlsx"
OUTPUT_DIR = PROJECT_ROOT / "outputs"
OUTPUT_DIR.mkdir(exist_ok=True)


# --------------------------------------------------
# LOAD DATA
# --------------------------------------------------
def load_data():
    """Load budget and advertising datasets from the Excel workbook."""

    budget_df = pd.read_excel(
        FILE_PATH,
        sheet_name="Budget vs Actual",
        header=3,
    )

    valid_categories = [
        "Headcount",
        "Media / Ad Spend",
        "Programs",
        "Tools & Licensing",
    ]

    budget_df = budget_df[
        budget_df["Cost Category"].isin(valid_categories)
    ].copy()

    ads_df = pd.read_excel(
        FILE_PATH,
        sheet_name="Ad Channel Performance",
        header=3,
    )

    valid_channels = ["Search", "Social", "Display", "Video"]

    ads_df = ads_df[
        ads_df["Channel"].isin(valid_channels)
    ].copy()

    return budget_df, ads_df


# --------------------------------------------------
# BUDGET ANALYSIS
# --------------------------------------------------
def analyze_budget(budget_df):
    """Calculate budget variances and summarize results by cost category."""

    budget_df["Variance ($000s)"] = (
        budget_df["Actual ($000s)"]
        - budget_df["Budget ($000s)"]
    )

    budget_df["Variance %"] = (
        budget_df["Variance ($000s)"]
        / budget_df["Budget ($000s)"]
    )

    budget_df["Review Flag"] = budget_df["Variance %"].apply(
        lambda value: "REVIEW" if abs(value) >= 0.10 else "OK"
    )

    total_budget = budget_df["Budget ($000s)"].sum()
    total_actual = budget_df["Actual ($000s)"].sum()
    total_variance = total_actual - total_budget
    total_variance_pct = total_variance / total_budget

    category_summary = (
        budget_df.groupby("Cost Category")
        .agg(
            Total_Budget=("Budget ($000s)", "sum"),
            Total_Actual=("Actual ($000s)", "sum"),
        )
    )

    category_summary["Variance"] = (
        category_summary["Total_Actual"]
        - category_summary["Total_Budget"]
    )

    category_summary["Variance %"] = (
        category_summary["Variance"]
        / category_summary["Total_Budget"]
    )

    summary = {
        "total_budget": total_budget,
        "total_actual": total_actual,
        "total_variance": total_variance,
        "total_variance_pct": total_variance_pct,
    }

    return budget_df, category_summary, summary


# --------------------------------------------------
# ADVERTISING PERFORMANCE ANALYSIS
# --------------------------------------------------
def analyze_ads(ads_df):
    """Aggregate advertising performance and calculate ROAS and CPA."""

    channel_summary = (
        ads_df.groupby("Channel")
        .agg(
            Total_Spend=("Spend ($000s)", "sum"),
            Total_Revenue=("Revenue ($000s)", "sum"),
            Total_Conversions=("Conversions", "sum"),
            Avg_CTR=("CTR", "mean"),
            Avg_CPC=("CPC ($)", "mean"),
            Avg_CVR=("CVR", "mean"),
        )
    )

    channel_summary["ROAS"] = (
        channel_summary["Total_Revenue"]
        / channel_summary["Total_Spend"]
    )

    channel_summary["CPA ($)"] = (
        channel_summary["Total_Spend"] * 1000
        / channel_summary["Total_Conversions"]
    )

    best_channel = channel_summary["ROAS"].idxmax()
    best_roas = channel_summary.loc[best_channel, "ROAS"]

    return channel_summary, best_channel, best_roas


# --------------------------------------------------
# VISUALIZATIONS
# --------------------------------------------------
def create_visualizations(category_summary, channel_summary):
    """Create charts for budget and advertising performance."""

    category_summary[["Total_Budget", "Total_Actual"]].plot(
        kind="bar",
        figsize=(10, 6),
    )
    plt.title("Budget vs Actual Spending by Cost Category")
    plt.xlabel("Cost Category")
    plt.ylabel("Amount ($000s)")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "budget_vs_actual.png")
    plt.close()

    channel_summary[["Total_Spend", "Total_Revenue"]].plot(
        kind="bar",
        figsize=(10, 6),
    )
    plt.title("Advertising Spend vs Revenue by Channel")
    plt.xlabel("Advertising Channel")
    plt.ylabel("Amount ($000s)")
    plt.xticks(rotation=0)
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "ad_spend_vs_revenue.png")
    plt.close()

    channel_summary["ROAS"].sort_values(ascending=False).plot(
        kind="bar",
        figsize=(8, 5),
    )
    plt.title("Return on Ad Spend (ROAS) by Channel")
    plt.xlabel("Advertising Channel")
    plt.ylabel("ROAS")
    plt.xticks(rotation=0)
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "channel_roas.png")
    plt.close()


# --------------------------------------------------
# MAIN WORKFLOW
# --------------------------------------------------
def main():
    if not FILE_PATH.exists():
        raise FileNotFoundError(
            f"Excel file not found: {FILE_PATH}\n"
            "Add the workbook to the data directory before running the analysis."
        )

    budget_df, ads_df = load_data()

    budget_df, category_summary, budget_summary = analyze_budget(budget_df)
    channel_summary, best_channel, best_roas = analyze_ads(ads_df)

    significant_variances = budget_df[
        abs(budget_df["Variance %"]) >= 0.10
    ]

    print("=" * 55)
    print("BUDGET PERFORMANCE SUMMARY")
    print("=" * 55)
    print(f"Total Budget: ${budget_summary['total_budget']:,.0f}K")
    print(f"Total Actual Spend: ${budget_summary['total_actual']:,.0f}K")
    print(f"Total Variance: ${budget_summary['total_variance']:,.0f}K")
    print(
        "Overall Variance %: "
        f"{budget_summary['total_variance_pct']:.2%}"
    )

    print("\nSIGNIFICANT VARIANCES")
    print("=" * 55)
    print(
        significant_variances[
            [
                "Cost Category",
                "Month",
                "Budget ($000s)",
                "Actual ($000s)",
                "Variance %",
            ]
        ].to_string(index=False)
    )

    print("\nADVERTISING CHANNEL PERFORMANCE")
    print("=" * 55)
    print(channel_summary.round(3))

    print("\nBEST PERFORMING CHANNEL")
    print("=" * 55)
    print(f"Channel: {best_channel}")
    print(f"ROAS: {best_roas:.2f}x")

    category_summary.to_csv(OUTPUT_DIR / "budget_summary.csv")
    channel_summary.to_csv(
        OUTPUT_DIR / "channel_performance_summary.csv"
    )

    create_visualizations(category_summary, channel_summary)

    print("\nAnalysis completed successfully.")
    print(f"Results saved to: {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
