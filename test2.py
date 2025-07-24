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
        "lose": "졌어요",
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
        "lose": "You lose",
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
        "button": "查看结果",
        "thinking": "电脑思考中...",
        "your_choice": "你的选择:",
        "computer_choice": "电脑的选择:",
        "tie": "平局! 🤝",
        "win": "你赢了! 🎉",
        "lose": "你输了",
        "score": "分数",
        "win_count": "赢了:",
        "lose_count": "输了:",
        "tie_count": "平局:",
        "reset": "重置分数",
        "mode": "选择游戏模式:",
        "single": "单人模式（对战电脑）",
        "multi": "多人模式（轮流出拳）",
        "play_again": "再来一次",
        "player1": "玩家1名字:",
        "player2": "玩家2名字:",
        "turn": "轮到:",
        "select_move": "选择剪刀、石头或布:",
        "make_move": "确认选择",
        "player_score": "玩家分数",
        "draw": "平局",
        "options": ["剪刀", "石头", "布"]
    },
    "日本語": {
        "choose": "じゃんけんの手を選んでください:",
        "button": "結果を見る",
        "thinking": "コンピューターが考えています...",
        "your_choice": "あなたの選択:",
        "computer_choice": "コンピューターの選択:",
        "tie": "あいこです！🤝",
        "win": "あなたの勝ち！🎉",
        "lose": "あなたの負けです",
        "score": "スコア",
        "win_count": "勝ち数:",
        "lose_count": "負け数:",
        "tie_count": "あいこ数:",
        "reset": "スコアをリセット",
        "mode": "ゲームモードを選択:",
        "single": "1人プレイ（コンピューターと対戦）",
        "multi": "2人プレイ（交互に出す）",
        "play_again": "もう一度プレイ",
        "player1": "プレイヤー1の名前:",
        "player2": "プレイヤー2の名前:",
        "turn": "ターン:",
        "select_move": "じゃんけんの手を選んでください:",
        "make_move": "決定",
        "player_score": "プレイヤースコア",
        "draw": "あいこ",
        "options": ["グー", "チョキ", "パー"]
    }
}

t = texts[lang]

mode = st.radio(t["mode"], [t["single"], t["multi"]])

if "score" not in st.session_state:
    st.session_state.score = {"win": 0, "lose": 0, "tie": 0}

if "multi_score" not in st.session_state:
    st.session_state.multi_score = {"player1": 0, "player2": 0, "draw": 0}

if "turn" not in st.session_state:
    st.session_state.turn = 1

if "multi_choices" not in st.session_state:
    st.session_state.multi_choices = {}

if "first_play" not in st.session_state:
    st.session_state.first_play = True

if "game_over" not in st.session_state:
    st.session_state.game_over = False

def judge(user, computer):
    wins = {
        "가위": "보",
        "바위": "가위",
        "보": "바위",
        "Scissors": "Paper",
        "Rock": "Scissors",
        "Paper": "Rock",
        "剪刀": "布",
        "石头": "剪刀",
        "布": "石头",
        "チョキ": "パー",
        "グー": "チョキ",
        "パー": "グー"
    }
    if user == computer:
        return "tie"
    elif wins.get(user) == computer:
        return "win"
    else:
        return "lose"

if mode == t["single"]:
    if not st.session_state.game_over:
        user_choice = st.radio(t["choose"], t["options"])
        if st.button(t["button"]):
            if st.session_state.first_play:
                st.write(t["thinking"])
                time.sleep(1)
                st.session_state.first_play = False

            computer_choice = random.choice(t["options"])
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

            st.session_state.game_over = True
    else:
        if st.button(t["play_again"]):
            st.session_state.game_over = False
            st
