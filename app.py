import streamlit as st
import random

# 페이지 기본 설정
st.set_page_config(page_title="Gender Reveal Bingo", page_icon="👶", layout="centered")

# CSS를 활용해 하트 버튼 크기와 스타일 예쁘게 지정
st.markdown("""
    <style>
    div.stButton > button {
        font-size: 30px !important;
        height: 80px !important;
        width: 100% !important;
        border-radius: 15px !important;
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
st.write(sub_title)
st.write("---")

# 2. 게임 상태(세션) 초기화
if 'board_setup' not in st.session_state:
    # 분홍 하트(💖) 5개, 파란 하트(💙) 4개 섞기
    hearts = ["💖"] * 5 + ["💙"] * 4
    random.shuffle(hearts)
    
    # 3x3 격자로 변환
    st.session_state.board = [hearts[i:i+3] for i in range(0, 9, 3)]
    # 사용자가 클릭한 칸을 기록할 행렬 (False로 초기화)
    st.session_state.revealed = [[False]*3 for _ in range(3)]
    # 찾은 분홍색 하트 개수
    st.session_state.pink_count = 0

board = st.session_state.board
revealed = st.session_state.revealed

# 3. 3x3 빙고판 화면에 그리기
for r in range(3):
    cols = st.columns(3)
    for c in range(3):
        # 이미 열린 칸인 경우 하트 표시
        if revealed[r][c]:
            cols[c].button(board[r][c], key=f"btn_{r}_{c}", disabled=True)
        else:
            # 아직 안 열린 칸은 물음표 상자 표시
            if cols[c].button("❓", key=f"btn_{r}_{c}"):
                revealed[r][c] = True
                # 분홍 하트일 경우 카운트 증가
                if board[r][c] == "💖":
                    st.session_state.pink_count += 1
                st.rerun()

st.write("---")

# 4. 성공 조건 확인 (분홍색 하트 5개가 모두 오픈되었을 때)
if st.session_state.pink_count == 5:
    st.balloons()  # 폭죽(풍선) 효과 날리기
    st.success(win_text)

# 게임 리셋 버튼
if st.button("다시 하기 / Reset 🔄", use_container_width=True):
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.rerun()