import streamlit as st
import google.generativeai as genai
from gtts import gTTS
import json

# --- 1. カギの設定 ---
try:
    api_key = st.secrets["GOOGLE_API_KEY"]
    # 窓口を「正式版(v1)」に固定するように設定
    genai.configure(api_key=api_key, transport='rest')
except:
    st.error("金庫(Secrets)の設定を確認してください。")
    st.stop()

st.title("🦖 AIむげんクイズ 👻")

def create_new_quiz():
    # 修正：最も軽量でエラーが出にくい「gemini-1.5-flash-8b」を指名
    try:
        model = genai.GenerativeModel('gemini-1.5-flash-8b')
        
        prompt = (
            "5歳児向けの楽しいクイズ（恐竜、妖怪、動物から1つ）を作って。"
            "必ず以下のJSON形式だけで出力して。余計な文字は一切不要。"
            "{'genre': 'ジャンル', 'q': '問題', 'a': '答え', 'img': '絵文字'}"
        )
        
        response = model.generate_content(
            prompt,
            generation_config={"response_mime_type": "application/json"}
        )
        
        return json.loads(response.text)
        
    except Exception as e:
        # エラーが出ても笑って次へ！
        return {"genre": "通信中", "q": f"AIがまだ寝ぼけてるよ！もう一回ボタンを押して！({e})", "a": "またね", "img": "💤"}

# --- 3. アプリの動き ---
if st.button("🌟 つぎの もんだいに する"):
    st.session_state.quiz_data = create_new_quiz()
    st.rerun()

if 'quiz_data' not in st.session_state:
    st.session_state.quiz_data = create_new_quiz()

q = st.session_state.quiz_data

# --- 4. 画面への表示 ---
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
            st.success(f"あたり！ せいかいは「{q['a']}」だよ！ {q['img']}")
        elif ans:
            st.error("おしい！ もういちど かんがえてみてね。")
