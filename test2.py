import streamlit as st
import random
import time
import matplotlib.pyplot as plt

st.title("가위바위보 게임 / Rock-Paper-Scissors Game")

# 다국어 선택
lang = st.selectbox("언어 선택 / Choose Language", ["한국어", "English"])

texts = {
    "한국어": {
        "choose": "가위, 바위, 보 중에서 선택하세요:",
        "button": "결과 확인",
        "thinking": "컴퓨터가 생각 중...",
        "your_choice": "당신의 선택:",
        "computer_choice": "컴퓨터의 선택:",
        "tie": "비겼어요!",
        "win": "이겼어요! 🎉",
        "lose": "졌어요 ㅠㅠ",
        "score": "점수",
        "win_count": "이긴 횟수:",
        "lose_count": "진 횟수:",
        "tie_count": "비긴 횟수:",
        "reset": "점수 초기화",
        "mode": "게임 모드 선택:",
        "single": "1인 플레이 (컴퓨터와 대결)",
        "multi": "2인 플레이 (친구와 번갈아)",
        "player1": "플레이어 1 이름:",
        "player2": "플레이어 2 이름:",
        "turn": "차례:",
        "select_move": "가위, 바위, 보 선택:",
        "make_move": "선택 완료",
        "stats": "통계 그래프",
        "player_score": "플레이어 점수",
        "draw": "무승부",
    },
    "English": {
        "choose": "Choose Rock, Paper, or Scissors:",
        "button": "Show Result",
        "thinking": "Computer is thinking...",
        "your_choice": "Your choice:",
        "computer_choice": "Computer's choice:",
        "tie": "It's a tie!",
        "win": "You win! 🎉",
        "lose": "You lose ㅠㅠ",
        "score": "Score",
        "win_count": "Wins:",
        "lose_count": "Losses:",
        "tie_count": "Ties:",
        "reset": "Reset Score",
        "mode": "Select Game Mode:",
        "single": "Single Player (vs Computer)",
        "multi": "Multiplayer (Take turns)",
        "player1": "Player 1 Name:",
        "player2": "Player 2 Name:",
        "turn": "Turn:",
        "select_move": "Choose Rock, Paper, or Scissors:",
        "make_move": "Confirm Move",
        "stats": "Statistics Chart",
        "player_score": "Player Scores",
        "draw": "Draw",
    }
}

t = texts[lang]

# 게임 모드 선택
mode = st.radio(t["mode"], [t["single"], t["multi"]])

# 점수, 선택 저장 초기화
if "score" not in st.session_state:
    st.session_state.score = {"win": 0, "lose": 0, "tie": 0}

if "multi_score" not in st.session_state:
    st.session_state.multi_score = {"player1": 0, "player2": 0, "draw": 0}

if "turn" not in st.session_state:
    st.session_state.turn = 1  # 1 or 2

if "multi_choices" not in st.session_state:
    st.session_state.multi_choices = {}

if "single_choice" not in st.session_state:
    st.session_state.single_choice = None

def judge(user, computer):
    wins = {
        "가위": "보",
        "바위": "가위",
        "보": "바위",
        "Scissors": "Paper",
        "Rock": "Scissors",
        "Paper": "Rock"
    }
    if user == computer:
        return "tie"
    elif wins.get(user) == computer:
        return "win"
    else:
        return "lose"

if mode == t["single"]:
    # 1인 플레이 (컴퓨터)
    user_choice = st.radio(t["choose"], ["가위", "바위", "보"] if lang == "한국어" else ["Scissors", "Rock", "Paper"])

    if st.button(t["button"]):
        st.write(t["thinking"])
        time.sleep(1)

        computer_choice = random.choice(["가위", "바위", "보"] if lang == "한국어" else ["Scissors", "Rock", "Paper"])
        st.write(f"### {t['your_choice']} {user_choice}")
        st.write(f"### {t['computer_choice']} {computer_choice}")

        result = judge(user_choice, computer_choice)
        if result == "win":
            st.session_state.score["win"] += 1
            st.write(f"### {t['win']}")
        elif result == "lose":
            st.session_state.score["lose"] += 1
            st.write(f"### {t['lose']}")
        else:
            st.session_state.score["tie"] += 1
            st.write(f"### {t['tie']}")

    st.write(f"## {t['score']}")
    st.write(f"{t['win_count']} {st.session_state.score['win']}")
    st.write(f"{t['lose_count']} {st.session_state.score['lose']}")
    st.write(f"{t['tie_count']} {st.session_state.score['tie']}")

elif mode == t["multi"]:
    # 2인 플레이
    player1 = st.text_input(t["player1"], value="Player1" if lang == "English" else "플레이어1")
    player2 = st.text_input(t["player2"], value="Player2" if lang == "English" else "플레이어2")

    st.write(f"## {t['turn']} {player1 if st.session_state.turn == 1 else player2}")

    move = st.radio(t["select_move"], ["가위", "바위", "보"] if lang == "한국어" else ["Scissors", "Rock", "Paper"], key="move")

    if st.button(t["make_move"]):
        current_player = "player1" if st.session_state.turn == 1 else "player2"
        st.session_state.multi_choices[current_player] = move
        st.write(f"{player1 if st.session_state.turn == 1 else player2} 선택: {move}")

        if len(st.session_state.multi_choices) == 2:
            # 두 플레이어 다 선택했으면 결과 판단
            p1_choice = st.session_state.multi_choices["player1"]
            p2_choice = st.session_state.multi_choices["player2"]

            st.write(f"{player1} 선택: {p1_choice}")
            st.write(f"{player2} 선택: {p2_choice}")

            result = judge(p1_choice, p2_choice)
            if result == "tie":
                st.session_state.multi_score["draw"] += 1
                st.write(f"### {t['tie']}")
            elif result == "win":
                st.session_state.multi_score["player1"] += 1
                st.write(f"### {player1} {t['win']}")
            else:
                st.session_state.multi_score["player2"] += 1
                st.write(f"### {player2} {t['win']}")

            # 턴 초기화 및 선택 초기화
            st.session_state.turn = 1
            st.session_state.multi_choices = {}
        else:
            # 상대방 차례로 넘김
            st.session_state.turn = 2 if st.session_state.turn == 1 else 1

    st.write(f"## {t['player_score']}")
    st.write(f"{player1}: {st.session_state.multi_score['player1']}")
    st.write(f"{player2}: {st.session_state.multi_score['player2']}")
    st.write(f"{t['draw']}: {st.session_state.multi_score['draw']}")

# 점수 초기화 버튼 (싱글 모드 점수 초기화와 멀티 모드 점수 초기화 동시에)
if st.button(t["reset"]):
    st.session_state.score = {"win": 0, "lose": 0, "tie": 0}
    st.session_state.multi_score = {"player1": 0, "player2": 0, "draw": 0}
    st.session_state.turn = 1
    st.session_state.multi_choices = {}
    st.experimental_rerun()

# 통계 그래프 (싱글 모드 기준)
if mode == t["single"]:
    labels = [t["win"], t["lose"], t["tie"]]
    sizes = [st.session_state.score["win"], st.session_state.score["lose"], st.session_state.score["tie"]]

    if sum(sizes) > 0:
        fig, ax = plt.subplots()
        ax.pie(sizes, labels=labels, autopct="%1.1f%%", startangle=90, colors=["#4CAF50", "#F44336", "#FFC107"])
        ax.axis("equal")
        st.write(f"## {t['stats']}")
        st.pyplot(fig)
