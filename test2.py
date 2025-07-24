import streamlit as st
import random
import time

st.title("가위바위보 게임 / Rock-Paper-Scissors Game")

lang = st.selectbox("언어 선택 / Choose Language / 语言选择 / 言語選択", ["한국어", "English", "中文", "日本語"])

texts = {
    "한국어": {
        "choose": "가위, 바위, 보 중에서 선택하세요:",
        "button": "결과 확인",
        "thinking": "컴퓨터가 생각 중...",
        "your_choice": "당신의 선택:",
        "computer_choice": "컴퓨터의 선택:",
        "tie": "비겼어요! 🤝",
        "win": "이겼어요! 🎉",
        "lose": "졌어요 😢",
        "score": "점수",
        "win_count": "이긴 횟수:",
        "lose_count": "진 횟수:",
        "tie_count": "비긴 횟수:",
        "reset": "점수 초기화",
        "mode": "게임 모드 선택:",
        "single": "1인 플레이 (컴퓨터와 대결)",
        "multi": "2인 플레이 (친구와 번갈아)",
        "play_again": "다시 하기",
        "player1": "플레이어 1 이름:",
        "player2": "플레이어 2 이름:",
        "turn": "차례:",
        "select_move": "가위, 바위, 보 선택:",
        "make_move": "선택 완료",
        "player_score": "플레이어 점수",
        "draw": "무승부",
        "options": ["가위", "바위", "보"]
    },
    "English": {
        "choose": "Choose Rock, Paper, or Scissors:",
        "button": "Show Result",
        "thinking": "Computer is thinking...",
        "your_choice": "Your choice:",
        "computer_choice": "Computer's choice:",
        "tie": "It's a tie! 🤝",
        "win": "You win! 🎉",
        "lose": "You lose 😢",
        "score": "Score",
        "win_count": "Wins:",
        "lose_count": "Losses:",
        "tie_count": "Ties:",
        "reset": "Reset Score",
        "mode": "Select Game Mode:",
        "single": "Single Player (vs Computer)",
        "multi": "Multiplayer (Take turns)",
        "play_again": "Play Again",
        "player1": "Player 1 Name:",
        "player2": "Player 2 Name:",
        "turn": "Turn:",
        "select_move": "Choose Rock, Paper, or Scissors:",
        "make_move": "Confirm Move",
        "player_score": "Player Scores",
        "draw": "Draw",
        "options": ["Scissors", "Rock", "Paper"]
    },
    "中文": {
        "choose": "请选择剪刀、石头或布:",
        "butt
