import streamlit as st
import google.generativeai as genai
from gtts import gTTS
import json

# --- 1. カギの設定 ---
try:
    api_key = st.secrets["GOOGLE_API_KEY"]
    # 道具箱が最新なら、これだけで正式版(v1)に繋がります
    genai.configure(api_key=api_key)
except:
    st.error("金庫(Secrets)の設定を確認してください。")
    st.stop()

st.title("🦖 AIむげんクイズ 👻")

def create_new_quiz():
    try:
        # 名前をシンプルに。最新の道具箱ならこれで通ります
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        prompt = (
            "5歳児向けの楽しい知育クイズを1問作って。"
            "必ず以下のJSON形式だけで出力して。余計な文字は不要。"
            "{'genre': 'ジャンル', 'q': '問題', 'a': '答え', 'img': '絵文字'}"
        )
        
        response = model.generate_content(
            prompt,
            generation_config={"response_mime_type": "application/json"}
        )
        return json.loads(response.text)
        
    except Exception as e:
        return {"genre": "通信中", "q": f"AIの耳を引っ張っています...もう一度ボタンを！({e})", "a": "またね", "img": "👂"}

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
        gTTS(q['q'], lang='ja').save("q.mp3")
        st.audio("q.mp3")

    ans = st.text_input("こたえは なあに？", key="input_box")
    if st.button("こたえあわせ"):
        if ans and (ans in q['a'] or q['a'] in ans):
            st.balloons()
            st.success(f"あたり！「{q['a']}」だよ {q['img']}")
