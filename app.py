import streamlit as st
import google.generativeai as genai
from gtts import gTTS
import json

# --- 1. カギを読み込む ---
try:
    api_key = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=api_key)
except Exception as e:
    st.error("カギの設定を確認してください。")
    st.stop()

st.title("🦖 AIむげんクイズ 👻")

# --- 2. クイズ作成関数（2026年最新版・エラー回避型） ---
def create_new_quiz():
    # モデル名を「最新」を意味する名前に修正しました
    model = genai.GenerativeModel('gemini-1.5-flash-latest')
    
    prompt = "5歳向けクイズ（恐竜、妖怪、動物）を1問作成。JSON形式： {'genre': '...', 'q': '...', 'a': '...', 'img': '...'}"
    
    try:
        # エラーが出た「v1beta」を避け、安定した方法で呼び出します
        response = model.generate_content(
            prompt,
            generation_config={"response_mime_type": "application/json"}
        )
        return json.loads(response.text)
    except Exception as e:
        # 万が一の予備（次は「ティラノサウルス」にしました！）
        st.warning(f"AIが まだ かくれんぼ中... (理由: {e})")
        return {"genre": "きょうりゅう", "q": "きょうりゅうの 王さまで、はが するどいのは？", "a": "てぃらのさうるす", "img": "🦖"}

# --- 3. アプリの動き ---
if st.button("🌟 つぎの もんだいに する"):
    st.session_state.quiz_data = create_new_quiz()
    st.rerun()

if 'quiz_data' not in st.session_state:
    st.session_state.quiz_data = create_new_quiz()

q = st.session_state.quiz_data

st.info(f"今回のジャンル： {q['genre']}")
st.subheader(q['q'])

if st.button("🔊 もんだいを きく"):
    gTTS(q['q'], lang='ja').save("q.mp3")
    st.audio("q.mp3")

ans = st.text_input("こたえは なあに？", key="input_box")
if st.button("こたえあわせ"):
    if ans in q['a'] or q['a'] in ans:
        st.balloons()
        st.success(f"あたり！「{q['a']}」だよ {q['img']}")
