import streamlit as st
import random
import time

# 설정
MAX_PLAYERS = 4
SHOW_TIME = 5  # 숫자 보여주는 시간(초)

# 세션 초기화
if "step" not in st.session_state:
    st.session_state.step = "intro"
if "players" not in st.session_state:
    st.session_state.players = {}
if "numbers" not in st.session_state:
    st.session_state.numbers = []
if "answers" not in st.session_state:
    st.session_state.answers = {}

st.title("🧠 기억력 숫자 합 맞추기 게임")

# 🎬 1. 게임 설명 화면
if st.session_state.step == "intro":
    st.header("🎮 게임 설명")
    st.markdown("""
    이 게임은 **기억력과 계산력**을 테스트하는 게임이야!  

    **게임 방식:**
    - 최대 4명까지 참여 가능
    - 모두가 준비되면 숫자 4개가 **5초간** 나타나
    - 그 후, 숫자는 사라지고 각자 **숫자들의 합**을 입력해야 해!
    - 정답 여부가 공개되고, 다시 시작할 수 있어

    👉 친구들과 함께 탭 여러 개로 접속해도 되고, 혼자 여러 이름으로 테스트해도 돼!
    """)

    if st.button("게임 시작하기"):
        st.session_state.step = "lobby"
        st.experimental_rerun()

# 🎮 2. 대기실
elif st.session_state.step == "lobby":
    name = st.text_input("너의 이름을 입력해줘")

    if name:
        if name not in st.session_state.players:
            st.session_state.players[name] = {"ready": False}

        st.subheader("🧍 대기 중인 플레이어")
        for player, info in st.session_state.players.items():
            st.write(f"🧑 {player} - {'✅ 준비됨' if info['ready'] else '❌ 대기중'}")
        
        if not st.session_state.players[name]["ready"]:
            if st.button("✅ 준비 완료"):
                st.session_state.players[name]["ready"] = True
                st.experimental_rerun()

        if all(info["ready"] for info in st.session_state.players.values()) and len(st.session_state.players) >= 2:
            st.success("🎉 모두 준비 완료! 숫자를 보여줄게!")
            st.session_state.numbers = [random.randint(1, 9) for _ in range(4)]
            st.session_state.step = "show"
            st.experimental_rerun()

# 👀 3. 숫자 보여주기
elif st.session_state.step == "show":
    st.subheader("👀 숫자를 기억해!")
    st.write(" + ".join(map(str, st.session_state.numbers)))
    st.info(f"{SHOW_TIME}초 후에 사라져!")

    time.sleep(SHOW_TIME)
    st.session_state.step = "guess"
    st.experimental_rerun()

# ❓ 4. 정답 입력
elif st.session_state.step == "guess":
    name = st.text_input("너의 이름을 다시 입력해줘 (입력 확인용)", key="guess_name")
    if name and name in st.session_state.players:
        st.subheader(f"{name}님, 숫자들의 합을 입력해주세요!")
        answer = st.number_input("합은 얼마였을까?", step=1, format="%d", key=name)

        if st.button("제출", key=f"submit_{name}"):
            st.session_state.answers[name] = answer
            if len(st.session_state.answers) == len(st.session_state.players):
                st.session_state.step = "result"
            st.experimental_rerun()

# ✅ 5. 결과 보기
elif st.session_state.step == "result":
    st.subheader("📊 결과")
    correct_sum = sum(st.session_state.numbers)
    st.write(f"🎯 정답: {correct_sum}")

    for player, ans in st.session_state.answers.items():
        if ans == correct_sum:
            st.success(f"{player}: 🎉 정답!")
        else:
            st.error(f"{player}: ❌ 오답! (입력한 값: {ans})")

    if st.button("🔁 다시 하기"):
        st.session_state.step = "intro"
        st.session_state.players = {}
        st.session_state.answers = {}
        st.session_state.numbers = []
        st.experimental_rerun()
