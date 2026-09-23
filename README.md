# Layoffs-Data-Analysis-SQL-Python

## Project Overview
End-to-end analysis of a global company layoffs dataset using SQL and Python, designed from a Senior Data Analyst / BI perspective.

### Dataset profile
- Records: 4,608
- Columns: 11
- Unique companies: 2,988
- Countries: 66
- Industries: 30
- Date range: 2020-03-11 to 2026-09-17
## Business Questions
1. How have layoffs changed over time?
2. Which companies drive the largest workforce impact?
3. Which countries and industries are most exposed?
4. Which industries have high frequency versus high severity?
5. How do layoffs vary by company stage?
6. Is funding associated with layoff size?
7. Which companies have repeated layoff events?
8. How severe are workforce reductions?
9. What data-quality limitations affect conclusions?

## Tools
- Python: pandas, NumPy, Matplotlib, Seaborn
- SQL: MS SQL

## Data Quality
Missing values:
- total_laid_off: 1,598 (34.7%)
- percentage_laid_off: 1,722 (37.4%)
- funds_raised: 549 (11.9%)
There are 0 exact duplicate rows.

**Analytical rule:** missing layoff counts are not treated as zero. Workforce-impact metrics use only records where `total_laid_off` is known.

## Executive Findings

### 1. Overall impact
Recorded layoffs where the employee count is available total approximately **932,431**. The median event is **90 employees**, indicating a strongly right-skewed distribution in which a small number of very large events materially affect the aggregate.

### 2. Time trend
The largest monthly recorded total is **January 2023**, at approximately **89,709 layoffs**. Early 2023 is a major concentration period in the dataset.

### 3. Company concentration
Top cumulative companies include:
- Amazon: 59,560
- Intel: 43,115
- Meta: 35,700
- Microsoft: 34,855
- Dell: 23,650

### 4. Geographic concentration
Top countries by recorded layoffs:
- United States: 660,568
- India: 67,889
- Germany: 32,153
- United Kingdom: 24,694
- Netherlands: 22,175

Country totals reflect the reporting coverage of this dataset and should not be interpreted as national unemployment statistics.

### 5. Industry exposure
Top industries by recorded layoffs:
- Other: 116,165
- Retail: 108,495
- Hardware: 105,480
- Consumer: 98,654
- Transportation: 71,023

A senior analyst should distinguish **event frequency** from **event severity**. An industry may have many announcements without producing the largest employee impact.

### 6. Funding relationship
The Pearson correlation between available funding and layoff count is approximately **0.12**. This is an association, not evidence of causation. Funding alone is not a sufficient workforce-risk predictor.

## Senior Analyst Business Insights

### Workforce impact is concentrated
A relatively small number of large employers materially influence aggregate layoffs. Executive monitoring should therefore track both event count and employees affected.

### Typical event size is much smaller than the average
The median is far below the mean, demonstrating right-skew. Median and percentile measures should be reported alongside averages.

### 2023 is a key benchmark period
The monthly series contains a pronounced early-2023 spike. Subsequent periods can be benchmarked against this period using comparable completed time windows.

### Geography changes the interpretation
The United States dominates recorded volume, with India as a significant secondary concentration. Workforce planning should be segmented by geography rather than relying on one global number.

### Industry frequency and impact tell different stories
Use both event count and total employees affected. Median event size provides a third view of severity.

### Company stage matters
Post-IPO companies account for a large share of recorded layoffs in this dataset. Stage segmentation should therefore be included in executive reporting.

### Repeat layoffs are a distinct risk pattern
Companies with multiple layoff events should be tracked separately because repeated restructuring is materially different from a one-time event.

## Recommended Executive KPIs
| KPI | Purpose |
|---|---|
| Total recorded layoffs | Workforce impact |
| Layoff events | Frequency |
| Median layoffs/event | Typical severity |
| Largest event | Extreme impact |
| Monthly layoffs | Trend |
| 3-month rolling layoffs | Short-term trend smoothing |
| Top companies | Concentration |
| Top industries | Sector exposure |
| Top countries | Geographic exposure |
| Repeat-layoff companies | Restructuring persistence |
| Workforce reduction % | Severity |
| Funding vs layoffs | Context |

## SQL
The SQL script uses MS SQL and covers:
- Aggregations
- CTEs
- Window functions
- `LAG`
- `DENSE_RANK`
- Percentiles
- Rolling 3-month totals
- Correlation
- Repeat-layoff analysis
- Data-quality checks
- Industry/country ranking

## Limitations
1. Many records lack an exact layoff count.
2. Many records lack workforce-reduction percentage.
3. Funding is incomplete.
4. Reporting coverage varies by geography/company.
5. 2026 is incomplete.
6. Companies may appear multiple times.
7. Missing headcount prevents reconstructing percentages.
8. Correlation does not establish causation.
9. Country totals are not national unemployment measures.
10. `Other` industry requires further investigation before strategic use.

## Conclusion
The dataset is most useful when layoffs are analyzed across **scale, frequency, concentration, industry, geography, severity and persistence**. The project demonstrates a senior-analyst approach: quantify the business impact, separate frequency from severity, identify concentration, test relationships carefully, and explicitly document data limitations.




