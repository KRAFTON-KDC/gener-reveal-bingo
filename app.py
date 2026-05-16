import streamlit as st
import random

st.set_page_config(page_title="Gender Reveal Tarot Bingo", page_icon="🔮", layout="centered")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@400;700&display=swap');

    /* ── 전체 배경 ── */
    .stApp {
        background: linear-gradient(135deg, #0f0c1b, #201a30, #0f0c1b);
    }

    h1, p, label {
        text-align: center !important;
        color: #f1e4c3 !important;
        font-family: 'Cinzel', 'Georgia', serif;
    }

    /* ── 라디오 버튼 중앙 정렬 ── */
    [data-testid="stRadio"] > div {
        justify-content: center !important;
    }

    /* ── Streamlit 컬럼 레이아웃 gap 완전 제거 ── */
    [data-testid="stHorizontalBlock"] {
        gap: 0px !important;
        margin: 0px !important;
        padding: 0px !important;
    }
    [data-testid="column"] {
        padding: 0px !important;
        min-width: 0 !important;
        flex: 1 1 0% !important;
    }
    [data-testid="column"] > div,
    [data-testid="column"] > div > div {
        margin: 0 !important;
        padding: 0 !important;
        width: 100% !important;
    }
    div.stButton {
        margin: 0 !important;
        padding: 0 !important;
        width: 100% !important;
    }

    /* ── 타로 카드 기본(뒷면) ── */
    div.stButton > button {
        font-size: clamp(20px, 5vw, 36px) !important;
        /* 세로가 긴 타로 카드 비율: vw 기준으로 모바일·PC 모두 대응 */
        height: clamp(100px, 22vw, 175px) !important;
        width: 100% !important;
        background: linear-gradient(145deg, #1d152b, #2d2244) !important;
        color: #e5c060 !important;
        border: 2px solid #e5c060 !important;
        border-radius: 10px !important;
        box-shadow: inset 0px 0px 12px rgba(229,192,96,0.15) !important;
        text-shadow: 0px 2px 4px rgba(0,0,0,0.8);
        transition: all 0.25s ease;
        margin: 0 !important;
        padding: 0 !important;
        display: block !important;
    }

    div.stButton > button:hover {
        transform: translateY(-3px);
        box-shadow: 0px 6px 18px rgba(229,192,96,0.35) !important;
        border-color: #fff !important;
    }

    /* ── 뒤집힌 카드(disabled) ── */
    div.stButton > button:disabled {
        background: #110b1a !important;
        border: 2px solid #5a447a !important;
        opacity: 1 !important;
        transform: none !important;
        box-shadow: none !important;
        font-size: clamp(22px, 6vw, 40px) !important;
    }

    /* ── 결과 팝업 오버레이 ── */
    .popup-overlay {
        position: fixed;
        top: 0; left: 0; width: 100vw; height: 100vh;
        background-color: rgba(10, 5, 20, 0.92);
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        z-index: 9999;
        animation: fadeIn 0.8s ease-out forwards;
    }

    .popup-content {
        background: linear-gradient(135deg, #2c1a4d, #140d26);
        padding: clamp(24px, 5vw, 48px) clamp(28px, 8vw, 64px);
        border-radius: 22px;
        border: 3px solid #ff79c6;
        text-align: center;
        box-shadow: 0px 0px 50px rgba(255, 121, 198, 0.5);
        max-width: 90vw;
        animation: popUp 0.5s 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275) both;
    }

    .popup-text {
        font-size: clamp(22px, 5vw, 40px) !important;
        font-weight: bold;
        color: #ff79c6 !important;
        text-shadow: 0px 0px 18px rgba(255, 121, 198, 0.7);
        font-family: 'Cinzel', 'Malgun Gothic', sans-serif;
        line-height: 1.4;
    }

    @keyframes fadeIn { from { opacity: 0; } to { opacity: 1; } }
    @keyframes popUp  { from { transform: scale(0.7); opacity: 0; } to { transform: scale(1); opacity: 1; } }
    </style>
""", unsafe_allow_html=True)

# ── 언어 선택 ──────────────────────────────────────────────
language = st.radio("Language / 언어 선택", ["한국어 🇰🇷", "English 🇺🇸"])

if language == "한국어 🇰🇷":
    title     = "🔮 꽁냥이는 공주님? 왕자님? 🔮"
    sub_title = "신비로운 타로 카드를 뒤집어 꽁냥이의 성별을 확인해보세요"
    main_win  = "💖 꽁냥이는 공주님! 💖"
    sub_win   = "✨ 예쁜 이모, 삼촌들 곧 만나요! ✨"
else:
    title     = "🔮 Boy? or Girl? 🔮"
    sub_title = "Flip the tarot cards to reveal the baby's gender"
    main_win  = "💖 Your beautiful granddaughter<br>is on her way! 💖"
    sub_win   = "A little princess is coming to steal Grandma and Grandpa's hearts! 👵👴"

st.markdown(f"<h1 style='font-size:clamp(22px,5vw,36px); font-weight:bold;'>{title}</h1>", unsafe_allow_html=True)
st.markdown(f"<p style='font-size:clamp(13px,3vw,16px); margin-bottom:24px;'>{sub_title}</p>", unsafe_allow_html=True)

# ── 세션 초기화 ────────────────────────────────────────────
if 'board' not in st.session_state:
    hearts = ["💖"] * 5 + ["💙"] * 4
    random.shuffle(hearts)
    st.session_state.board    = [hearts[i:i+3] for i in range(0, 9, 3)]
    st.session_state.revealed = [[False]*3 for _ in range(3)]
    st.session_state.pink_count = 0

board    = st.session_state.board
revealed = st.session_state.revealed

# ── 3×3 빙고판 ─────────────────────────────────────────────
for r in range(3):
    cols = st.columns(3)
    for c in range(3):
        if revealed[r][c]:
            cols[c].button(board[r][c], key=f"btn_{r}_{c}", disabled=True)
        else:
            if cols[c].button("✨", key=f"btn_{r}_{c}"):
                st.session_state.revealed[r][c] = True
                if board[r][c] == "💖":
                    st.session_state.pink_count += 1
                st.rerun()

st.write("")

# ── 결과 팝업 ──────────────────────────────────────────────
if st.session_state.pink_count == 5:
    st.balloons()
    st.markdown(f"""
        <div class="popup-overlay">
            <div class="popup-content">
                <div class="popup-text">{main_win}</div>
                <p style="margin-top:20px; color:#f1e4c3 !important;
                          font-size:clamp(15px,3vw,22px); line-height:1.6;
                          font-weight:bold; font-family:'Malgun Gothic',sans-serif;">
                    {sub_win}
                </p>
            </div>
        </div>
    """, unsafe_allow_html=True)

# ── 리셋 버튼 ──────────────────────────────────────────────
if st.button("다시 하기 / Reset 🔄", use_container_width=True):
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.rerun()
