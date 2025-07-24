import streamlit as st
import random
import time

# 🌐 언어 설정
LANGS = {
    "ko": {
        "title": "🧠 기억력 숫자 합 맞추기 게임",
        "intro": "📝 게임 설명",
        "intro_text": """
- 최대 4명까지 참여 가능
- 20단계까지 진행되며, 4단계마다 난이도가 올라가
- 각 단계마다 숫자들을 보여주고, 숫자의 합을 맞춰야 해
- 맞출수록 점수를 얻고, 마지막엔 랭킹이 나와!

👉 친구들이랑 같이 하면 더 재밌어!
""",
        "start": "게임 시작",
        "name": "이름을 입력해줘",
        "ready": "준비 완료",
        "waiting": "대기 중인 플레이어",
        "start_game": "모두 준비 완료! 게임 시작!",
        "remember": "숫자를 기억해!",
        "input_sum": "숫자의 합을 입력해줘!",
        "submit": "제출",
        "result": "결과",
        "correct": "정답!",
        "wrong": "오답!",
        "answer_was": "정답은",
        "next": "다음 단계",
        "ranking": "최종 랭킹",
        "restart": "다시 시작"
    },
    "en": {
        "title": "🧠 Memory Number Sum Game",
        "intro": "📝 Game Instructions",
        "intro_text": """
- Up to 4 players can join
- There are 20 levels; every 4 levels, difficulty increases
- Remember the numbers and enter their sum
- The more correct answers, the higher your rank!

👉 Play with friends for more fun!
""",
        "start": "Start Game",
        "name": "Enter your name",
        "ready": "Ready",
        "waiting": "Waiting Players",
        "start_game": "Everyone's ready! Let's go!",
        "remember": "Remember the numbers!",
        "input_sum": "Enter the sum of the numbers!",
        "submit": "Submit",
        "result": "Results",
        "correct": "Correct!",
        "wrong": "Wrong!",
        "answer_was": "The correct sum was",
        "next": "Next Level",
        "ranking": "Final Ranking",
        "restart": "Restart"
    }
}

# ⚙️ 설정
TOTAL_LEVELS = 20
SHOW_TIME = 3
MAX_PLAYERS = 4
MIN_PLAYERS = 2

# 난이도 설정 함수
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

# 세션 초기화
if "lang" not in st.session_state:
    lang = st.selectbox("🌐 언어 선택 / Language", ["한국어", "English"])
    st.session_state.lang = "ko" if lang == "한국어" else "en"
    st.stop()

L = LANGS[st.session_state.lang]

if "step" not in st.session_state:
    st.session_state.step = "intro"
if "players" not in st.session_state:
    st.session_state.players = {}
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

st.title(L["title"])

# 1. 설명
if st.session_state.step == "intro":
    st.header(L["intro"])
    st.markdown(L["intro_text"])
    if st.button(L["start"]):
        st.session_state.step = "lobby"
        st.experimental_rerun()

# 2. 대기실
elif st.session_state.step == "lobby":
    name = st.text_input(f"🧑 {L['name']}")
    if name:
        if name not in st.session_state.players:
            st.session_state.players[name] = True
            st.session_state.scores[name] = 0

        st.subheader(L["waiting"])
        for p in st.session_state.players:
            st.write(f"✅ {p} {'(Ready)' if p in st.session_state.ready else ''}")

        if name not in st.session_state.ready:
            if st.button(L["ready"]):
                st.session_state.ready.add(name)
                st.experimental_rerun()

        if (
            len(st.session_state.ready) == len(st.session_state.players)
            and MIN_PLAYERS <= len(st.session_state.players) <= MAX_PLAYERS
        ):
            st.success(L["start_game"])
            st.session_state.step = "show"
            st.experimental_rerun()

# 3. 숫자 보여주기
elif st.session_state.step == "show":
    st.subheader(L["remember"])
    count, max_val = get_level_setting(st.session_state.level)
    st.session_state.numbers = [random.randint(1, max_val) for _ in range(count)]
    st.write(" + ".join(map(str, st.session_state.numbers)))
    time.sleep(SHOW_TIME)
    st.session_state.step = "guess"
    st.experimental_rerun()

# 4. 정답 입력
elif st.session_state.step == "guess":
    name = st.text_input(f"🧑 {L['name']}", key="guess_name")

    if name in st.session_state.players and name not in st.session_state.answers:
        st.subheader(L["input_sum"])
        ans = st.number_input("➡️", step=1, format="%d", key=f"ans_{name}")
        if st.button(L["submit"], key=f"submit_{name}"):
            st.session_state.answers[name] = ans
            correct = sum(st.session_state.numbers)
            if ans == correct:
                st.session_state.scores[name] += 1
            if len(st.session_state.answers) == len(st.session_state.players):
                st.session_state.step = "result"
            st.experimental_rerun()

    elif name in st.session_state.answers:
        st.success("✅ 제출 완료! 기다려주세요.")

# 5. 결과 및 다음 단계
elif st.session_state.step == "result":
    st.subheader(L["result"])
    correct = sum(st.session_state.numbers)
    st.write(f"{L['answer_was']}: {correct}")
    for player, ans in st.session_state.answers.items():
        if ans == correct:
            st.success(f"{player}: ✅ {L['correct']}")
        else:
            st.error(f"{player}: ❌ {L['wrong']} ({ans})")

    if st.session_state.level < TOTAL_LEVELS:
        if st.button(L["next"]):
            st.session_state.level += 1
            st.session_state.answers = {}
            st.session_state.step = "show"
            st.experimental_rerun()
    else:
        st.session_state.step = "ranking"
        st.experimental_rerun()

# 6. 랭킹
elif st.session_state.step == "ranking":
    st.header(f"🏆 {L['ranking']}")
    ranked = sorted(st.session_state.scores.items(), key=lambda x: -x[1])
    for i, (name, score) in enumerate(ranked, 1):
        st.write(f"{i}등. {name} - {score}점")

    if st.button(L["restart"]):
        for key in ["step", "players", "ready", "level", "numbers", "answers", "scores"]:
            if key in st.session_state:
                del st.session_state[key]
        st.experimental_rerun()
