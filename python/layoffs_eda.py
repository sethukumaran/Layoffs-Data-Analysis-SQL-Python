"""
Layoffs Dataset — End-to-End Exploratory Data Analysis
"""

from pathlib import Path
import warnings
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

warnings.filterwarnings("ignore")
sns.set_theme(style="whitegrid")

DATA_PATH = Path("layoffs.csv")
FIG_DIR = Path("figures")
FIG_DIR.mkdir(exist_ok=True)

# 1. Load and standardize
df = pd.read_csv(DATA_PATH)
df["date"] = pd.to_datetime(df["date"], errors="coerce")
df["date_added"] = pd.to_datetime(df["date_added"], errors="coerce")

for col in ["total_laid_off", "percentage_laid_off", "funds_raised"]:
    df[col] = pd.to_numeric(df[col], errors="coerce")

known = df.dropna(subset=["total_laid_off"]).copy()

# 2. Basic EDA
print("="*80)
print("DATASET OVERVIEW")
print("="*80)
print("Shape:", df.shape)
print("\nColumns:", df.columns.tolist())
print("\nData types:\n", df.dtypes)
print("\nMissing values:\n",
      pd.DataFrame({"count": df.isna().sum(),
                    "pct": (df.isna().mean()*100).round(2)})
      .sort_values("count", ascending=False))
print("\nDuplicate rows:", df.duplicated().sum())
print("\nNumeric summary:\n", df[["total_laid_off","percentage_laid_off","funds_raised"]].describe().T)
print("\nDate range:", df["date"].min(), "to", df["date"].max())

# 3. Data quality checks
print("\nNegative layoffs:", (df["total_laid_off"] < 0).sum())
print("Negative funding:", (df["funds_raised"] < 0).sum())
print("Percentage outside 0-1:",
      ((df["percentage_laid_off"] < 0) | (df["percentage_laid_off"] > 1)).sum())

# 4. KPIs
print("\nCORE KPIs")
print("Recorded layoffs:", f"{known.total_laid_off.sum():,.0f}")
print("Median event:", f"{known.total_laid_off.median():,.0f}")
print("Mean event:", f"{known.total_laid_off.mean():,.1f}")
print("Known layoff-count events:", f"{len(known):,}")

# 5. Distribution
fig, ax = plt.subplots(figsize=(10,5))
sns.histplot(known["total_laid_off"], bins=50, ax=ax)
ax.set(title="Distribution of Layoffs per Event",
       xlabel="Employees Laid Off", ylabel="Number of Events")
plt.tight_layout()
plt.savefig(FIG_DIR/"01_layoff_distribution.png", dpi=200)
plt.close()

plt.figure(figsize=(10,5))
sns.histplot(np.log1p(known["total_laid_off"]), bins=50)
plt.title("Log Distribution of Layoff Counts")
plt.xlabel("log(1 + employees laid off)")
plt.tight_layout()
plt.savefig(FIG_DIR/"02_log_layoff_distribution.png", dpi=200)
plt.close()

# 6. Time series
monthly = known.set_index("date")["total_laid_off"].resample("MS").sum()
annual = known.set_index("date")["total_laid_off"].resample("YS").sum()

plt.figure(figsize=(14,6))
plt.plot(monthly.index, monthly.values, linewidth=2)
plt.title("Monthly Recorded Layoffs")
plt.xlabel("Month"); plt.ylabel("Employees Laid Off")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig(FIG_DIR/"03_monthly_layoffs.png", dpi=200)
plt.close()

plt.figure(figsize=(11,5))
sns.barplot(x=annual.index.year.astype(str), y=annual.values)
plt.title("Annual Recorded Layoffs")
plt.xlabel("Year"); plt.ylabel("Employees Laid Off")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig(FIG_DIR/"04_annual_layoffs.png", dpi=200)
plt.close()

print("\nAnnual layoffs:\n", annual)
print("\nAnnual YoY % change:\n", (annual.pct_change()*100).round(2))

# 7. Company analysis
company = known.groupby("company")["total_laid_off"].sum().sort_values(ascending=False).head(15)
plt.figure(figsize=(12,7))
sns.barplot(x=company.values, y=company.index, orient="h")
plt.title("Top 15 Companies by Recorded Layoffs")
plt.xlabel("Employees Laid Off"); plt.ylabel("Company")
plt.tight_layout()
plt.savefig(FIG_DIR/"05_top_companies.png", dpi=200)
plt.close()

# 8. Country analysis
country = known.groupby("country")["total_laid_off"].sum().sort_values(ascending=False).head(15)
plt.figure(figsize=(12,7))
sns.barplot(x=country.values, y=country.index, orient="h")
plt.title("Top 15 Countries by Recorded Layoffs")
plt.xlabel("Employees Laid Off"); plt.ylabel("Country")
plt.tight_layout()
plt.savefig(FIG_DIR/"06_top_countries.png", dpi=200)
plt.close()

# 9. Industry analysis: impact and event volume
industry = known.groupby("industry")["total_laid_off"].sum().sort_values(ascending=False).head(15)
plt.figure(figsize=(12,7))
sns.barplot(x=industry.values, y=industry.index, orient="h")
plt.title("Top 15 Industries by Recorded Layoffs")
plt.xlabel("Employees Laid Off"); plt.ylabel("Industry")
plt.tight_layout()
plt.savefig(FIG_DIR/"07_top_industries.png", dpi=200)
plt.close()

