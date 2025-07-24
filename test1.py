import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="학생 고민 상담", page_icon="📝")

# 제목
st.title("📝 학생 고민 상담실")
st.write("너의 고민을 안전하게 공유할 수 있는 공간이야. 어떤 이야기든 괜찮아!")

# 입력 폼
with st.form("counseling_form"):
    age_group = st.selectbox("나이대나 학년을 선택해줘", ["중학생", "고1", "고2", "고3", "졸업생"])
    concern = st.text_area("지금 마음속에 있는 고민을 적어줘 (익명)", height=200)
    submitted = st.form_submit_button("보내기")

    if submitted:
        if concern.strip() == "":
            st.warning("고민을 입력해줘야 해!")
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

            st.success("고마워. 너의 고민은 소중하게 다뤄질 거야.")
            st.info("너 혼자만 그런 거 아니야. 누구나 힘든 시간을 겪어. 응원할게!")

# 다운로드 버튼 (선생님용)
with st.expander("📥 상담 데이터 다운로드 (선생님용)"):
    try:
        df = pd.read_csv("counsel_data.csv")
        st.download_button(
            label="CSV 파일 다운로드",
            data=df.to_csv(index=False).encode("utf-8-sig"),
            file_name="counsel_data.csv",
            mime="text/csv"
        )
    except FileNotFoundError:
        st.warning("아직 저장된 상담 데이터가 없어.")
