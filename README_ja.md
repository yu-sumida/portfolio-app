# 日本語感情分析アプリ（portfolio-app-github）

Python（Streamlit）で作成した、日本語ツイートの感情を分析するWebアプリです。



## 機能紹介

- 日本語のテキストを入力すると、感情（ポジティブ・ネガティブ）を自動判定
- CSVファイルをアップロードし、複数データを一括分析可能
- 感情の分析結果をグラフ（棒グラフ・時系列グラフ）で表示可能
- 分析結果をCSV形式でダウンロード可能



## 使用している技術・ライブラリ

- Python 3
- Streamlit（Webアプリ作成）
- Hugging Face Transformers（感情分析モデル）
- Altair（データ可視化）
- Pandas（データ操作）



## インストール方法・使い方

### 1. 必要なライブラリをインストール

`pip install -r requirements.txt`

### 2. アプリを実行

`streamlit run simple_app_github.py`

### 3. ブラウザで表示

ターミナルに表示されたURL（例: http://localhost:8501）をクリック

## 注意点

- 本アプリで使用している感情分析モデル（jarvisx17/japanese-sentiment-analysis）は、ポジティブ・ネガティブの2種類の分類です。
- APIキーや個人情報は含まれていません。
- CSVファイルをアップロードする場合、CSVファイルの中身はシンプルな文章でお願いいたします。

```markdown
|                               |
|今日は最高に楽しかった！         |
|明日は仕事で憂鬱…       　　　　 |
|なんだか気分が乗らない           |
|カフェでまったりしてリフレッシュ！|
|寝坊して最悪な気分だ             |