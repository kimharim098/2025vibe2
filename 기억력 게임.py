import streamlit as st
import random
import time

st.title("테스트 기억력 게임")

if "step" not in st.session_state:
    st.session_state.step = "start"

if st.session_state.step == "start":
    if st.button("숫자 보여줘"):
        st.session_state.numbers = [random.randint(1, 9) for _ in range(3)]
        st.session_state.step = "show"
        st.experimental_rerun()

elif st.session_state.step == "show":
    st.write("기억해:", st.session_state.numbers)
    time.sleep(3)
    st.session_state.step = "guess"
    st.experimental_rerun()

elif st.session_state.step == "guess":
    answer = st.number_input("합이 뭐였을까?", step=1, format="%d")
    if st.button("제출"):
        if answer == sum(st.session_state.numbers):
            st.success("정답!")
        else:
            st.error(f"틀렸어! 정답은 {sum(st.session_state.numbers)}")
        st.session_state.step = "start"
