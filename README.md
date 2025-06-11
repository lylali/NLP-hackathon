# 📰 Multilingual News Analyzer

A pipeline for comparing Chinese and English news articles using Natural Language Processing (NLP). This project extracts named entities and sentiment from raw news text, aggregates the results into a CSV, and generates visual summaries such as sentiment distribution charts and word clouds.

## 📁 Project Structure

├── data/
│ ├── news-cn.txt # Raw Chinese articles (one per line)
│ ├── news-en.txt # Raw English articles (one per line)
│ ├── outputs/
│ │ ├── csv/
│ │ │ └── ner_sentiment_output.csv # Combined NER + Sentiment data
│ │ └── graphs/
│ │ ├── sentiment_distribution.png
│ │ └── entity_wordcloud.png
├── functions.py # Utility functions for NER and sentiment
├── analyzer.py # NewsAnalyzer class with core NLP logic
├── pipeline.py # Orchestrates full pipeline (load -> analyze -> export)
├── visualization.py # Generates graphs from the CSV
├── config.yaml # Configurable paths and settings (optional)
├── requirements.txt # Project dependencies
├── README.md # You are here!


## 🚀 Features

- **Named Entity Recognition (NER)**: Extracts `PERSON`, `ORG`, and `GPE` entities.
- **Sentiment Analysis**: Classifies article tone as POSITIVE, NEGATIVE, or NEUTRAL.
- **Multilingual Support**: Handles both Chinese and English articles.
- **Visualization**:
  - Bar chart of sentiment distribution.
  - Word cloud of named entities.
- **CSV Export**: Aggregates all results for further analysis.

## 🛠️ Installation

1. **Clone the repo**
   ```bash
   git clone https://github.com/lylali/NLP-hackathon.git
   cd NLP-hackathon
   ```

2. **Set up a virtual environment**
    ```bash
    python -m venv .venv
    source .venv/bin/activate  # on Windows: .venv\Scripts\activate

3. **Install dependencies**
    ```bash
    pip install -r requirements.txt
    ```

4. (Optional): Download spaCy model
    ```bash
    python -m spacy download en_core_web_sm
    ```

## 📊 Usage
1. Get news data
   Use json data or the dumb txt data I'm currently using

2. Run the pipeline
   ```bash
   python pipeline.py
   ```

## ⚙️ Configuration
    ```yaml
    input_paths:
    english: data/news-en.txt
    chinese: data/news-cn.txt
    output_paths:
    csv: data/outputs/csv/ner_sentiment_output.csv
    graphs: data/outputs/graphs/
    ```

## 🧠 Dependencies
- spaCy for NER
- transformers by Hugging Face for sentiment analysis
- pandas, matplotlib, wordcloud for data handling and visualization
- See full list in requirements.txt

## 📝 License
MIT License – feel free to use, modify, and share.

