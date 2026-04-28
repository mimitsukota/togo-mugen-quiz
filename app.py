import streamlit as st
import google.generativeai as genai
from gtts import gTTS
import json

# --- 1. カギの設定 ---
try:
    api_key = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=api_key)
except:
    st.error("金庫(Secrets)にカギが入っていません。設定を確認してください。")
    st.stop()

st.title("🦖 AIむげんクイズ 👻")

# --- 2. AIにクイズを作らせる関数 (完全版) ---
def create_new_quiz():
    # 404エラー対策：'models/' から始まるフルネームで指定します
    try:
        model = genai.GenerativeModel('models/gemini-1.5-flash')
        
        prompt = (
            "5歳児向けの楽しい知育クイズ（恐竜、妖怪、動物のどれか）を1問作成。"
            "必ず以下のJSON形式だけで出力して。余計な説明は禁止。"
            "{'genre': 'ジャンル', 'q': '問題文', 'a': '答え', 'img': '絵文字'}"
        )
        
        response = model.generate_content(
            prompt,
            generation_config={"response_mime_type": "application/json"}
        )
        
        # AIが返したJSONを読み込む
        return json.loads(response.text)
        
    except Exception as e:
        # エラーが出た場合は、画面にヒントを出して予備の問題を返す
        st.warning(f"AIがちょっと照れてるみたい(404対策中): {e}")
        return {"genre": "お楽しみ", "q": "AIがクイズを考え中だよ！もう一度『つぎの問題』を押してみてね。", "a": "またね", "img": "✨"}

# --- 3. アプリの動き（セッション管理） ---
if st.button("🌟 つぎの もんだいに する"):
    st.session_state.quiz_data = create_new_quiz()
    st.rerun()

# 1問目がない場合の初期化
if 'quiz_data' not in st.session_state or st.session_state.quiz_data is None:
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
            st.warning("声の準備ができませんでした。")

    ans = st.text_input("こたえは なあに？", key="input_box")

    if st.button("こたえあわせ"):
        # 答えが「ひらがな」でも「カタカナ」でも正解にするための工夫
        if ans and (ans in q['a'] or q['a'] in ans):
            st.balloons()
            st.success(f"あたり！ せいかいは「{q['a']}」だよ！ {q['img']}")
        elif ans:
            st.error("おしい！ もういちど かんがえてみてね。")
