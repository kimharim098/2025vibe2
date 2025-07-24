import streamlit as st
import random
import time

TOTAL_LEVELS = 20
SHOW_TIME = 5
MAX_PLAYERS = 4

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

# 초기화
for key in ["step", "players", "ready", "level", "numbers", "answers", "scores", "show_start_time"]:
    if key not in st.session_state:
        if key == "step":
            st.session_state.step = "intro"
        elif key == "players":
            st.session_state.players = []
        elif key == "ready":
            st.session_state.ready = set()
        elif key == "level":
            st.session_state.level = 1
        elif key == "numbers":
            st.session_state.numbers = []
        elif key == "answers":
            st.session_state.answers = {}
        elif key == "scores":
            st.session_state.scores = {}
        elif key == "show_start_time":
            st.session_state.show_start_time = None

st.title("기억력 숫자 합 맞추기 게임")

if st.session_state.step == "intro":
    players_num = st.slider("플레이어 수 선택 (1~4명)", 1, MAX_PLAYERS, 1)
    names = []
    for i in range(players_num):
        name = st.text_input(f"플레이어 {i+1} 이름", key=f"name_{i}")
        if name:
            names.append(name)

    if len(names) == players_num:
        if st.button("게임 시작"):
            st.session_state.players = names
            st.session_state.scores = {name: 0 for name in names}
            st.session_state.ready = set()
            st.session_state.level = 1
            st.session_state.step = "lobby"
            st.experimental_rerun()

elif st.session_state.step == "lobby":
    st.write("대기 중인 플레이어:")
    for p in st.session_state.players:
        st.write(f"- {p} {'✅' if p in st.session_state.ready else '❌'}")

    ready_name = st.text_input("준비 완료할 이름 입력", key="ready_name")
    if ready_name in st.session_state.players and ready_name not in st.session_state.ready:
        if st.button("준비 완료"):
            st.session_state.ready.add(ready_name)
            st.experimental_rerun()

    if len(st.session_state.ready) == len(st.session_state.players):
        st.success("모두 준비 완료! 게임 시작합니다.")
        st.session_state.step = "show"
        st.session_state.show_start_time = time.time()
        st.session_state.numbers = []
        st.experimental_rerun()

elif st.session_state.step == "show":
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
        st.info(f"숫자 사라질 때까지 {SHOW_TIME - int(elapsed)}초 남음")
        st.experimental_rerun()

elif st.session_state.step == "guess":
    correct_sum = sum(st.session_state.numbers)
    guess_name = st.text_input("이름 입력", key="guess_name")

    if guess_name in st.session_state.players:
        if guess_name in st.session_state.answers:
            st.success("이미 제출했습니다. 기다려 주세요.")
        else:
            answer = st.number_input("합 입력", step=1, format="%d", key=f"answer_{guess_name}")
            if st.button("제출", key=f"submit_{guess_name}"):
                st.session_state.answers[guess_name] = answer
                if answer == correct_sum:
                    st.session_state.scores[guess_name] += 1
                if len(st.session_state.answers) == len(st.session_state.players):
                    st.session_state.step = "result"
                st.experimental_rerun()

elif st.session_state.step == "result":
    correct_sum = sum(st.session_state.numbers)
    st.write(f"정답은 {correct_sum} 입니다.")

    for p in st.session_state.players:
        ans = st.session_state.answers.get(p)
        if ans == correct_sum:
            st.success(f"{p}: 정답!")
        else:
            st.error(f"{p}: 틀렸어요. 정답은 {correct_sum}")

    if st.session_state.level < TOTAL_LEVELS:
        if st.button("다음 단계"):
            st.session_state.level += 1
            st.session_state.numbers = []
            st.session_state.answers = {}
            st.session_state.step = "show"
            st.session_state.show_start_time = time.time()
            st.experimental_rerun()
    else:
        if st.button("최종 랭킹 보기"):
            st.session_state.step = "ranking"
            st.experimental_rerun()

elif st.session_state.step == "ranking":
    ranking = sorted(st.session_state.scores.items(), key=lambda x: x[1], reverse=True)
    st.write("최종 랭킹:")
    for i, (name, score) in enumerate(ranking, 1):
        st.write(f"{i}위: {name} - {score}점")

    if st.button("다시 시작"):
        for key in ["step", "players", "ready", "level", "numbers", "answers", "scores", "show_start_time"]:
            if key in st.session_state:
                del st.session_state[key]
        st.experimental_rerun()
