import streamlit as st
import google.generativeai as genai
import json

# --- 1. カギの設定 ---
try:
    api_key = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=api_key)
except:
    st.error("金庫(Secrets)にカギを入れてください！")
    st.stop()

st.title("🦖 AIむげんクイズ 👻")

def create_new_quiz():
    try:
        # 2026年、最も信頼されている「gemini-1.5-flash」を指名
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        prompt = (
            "5歳児向けの楽しい知育クイズを1問作ってください。"
            "ジャンルは恐竜、妖怪、動物からランダムに。"
            "必ず以下のJSON形式だけで出力して。余計な説明は禁止。"
            "{'genre': 'ジャンル', 'q': '問題文', 'a': '答え', 'img': '絵文字'}"
        )
        
        # 正式版(v1)として通信するように強制
        response = model.generate_content(
            prompt,
            generation_config={"response_mime_type": "application/json"}
        )
        return json.loads(response.text)
    except Exception as e:
        return {"genre": "夢の中", "q": f"AIのほっぺを つねっています...もう一度！({e})", "a": "またね", "img": "💤"}

# --- 2. 動きの設定 ---
if st.button("🌟 つぎの もんだいに する"):
    st.session_state.quiz_data = create_new_quiz()
    st.rerun()

if 'quiz_data' not in st.session_state:
    st.session_state.quiz_data = create_new_quiz()

q = st.session_state.quiz_data

# --- 3. 画面の表示 ---
if q:
    st.info(f"ジャンル： {q['genre']}")
    st.subheader(q['q'])
    ans = st.text_input("こたえは なあに？", key="input_box")
    if st.button("こたえあわせ"):
        if ans and (ans in q['a'] or q['a'] in ans):
            st.balloons()
            st.success(f"あたり！「{q['a']}」だよ {q['img']}")