industry_events = df["industry"].value_counts().head(15)
plt.figure(figsize=(12,7))
sns.barplot(x=industry_events.values, y=industry_events.index, orient="h")
plt.title("Top 15 Industries by Number of Layoff Events")
plt.xlabel("Number of Events"); plt.ylabel("Industry")
plt.tight_layout()
plt.savefig(FIG_DIR/"08_industry_event_volume.png", dpi=200)
plt.close()

# 10. Funding vs layoffs
funding_df = df.dropna(subset=["funds_raised","total_laid_off"]).copy()
plt.figure(figsize=(10,6))
sns.scatterplot(data=funding_df, x="funds_raised", y="total_laid_off", alpha=.35)
plt.xscale("log"); plt.yscale("log")
plt.title("Funding vs. Layoffs — Log Scale")
plt.xlabel("Funds Raised"); plt.ylabel("Employees Laid Off")
plt.tight_layout()
plt.savefig(FIG_DIR/"09_funding_vs_layoffs.png", dpi=200)
plt.close()
print("\nFunding/layoffs correlation:",
      funding_df[["funds_raised","total_laid_off"]].corr().iloc[0,1])

# 11. Layoff percentage
pct = df.dropna(subset=["percentage_laid_off"]).copy()
pct["layoff_pct"] = pct["percentage_laid_off"]*100
plt.figure(figsize=(10,5))
sns.histplot(pct["layoff_pct"], bins=40)
plt.title("Distribution of Workforce Reduction Percentage")
plt.xlabel("Workforce Laid Off (%)")
plt.tight_layout()
plt.savefig(FIG_DIR/"10_layoff_percentage_distribution.png", dpi=200)
plt.close()

# 12. Stage analysis
stage = (known.groupby("stage")
         .agg(events=("company","size"),
              total_laid_off=("total_laid_off","sum"),
              median_laid_off=("total_laid_off","median"))
         .sort_values("total_laid_off", ascending=False))
print("\nStage summary:\n", stage)

plt.figure(figsize=(12,7))
sns.barplot(x=stage.head(12)["total_laid_off"],
            y=stage.head(12).index, orient="h")
plt.title("Layoffs by Company Stage")
plt.xlabel("Employees Laid Off"); plt.ylabel("Stage")
plt.tight_layout()
plt.savefig(FIG_DIR/"11_stage_layoffs.png", dpi=200)
plt.close()

# 13. Country share
country_all = known.groupby("country")["total_laid_off"].sum().sort_values(ascending=False)
share = (country_all / country_all.sum() * 100).head(10)
plt.figure(figsize=(10,6))
sns.barplot(x=share.values, y=share.index, orient="h")
plt.title("Top 10 Countries — Share of Recorded Layoffs")
plt.xlabel("Share (%)"); plt.ylabel("Country")
plt.tight_layout()
plt.savefig(FIG_DIR/"12_country_share.png", dpi=200)
plt.close()

# 14. Calendar heatmap
cal = monthly.to_frame("layoffs")
cal["year"] = cal.index.year
cal["month"] = cal.index.month
heat = cal.pivot(index="year", columns="month", values="layoffs")
plt.figure(figsize=(14,6))
sns.heatmap(heat, linewidths=.5)
plt.title("Monthly Layoff Intensity Heatmap")
plt.xlabel("Month"); plt.ylabel("Year")
plt.tight_layout()
plt.savefig(FIG_DIR/"13_layoff_heatmap.png", dpi=200)
plt.close()

# 15. Top events
top_events = known.sort_values("total_laid_off", ascending=False).head(20)[
    ["company","date","total_laid_off","percentage_laid_off",
     "industry","stage","country"]
]
print("\nTop 20 individual events:\n", top_events.to_string(index=False))

# 16. Concentration metrics
top10_company_share = company.head(10).sum() / known.total_laid_off.sum() * 100
top10_country_share = country.head(10).sum() / known.total_laid_off.sum() * 100
print("\nTop 10 company share:", round(top10_company_share,2), "%")
print("Top 10 country share:", round(top10_country_share,2), "%")
print("Peak month:", monthly.idxmax().strftime("%Y-%m"),
      f"({monthly.max():,.0f})")

# 17. Export analytical tables
with pd.ExcelWriter("layoffs_analysis_summary.xlsx", engine="openpyxl") as writer:
    annual.to_frame("total_laid_off").to_excel(writer, sheet_name="Annual")
    monthly.to_frame("total_laid_off").to_excel(writer, sheet_name="Monthly")
    company.to_frame("total_laid_off").to_excel(writer, sheet_name="Top_Companies")
    country.to_frame("total_laid_off").to_excel(writer, sheet_name="Top_Countries")
    industry.to_frame("total_laid_off").to_excel(writer, sheet_name="Top_Industries")
    stage.to_excel(writer, sheet_name="Stage")
    top_events.to_excel(writer, sheet_name="Top_Events", index=False)

print("\nEDA completed. Figures saved to ./figures/")
