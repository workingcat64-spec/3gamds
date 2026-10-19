
import random
import streamlit as st

# 페이지 설정
st.set_page_config(
    page_title="가위바위보 챌린지",
    page_icon="✊",
    layout="centered",
)

# 게임 선택지
CHOICES = {
    "가위": "✌️",
    "바위": "✊",
    "보": "✋",
}

# 승패 판정
def get_result(user_choice, computer_choice):
    if user_choice == computer_choice:
        return "draw", "🤝 무승부!", "두 사람의 선택이 같아요!"

    win_cases = {
        ("가위", "보"),
        ("바위", "가위"),
        ("보", "바위"),
    }

    if (user_choice, computer_choice) in win_cases:
        return "win", "🎉 승리!", "완벽해요! 컴퓨터를 이겼어요!"

    return "lose", "😵 패배!", "아쉬워요! 다음 판에는 이길 수 있어요!"


# 세션 상태 초기화
if "wins" not in st.session_state:
    st.session_state.wins = 0
if "losses" not in st.session_state:
    st.session_state.losses = 0
if "draws" not in st.session_state:
    st.session_state.draws = 0
if "last_game" not in st.session_state:
    st.session_state.last_game = None


# 디자인 CSS
st.markdown(
    """
    <style>
    .stApp {
        background: linear-gradient(180deg, #eef2ff 0%, #f8fafc 55%, #ffffff 100%);
    }

    .main .block-container {
        max-width: 760px;
        padding-top: 2rem;
        padding-bottom: 3rem;
    }

    .hero {
        background: linear-gradient(135deg, #6366f1, #8b5cf6);
        color: white;
        padding: 2rem 1.5rem;
        border-radius: 24px;
        text-align: center;
        box-shadow: 0 10px 30px rgba(99, 102, 241, 0.20);
        margin-bottom: 1.5rem;
    }

    .hero h1 {
        font-size: 2.1rem;
        margin: 0;
        font-weight: 800;
    }

    .hero p {
        margin: 0.8rem 0 0;
        font-size: 1rem;
        opacity: 0.95;
    }

    .section-title {
        text-align: center;
        color: #312e81;
        font-size: 1.25rem;
        font-weight: 800;
        margin: 1.2rem 0 0.5rem;
    }

    .game-card {
        background: white;
        padding: 1.2rem;
        border: 1px solid #e0e7ff;
        border-radius: 20px;
        text-align: center;
        box-shadow: 0 5px 18px rgba(30, 41, 59, 0.05);
        height: 100%;
    }

    .game-emoji {
        font-size: 3.5rem;
        margin: 0.4rem 0;
    }

    .game-label {
        color: #64748b;
        font-size: 0.9rem;
        font-weight: 700;
    }

    .game-choice {
        color: #1e1b4b;
        font-size: 1.4rem;
        font-weight: 800;
    }

    .result-card {
        background: white;
        padding: 1.5rem 1rem;
        border-radius: 22px;
        text-align: center;
        border: 2px solid #c7d2fe;
        margin: 1rem 0;
    }

    .result-title {
        font-size: 2rem;
        font-weight: 900;
        color: #4338ca;
        margin-bottom: 0.4rem;
    }

    .result-description {
        font-size: 1rem;
        color: #475569;
    }

    div.stButton > button {
        border-radius: 14px;
        font-weight: 700;
        min-height: 3rem;
        transition: all 0.2s ease;
    }

    div.stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #6366f1, #8b5cf6);
        border: none;
    }

    .footer {
        color: #94a3b8;
        text-align: center;
        font-size: 0.85rem;
        margin-top: 2rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# 상단 제목
st.markdown(
    """
    <div class="hero">
        <h1>✊ 가위바위보 챌린지</h1>
        <p>운과 전략으로 컴퓨터를 이겨 보세요! 🎮</p>
    </div>
    """,
    unsafe_allow_html=True,
)

# 점수판
st.markdown(
    '<div class="section-title">🏆 나의 전적</div>',
    unsafe_allow_html=True,
)

score1, score2, score3 = st.columns(3)

with score1:
    st.metric("🎉 승리", st.session_state.wins)

with score2:
    st.metric("😵 패배", st.session_state.losses)

with score3:
    st.metric("🤝 무승부", st.session_state.draws)

total_games = (
    st.session_state.wins
    + st.session_state.losses
    + st.session_state.draws
)

if total_games > 0:
    win_rate = st.session_state.wins / total_games * 100
else:
    win_rate = 0.0

st.progress(win_rate / 100)
st.caption(f"총 {total_games}판 플레이 · 승률 {win_rate:.1f}%")


# 선택 영역
st.markdown(
    '<div class="section-title">👇 무엇을 낼까요?</div>',
    unsafe_allow_html=True,
)

st.write("가위, 바위, 보 중 하나를 선택하고 대결을 시작하세요!")

choice_columns = st.columns(3)
user_choice = None

choice_names = ["가위", "바위", "보"]

for i, choice in enumerate(choice_names):
    with choice_columns[i]:
        st.markdown(
            f"""
            <div class="game-card">
                <div class="game-emoji">{CHOICES[choice]}</div>
                <div class="game-choice">{choice}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        if st.button(
            f"{choice} 선택하기",
            key=f"choose_{choice}",
            use_container_width=True,
            type="primary" if choice == "바위" else "secondary",
        ):
            user_choice = choice

# 게임 실행
if user_choice is not None:
    computer_choice = random.choice(choice_names)

    result_type, result_title, result_message = get_result(
        user_choice,
        computer_choice,
    )

    if result_type == "win":
        st.session_state.wins += 1
        st.balloons()
    elif result_type == "lose":
        st.session_state.losses += 1
    else:
        st.session_state.draws += 1

    st.session_state.last_game = {
        "user": user_choice,
        "computer": computer_choice,
        "type": result_type,
        "title": result_title,
        "message": result_message,
    }

# 최근 대결 결과
if st.session_state.last_game is not None:
    game = st.session_state.last_game

    st.markdown("---")
    st.markdown(
        '<div class="section-title">⚔️ 대결 결과</div>',
        unsafe_allow_html=True,
    )

    left, middle, right = st.columns([2, 1, 2])

    with left:
        st.markdown(
            f"""
            <div class="game-card">
                <div class="game-label">🙋 나의 선택</div>
                <div class="game-emoji">{CHOICES[game["user"]]}</div>
                <div class="game-choice">{game["user"]}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with middle:
        st.markdown(
            """
            <div style="text-align:center; padding-top:2.5rem;">
                <div style="font-size:1.8rem; font-weight:900; color:#8b5cf6;">
                    VS
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with right:
        st.markdown(
            f"""
            <div class="game-card">
                <div class="game-label">🤖 컴퓨터의 선택</div>
                <div class="game-emoji">{CHOICES[game["computer"]]}</div>
                <div class="game-choice">{game["computer"]}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    if game["type"] == "win":
        st.success(f'{game["title"]}\n\n{game["message"]}')
    elif game["type"] == "lose":
        st.error(f'{game["title"]}\n\n{game["message"]}')
    else:
        st.info(f'{game["title"]}\n\n{game["message"]}')

    if st.button(
        "🔄 한 판 더 하기",
        use_container_width=True,
        type="primary",
    ):
        st.rerun()

# 점수 초기화
st.markdown("---")

if st.button("🧹 점수 초기화", use_container_width=True):
    st.session_state.wins = 0
    st.session_state.losses = 0
    st.session_state.draws = 0
    st.session_state.last_game = None
    st.rerun()

st.markdown(
    """
    <div class="footer">
        ✨ 가위바위보 챌린지 · 오늘의 승자는 바로 당신! ✨
    </div>
    """,
    unsafe_allow_html=True,
)
