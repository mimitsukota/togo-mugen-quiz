import streamlit as st
import google.generativeai as genai
from gtts import gTTS
import json

# --- 1. カギを読み込む (Secretsから) ---
try:
    api_key = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=api_key)
except Exception as e:
    st.error("カギが まだセットされていないみたい！ 金庫(Secrets)をチェックしてね。")
    st.stop()

st.title("🦖 AIむげんクイズ 👻")

# --- 2. クイズをAIに作ってもらう (5歳向け最新版) ---
def create_new_quiz():
    # 2026年4月時点で最も安定しているモデル名
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    # 5歳向けに、少し特徴を増やした命令にしています
    prompt = "5歳児向けの知育クイズ（恐竜、妖怪、動物から1つ）を1問作って。特徴を2つ以上入れて、少し考えさせる楽しい問題にして。必ず以下の形式のJSONデータだけを出力して。解説は不要。 {'genre': 'ジャンル', 'q': '問題文', 'a': '答えのひらがな', 'img': '絵文字'}"
    
    try:
        # AIに「おしゃべり禁止、データだけ頂戴」と命令
        response = model.generate_content(
            prompt,
            generation_config={"response_mime_type": "application/json"}
        )
        # AIの答えをプログラムが読める形に変換
        return json.loads(response.text)
    except Exception as e:
        # 万が一AIがエラーを出した時の「予備問題」
        st.warning(f"AIが まだ かくれんぼしてるよ (理由: {e})")
        return {"genre": "どうぶつ", "q": "くびが ながくて、せが とっても たかい、きいろい どうぶつは なーんだ？", "a": "きりん", "img": "🦒"}

# --- 3. アプリの動きを管理する仕組み ---
# 「つぎのもんだいに する」ボタンが押されたら新しく作る
if st.button("🌟 つぎの もんだいに する"):
    st.session_state.quiz_data = create_new_quiz()
    st.rerun()

# 最初に画面を開いたときに1問目を作る
if 'quiz_data' not in st.session_state:
    st.session_state.quiz_data = create_new_quiz()

q = st.session_state.quiz_data

# --- 4. 画面の表示 ---
st.info(f"今回のジャンル： {q['genre']}")
st.subheader(q['q'])

# 声で聞くボタン
if st.button("🔊 もんだいを きく"):
    gTTS(q['q'], lang='ja').save("q.mp3")
    st.audio("q.mp3")

# 答えを入力する場所
ans = st.text_input("こたえは なあに？", key="input_box")

# 答え合わせボタン
if st.button("こたえあわせ"):
    if ans in q['a'] or q['a'] in ans:
        st.balloons()
        st.success(f"あたり！ せいかいは「{q['a']}」だよ！ {q['img']}")
    elif ans == "":
        st.write("なにか かいてみてね！")
    else:
        st.error("おしい！ もういちど かんがえてみてね。")
