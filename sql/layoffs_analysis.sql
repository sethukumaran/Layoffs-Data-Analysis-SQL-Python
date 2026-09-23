-- ============================================================
-- LAYOFFS DATASET — BUSINESS ANALYSIS SQL
-- Dialect: PostgreSQL
-- ============================================================
-- Table: layoffs
-- Columns:
-- company, location, total_laid_off, date,
-- percentage_laid_off, industry, source, stage,
-- funds_raised, country, date_added
-- ============================================================

-- 1. Dataset profile
SELECT COUNT(*) AS total_records,
       COUNT(DISTINCT company) AS companies,
       COUNT(DISTINCT country) AS countries,
       COUNT(DISTINCT industry) AS industries,
       MIN(date) AS first_date,
       MAX(date) AS last_date
FROM layoffs;

-- 2. Missing-value audit
SELECT
    COUNT(*) FILTER (WHERE total_laid_off IS NULL) AS missing_layoffs,
    COUNT(*) FILTER (WHERE percentage_laid_off IS NULL) AS missing_percentage,
    COUNT(*) FILTER (WHERE funds_raised IS NULL) AS missing_funding,
    COUNT(*) FILTER (WHERE industry IS NULL) AS missing_industry,
    COUNT(*) FILTER (WHERE country IS NULL) AS missing_country,
    COUNT(*) FILTER (WHERE stage IS NULL) AS missing_stage
FROM layoffs;

-- 3. Core KPIs
SELECT
    COUNT(*) FILTER (WHERE total_laid_off IS NOT NULL) AS known_events,
    SUM(total_laid_off) AS total_recorded_layoffs,
    AVG(total_laid_off) AS avg_event_size,
    PERCENTILE_CONT(.50) WITHIN GROUP (ORDER BY total_laid_off) AS median_event_size,
    MAX(total_laid_off) AS largest_event
FROM layoffs;

-- 4. Monthly trend
SELECT DATE_TRUNC('month', date)::date AS month,
       SUM(total_laid_off) AS layoffs,
       COUNT(*) AS events
FROM layoffs
WHERE total_laid_off IS NOT NULL
GROUP BY 1
ORDER BY 1;

-- 5. Annual trend
SELECT EXTRACT(YEAR FROM date)::int AS year,
       SUM(total_laid_off) AS layoffs,
       COUNT(*) AS events
FROM layoffs
WHERE total_laid_off IS NOT NULL
GROUP BY 1
ORDER BY 1;

-- 6. Year-over-year change
WITH yearly AS (
    SELECT EXTRACT(YEAR FROM date)::int AS year,
           SUM(total_laid_off) AS layoffs
    FROM layoffs
    WHERE total_laid_off IS NOT NULL
    GROUP BY 1
)
SELECT year,
       layoffs,
       LAG(layoffs) OVER (ORDER BY year) AS prior_year,
       ROUND(100.0 * (layoffs - LAG(layoffs) OVER (ORDER BY year))
       / NULLIF(LAG(layoffs) OVER (ORDER BY year),0), 2) AS yoy_pct
FROM yearly
ORDER BY year;

-- 7. Top companies
SELECT company,
       SUM(total_laid_off) AS total_laid_off,
       COUNT(*) AS events,
       AVG(total_laid_off) AS avg_event_size
FROM layoffs
WHERE total_laid_off IS NOT NULL
GROUP BY company
ORDER BY total_laid_off DESC
LIMIT 20;

-- 8. Largest individual events
SELECT company, date, total_laid_off, percentage_laid_off,
       industry, stage, country
FROM layoffs
WHERE total_laid_off IS NOT NULL
ORDER BY total_laid_off DESC
LIMIT 20;

-- 9. Country impact
SELECT country,
       SUM(total_laid_off) AS total_laid_off,
       COUNT(*) AS events,
       AVG(total_laid_off) AS avg_event_size
FROM layoffs
WHERE total_laid_off IS NOT NULL
GROUP BY country
ORDER BY total_laid_off DESC
LIMIT 20;

-- 10. Industry impact
SELECT industry,
       SUM(total_laid_off) AS total_laid_off,
       COUNT(*) AS events,
       AVG(total_laid_off) AS avg_event_size,
       PERCENTILE_CONT(.50) WITHIN GROUP (ORDER BY total_laid_off) AS median_event_size
FROM layoffs
WHERE total_laid_off IS NOT NULL
GROUP BY industry
ORDER BY total_laid_off DESC;

-- 11. Industry frequency vs severity
SELECT industry,
       COUNT(*) AS events,
       SUM(total_laid_off) AS total_laid_off,
       AVG(total_laid_off) AS avg_event_size
FROM layoffs
WHERE total_laid_off IS NOT NULL
GROUP BY industry
ORDER BY total_laid_off DESC;

-- 12. Company stage
SELECT stage,
       COUNT(*) AS events,
       SUM(total_laid_off) AS total_laid_off,
       AVG(total_laid_off) AS avg_event_size,
       PERCENTILE_CONT(.50) WITHIN GROUP (ORDER BY total_laid_off) AS median_event_size
