"""
Netflix Data Analysis Project - Step 3: SQL Layer
Loads cleaned data into SQLite and runs analytical queries.
This proves SQL skill independent of pandas - a common BA/DA interview ask.
"""
import pandas as pd
import sqlite3

df = pd.read_csv('netflix_cleaned.csv')
conn = sqlite3.connect('netflix.db')
df.to_sql('netflix', conn, if_exists='replace', index=False)

queries = {
"1. Top 10 genres by title count": """
    SELECT primary_genre, COUNT(*) AS title_count
    FROM netflix
    GROUP BY primary_genre
    ORDER BY title_count DESC
    LIMIT 10;
""",

"2. Year-over-year content growth": """
    SELECT year_added, COUNT(*) AS titles_added
    FROM netflix
    GROUP BY year_added
    ORDER BY year_added;
""",

"3. Average movie duration by rating (Movies only)": """
    SELECT rating, ROUND(AVG(duration_value), 1) AS avg_minutes, COUNT(*) AS movie_count
    FROM netflix
    WHERE type = 'Movie'
    GROUP BY rating
    HAVING movie_count >= 20
    ORDER BY avg_minutes DESC;
""",

"4. Top 5 countries producing TV Shows": """
    SELECT primary_country, COUNT(*) AS show_count
    FROM netflix
    WHERE type = 'TV Show' AND primary_country != 'Unknown'
    GROUP BY primary_country
    ORDER BY show_count DESC
    LIMIT 5;
""",

"5. Content mix (Movie vs TV Show) by top 5 countries": """
    SELECT primary_country,
           SUM(CASE WHEN type='Movie' THEN 1 ELSE 0 END) AS movies,
           SUM(CASE WHEN type='TV Show' THEN 1 ELSE 0 END) AS tv_shows
    FROM netflix
    WHERE primary_country IN (
        SELECT primary_country FROM netflix
        WHERE primary_country != 'Unknown'
        GROUP BY primary_country
        ORDER BY COUNT(*) DESC
        LIMIT 5
    )
    GROUP BY primary_country
    ORDER BY (movies + tv_shows) DESC;
""",
}

with open('sql_query_results.txt', 'w') as f:
    for title, q in queries.items():
        result = pd.read_sql_query(q, conn)
        print(f"\n=== {title} ===")
        print(result.to_string(index=False))
        f.write(f"=== {title} ===\n{q}\n{result.to_string(index=False)}\n\n")

conn.close()
print("\n\nSaved netflix.db (SQLite database) and sql_query_results.txt")
