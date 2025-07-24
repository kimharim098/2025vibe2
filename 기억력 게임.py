import streamlit as st
import random
import time

# 다국어 텍스트
TEXTS = {
    "ko": {
        "title": "🧠 기억력 숫자 합 맞추기 게임",
        "intro": """이 게임은 최대 4명이 함께하는 기억력 게임입니다.
20단계까지 숫자의 합을 맞추고, 4단계마다 난이도가 올라갑니다.
숫자를 잘 기억하고 합을 맞춰보세요!""",
        "start": "게임 시작",
        "players": "플레이어 수 (1~4명)",
        "input_name": "플레이어 이름 입력",
        "ready": "준비 완료",
        "waiting": "대기 중인 플레이어",
        "all_ready": "모두 준비 완료! 게임 시작합니다.",
        "remember": "아래 숫자들을 기억하세요!",
        "time_left": "숫자 사라질 때까지 남은 시간:",
        "input_sum": "숫자의 합을 입력하세요",
        "submit": "제출",
        "correct": "정답입니다!",
        "wrong": "틀렸어요! 정답은",
        "next": "다음 단계",
        "ranking": "최종 랭킹",
        "restart": "다시 시작",
        "language": "언어 선택",
        "already_submitted": "이미 제출하셨습니다. 기다려주세요."
    },
    "en": {
        "title": "🧠 Memory Number Sum Game",
        "intro": """This game is a memory game for up to 4 players.
Guess the sum of numbers up to 20 levels.
Difficulty increases every 4 levels.
Try to remember and sum the numbers!""",
        "start": "Start Game",
        "players": "Number of Players (1~4)",
        "input_name": "Enter Player Name",
        "ready": "Ready",
        "waiting": "Waiting Players",
        "all_ready": "All players ready! Starting game.",
        "remember": "Remember these numbers!",
        "time_left": "Time left before numbers disappear:",
        "input_sum": "Enter the sum of numbers",
        "submit": "Submit",
        "correct": "Correct!",
        "wrong": "Wrong! The answer was",
        "next": "Next Level",
        "ranking": "Final Ranking",
        "restart": "Restart",
        "language": "Choose Language",
        "already_submitted": "You already submitted. Please wait."
    }
}

TOTAL_LEVELS = 20
MAX_PLAYERS = 4
MIN_PLAYERS = 1
SHOW_TIME = 5  # 숫자 보여주는 시간(초)

# 난이도 설정
def get_level_setting(level):
    if level <= 4:
        return 3, 9
    elif level <= 8:
        return 4, 20
    elif level <= 12:
        return 5, 30
    elif level <= 16:
        return 6, 50
    else:
        return 7, 99

# 상태 초기화
if "lang" not in st.session_state:
    lang_choice = st.sidebar.radio("🌐 Language / 언어 선택", ["한국어", "English"])
    st.session_state.lang = "ko" if lang_choice == "한국어" else "en"
    st.stop()

L = TEXTS[st.session_state.lang]

if "step" not in st.session_state:
    st.session_state.step = "intro"

if "players" not in st.session_state:
    st.session_state.players = []

if "ready" not in st.session_state:
    st.session_state.ready = set()

if "level" not in st.session_state:
    st.session_state.level = 1

if "numbers" not in st.session_state:
    st.session_state.numbers = []

if "answers" not in st.session_state:
    st.session_state.answers = {}

if "scores" not in st.session_state:
    st.session_state.scores = {}

if "show_start_time" not in st.session_state:
    st.session_state.show_start_time = None

st.title(L["title"])

