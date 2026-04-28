import streamlit as st
import google.generativeai as genai
from gtts import gTTS
import json

# --- 1. カギの設定 (Secretsから読み込み) ---
try:
    api_key = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=api_key)
except:
    st.error("金庫(Secrets)にカギが入っていないようです。")
    st.stop()

st.title("🦖 AIむげんクイズ 👻")

# --- 2. AIにクイズを作らせる魔法の関数 ---
def create_new_quiz():
    # 無料枠が安定している「1.5-flash」を指名
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    # AIへの命令（5歳向け、JSON形式を指定）
    prompt = "5歳児向けの楽しい知育クイズを1問作って。ジャンルは恐竜、妖怪、動物から選んで。必ず以下のJSON形式だけで出力して。 {'genre': 'ジャンル', 'q': '問題文', 'a': '答えのひらがな', 'img': '絵文字'}"
    
    try:
        response = model.generate_content(
            prompt,
            generation_config={"response_mime_type": "application/json"}
        )
        # AIが書いたテキストを、プログラムが使えるデータに変換
        return json.loads(response.text)
    except Exception as e:
        # もしエラーが出たら、画面に原因を表示する
        st.error(f"AIがエラーを出しました: {e}")
        return None

# --- 3. アプリの動きを管理する仕組み ---
# 「つぎのもんだいに する」ボタン
if st.button("🌟 つぎの もんだいに する"):
    st.session_state.quiz_data = create_new_quiz()
    st.rerun()

# 最初にページを開いたときに1問目を作る
if 'quiz_data' not in st.session_state or st.session_state.quiz_data is None:
    st.session_state.quiz_data = create_new_quiz()

q = st.session_state.quiz_data

# --- 4. 画面に表示する ---
if q:
    st.info(f"今回のジャンル： {q['genre']}")
    st.subheader(q['q'])

    # 声を出すボタン
    if st.button("🔊 もんだいを きく"):
        gTTS(q['q'], lang='ja').save("q.mp3")
        st.audio("q.mp3")

    # 回答入力
    ans = st.text_input("こたえは なあに？", key="input_box")

    # 答え合わせボタン
    if st.button("こたえあわせ"):
        if ans in q['a'] or q['a'] in ans:
            st.balloons()
            st.success(f"あたり！ せいかいは「{q['a']}」だよ！ {q['img']}")
        else:
            st.error("おしい！ もういちど かんがえてみてね。")
