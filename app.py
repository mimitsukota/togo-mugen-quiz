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
    # 修正：'models/' を外して、かつ呼び出し方式を最もシンプルな形に。
    # これで通らない場合はGoogleのサーバー側の一時的な機嫌待ちになります。
    try:
        # 名前をあえて gemini-pro に戻し、最新のAPIキーで通るか試します
        model = genai.GenerativeModel('gemini-pro')
        
        prompt = (
            "5歳児向けの楽しいクイズ（恐竜、妖怪、動物から1つ）を作って。"
            "必ず以下のJSON形式だけで出力して。余計な文字は一切不要。"
            "{'genre': 'ジャンル', 'q': '問題', 'a': '答え', 'img': '絵文字'}"
        )
        
        # response_mime_type を使わず、あえて昔ながらの自由形式で投げます
        response = model.generate_content(prompt)
        
        # AIがJSON以外の余計なことを言った場合のために、掃除する処理を追加
        raw_text = response.text.replace('```json', '').replace('```', '').strip()
        return json.loads(raw_text)
        
    except Exception as e:
        return {"genre": "通信中", "q": f"AIの布団を剥ぎ取っています...もう一度！({e})", "a": "またね", "img": "🛌"}

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
