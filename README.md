# CodeAlpha
1️⃣ Task 1 — Web Scraping (Quotes Dataset)

Scraped quotes, authors, and tags from quotes.toscrape.com
Used requests and BeautifulSoup
Saved dataset as quotes.csv
Handled pagination, cleaned extracted text, and created a structured dataset

Output file:

quotes.csv

Key Columns:

text – Quote content
author – Author name
tags – Comma-separated tags

2️⃣ Task 2 — Exploratory Data Analysis (EDA)

Performed analysis on the scraped dataset to understand distributions, patterns, and trends.
Steps Included:

Loaded quotes.csv using pandas
Created new column quote_len

Identified:

Top authors by quote count
Most common tags
Distribution of quote lengths
Generated bar charts and histograms using matplotlib
Exported charts to eda/visuals/

Generated Visuals:

top_authors.png
top_tags.png
quote_length_hist.png

Other Outputs:
top_authors.csv
top_tags.csv
eda_summary.txt

3️⃣ Task 3 — Sentiment Analysis

Performed lexicon-based sentiment classification on the quotes.
Process Includes:
Preprocessing text (cleaning, tokenizing)

Using custom lexicon lists:
Positive words
Negative words

Calculating:
sentiment label (positive / negative / neutral)
pos_count
neg_count

Output files:
quotes_sentiment.csv – full results with sentiment labels
sentiment_summary.csv – count of each sentiment
sentiment_examples.csv – sample quotes for each label
project/
│
├── quotes.csv
│
├── web_scraping/
│   └── scrape_quotes.py
│
├── eda/
│   ├── eda_quotes.py
│   └── visuals/
│       ├── top_authors.png
│       ├── top_tags.png
│       ├── quote_length_hist.png
│       ├── top_authors.csv
│       ├── top_tags.csv
│       └── eda_summary.txt
│
└── sentiment/
    ├── sentiment_analysis.py
    ├── quotes_sentiment.csv
    ├── sentiment_summary.csv
    └── sentiment_examples.csv
