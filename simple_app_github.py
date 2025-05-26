import os
import json
import pandas as pd
import streamlit as st
from transformers import pipeline
from collections import Counter
import altair as alt
from datetime import datetime

# 感情分析モデルの読み込み（CPU指定）
classifier = pipeline(
    "sentiment-analysis",
    model="jarvisx17/japanese-sentiment-analysis",
    device=-1  # CPUで実行
)
# --- キャッシュ読み込み・保存・初期化 ---
CACHE_FILE = "simple_cache.json"

def load_cache():
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def save_cache(cache):
    with open(CACHE_FILE, "w", encoding="utf-8") as f:
        json.dump(cache, f, ensure_ascii=False)

def clear_cache():
    if os.path.exists(CACHE_FILE):
        os.remove(CACHE_FILE)

# --- ページ設定 ---
st.set_page_config(page_title="日本語感情分析", layout="wide")
st.title("🧠 日本語感情分析アプリ")
st.markdown("### 入力された日本語テキストの感情をAIが自動で分析します。")

# --- キャッシュ初期化ボタン（サイドバー） ---
if st.sidebar.button("🗑️ キャッシュを初期化"):
    clear_cache()
    st.sidebar.success("✅ キャッシュを初期化しました")

# 入力欄（複数行対応）
user_input = st.text_area("📝 テキストを入力してください（1行でも長文でもOK）", height=100)

# 感情分析の実行
cache = load_cache()
if st.button("分析する") and user_input.strip():
    if user_input in cache:
        st.info("✅ キャッシュから結果を取得しました")
        result = cache[user_input]
    else:
        st.info("🔍 新しく分析中...")
        result = classifier(user_input)[0]
        result["timestamp"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cache[user_input] = result
        save_cache(cache)

    label = result["label"].lower()

    if result["label"] == "positive":
        st.success(f"😊 感情: {result['label']}（スコア: {result['score']:.2f}）")
    elif result["label"] == "negative":
        st.error(f"😢 感情: {result['label']}（スコア: {result['score']:.2f}）")
    else:
        st.info(f"🤔 感情: {result['label']}（スコア: {result['score']:.2f}）")


# --- タブで切り替え ---
tab1, tab2, tab3 = st.tabs(["📄 分析結果一覧", "📊 感情分布グラフ", "📈 スコア時系列グラフ"])

# 分析結果一覧
with tab1:
    if cache:
        df = pd.DataFrame([
            {"テキスト": k, "感情": v["label"], "スコア": f"{v['score']:.2f}", "日時": v.get("timestamp", "")}
            for k, v in cache.items()
        ])
        st.dataframe(df)
        csv = df.to_csv(index=False, encoding="utf-8-sig")
        st.download_button("📥 分析結果をCSVでダウンロード", csv, "sentiment_results.csv", "text/csv")
    else:
        st.info("まだ分析履歴がありません。")

#　感情グラフ
with tab2:
    if cache:
        all_labels = [v["label"] for v in cache.values() if "label" in v]
        if all_labels:
            label_counts = Counter(all_labels)
            chart_data = [{"感情": label, "件数": count} for label, count in label_counts.items()]
            chart = alt.Chart(alt.Data(values=chart_data)).mark_bar().encode(
                x="感情:N", y="件数:Q", color="感情:N"
            ).properties(title="感情の分布")
            st.altair_chart(chart, use_container_width=True)
        else:
            st.info("データが不足しています。")

# スコア時系列グラフ
with tab3:
    if cache:
        df_score = pd.DataFrame([
            {
                "テキスト": k,
                "感情": v["label"],
                "スコア": float(v["score"]),
                "日時": v.get("timestamp", "")
            }
            for k, v in cache.items() if "timestamp" in v
        ])
        df_score["日時"] = pd.to_datetime(df_score["日時"], errors="coerce")
        df_score = df_score.dropna(subset=["日時"])
        if not df_score.empty:
            chart = alt.Chart(df_score).mark_line(
                point=alt.OverlayMarkDef(filled=True, size=80),
                interpolate="monotone"
            ).encode(
                x=alt.X("日時:T", axis=alt.Axis(title="日時", format="%m/%d %H:%M")),
                y=alt.Y("スコア:Q", scale=alt.Scale(domain=[0.5, 1.0]), axis=alt.Axis(title="感情スコア")),
                color=alt.Color("感情:N", scale=alt.Scale(domain=["positive", "negative"], range=["steelblue", "crimson"])),
                tooltip=["テキスト", "感情", "スコア", "日時"]
            ).properties(width=700, height=400)
            st.altair_chart(chart, use_container_width=True)
        else:
            st.info("時系列グラフに必要なデータがまだありません。")

st.markdown("---")
st.markdown("## 🐦 サンプルCSVを使った感情分析")

uploaded_file = st.file_uploader("📤 ツイートCSVファイルをアップロード", type="csv")

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.write("📃 ツイート一覧（最初の5件）:")
    st.dataframe(df.head())

    st.markdown("### 🧠 感情分析結果")
    for i, text in enumerate(df["text"].dropna().tolist()):
        result = classifier(text)[0]
        label = result["label"]
        score = result["score"]
        st.write(f"{i+1}. ✍️ {text[:60]}")
        st.write(f"→ 感情: **{label}**（スコア: {score:.2f}）")

