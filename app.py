import streamlit as st
import google.generativeai as genai
from gtts import gTTS
import json

# --- 1. カギの設定 (StreamlitのSecretsから読み込み) ---
try:
    api_key = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=api_key)
except:
    st.error("金庫(Secrets)にカギが入っていないようです。設定を確認してください。")
    st.stop()

st.title("🦖 AIむげんクイズ 👻")

# --- 2. AIにクイズを作らせる関数 (404エラー対策済み) ---
def create_new_quiz():
    # 404エラーを避けるため、最も安定している「gemini-1.5-flash」を指名します
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    prompt = (
        "5歳児向けの楽しい知育クイズを1問作ってください。"
        "ジャンルは『恐竜』『妖怪』『動物』のどれか。答えはひらがなで。"
        "必ず以下のJSON形式だけで出力して、余計な説明は一切書かないでください。"
        "{'genre': 'ジャンル', 'q': '問題文', 'a': '答えのひらがな', 'img': '絵文字'}"
    )
    
    try:
        # JSON形式で受け取るための最新の通信設定です
        response = model.generate_content(
            prompt,
            generation_config={"response_mime_type": "application/json"}
        )
        # AIの回答を解析
        return json.loads(response.text)
    except Exception as e:
        # もしエラーが出た場合、画面に原因を表示します
        st.error(f"AIがエラーを出しました: {e}")
        # 万が一の予備（これが出たらカギの設定にまだ問題があります）
        return {"genre": "エラー", "q": "AIが まだ かくれんぼしているみたい。カギを もういちど 確認してね！", "a": "ごめんね", "img": "⚠️"}

# --- 3. アプリの動き（セッション管理） ---
# ボタンを押したら新しい問題をAIに頼む
if st.button("🌟 つぎの もんだいに する"):
    st.session_state.quiz_data = create_new_quiz()
    st.rerun()

# 最初にアプリを開いたときの1問目を準備
if 'quiz_data' not in st.session_state or st.session_state.quiz_data is None:
    st.session_state.quiz_data = create_new_quiz()

q = st.session_state.quiz_data

# --- 4. 画面への表示 ---
if q:
    st.info(f"今回のジャンル： {q['genre']}")
    st.subheader(q['q'])

    # 音声を生成して再生するボタン
    if st.button("🔊 もんだいを きく"):
        try:
            tts = gTTS(q['q'], lang='ja')
            tts.save("q.mp3")
            st.audio("q.mp3")
        except:
            st.warning("声の準備ができませんでした。")

    # 回答欄
    ans = st.text_input("こたえは なあに？", key="input_box")

    # 答え合わせボタン
    if st.button("こたえあわせ"):
        if ans in q['a'] or q['a'] in ans:
            st.balloons()
            st.success(f"あたり！ せいかいは「{q['a']}」だよ！ {q['img']}")
        else:
            st.error("おしい！ もういちど かんがえてみてね。")
