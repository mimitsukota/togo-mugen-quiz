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
    # 修正ポイント：モデル名を「正式なフルパス」で指定します
    # これにより v1beta のエラーを力技で回避します
    try:
        # モデル指定を最も確実な形式に変更
        model = genai.GenerativeModel(model_name='models/gemini-1.5-flash')
        
        prompt = (
            "5歳児向けの楽しい知育クイズを1問作って。"
            "ジャンルは恐竜、妖怪、動物からランダムに。"
            "必ず以下のJSON形式だけで出力してください。余計な文字は一切不要です。"
            "{'genre': 'ジャンル', 'q': '問題文', 'a': '答え', 'img': '絵文字'}"
        )
        
        # 2026年の標準的な呼び出し方に整理
        response = model.generate_content(
            prompt,
            generation_config={"response_mime_type": "application/json"}
        )
        
        return json.loads(response.text)
        
    except Exception as e:
        # ここでエラーが出ても笑って飛ばせるように！
        return {"genre": "通信中", "q": f"AIがまだ照れてるよ！もう一度ボタンをポチッと！({e})", "a": "またね", "img": "⚙️"}

# --- 3. アプリの動き ---
if st.button("🌟 つぎの もんだいに する"):
    st.session_state.quiz_data = create_new_quiz()
    st.rerun()

if 'quiz_data' not in st.session_state:
    st.session_state.quiz_data = create_new_quiz()

q = st.session_state.quiz_data

# --- 4. 画面への表示 ---
if q:
    st.info(f"ジャンル： {q['genre']}")
    st.subheader(q['q'])
    
    if st.button("🔊 もんだいを きく"):
        try:
            tts = gTTS(q['q'], lang='ja')
            tts.save("q.mp3")
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
