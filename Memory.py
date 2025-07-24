import streamlit as st
import random
import time

TOTAL_LEVELS = 20
SHOW_TIME = 5

def get_setting(level):
    if level <= 4: return 3, 9
    if level <= 8: return 4, 20
    if level <= 12: return 5, 30
    if level <= 16: return 6, 50
    return 7, 99

if "step" not in st.session_state:
    st.session_state.step = "start"
if "level" not in st.session_state:
    st.session_state.level = 1
if "numbers" not in st.session_state:
    st.session_state.numbers = []
if "answer" not in st.session_state:
    st.session_state.answer = None
if "show_time" not in st.session_state:
    st.session_state.show_time = None

st.title("기억력 숫자 합 맞추기 게임")

if st.session_state.step == "start":
    if st.button("게임 시작"):
        st.session_state.level = 1
        st.session_state.step = "show"
        st.session_state.show_time = time.time()
        st.experimental_rerun()

elif st.session_state.step == "show":
    count, max_num = get_setting(st.session_state.level)
    if not st.session_state.numbers:
        st.session_state.numbers = [random.randint(1, max_num) for _ in range(count)]
    st.write(" + ".join(map(str, st.session_state.numbers)))

    if time.time() - st.session_state.show_time > SHOW_TIME:
        st.session_state.step = "input"
        st.experimental_rerun()
    else:
        st.info(f"{SHOW_TIME - int(time.time() - st.session_state.show_time)}초 후에 문제 사라짐")

elif st.session_state.step == "input":
    st.write("숫자들의 합을 입력하세요")
    user_input = st.number_input("답", step=1, format="%d")
    if st.button("제출"):
        st.session_state.answer = user_input
        st.session_state.step = "result"
        st.experimental_rerun()

elif st.session_state.step == "result":
    correct = sum(st.session_state.numbers)
    if st.session_state.answer == correct:
        st.success(f"정답! 합은 {correct} 입니다.")
        st.session_state.level += 1
    else:
        st.error(f"틀렸어요. 정답은 {correct} 입니다.")
    if st.session_state.level > TOTAL_LEVELS:
        st.write("게임 종료! 수고했어요.")
        if st.button("처음으로"):
            for key in ["step","level","numbers","answer","show_time"]:
                if key in st.session_state:
                    del st.session_state[key]
            st.experimental_rerun()
    else:
        if st.button("다음 문제"):
            st.session_state.numbers = []
            st.session_state.answer = None
            st.session_state.step = "show"
            st.session_state.show_time = time.time()
            st.experimental_rerun()
