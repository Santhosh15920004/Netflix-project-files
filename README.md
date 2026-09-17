# Netflix Content & Viewership Analysis

Data analysis project on Netflix's global content catalog (8,807 titles) using **Python (Pandas)**, **SQL (SQLite)**, and **Matplotlib**, with insights ready for a Power BI dashboard.

## Dataset
`netflix_titles.csv` — Netflix's public catalog metadata: type, title, director, cast, country, date added, release year, rating, duration, and genre.

## Project Structure
```
01_clean_data.py       # Cleaning + feature engineering -> netflix_cleaned.csv
02_eda.py               # Exploratory analysis + 7 charts -> ./charts/
03_sql_analysis.py      # SQL queries via SQLite -> netflix.db, sql_query_results.txt
netflix_cleaned.csv     # Cleaned dataset (8,790 rows)
charts/                 # 7 PNG charts
```

## Data Cleaning
- Filled missing `director`, `cast`, `country` with "Unknown" (metadata gaps, not data errors)
- Dropped 17 rows missing `rating`, `duration`, or `date_added` (couldn't be safely inferred)
- Parsed `date_added` into a proper datetime; extracted `year_added` / `month_added`
- Split `duration` into a numeric value + unit (minutes for movies, seasons for TV shows)
- Extracted `primary_country` and `primary_genre` from multi-value fields

## Key Findings
1. **Catalog mix:** 69.7% Movies vs 30.3% TV Shows.
2. **Growth:** Additions rose from single digits (2008–2014) to a peak of 2,016 titles in 2019, then declined through 2020–2021 — consistent with Netflix shifting toward originals and slowing licensed-content acquisition.
3. **Format shift:** TV Show share of new additions grew from 50% (2008) to a high in the mid-2010s before Movies regained dominance — original series investment shows up here.
4. **Geography:** The US leads with 3,202 titles, followed by India (1,008). The US and India differ sharply in mix — the US catalog is 74% Movies, while Japan and South Korea skew TV-heavy (67% and 65% TV Shows respectively), reflecting regional content strategy.
5. **Genre:** Dramas (1,599) and Comedies (1,210) dominate the catalog.
6. **Rating:** TV-MA is the most common rating (36.5% of titles) — Netflix's catalog skews toward mature content.
7. **Seasonality:** July sees the most content additions historically (827 titles).

## SQL Skills Demonstrated
- Aggregation & GROUP BY (genre, country, year counts)
- Conditional aggregation (CASE WHEN for Movie/TV Show mix by country)
- Subqueries (top-5 country filtering)
- HAVING clauses (filtering aggregated results)

## Next Step: Power BI Dashboard
Load `netflix_cleaned.csv` into Power BI and build:
- Slicers: year, country, genre, type
- Line chart: content growth by year
- Map: title count by country
- Bar chart: genre distribution
- KPI cards: total titles, % Movies vs TV Shows

## Resume Bullet
> Analyzed 8,790 Netflix titles using Python and SQL to uncover content growth and regional programming trends; built 7 visualizations revealing a peak of 2,016 titles added in 2019 and sharp Movie/TV mix differences across the US, India, Japan, and South Korea.
