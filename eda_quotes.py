# eda_quotes.py  (robust version)
# Requirements: pandas, matplotlib
# Usage: run from project root with: python eda\eda_quotes.py
import os
import sys
import pandas as pd

# Use Agg backend so matplotlib works without display
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# --- Path setup (robust) ---
# If this script is in eda/ and you run from project root,
# we expect quotes.csv in project root (parent of eda/)
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, '..'))
QUOTES_CSV = os.path.join(PROJECT_ROOT, 'quotes.csv')
VIS_DIR = os.path.join(SCRIPT_DIR, 'visuals')

# Create visuals dir
os.makedirs(VIS_DIR, exist_ok=True)

# --- Diagnostics ---
print("Running EDA (robust) ...")
print("Script directory:", SCRIPT_DIR)
print("Project root (expected location of quotes.csv):", PROJECT_ROOT)
print("Expecting quotes.csv at:", QUOTES_CSV)
if not os.path.exists(QUOTES_CSV):
    print("\nERROR: quotes.csv not found at expected location.")
    print("Please ensure you ran Task 1 and quotes.csv exists in the project root folder:")
    print("  ->", PROJECT_ROOT)
    sys.exit(1)

# --- Load data ---
try:
    df = pd.read_csv(QUOTES_CSV)
except Exception as e:
    print("Error reading quotes.csv:", e)
    sys.exit(1)

print("Rows loaded:", len(df))
# Ensure expected columns exist
for col in ['text', 'author', 'tags']:
    if col not in df.columns:
        print(f"Warning: column '{col}' missing in quotes.csv. Adding empty column.")
        df[col] = ''

# --- EDA computations ---
df['quote_len'] = df['text'].astype(str).str.len()

# Top authors
top_authors = df['author'].value_counts().head(20)
print("\nTop authors (preview):")
print(top_authors.head(10).to_string())

# Most common tags
tags_series = df['tags'].fillna('').apply(lambda s: [t.strip() for t in str(s).split(',') if t.strip()])
all_tags = [tag for sub in tags_series for tag in sub]
if len(all_tags) == 0:
    tags_count = pd.Series([], dtype=int)
else:
    tags_count = pd.Series(all_tags).value_counts().head(30)
print("\nTop tags (preview):")
print(tags_count.head(10).to_string())

# Quote length stats
mean_len = df['quote_len'].mean()
median_len = df['quote_len'].median()
print(f"\nQuote length: mean = {mean_len:.2f}, median = {median_len}")

# --- Plots (saved to eda/visuals/) ---
# Top authors plot (limit to top 10)
ta_plot = top_authors.head(10)
plt.figure(figsize=(8,6))
ta_plot.sort_values().plot(kind='barh')
plt.title('Top Authors by Quote Count')
plt.xlabel('Number of Quotes')
plt.tight_layout()
ta_path = os.path.join(VIS_DIR, 'top_authors.png')
plt.savefig(ta_path)
plt.close()
print("Saved:", ta_path)

# Top tags plot (if tags exist)
if not tags_count.empty:
    plt.figure(figsize=(10,5))
    tags_count.head(15).plot(kind='bar')
    plt.title('Top Tags')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    tt_path = os.path.join(VIS_DIR, 'top_tags.png')
    plt.savefig(tt_path)
    plt.close()
    print("Saved:", tt_path)
else:
    print("No tags found — skipping top_tags plot.")

# Quote length histogram
plt.figure(figsize=(8,5))
df['quote_len'].hist(bins=25)
plt.title('Distribution of Quote Lengths (chars)')
plt.xlabel('Length (characters)')
plt.ylabel('Count')
plt.tight_layout()
ql_path = os.path.join(VIS_DIR, 'quote_length_hist.png')
plt.savefig(ql_path)
plt.close()
print("Saved:", ql_path)

# Save summary CSVs
ta_csv = os.path.join(VIS_DIR, 'top_authors.csv')
top_authors.to_csv(ta_csv, header=['count'])
print("Saved:", ta_csv)

if not tags_count.empty:
    tt_csv = os.path.join(VIS_DIR, 'top_tags.csv')
    tags_count.to_csv(tt_csv, header=['count'])
    print("Saved:", tt_csv)

# Save a short summary text
summary_path = os.path.join(VIS_DIR, 'eda_summary.txt')
with open(summary_path, 'w', encoding='utf-8') as f:
    f.write(f"total_quotes: {len(df)}\n")
    f.write(f"unique_authors: {int(df['author'].nunique())}\n")
    f.write(f"unique_tags: {len(set(all_tags))}\n")
    f.write(f"mean_quote_len: {mean_len:.2f}\n")
    f.write(f"median_quote_len: {median_len}\n")
print("Saved:", summary_path)

print("\nEDA finished successfully. Visuals and summaries are in:", VIS_DIR)
