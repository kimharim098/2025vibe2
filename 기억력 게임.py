import streamlit as st
import random
import time

# =============================
# 🌐 다국어 지원 텍스트
# =============================
TEXT = {
    "ko": {
        "title": "기억력 숫자 게임",
        "intro": "이 게임은 20단계까지 숫자의 합을 맞추는 기억력 게임입니다.\n4단계마다 난이도가 상승하며, 최대 4명이 함께 플레이할 수 있습니다.",
        "start": "게임 시작",
        "players": "플레이어 수 (1~4명):",
        "names": "플레이어 이름 입력:",
        "show_numbers": "숫자 보여주기",
        "guess_sum": "숫자의 합을 입력하세요:",
        "correct": "정답입니다!",
        "wrong": "틀렸어요! 정답은",
        "next": "다음 단계",
        "ranking": "최종 랭킹",
        "language": "언어 선택",
    },
    "en": {
        "title": "Memory Number Game",
        "intro": "This is a memory game where you guess the sum of numbers for 20 stages.\nDifficulty increases every 4 stages and up to 4 players can play.",
        "start": "Start Game",
        "players": "Number of Players (1-4):",
        "names": "Enter Player Names:",
        "show_numbers": "Show Numbers",
        "guess_sum": "Enter the sum of the numbers:",
        "correct": "Correct!",
        "wrong": "Wrong! The answer was",
        "next": "Next Stage",
        "ranking": "Final Ranking",
        "language": "Choose Language",
    }
}

# =============================
# 상태 초기화
# =============================
if "lang" not in st.session_state:
    st.session_state.lang = "ko"
if "step" not in st.session_state:
    st.session_state.step = "intro"
if "stage" not in st.session_state:
    st.session_state.stage = 1
if "scores" not in st.session_state:
    st.session_state.scores = {}
if "players" not in st.session_state:
    st.session_state.players = []
if "numbers" not in st.session_state:
    st.session_state.numbers = []

T = TEXT[st.session_state.lang]

# =============================
# 언어 선택
# =============================
st.sidebar.title(T["language"])
lang_select = st.sidebar.radio("", ["한국어", "English"])
if lang_select == "English":
    st.session_state.lang = "en"
else:
    st.session_state.lang = "ko"
T = TEXT[st.session_state.lang]

st.title(T["title"])

# =============================
# 단계별 난이도 설정
# =============================
def get_level(stage):
    if stage <= 4:
        return 3, 9
    elif stage <= 8:
        return 4, 20
    elif stage <= 12:
        return 5, 30
    elif stage <= 16:
        return 6, 50
    else:
        return 7, 99

# =============================
# 게임 단계별 화면
# =============================
if st.session_state.step == "intro":
    st.markdown(T["intro"])
    players_num = st.slider(T["players"], 1, 4, 1)
    names = []
    for i in range(players_num):
        name = st.text_input(f"{T['names']} {i+1}", key=f"name_{i}")
        if name:
            names.append(name)
    if len(names) == players_num:
        if st.button(T["start"]):
            st.session_state.players = names
            for n in names:
                st.session_state.scores[n] = 0
            st.session_state.step = "show"
            st.experimental_rerun()

elif st.session_state.step == "show":
    count, maxnum = get_level(st.session_state.stage)
    st.session_state.numbers = [random.randint(1, maxnum) for _ in range(count)]
    st.write(f"Stage {st.session_state.stage} : {count} numbers")
    st.write(" + ".join(map(str, st.session_state.numbers)))
    time.sleep(2.5 + count * 0.3)
    st.session_state.step = "guess"
    st.experimental_rerun()

elif st.session_state.step == "guess":
    correct = sum(st.session_state.numbers)
    guesses = {}
    for name in st.session_state.players:
        guesses[name] = st.number_input(f"{name} - {T['guess_sum']}", step=1, key=f"guess_{name}")
    if st.button(T["next"]):
        for name in st.session_state.players:
            if guesses[name] == correct:
                st.success(f"{name} - {T['correct']}")
                st.session_state.scores[name] += 1
            else:
                st.error(f"{name} - {T['wrong']} {correct}")
        if st.session_state.stage >= 20:
            st.session_state.step = "end"
        else:
            st.session_state.stage += 1
            st.session_state.step = "show"
        st.experimental_rerun()

elif st.session_state.step == "end":
    st.subheader(T["ranking"])
    ranking = sorted(st.session_state.scores.items(), key=lambda x: x[1], reverse=True)
    for i, (name, score) in enumerate(ranking, start=1):
        st.write(f"{i}위 - {name}: {score}점")
    if st.button("다시 시작" if st.session_state.lang == "ko" else "Restart"):
        for k in ["step", "stage", "scores", "players", "numbers"]:
            st.session_state.pop(k, None)
        st.experimental_rerun()
