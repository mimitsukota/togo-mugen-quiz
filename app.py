import streamlit as st
import google.generativeai as genai
import json

# --- 1. カギの設定 ---
try:
    api_key = st.secrets["GOOGLE_API_KEY"]
    # 道具箱を最新にすれば、これだけで「正式版(v1)」へ繋がります
    genai.configure(api_key=api_key)
except:
    st.error("金庫(Secrets)の設定を確認してください。")
    st.stop()

st.title("🦖 AIむげんクイズ 👻")

def create_new_quiz():
    # 2026年現在、最もエラーが出にくい「gemini-1.5-flash」を指名
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        prompt = (
            "5歳児向けの楽しい知育クイズ（恐竜、妖怪、動物から1つ）を作って。"
            "必ず以下のJSON形式だけで出力して。余計な説明は一切不要。"
            "{'genre': 'ジャンル', 'q': '問題文', 'a': '答え', 'img': '絵文字'}"
        )
        
        # JSON形式での出力をAIに強制する最新の設定
        response = model.generate_content(
            prompt,
            generation_config={"response_mime_type": "application/json"}
        )
        return json.loads(response.text)
        
    except Exception as e:
        return {"genre": "凍結中", "q": f"AIが氷漬けになっています...もう一度！({e})", "a": "またね", "img": "❄️"}

# --- 3. 画面の動き ---
if st.button("🌟 つぎの もんだいに する"):
    st.session_state.quiz_data = create_new_quiz()
    st.rerun()

if 'quiz_data' not in st.session_state:
    st.session_state.quiz_data = create_new_quiz()

q = st.session_state.quiz_data

if q:
    st.info(f"ジャンル： {q['genre']}")
    st.subheader(q['q'])
    ans = st.text_input("こたえは なあに？", key="input_box")
    if st.button("こたえあわせ"):
        if ans and (ans in q['a'] or q['a'] in ans):
            st.balloons()
            st.success(f"あたり！「{q['a']}」だよ {q['img']}")
