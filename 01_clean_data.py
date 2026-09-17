"""
Netflix Data Analysis Project - Step 1: Data Cleaning
Cleans netflix_titles.csv and outputs netflix_cleaned.csv
"""
import pandas as pd
import numpy as np

df = pd.read_csv('netflix_titles.csv')
print(f"Raw shape: {df.shape}")

# --- 1. Handle missing values ---
# director/cast/country: fill with 'Unknown' (many titles genuinely lack this metadata)
df['director'] = df['director'].fillna('Unknown')
df['cast'] = df['cast'].fillna('Unknown')
df['country'] = df['country'].fillna('Unknown')

# rating/duration: only a handful missing -> drop those rows (can't safely infer)
df = df.dropna(subset=['rating', 'duration'])

# date_added: drop rows missing this since it's needed for time-based analysis
df = df.dropna(subset=['date_added'])
df['date_added'] = df['date_added'].str.strip()
df['date_added'] = pd.to_datetime(df['date_added'], format='%B %d, %Y')

# --- 2. Feature engineering ---
df['year_added'] = df['date_added'].dt.year
df['month_added'] = df['date_added'].dt.month_name()

# split duration into numeric value + unit (movies = minutes, TV shows = seasons)
df['duration_value'] = df['duration'].str.extract(r'(\d+)').astype(int)
df['duration_unit'] = np.where(df['type'] == 'Movie', 'min', 'season(s)')

# primary country = first listed country (many titles are multi-country co-productions)
df['primary_country'] = df['country'].apply(lambda x: x.split(',')[0].strip())

# primary genre = first listed genre from 'listed_in'
df['primary_genre'] = df['listed_in'].apply(lambda x: x.split(',')[0].strip())

# --- 3. Save cleaned dataset ---
df.to_csv('netflix_cleaned.csv', index=False)
print(f"Cleaned shape: {df.shape}")
print(f"Rows dropped: {8807 - df.shape[0]}")
print("\nSaved -> netflix_cleaned.csv")
print("\nSample:")
print(df[['title','type','year_added','primary_country','primary_genre','duration_value','duration_unit']].head())
