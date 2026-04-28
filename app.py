import streamlit as st
import google.generativeai as genai
from gtts import gTTS
import json
import os

# --- 1. カギの設定と「正式窓口」の強制指定 ---
try:
    api_key = st.secrets["GOOGLE_API_KEY"]
    # 【ここが重要！】古い窓口(v1beta)を無視して、正式版(v1)を使うように強制します
    os.environ["GOOGLE_API_VERSION"] = "v1" 
    genai.configure(api_key=api_key)
except:
    st.error("金庫(Secrets)の設定を確認してください。")
    st.stop()

st.title("🦖 AIむげんクイズ 👻")

def create_new_quiz():
    # モデル名を最新の安定版に固定
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        prompt = (
            "5歳児向けの楽しい知育クイズを1問だけ作って。"
            "ジャンルは恐竜、妖怪、動物からランダムに。"
            "必ずこのJSON形式だけで出力して。 {'genre': 'ジャンル', 'q': '問題', 'a': '答え', 'img': '絵文字'}"
        )
        
        response = model.generate_content(
            prompt,
            generation_config={"response_mime_type": "application/json"}
        )
        return json.loads(response.text)
        
    except Exception as e:
        # エラーが出ても「次へ」を促す
        return {"genre": "通信中", "q": f"AIがちょっと照れてるね。もう一度『つぎ』を押して！({e})", "a": "またね", "img": "⚙️"}

# --- 3. アプリの動き ---
if st.button("🌟 つぎの もんだいに する"):
    st.session_state.quiz_data = create_new_quiz()
    st.rerun()

if 'quiz_data' not in st.session_state:
    st.session_state.quiz_data = create_new_quiz()

q = st.session_state.quiz_data

if q:
    st.info(f"ジャンル： {q['genre']}")
    st.subheader(q['q'])
    
    if st.button("🔊 もんだいを きく"):
        gTTS(q['q'], lang='ja').save("q.mp3")
        st.audio("q.mp3")

    ans = st.text_input("こたえは なあに？", key="input_box")
    if st.button("こたえあわせ"):
        if ans and (ans in q['a'] or q['a'] in ans):
            st.balloons()
            st.success(f"あたり！「{q['a']}」だよ {q['img']}")
