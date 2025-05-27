# Japanese Sentiment Analysis App (portfolio-app-github)

This is a web application for analyzing the sentiment of Japanese tweets, built with Python and Streamlit.

For Japanese, see [README_ja.md](./README_ja.md)

## Features

- Automatically classifies Japanese text as **Positive** or **Negative** using AI
- Supports batch analysis by uploading a CSV file
- Visualizes results with bar charts and time-series graphs
- Allows downloading analysis results as a CSV file


## Technologies Used

- Python 3
- Streamlit (Web app framework)
- Hugging Face Transformers (Sentiment analysis model)
- Altair (Data visualization)
- Pandas (Data processing)


## Installation & Usage

### 1. Install required libraries

`pip install -r requirements.txt`

### 2.Run the app

`streamlit run simple_app_github.py`

### 3. Open the app in your browser
Click the URL shown in your terminal (for example: http://localhost:8501).

## Notes
- The sentiment analysis model (jarvisx17/japanese-sentiment-analysis) supports only two classes: Positive and Negative.
- No API keys or personal information are included in this repository.
- If you upload a CSV file, please ensure that the contents consist of simple sentences.

```markdown
| Japanese                       | English translation                        |
| ------------------------------ | ------------------------------------------ |
| 今日は最高に楽しかった！            | I had an amazing time today!               |
| 明日は仕事で憂鬱…                  | I feel down because I have to work tomorrow... |
| なんだか気分が乗らない             | I just can’t get in the mood.              |
| カフェでまったりしてリフレッシュ！ | I relaxed at a café and refreshed myself!  |
| 寝坊して最悪な気分だ               | I overslept and feel terrible.             |
