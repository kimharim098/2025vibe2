import streamlit as st
import time

if "start_time" not in st.session_state:
    st.session_state.start_time = time.time()

elapsed = time.time() - st.session_state.start_time

if elapsed < 5:
    st.write(f"남은 시간: {int(5 - elapsed)}초")
    st.experimental_rerun()
else:
    st.write("시간 종료!")
