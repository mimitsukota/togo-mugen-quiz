import streamlit as st
import google.generativeai as genai
from gtts import gTTS
import json

# --- 1. カギの設定 (StreamlitのSecretsから読み込み) ---
try:
    # 以前のアカウント「gu...」やカギ「A...0」が正しくSecretsに貼られている前提です
    api_key = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=api_key)
except:
    st.error("金庫(Secrets)にカギが入っていないようです。")
    st.stop()

st.title("🦖 AIむげんクイズ 👻")

# --- 2. AIにクイズを作らせる関数 ---
def create_new_quiz():
    # 修正：最も汎用的な「gemini-pro」という名前に変更しました
    # これにより「1.5-flashが見つからない」という404エラーを回避します
    try:
        model = genai.GenerativeModel('gemini-pro')
        
        prompt = (
            "5歳児向けの楽しい知育クイズ（恐竜、妖怪、動物のどれか）を1問作って。"
            "必ず以下のJSON形式だけで出力して。解説は不要。"
            "{'genre': 'ジャンル', 'q': '問題文', 'a': '答えのひらがな', 'img': '絵文字'}"
        )
        
        response = model.generate_content(prompt)
        # JSON部分だけを取り出すための処理
        res_text = response.text.replace('```json', '').replace('```', '').strip()
        return json.loads(res_text)
        
    except Exception as e:
        st.error(f"AIがエラーを出しました: {e}")
        # これが出た場合は、カギ自体の有効化（Terms of Service等）が未完了の可能性があります
        return {"genre": "かくれんぼ中", "q": "AIが まだ かくれんぼしているみたい。カギを もういちど 確認してね！", "a": "ごめんね", "img": "⚠️"}

# --- 3. アプリの動き（セッション管理） ---
if st.button("🌟 つぎの もんだいに する"):
    st.session_state.quiz_data = create_new_quiz()
    st.rerun()

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
        if ans in q['a'] or q['a'] in ans:
            st.balloons()
            st.success(f"あたり！ せいかいは「{q['a']}」だよ！ {q['img']}")
        else:
            st.error("おしい！ もういちど かんがえてみてね。")
