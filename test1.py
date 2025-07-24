import streamlit as st
import openai
from datetime import datetime
import pandas as pd

# 🔐 여기에 본인 OpenAI API 키 꼭 넣기!
openai.api_key = "YOUR_OPENAI_API_KEY"

st.set_page_config(page_title="AI 상담소", page_icon="💬")

st.title("💬 AI 익명 고민 상담소")
st.write("나이대 선택 후 고민을 적으면, AI가 맞춤형으로 따뜻한 답변을 해줘요.")

# 사용자 입력 폼
with st.form("counsel_form"):
    age_group = st.selectbox(
        "당신의 나이대는?",
        ["초등학생", "중학생", "고등학생", "대학생", "청년 (20~30대)", "중장년 (40~50대)", "시니어 (60대 이상)"]
    )
    concern = st.text_area("지금 고민하는 내용을 솔직하게 적어주세요. (익명)", height=200)
    submitted = st.form_submit_button("상담받기")

def generate_ai_response(age_group, concern):
    prompt = (
        f"다음은 {age_group} 사용자의 고민입니다:\n"
        f"\"{concern}\"\n"
        f"이 사용자의 감정을 공감하고 따뜻하게 위로하며, 현실적인 조언과 격려를 담은 답변을 해주세요."
    )
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=300,
            temperature=0.8,
        )
        return response.choices[0].message["content"].strip()
    except Exception as e:
        return f"오류가 발생했어요: {e}"

if submitted:
    if not concern.strip():
        st.warning("고민 내용을 입력해 주세요.")
    else:
        with st.spinner("AI 상담사가 고민을 듣고 있어요..."):
            answer = generate_ai_response(age_group, concern)

        st.success("AI 상담 답변이 도착했어요.")
        st.markdown(f"### 💡 AI 상담 답변:\n{answer}")

        # 상담 기록 저장 (csv)
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        new_record = pd.DataFrame({
            "시간": [timestamp],
            "나이대": [age_group],
            "고민": [concern],
            "답변": [answer]
        })

        try:
            old_records = pd.read_csv("counsel_data.csv")
            records = pd.concat([old_records, new_record], ignore_index=True)
        except FileNotFoundError:
            records = new_record

        records.to_csv("counsel_data.csv", index=False)
