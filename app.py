import streamlit as st
import google.generativeai as genai
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
    # 修正：最新モデルが「ない」と言われるなら、
    # 誰でも持っているはずの基本モデル 'gemini-pro' に戻します。
    try:
        model = genai.GenerativeModel('gemini-pro')
        
        prompt = (
            "5歳児向けの楽しい知育クイズを1問作ってください。"
            "ジャンルは恐竜、妖怪、動物からランダムに。"
            "必ず以下のJSON形式だけで出力して。余計な文字は一切不要。"
            "{'genre': 'ジャンル', 'q': '問題文', 'a': '答え', 'img': '絵文字'}"
        )
        
        # 2026年の新機能(JSONモード)を使わず、あえて「昔ながらの通信」をします
        response = model.generate_content(prompt)
        
        # AIが喋った中から強引に { } の部分だけを抜き出す除霊マジック
        t = response.text
        start = t.find('{')
        end = t.rfind('}') + 1
        return json.loads(t[start:end])
        
    except Exception as e:
        return {"genre": "深い眠り", "q": f"AIを氷水に沈めました...もう一度！({e})", "a": "またね", "img": "🧊"}

# --- 2. 動き ---
if st.button("🌟 つぎの もんだいに する"):
    st.session_state.quiz_data = create_new_quiz()
    st.rerun()

if 'quiz_data' not in st.session_state:
    st.session_state.quiz_data = create_new_quiz()

q = st.session_state.quiz_data

# --- 3. 表示 ---
if q:
    st.info(f"ジャンル： {q['genre']}")
    st.subheader(q['q'])
    ans = st.text_input("こたえは なあに？", key="input_box")
    if st.button("こたえあわせ"):
        if ans and (ans in q['a'] or q['a'] in ans):
            st.balloons()
            st.success(f"あたり！「{q['a']}」だよ {q['img']}")
