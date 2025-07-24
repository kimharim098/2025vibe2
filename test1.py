import streamlit as st
import pandas as pd
from datetime import datetime
import openai  # 👈 OpenAI API 사용

# 🔐 OpenAI API 키 입력
openai.api_key = "YOUR_OPENAI_API_KEY"

st.set_page_config(page_title="AI 고민 상담소", page_icon="🧠")
st.title("🧠 감정에 공감하는 AI 고민 상담소")
st.write("당신만의 고민에 진심으로 귀 기울이는 AI 상담사가 함께할게요.")

# 사용자 입력 폼
with st.form("counsel_form"):
    age_group = st.selectbox(
        "당신의 나이대는?",
        ["초등학생", "중학생", "고등학생", "대학생", "청년 (20~30대)", "중장년 (40~50대)", "시니어 (60대 이상)"]
    )
    concern = st.text_area("당신의 고민을 자유롭게 적어주세요. (익명)", height=200)
    submitted = st.form_submit_button("보내기")

# GPT 응답 생성 함수
def generate_response(age_group, concern):
    prompt = (
        f"다음은 {age_group} 사용자가 털어놓은 고민입니다:\n\n"
        f"\"{concern}\"\n\n"
        f"이 사용자의 고민에 진심으로 공감하고 위로해주는 따뜻한 상담사처럼 답변을 작성해 주세요. "
        f"너무 짧지 않게 쓰고, 직접적인 위로와 조언을 포함해 주세요."
    )
    response = openai.ChatCompletion.create(
        model="gpt-4",  # 또는 gpt-3.5-turbo 사용 가능
        messages=[{"role": "user", "content": prompt}],
        max_tokens=300,
        temperature=0.8
    )
    return response.choices[0].message["content"]

# 결과 출력
if submitted:
    if concern.strip() == "":
        st.warning("고민 내용을 입력해 주세요.")
    else:
        with st.spinner("AI 상담사가 당신의 고민을 듣고 있어요..."):
            ai_response = generate_response(age_group, concern)

        # 저장
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        new_data = pd.DataFrame({
            "시간": [timestamp],
            "나이대": [age_group],
            "고민 내용": [concern],
            "AI 응답": [ai_response]
        })

        try:
            old_data = pd.read_csv("counsel_data.csv")
            data = pd.concat([old_data, new_data], ignore_index=True)
        except FileNotFoundError:
            data = new_data

        data.to_csv("counsel_data.csv", index=False)

        # 출력
        st.success("고민을 들어줘서 고마워요. AI 상담사의 답변은 아래와 같아요:")
        st.markdown(f"**💬 AI 상담사의 답변:**\n\n{ai_response}")

# 관리자 다운로드
with st.expander("📥 상담 데이터 다운로드 (관리자용)"):
    try:
        df = pd.read_csv("counsel_data.csv")
        st.download_button(
            label="CSV 파일 다운로드",
            data=df.to_csv(index=False).encode("utf-8-sig"),
            file_name="counsel_data.csv",
            mime="text/csv"
        )
    except FileNotFoundError:
        st.warning("저장된 상담 데이터가 아직 없습니다.")
