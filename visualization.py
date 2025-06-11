import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import seaborn as sns
import ast
import os

def generate_sentiment_bar_chart(df, output_path):
    plt.figure(figsize=(8, 6))
    sentiment_counts = df['sentiment_label'].value_counts()
    sns.barplot(x=sentiment_counts.index, y=sentiment_counts.values)
    plt.title("Sentiment Distribution")
    plt.xlabel("Sentiment")
    plt.ylabel("Count")
    plt.tight_layout()
    plt.savefig(os.path.join(output_path, "sentiment_distribution.png"))
    plt.close()

def generate_entity_wordcloud(df, output_path):
    all_entities = []
    for entities_str in df['entities']:
        try:
            entities = ast.literal_eval(entities_str)
            all_entities.extend([e['word'] for e in entities])
        except Exception:
            continue

    text = " ".join(all_entities)
    wordcloud = WordCloud(width=800, height=400, background_color="white").generate(text)
    wordcloud.to_file(os.path.join(output_path, "entity_wordcloud.png"))

# def generate_all(csv_path, output_path):
#     df = pd.read_csv(csv_path)
#     generate_sentiment_bar_chart(df, output_path)
#     generate_entity_wordcloud(df, output_path)
