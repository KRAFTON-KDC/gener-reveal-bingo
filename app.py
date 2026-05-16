import streamlit as st
import random

# 페이지 기본 설정
st.set_page_config(page_title="Gender Reveal Bingo", page_icon="👶", layout="centered")

# CSS를 활용해 카드 간격을 줄이고 디자인을 스크린샷처럼 예쁘게 수정
st.markdown("""
    <style>
    /* 전체 배경을 어둡게 */
    .stApp {
        background-color: #11141a;
    }
    
    /* 3x3 빙고판을 감싸는 컨테이너 간격 조절 */
    [data-testid="stHorizontalBlock"] {
        gap: 15px !important; /* 카드 좌우 간격을 좁게 설정 */
        margin-bottom: 15px;  /* 카드 상하 간격 설정 */
    }
    
    /* 버튼(카드) 디자인 수정 */
    div.stButton > button {
        font-size: 28px !important;
        height: 140px !important; /* 가로세로 비율을 스크린샷처럼 세로가 길게 설정 */
        width: 100% !important;
        background-color: #21242c !important; /* 카드 기본 배경색 */
        color: #ff4a4a !important;            /* 물음표(?) 색상 (주황/빨강 계열) */
        border: 1px solid #31353f !important; /* 카드 테두리 선 */
        border-radius: 20px !important;       /* 부드러운 라운드 카드 효과 */
        transition: all 0.3s ease;
    }
    
    /* 카드가 뒤집혔을 때(disabled 상태)의 스타일 */
    div.stButton > button:disabled {
        background-color: #1a1c23 !important;
        border: 1px solid #414654 !important;
        color: white !important;
        opacity: 1 !important; /* 흐려짐 방지 */
    }
    </style>
""", unsafe_allow_html=True)

# 1. 언어 선택 (국문 / 영문)
language = st.radio("Language / 언어 선택", ["한국어 🇰🇷", "English 🇺🇸"], horizontal=True)

# 언어별 텍스트 설정
if language == "한국어 🇰🇷":
    title = "👶 꽁냥이는 공주님? 왕자님? 👶"
    sub_title = "빙고 칸을 하나씩 눌러 꽁냥이의 성별을 확인해보세요!"
    win_text = "🎉 꽁냥이는 공주님! 🎉"
else:
    title = "👶 Boy? or Girl? 👶"
    sub_title = "Click the cells one by one to reveal the baby's gender!"
    win_text = "🎉 Baby's a girl! 🎉"

st.title(title)
st.markdown(f"<p style='color: #8a8f98;'>{sub_title}</p>", unsafe_allow_html=True)
st.write("---")

# 2. 게임 상태(세션) 초기화
if 'board' not in st.session_state:
    # 분홍 하트(💖) 5개, 파란 하트(💙) 4개 섞기
    hearts = ["💖"] * 5 + ["💙"] * 4
    random.shuffle(hearts)
    
    # 데이터 저장
    st.session_state.board = [hearts[i:i+3] for i in range(0, 9, 3)]
    st.session_state.revealed = [[False]*3 for _ in range(3)]
    st.session_state.pink_count = 0

# 상태 동기화
board = st.session_state.board
revealed = st.session_state.revealed

# 3. 3x3 빙고판 화면에 그리기
for r in range(3):
    cols = st.columns(3) # 3열 레이러웃 생성
    for c in range(3):
        # 이미 뒤집힌 카드인 경우 하트 표시
        if revealed[r][c]:
            cols[c].button(board[r][c], key=f"btn_{r}_{c}", disabled=True)
        else:
            # 아직 안 뒤집힌 카드는 주황색 물음표(?) 표시
            if cols[c].button("?", key=f"btn_{r}_{c}"):
                st.session_state.revealed[r][r if r==c else c] = True # 세션 상태 직접 변경
                st.session_state.revealed[r][c] = True
                
                # 분홍 하트일 경우 카운트 증가
                if board[r][c] == "💖":
                    st.session_state.pink_count += 1
                
                # 버튼을 누른 즉시 화면을 새로고침하여 카드가 뒤집히도록 처리
                st.rerun()

st.write("---")

# 4. 성공 조건 확인 (분홍색 하트 5개가 모두 오픈되었을 때)
if st.session_state.pink_count == 5:
    st.balloons()  # 폭죽 효과
    st.success(win_text)

# 게임 리셋 버튼
if st.button("다시 하기 / Reset 🔄", use_container_width=True):
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.rerun()
