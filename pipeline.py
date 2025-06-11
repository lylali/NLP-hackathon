import pandas as pd
from functions import clean_text, detect_language
from analyzer import NewsAnalyzer
from visualization import generate_sentiment_bar_chart, generate_entity_wordcloud

# Load raw text files
with open("data/news-cn.txt", "r", encoding="utf-8") as f_cn:
    cn_articles = f_cn.readlines()

with open("data/news-en.txt", "r", encoding="utf-8") as f_en:
    en_articles = f_en.readlines()

# Construct dataframe
df_cn = pd.DataFrame({
    'content': cn_articles,
    'country': 'China'
})

df_en = pd.DataFrame({
    'content': en_articles,
    'country': 'English-Speaking'  # You can use a specific country if known
})

# Combine into one dataframe
df = pd.concat([df_cn, df_en], ignore_index=True)

# Initialize analyzer
analyzer = NewsAnalyzer()

# Step 1: Clean and detect language
df['cleaned_text'] = df['content'].fillna('').apply(clean_text)
df['language'] = df['cleaned_text'].apply(detect_language)

# Step 2: Run NER
df['entities'] = df['cleaned_text'].apply(analyzer.run_ner)

# Step 3: Run Sentiment Analysis
sentiment_results = df['cleaned_text'].apply(analyzer.run_sentiment)
df['sentiment_label'] = sentiment_results.apply(lambda x: x[0])
df['sentiment_score'] = sentiment_results.apply(lambda x: x[1])

# Save output
output_path = "data/outputs"
df.to_csv("data/outputs/output.csv", index=False)
generate_sentiment_bar_chart(df, output_path)
generate_entity_wordcloud(df, output_path)

print("NER and Sentiment Analysis completed. Output saved.")
