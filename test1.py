import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="고민 상담 공간", page_icon="💬")

# 제목
st.title("💬 익명 고민 상담 공간")
st.write("누구나 편하게 고민을 털어놓을 수 있는 곳이야. 너의 이야기를 진심으로 들어줄게.")

# 입력 폼
with st.form("counseling_form"):
    age_group = st.selectbox(
        "당신의 나이대는 어떻게 되나요?",
        ["초등학생", "중학생", "고등학생", "대학생", "청년 (20~30대)", "중장년 (40~50대)", "시니어 (60대 이상)"]
    )
    concern = st.text_area("지금 하고 싶은 이야기나 고민을 적어주세요 (익명)", height=200)
    submitted = st.form_submit_button("보내기")

    if submitted:
        if concern.strip() == "":
            st.warning("고민을 입력해 주세요.")
        else:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            new_data = pd.DataFrame({
                "시간": [timestamp],
                "나이대": [age_group],
                "고민": [concern]
            })

            try:
                old_data = pd.read_csv("counsel_data.csv")
                data = pd.concat([old_data, new_data], ignore_index=True)
            except FileNotFoundError:
                data = new_data

            data.to_csv("counsel_data.csv", index=False)

            # 위로 메시지 출력
            st.success("고민을 잘 적어줘서 고마워요. 당신의 이야기는 소중하게 다뤄질 거예요.")
            st.info("마음이 힘들 때는 혼자 견디지 말고 꼭 이야기해 주세요. 당신의 마음을 응원합니다.")

# 다운로드 버튼 (관리자용)
with st.expander("📥 상담 데이터 다운로드 (관리자 전용)"):
    try:
        df = pd.read_csv("counsel_data.csv")
        st.download_button(
            label="CSV 파일 다운로드",
            data=df.to_csv(index=False).encode("utf-8-sig"),
            file_name="counsel_data.csv",
            mime="text/csv"
        )
    except FileNotFoundError:
        st.warning("아직 저장된 상담 데이터가 없습니다.")
