import streamlit as st
import google.generativeai as genai
from gtts import gTTS
import json

# --- 1. カギの設定 ---
try:
    api_key = st.secrets["GOOGLE_API_KEY"]
    # ここで「正式版(v1)」の窓口を使うように設定を確実にします
    genai.configure(api_key=api_key)
except:
    st.error("金庫(Secrets)にカギが入っていないようです。")
    st.stop()

st.title("🦖 AIむげんクイズ 👻")

# --- 2. AIにクイズを作らせる関数 (最新の正式版仕様) ---
def create_new_quiz():
    # 2026年現在、最もエラーが出にくい正式名称「gemini-1.5-flash」を使用します
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        prompt = (
            "5歳児向けの楽しい知育クイズ（恐竜、妖怪、動物のどれか）を1問作って。"
            "必ず以下のJSON形式だけで出力して。余計な説明は一切書かないで。"
            "{'genre': 'ジャンル', 'q': '問題文', 'a': '答えのひらがな', 'img': '絵文字'}"
        )
        
        # 安全にJSONを受け取るための設定
        response = model.generate_content(
            prompt,
            generation_config={"response_mime_type": "application/json"}
        )
        
        return json.loads(response.text)
        
    except Exception as e:
        # エラーが出た場合、詳細を表示して原因を突き止めやすくします
        st.error(f"AIとの接続でエラーが発生しました: {e}")
        return {"genre": "準備中", "q": "AIが まだ おねむみたい。もういちど ボタンを おしてみてね！", "a": "ごめんね", "img": "💤"}

# --- 3. アプリの動き（セッション管理） ---
if st.button("🌟 つぎの もんだいに する"):
    # 新しい問題を作る際に、キャッシュをクリアして確実にAIを呼び出します
    st.session_state.quiz_data = create_new_quiz()
    st.rerun()

if 'quiz_data' not in st.session_state or st.session_state.quiz_data is None:
    st.session_state.quiz_data = create_new_quiz()

q = st.session_state.quiz_data

# --- 4. 画面への表示 ---
if q:
    st.info(f"ジャンル： {q['genre']}")
    st.subheader(q['q'])

    if st.button("🔊 もんだいを きく"):
        try:
            gTTS(q['q'], lang='ja').save("q.mp3")
            st.audio("q.mp3")
        except:
            st.warning("声の準備ができませんでした。")

    ans = st.text_input("こたえは なあに？", key="input_box")

    if st.button("こたえあわせ"):
        if ans in q['a'] or q['a'] in ans:
            st.balloons()
            st.success(f"あたり！ せいかいは「{q['a']}」だよ！ {q['img']}")
        else:
            st.error("おしい！ もういちど かんがえてみてね。")
