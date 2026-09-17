"""
Netflix Data Analysis Project - Step 2: Exploratory Data Analysis
Generates charts into ./charts/ and prints key findings.
"""
import pandas as pd
import matplotlib.pyplot as plt
import os

df = pd.read_csv('netflix_cleaned.csv')
os.makedirs('charts', exist_ok=True)
plt.rcParams['figure.figsize'] = (9, 5)

# --- 1. Movies vs TV Shows split ---
type_counts = df['type'].value_counts()
plt.figure()
plt.bar(type_counts.index, type_counts.values, color=['#E50914', '#221f1f'])
plt.title('Netflix Catalog: Movies vs TV Shows')
plt.ylabel('Number of Titles')
plt.savefig('charts/01_type_split.png', bbox_inches='tight')
plt.close()

# --- 2. Content added per year (growth trend) ---
yearly = df.groupby('year_added').size()
plt.figure()
plt.plot(yearly.index, yearly.values, marker='o', color='#E50914')
plt.title('Netflix Content Growth by Year Added')
plt.xlabel('Year Added')
plt.ylabel('Titles Added')
plt.grid(alpha=0.3)
plt.savefig('charts/02_yearly_growth.png', bbox_inches='tight')
plt.close()

# --- 3. Movies vs TV share over time ---
type_by_year = df.groupby(['year_added', 'type']).size().unstack(fill_value=0)
type_share = type_by_year.div(type_by_year.sum(axis=1), axis=0) * 100
plt.figure()
plt.stackplot(type_share.index, type_share['Movie'], type_share['TV Show'],
              labels=['Movie', 'TV Show'], colors=['#E50914', '#221f1f'], alpha=0.85)
plt.title('Movie vs TV Show Share of Additions by Year (%)')
plt.ylabel('% of titles added that year')
plt.legend(loc='upper left')
plt.savefig('charts/03_type_share_over_time.png', bbox_inches='tight')
plt.close()

# --- 4. Top 10 countries by content volume ---
top_countries = df[df['primary_country'] != 'Unknown']['primary_country'].value_counts().head(10)
plt.figure()
plt.barh(top_countries.index[::-1], top_countries.values[::-1], color='#E50914')
plt.title('Top 10 Countries by Number of Titles')
plt.xlabel('Number of Titles')
plt.savefig('charts/04_top_countries.png', bbox_inches='tight')
plt.close()

# --- 5. Top 10 genres ---
top_genres = df['primary_genre'].value_counts().head(10)
plt.figure()
plt.barh(top_genres.index[::-1], top_genres.values[::-1], color='#221f1f')
plt.title('Top 10 Genres on Netflix')
plt.xlabel('Number of Titles')
plt.savefig('charts/05_top_genres.png', bbox_inches='tight')
plt.close()

# --- 6. Rating distribution ---
top_ratings = df['rating'].value_counts().head(8)
plt.figure()
plt.bar(top_ratings.index, top_ratings.values, color='#E50914')
plt.title('Content Rating Distribution (Top 8)')
plt.ylabel('Number of Titles')
plt.xticks(rotation=45)
plt.savefig('charts/06_rating_distribution.png', bbox_inches='tight')
plt.close()

# --- 7. Seasonality: month added ---
month_order = ['January','February','March','April','May','June','July',
                'August','September','October','November','December']
monthly = df['month_added'].value_counts().reindex(month_order)
plt.figure()
plt.bar(monthly.index, monthly.values, color='#221f1f')
plt.title('Content Additions by Month (All Years Combined)')
plt.ylabel('Number of Titles')
plt.xticks(rotation=45)
plt.savefig('charts/07_seasonality.png', bbox_inches='tight')
plt.close()

print("All 7 charts saved to ./charts/\n")

# --- Print key findings for the summary writeup ---
print("=== KEY FINDINGS ===")
movie_pct = (df['type'] == 'Movie').mean() * 100
print(f"1. Catalog split: {movie_pct:.1f}% Movies, {100-movie_pct:.1f}% TV Shows")

first_year, last_year = yearly.index.min(), yearly.index.max()
growth = (yearly[last_year-1] - yearly[first_year]) / yearly[first_year] * 100 if yearly[first_year] > 0 else 0
peak_year = yearly.idxmax()
print(f"2. Titles added peaked in {peak_year} ({yearly[peak_year]} titles); "
      f"catalog grew from {yearly[first_year]} (in {first_year}) to {yearly[peak_year]} at peak")

tv_share_first = type_share['TV Show'].iloc[0]
tv_share_last = type_share['TV Show'].iloc[-2]  # second-to-last to avoid partial final year
print(f"3. TV Show share of additions moved from {tv_share_first:.1f}% "
      f"({type_share.index[0]}) to {tv_share_last:.1f}% ({type_share.index[-2]})")

print(f"4. Top content-producing country: {top_countries.index[0]} ({top_countries.iloc[0]} titles), "
      f"followed by {top_countries.index[1]} ({top_countries.iloc[1]})")

print(f"5. Most common genre: {top_genres.index[0]} ({top_genres.iloc[0]} titles)")

print(f"6. Most common rating: {top_ratings.index[0]} ({top_ratings.iloc[0]} titles, "
      f"{top_ratings.iloc[0]/len(df)*100:.1f}% of catalog)")

peak_month = monthly.idxmax()
print(f"7. Most titles are added in {peak_month} ({monthly[peak_month]} titles historically)")
