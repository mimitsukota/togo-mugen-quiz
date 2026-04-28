import streamlit as st
import google.generativeai as genai
from gtts import gTTS
import json

# --- 1. カギの設定 ---
try:
    api_key = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=api_key)
except:
    st.error("金庫(Secrets)の設定を確認してください。")
    st.stop()

st.title("🦖 AIむげんクイズ 👻")

def create_new_quiz():
    # 修正：モデル名を「gemini-1.5-flash」一択にし、余計な設定を全カット
    try:
        # 2026年現在、最も普及しているモデル名に絞ります
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        prompt = (
            "5歳児向けの楽しいクイズ（恐竜、妖怪、動物から1つ）を作って。"
            "必ず以下のJSON形式だけで出力して。"
            "{'genre': 'ジャンル', 'q': '問題', 'a': '答え', 'img': '絵文字'}"
        )
        
        # 最もシンプルな呼び出し
        response = model.generate_content(prompt)
        
        # JSONを無理やり抜き出す力技
        t = response.text
        start = t.find('{')
        end = t.rfind('}') + 1
        return json.loads(t[start:end])
        
    except Exception as e:
        return {"genre": "爆睡中", "q": f"AIにバケツで水をかけました...もう一度！({e})", "a": "またね", "img": "🪣"}

# --- 3. 画面の動き ---
if st.button("🌟 つぎの もんだいに する"):
    st.session_state.quiz_data = create_new_quiz()
    st.rerun()

if 'quiz_data' not in st.session_state:
    st.session_state.quiz_data = create_new_quiz()

q = st.session_state.quiz_data

if q:
    st.info(f"今回のジャンル： {q['genre']}")
    st.subheader(q['q'])
    
    if st.button("🔊 もんだいを きく"):
        try:
            gTTS(q['q'], lang='ja').save("q.mp3")
            st.audio("q.mp3")
        except:
            st.warning("声の準備中...")

    ans = st.text_input("こたえは なあに？", key="input_box")
    if st.button("こたえあわせ"):
        if ans and (ans in q['a'] or q['a'] in ans):
            st.balloons()
            st.success(f"あたり！「{q['a']}」だよ {q['img']}")
