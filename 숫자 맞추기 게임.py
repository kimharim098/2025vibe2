import streamlit as st
import random

if 'target' not in st.session_state or 'guess_count' not in st.session_state:
    st.session_state.target = random.randint(1, 100)
    st.session_state.guess_count = 0

st.title("숫자 맞추기 게임")

# 다시하기 버튼 (누르면 상태 초기화)
if st.button("다시하기"):
    st.session_state.target = random.randint(1, 100)
    st.session_state.guess_count = 0
    st.success("게임이 초기화됐어! 숫자를 다시 맞춰봐 :)")

with st.form(key='guess_form'):
    guess = st.number_input("1부터 100 사이 숫자를 입력하세요", min_value=1, max_value=100, step=1)
    submit = st.form_submit_button("제출")

if submit:
    st.session_state.guess_count += 1

    if guess < st.session_state.target:
        st.write("더 높은 숫자야!")
    elif guess > st.session_state.target:
        st.write("더 낮은 숫자야!")
    else:
        st.write(f"🎉 축하해! {st.session_state.guess_count}번 만에 맞췄어! 🎉")
