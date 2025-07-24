import streamlit as st
import random
import time

st.title("가위바위보 게임 / Rock-Paper-Scissors Game")

# 다국어 선택 (한국어, 영어)
lang = st.selectbox("언어 선택 / Choose Language", ["한국어", "English"])

# 텍스트 딕셔너리 (간단한 예)
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
    }
}

t = texts[lang]

# 점수 기록용 세션 상태 초기화
if "win" not in st.session_state:
    st.session_state.win = 0
if "lose" not in st.session_state:
    st.session_state.lose = 0
if "tie" not in st.session_state:
    st.session_state.tie = 0

user_choice = st.radio(t["choose"], ["가위", "바위", "보"] if lang=="한국어" else ["Scissors", "Rock", "Paper"])

if st.button(t["button"]):
    st.write(t["thinking"])
    time.sleep(1)  # 컴퓨터가 생각하는 딜레이

    computer_choice = random.choice(["가위", "바위", "보"] if lang=="한국어" else ["Scissors", "Rock", "Paper"])

    st.write(f"### {t['your_choice']} {user_choice}")
    st.write(f"### {t['computer_choice']} {computer_choice}")

    def judge(user, computer):
        if user == computer:
            return "tie"
        elif (user == "가위" and computer == "보") or \
             (user == "바위" and computer == "가위") or \
             (user == "보" and computer == "바위") or \
             (user == "Scissors" and computer == "Paper") or \
             (user == "Rock" and computer == "Scissors") or \
             (user == "Paper" and computer == "Rock"):
            return "win"
        else:
            return "lose"

    result = judge(user_choice, computer_choice)
    if result == "win":
        st.session_state.win += 1
        st.write(f"### {t['win']}")
    elif result == "lose":
        st.session_state.lose += 1
        st.write(f"### {t['lose']}")
    else:
        st.session_state.tie += 1
        st.write(f"### {t['tie']}")

st.write(f"## {t['score']}")
st.write(f"{t['win_count']} {st.session_state.win}")
st.write(f"{t['lose_count']} {st.session_state.lose}")
st.write(f"{t['tie_count']} {st.session_state.tie}")

if st.button(t["reset"]):
    st.session_state.win = 0
    st.session_state.lose = 0
    st.session_state.tie = 0
    st.experimental_rerun()
