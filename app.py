import streamlit as st
import google.generativeai as genai
from gtts import gTTS
import json
import re
import tempfile

# --- 1. カギを読み込む ---
try:
    api_key = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=api_key)
except Exception:
    st.error("カギの設定を確認してください。")
    st.stop()

st.title("🦖 AIむげんクイズ 👻")

# --- 2. クイズ作成関数（安定版） ---
def create_new_quiz():
    # ★ここを修正（latestをやめる）
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    prompt = """5歳向けクイズ（恐竜、妖怪、動物）を1問作成してください。
必ずJSONのみで答えてください。
{
 "genre": "...",
 "q": "...",
 "a": "...",
 "img": "..."
}"""

    try:
        response = model.generate_content(prompt)
        text = response.text

        # ```json ``` の除去（壊れ防止）
        text = re.sub(r"```json|```", "", text).strip()

        return json.loads(text)

    except Exception as e:
        st.warning(f"AIが まだ かくれんぼ中... (理由: {e})")
        return {
            "genre": "きょうりゅう",
            "q": "きょうりゅうの 王さまで、はが するどいのは？",
            "a": "てぃらのさうるす",
            "img": "🦖"
        }

# --- 3. アプリの動き ---
if st.button("🌟 つぎの もんだいに する"):
    st.session_state.quiz_data = create_new_quiz()
    st.rerun()

if 'quiz_data' not in st.session_state:
    st.session_state.quiz_data = create_new_quiz()

q = st.session_state.quiz_data

st.info(f"今回のジャンル： {q['genre']}")
st.subheader(q['q'])

# --- 音声 ---
if st.button("🔊 もんだいを きく"):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
        gTTS(q['q'], lang='ja').save(fp.name)
        st.audio(fp.name)

# --- 回答 ---
ans = st.text_input("こたえは なあに？", key="input_box")

if st.button("こたえあわせ"):
    if ans == "":
        st.warning("こたえをいれてね！")
    elif ans in q['a'] or q['a'] in ans:
        st.balloons()
        st.success(f"あたり！「{q['a']}」だよ {q['img']}")
    else:
        st.error(f"ちがうよ！せいかいは「{q['a']}」だよ")