FROM layoffs
WHERE total_laid_off IS NOT NULL
GROUP BY stage
ORDER BY total_laid_off DESC;

-- 13. Workforce-reduction bands
SELECT CASE
         WHEN percentage_laid_off < .10 THEN '<10%'
         WHEN percentage_laid_off < .25 THEN '10%-24.9%'
         WHEN percentage_laid_off < .50 THEN '25%-49.9%'
         WHEN percentage_laid_off < .75 THEN '50%-74.9%'
         WHEN percentage_laid_off < 1.00 THEN '75%-99.9%'
         WHEN percentage_laid_off = 1.00 THEN '100%'
         ELSE 'Other'
       END AS reduction_band,
       COUNT(*) AS events
FROM layoffs
WHERE percentage_laid_off IS NOT NULL
GROUP BY 1
ORDER BY 1;

-- 14. Fully affected events
SELECT company, date, total_laid_off,
       percentage_laid_off, industry, country, stage
FROM layoffs
WHERE percentage_laid_off = 1
ORDER BY date DESC;

-- 15. Funding bands
SELECT CASE
         WHEN funds_raised < 50 THEN '<$50M'
         WHEN funds_raised < 100 THEN '$50M-$99M'
         WHEN funds_raised < 500 THEN '$100M-$499M'
         WHEN funds_raised < 1000 THEN '$500M-$999M'
         ELSE '$1B+'
       END AS funding_band,
       COUNT(*) AS events,
       SUM(total_laid_off) AS total_laid_off,
       AVG(total_laid_off) AS avg_laid_off
FROM layoffs
WHERE funds_raised IS NOT NULL
  AND total_laid_off IS NOT NULL
GROUP BY 1
ORDER BY MIN(funds_raised);

-- 16. Funding / layoffs correlation
SELECT CORR(funds_raised, total_laid_off) AS correlation
FROM layoffs
WHERE funds_raised IS NOT NULL
  AND total_laid_off IS NOT NULL;

-- 17. Repeat layoffs
SELECT company,
       COUNT(*) AS event_count,
       SUM(total_laid_off) AS total_laid_off,
       MIN(date) AS first_event,
       MAX(date) AS latest_event
FROM layoffs
WHERE total_laid_off IS NOT NULL
GROUP BY company
HAVING COUNT(*) >= 2
ORDER BY total_laid_off DESC;

-- 18. Share of layoffs from repeat-layoff companies
WITH company_summary AS (
    SELECT company,
           COUNT(*) AS event_count,
           SUM(total_laid_off) AS total_laid_off
    FROM layoffs
    WHERE total_laid_off IS NOT NULL
    GROUP BY company
)
SELECT
    COUNT(*) FILTER (WHERE event_count >= 2) AS repeat_companies,
    SUM(total_laid_off) FILTER (WHERE event_count >= 2) AS repeat_company_layoffs,
    SUM(total_laid_off) AS all_layoffs,
    ROUND(100.0 * SUM(total_laid_off) FILTER (WHERE event_count >= 2)
          / NULLIF(SUM(total_laid_off),0), 2) AS pct_from_repeat_companies
FROM company_summary;

-- 19. Rolling 3-month layoffs
WITH monthly AS (
    SELECT DATE_TRUNC('month', date)::date AS month,
           SUM(total_laid_off) AS layoffs
    FROM layoffs
    WHERE total_laid_off IS NOT NULL
    GROUP BY 1
)
SELECT month,
       layoffs,
       SUM(layoffs) OVER (
           ORDER BY month ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
       ) AS rolling_3_month_layoffs
FROM monthly
ORDER BY month;

-- 20. Industry rank within year
WITH annual_industry AS (
    SELECT EXTRACT(YEAR FROM date)::int AS year,
           industry,
           SUM(total_laid_off) AS layoffs
    FROM layoffs
    WHERE total_laid_off IS NOT NULL
    GROUP BY 1,2
)
SELECT year, industry, layoffs,
       DENSE_RANK() OVER (PARTITION BY year ORDER BY layoffs DESC) AS rank
FROM annual_industry
ORDER BY year, rank;

-- 21. Country rank within year
WITH annual_country AS (
    SELECT EXTRACT(YEAR FROM date)::int AS year,
           country,
           SUM(total_laid_off) AS layoffs
    FROM layoffs
    WHERE total_laid_off IS NOT NULL
    GROUP BY 1,2
)
SELECT year, country, layoffs,
       DENSE_RANK() OVER (PARTITION BY year ORDER BY layoffs DESC) AS rank
FROM annual_country
ORDER BY year, rank;

-- 22. 2026 partial-year snapshot
SELECT DATE_TRUNC('month', date)::date AS month,
       COUNT(*) AS events,
       SUM(total_laid_off) AS layoffs
FROM layoffs
WHERE date >= DATE '2026-01-01'
  AND total_laid_off IS NOT NULL
GROUP BY 1
ORDER BY 1;

-- 23. Data-quality anomalies
SELECT *
FROM layoffs
WHERE total_laid_off < 0
   OR percentage_laid_off < 0
   OR percentage_laid_off > 1
   OR funds_raised < 0;
