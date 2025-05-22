import pandas as pd
import sqlite3
from datetime import datetime

# === File paths ===
tracks_file = r'C:\Users\CHARAN\spotify_tracks_data_2023.csv'
albums_file = r'C:\Users\CHARAN\spotify-albums_data_2023.csv'
db_file = r'C:\Users\CHARAN\spotify_cleaned.db'

# === Load CSVs ===
print("Loading CSV files...")
tracks_df = pd.read_csv(tracks_file)
albums_df = pd.read_csv(albums_file)

# === Step 1: Cleaning Tracks Data ===
print("Cleaning and merging data...")

# Drop nulls
tracks_df.dropna(inplace=True)
albums_df.dropna(subset=['track_id'], inplace=True)

# Rename columns for clarity
tracks_df.rename(columns={'id': 'track_id'}, inplace=True)

# Merge on track_id
merged_df = pd.merge(albums_df, tracks_df, on='track_id', how='inner')

# === Step 2: Transform Data ===

# a. Add 'radio_mix' column (True if <= 180 seconds)
merged_df['radio_mix'] = merged_df['duration_sec'] <= 180

# b. Filter only non-explicit tracks with popularity > 50
filtered_df = merged_df[
    (merged_df['explicit'] == False) &
    (merged_df['track_popularity'] > 50)
]

# === Step 3: Load into SQLite ===
print("Loading into SQLite...")

conn = sqlite3.connect(db_file)
filtered_df.to_sql('spotify_data', conn, if_exists='replace', index=False)

# === Step 4: Run Queries ===
print("\nTop 20 Labels by Total Tracks:")
query1 = """
SELECT label, COUNT(*) as total_tracks
FROM spotify_data
GROUP BY label
ORDER BY total_tracks DESC
LIMIT 20;
"""
labels_df = pd.read_sql(query1, conn)
print(labels_df)

print("\nTop 25 Popular Tracks Released Between 2020 and 2023:")
query2 = """
SELECT track_name, track_popularity, release_date
FROM spotify_data
WHERE release_date BETWEEN '2020-01-01' AND '2023-12-31'
ORDER BY track_popularity DESC
LIMIT 25;
"""
tracks_df = pd.read_sql(query2, conn)
print(tracks_df)

# Closing connection
conn.close()

print("\n✅ ETL and queries complete.")