# 1. 게임 소개 및 플레이어 이름 입력
if st.session_state.step == "intro":
    st.write(L["intro"])
    players_num = st.slider(L["players"], MIN_PLAYERS, MAX_PLAYERS, 1)

    names = []
    for i in range(players_num):
        name = st.text_input(f"{L['input_name']} {i+1}", key=f"name_{i}")
        if name:
            names.append(name)

    if len(names) == players_num:
        if st.button(L["start"]):
            st.session_state.players = names
            st.session_state.scores = {n: 0 for n in names}
            st.session_state.ready = set()
            st.session_state.level = 1
            st.session_state.step = "lobby"
            st.experimental_rerun()

# 2. 대기실, 준비하기
elif st.session_state.step == "lobby":
    st.header(L["waiting"])
    for p in st.session_state.players:
        st.write(f"- {p} {'✅' if p in st.session_state.ready else '❌'}")

    name = st.text_input(L["input_name"], key="lobby_name")
    if name and name in st.session_state.players and name not in st.session_state.ready:
        if st.button(L["ready"]):
            st.session_state.ready.add(name)
            st.experimental_rerun()

    if len(st.session_state.ready) == len(st.session_state.players):
        st.success(L["all_ready"])
        st.session_state.step = "show"
        st.session_state.show_start_time = time.time()
        st.session_state.numbers = []
        st.experimental_rerun()

# 3. 숫자 보여주기
elif st.session_state.step == "show":
    st.header(L["remember"])
    count, max_num = get_level_setting(st.session_state.level)
    if not st.session_state.numbers:
        st.session_state.numbers = [random.randint(1, max_num) for _ in range(count)]

    st.write(" + ".join(map(str, st.session_state.numbers)))

    elapsed = time.time() - st.session_state.show_start_time
    if elapsed >= SHOW_TIME:
        st.session_state.step = "guess"
        st.session_state.show_start_time = None
        st.experimental_rerun()
    else:
        st.info(f"{L['time_left']} {SHOW_TIME - int(elapsed)}초")
        st.experimental_rerun()

# 4. 답 입력
elif st.session_state.step == "guess":
    st.header(L["input_sum"])
    correct_sum = sum(st.session_state.numbers)

    name = st.text_input(L["input_name"], key="guess_name")
    if name and name in st.session_state.players:
        if name in st.session_state.answers:
            st.success(L["already_submitted"])
        else:
            answer = st.number_input("", step=1, format="%d", key=f"answer_{name}")
            if st.button(L["submit"], key=f"submit_{name}"):
                st.session_state.answers[name] = answer
                if answer == correct_sum:
                    st.session_state.scores[name] += 1
                if len(st.session_state.answers) == len(st.session_state.players):
                    st.session_state.step = "result"
                st.experimental_rerun()

# 5. 결과 및 다음 단계 or 랭킹
elif st.session_state.step == "result":
    st.header(L["result"])
    correct_sum = sum(st.session_state.numbers)
    st.write(f"{L['wrong']} {correct_sum}")

    for p in st.session_state.players:
        ans = st.session_state.answers.get(p)
        if ans == correct_sum:
            st.success(f"{p}: {L['correct']}")
        else:
            st.error(f"{p}: {L['wrong']} {correct_sum}")

    if st.session_state.level < TOTAL_LEVELS:
        if st.button(L["next"]):
            st.session_state.level += 1
            st.session_state.numbers = []
            st.session_state.answers = {}
            st.session_state.step = "show"
            st.session_state.show_start_time = time.time()
            st.experimental_rerun()
    else:
        if st.button(L["ranking"]):
            st.session_state.step = "ranking"
            st.experimental_rerun()

# 6. 최종 랭킹
elif st.session_state.step == "ranking":
    st.header(L["ranking"])
    ranking = sorted(st.session_state.scores.items(), key=lambda x: x[1], reverse=True)
    for i, (name, score) in enumerate(ranking, 1):
        st.write(f"{i}위: {name} - {score}점")
    if st.button(L["restart"]):
        for key in ["step", "players", "ready", "level", "numbers", "answers", "scores", "show_start_time"]:
            if key in st.session_state:
                del st.session_state[key]
        st.experimental_rerun()
