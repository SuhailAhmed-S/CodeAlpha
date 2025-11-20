# sentiment_analysis.py
# Simple lexicon-based sentiment for quotes.csv
# Usage (from project root): python sentiment\sentiment_analysis.py

import os
import sys
import re
import pandas as pd

# --- Paths ---
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, '..'))
QUOTES_CSV = os.path.join(PROJECT_ROOT, 'quotes.csv')
OUT_CSV = os.path.join(SCRIPT_DIR, 'quotes_sentiment.csv')
SUMMARY_CSV = os.path.join(SCRIPT_DIR, 'sentiment_summary.csv')
EXAMPLES_CSV = os.path.join(SCRIPT_DIR, 'sentiment_examples.csv')

# --- Small lexicons (extend if you want) ---
POS_WORDS = {
    "good","great","happy","love","wonderful","best","amazing","awesome","excellent",
    "positive","delight","joy","like","enjoy","beautiful","success","peace","inspire","inspirational","best"
}
NEG_WORDS = {
    "bad","sad","hate","angry","worse","terrible","awful","horrible","ugly","pain",
    "failure","difficult","hard","angst","regret","problem","negative"
}

def clean_text(text):
    if not isinstance(text, str):
        return ""
    # lower, remove punctuation except apostrophes, collapse spaces
    t = re.sub(r"[^\w\s']", " ", text.lower())
    t = re.sub(r"\s+", " ", t).strip()
    return t

def score_text(text):
    t = clean_text(text)
    words = t.split()
    pos = sum(1 for w in words if w in POS_WORDS)
    neg = sum(1 for w in words if w in NEG_WORDS)
    score = pos - neg
    if score > 0:
        return "positive", pos, neg
    elif score < 0:
        return "negative", pos, neg
    else:
        return "neutral", pos, neg

def main():
    print("Sentiment analysis starting...")
    if not os.path.exists(QUOTES_CSV):
        print("ERROR: quotes.csv not found at:", QUOTES_CSV)
        sys.exit(1)

    df = pd.read_csv(QUOTES_CSV)
    # Ensure columns
    if 'text' not in df.columns:
        print("ERROR: quotes.csv must have a 'text' column.")
        sys.exit(1)

    # Apply scoring
    results = []
    for idx, row in df.iterrows():
        text = row.get('text', '')
        sentiment, pos_count, neg_count = score_text(text)
        out = row.to_dict()
        out.update({
            "sentiment": sentiment,
            "pos_count": pos_count,
            "neg_count": neg_count,
        })
        results.append(out)

    out_df = pd.DataFrame(results)
    out_df.to_csv(OUT_CSV, index=False)
    print("Saved sentiment results to:", OUT_CSV)

    # Summary counts
    summary = out_df['sentiment'].value_counts().rename_axis('sentiment').reset_index(name='count')
    summary.to_csv(SUMMARY_CSV, index=False)
    print("Saved sentiment summary to:", SUMMARY_CSV)
    print(summary.to_string(index=False))

    # Examples: first 5 of each sentiment
    examples = out_df.groupby('sentiment').head(5)[['sentiment','text','author','pos_count','neg_count']].reset_index(drop=True)
    examples.to_csv(EXAMPLES_CSV, index=False)
    print("Saved sentiment examples to:", EXAMPLES_CSV)

    print("Done.")

if __name__ == "__main__":
    main()
