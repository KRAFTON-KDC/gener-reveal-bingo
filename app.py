import streamlit as st
import random

# 페이지 기본 설정
st.set_page_config(page_title="Gender Reveal Tarot Bingo", page_icon="🔮", layout="centered")

# 신비로운 타로 카드 감성의 고급 CSS 스타일링
st.markdown("""
    <style>
    /* 전체 배경: 깊고 어두운 우주/타로 감성 */
    .stApp {
        background: linear-gradient(135deg, #0f0c1b, #201a30, #0f0c1b);
    }
    
    /* 제목 및 레이블 텍스트 스타일 */
    h1, p, label {
        text-align: center !important;
        color: #f1e4c3 !important; /* 부드러운 골드빛 텍스트 */
        font-family: 'Georgia', serif;
    }
    
    /* 라디오 버튼 정렬 중앙 배치 */
    [data-testid="stRadio"] > div {
        justify-content: center !important;
    }

    /* 🔥 핵심: 3x3 카드가 완전히 밀착되도록 간격 제거 */
    [data-testid="stHorizontalBlock"] {
        gap: 0px !important; 
        margin-bottom: 0px !important;
        padding: 0px !important;
    }
    [data-testid="column"] {
        padding: 2px !important; /* 카드 간의 아주 미세한 경계선만 남김 */
    }
    
    /* 🔮 예쁜 타로 카드 뒷면/앞면 디자인 변경 */
    div.stButton > button {
        font-size: 32px !important;
        height: 160px !important; /* 세로가 긴 타로 카드 비율 */
        width: 100% !important;
        background: linear-gradient(145deg, #1d152b, #2d2244) !important; /* 신비로운 보랏빛 밤 */
        color: #e5c060 !important; /* 신비로운 주황/골드 빛 물음표 */
        border: 2px solid #e5c060 !important; /* 화려한 골드 테두리 */
        border-radius: 12px !important;
        box-shadow: 0px 4px 10px rgba(0,0,0,0.5), inset 0px 0px 15px rgba(229,192,96,0.2) !important; /* 내부 발광 효과 */
        text-shadow: 0px 2px 4px rgba(0,0,0,0.8);
        transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
    }
    
    /* 카드 마우스 호버 효과 */
    div.stButton > button:hover {
        transform: translateY(-4px);
        box-shadow: 0px 8px 20px rgba(229,192,96,0.4) !important;
        border-color: #fff !important;
    }
    
    /* 오픈된 타로 카드 스타일 (disabled 상태) */
    div.stButton > button:disabled {
        background: #110b1a !important;
        border: 2px solid #5a447a !important;
        opacity: 1 !important;
        transform: none !important;
        box-shadow: none !important;
    }

    /* 🚨 축하 화면 오버레이 (화면 중앙 큰 팝업창 효과) */
    .popup-overlay {
        position: fixed;
        top: 0; left: 0; width: 100vw; height: 100vh;
        background-color: rgba(10, 5, 20, 0.9);
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        z-index: 9999;
        animation: fadeIn 0.8s ease-out forwards;
    }
    
    .popup-content {
        background: linear-gradient(135deg, #2c1a4d, #140d26);
        padding: 40px 60px;
        border-radius: 25px;
        border: 3px solid #ff79c6; /* 공주님을 뜻하는 핑크 골드 테두리 */
        text-align: center;
        box-shadow: 0px 0px 50px rgba(255, 121, 198, 0.6);
        transform: scale(0.7);
        animation: popUp 0.5s 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275) forwards;
    }
    
    .popup-text {
        font-size: 45px !important;
        font-weight: bold;
        color: #ff79c6 !important;
        text-shadow: 0px 0px 20px rgba(255, 121, 198, 0.8);
        font-family: 'MaplestoryOTFBold', 'Malgun Gothic', sans-serif;
    }

    /* 애니메이션 효과 */
    @keyframes fadeIn { from { opacity: 0; } to { opacity: 1; } }
    @keyframes popUp { from { transform: scale(0.7); opacity: 0; } to { transform: scale(1); opacity: 1; } }
    </style>
""", unsafe_allow_html=True)

# 1. 언어 선택 (국문 / 영문)
language = st.radio("Language / 언어 선택", ["한국어 🇰🇷", "English 🇺🇸"])

# 언어별 텍스트 설정
if language == "한국어 🇰🇷":
    title = "🔮 꽁냥이는 공주님? 왕자님? 🔮"
    sub_title = "신비로운 타로 카드를 뒤집어 꽁냥이의 성별을 확인해보세요"
    win_text = "💖 꽁냥이는 공주님! 💖"
else:
    title = "🔮 Boy? or Girl? 🔮"
    sub_title = "Flip the tarot cards to reveal the baby's gender"
    win_text = "💖 Baby's a girl! 💖"

st.markdown(f"<h1 style='font-size: 36px; font-weight: bold;'>{title}</h1>", unsafe_allow_html=True)
st.markdown(f"<p style='font-size: 16px; margin-bottom: 30px;'>{sub_title}</p>", unsafe_allow_html=True)

# 2. 게임 상태(세션) 초기화
if 'board' not in st.session_state:
    # 분홍 하트(💖) 5개, 파란 하트(💙) 4개 조합 생성 후 셔플
    hearts = ["💖"] * 5 + ["💙"] * 4
    random.shuffle(hearts)
    
    st.session_state.board = [hearts[i:i+3] for i in range(0, 9, 3)]
    st.session_state.revealed = [[False]*3 for _ in range(3)]
    st.session_state.pink_count = 0

board = st.session_state.board
revealed = st.session_state.revealed

# 3. 3x3 밀착형 타로 빙고판 구현
for r in range(3):
    cols = st.columns(3)
    for c in range(3):
        if revealed[r][c]:
            # 뒤집힌 카드는 해당 하트 이모지를 보여줌
            cols[c].button(board[r][c], key=f"btn_{r}_{c}", disabled=True)
        else:
            # 타로 카드 뒷면 감성의 신비로운 눈 문양(✨)이나 물음표 구현
            if cols[c].button("✨", key=f"btn_{r}_{c}"):
                st.session_state.revealed[r][c] = True
                if board[r][c] == "💖":
                    st.session_state.pink_count += 1
                st.rerun()

st.write("")
st.write("")

# 4. 결과 창 (성공 시 전체 화면 중앙에 거대한 팝업창 띄우기)
if st.session_state.pink_count == 5:
    st.balloons() # 배경에 날아다니는 풍선 폭죽 효과
    
    # HTML/CSS 오버레이 팝업창 주입
    st.markdown(f"""
        <div class="popup-overlay">
            <div class="popup-content">
                <div class="popup-text">{win_text}</div>
                <p style="margin-top:20px; color:#aaa !important; font-size:16px;">축하합니다! 축복 속에서 건강하게 자라나길 바랍니다.</p>
            </div>
        </div>
    """, unsafe_allow_html=True)

# 게임 리셋 버튼
if st.button("다시 하기 / Reset 🔄", use_container_width=True):
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.rerun()
