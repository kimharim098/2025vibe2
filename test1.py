import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="따뜻한 익명 고민 상담소", page_icon="🌈")

st.title("🌈 익명 고민 상담소")
st.write("누구나 털어놓을 수 있는 공간이에요. 당신의 이야기를 진심으로 들어줄게요.")

# 긴 상담 메시지들
response_dict = {
    "학업": (
        "공부는 늘 쉽지 않죠. 노력해도 성과가 바로 안 보이면 정말 지치기도 하고요.\n"
        "하지만 그 과정 속에서 당신은 분명히 자라고 있어요. 때론 쉬어가는 것도 필요해요.\n"
        "지금 힘든 건 당신이 잘하고 싶어하기 때문이에요. 그 마음이 이미 너무 소중해요.\n"
        "어떤 결과든, 지금의 당신은 충분히 멋지고 훌륭하답니다."
    ),
    "감정/우울/불안": (
        "지금 느끼는 감정은 너무 자연스러운 거예요. 우울하거나 불안한 순간은 누구에게나 찾아오고요.\n"
        "그렇다고 당신이 약하다는 건 절대 아니에요. 오히려 감정을 인식하고 표현한다는 건 강하다는 증거예요.\n"
        "지금 당장은 힘들 수 있지만, 그 감정이 당신을 집어삼키도록 두지 마세요.\n"
        "작은 일부터 해보면서, 천천히 다시 나를 돌보는 시간을 가져봐요. 당신은 절대 혼자가 아니에요."
    ),
    "인간관계": (
        "사람들과의 관계는 정말 어렵죠. 이해받지 못하거나, 오해받을 때 상처도 크고요.\n"
        "모든 사람에게 사랑받을 수는 없어요. 중요한 건, 당신이 스스로를 이해하고 존중하는 거예요.\n"
        "괜찮아요. 인연은 흘러가기도 하고, 다시 다가오기도 해요. 너무 자신을 탓하지 말아요.\n"
        "지금 힘든 마음, 여기선 온전히 인정받아도 돼요."
    ),
    "가족 문제": (
        "가족과의 관계는 누구보다 가까우면서도, 때로는 가장 어려운 사이일 수 있어요.\n"
        "가족이라고 해서 무조건 이해할 수 있는 건 아니고, 상처가 깊을 수도 있어요.\n"
        "당신의 감정은 정당해요. 억지로 참지 않아도 돼요. 필요하다면 거리를 두는 것도 괜찮아요.\n"
        "무엇보다 당신의 마음이 먼저예요. 누구보다 당신을 아껴야 할 사람은 바로 당신이니까요."
    ),
    "진로/미래": (
        "미래를 생각하면 막막할 수 있어요. 남들과 비교하게 되고, 내 길이 맞는지도 불안하죠.\n"
        "하지만 인생은 정해진 답이 없어요. 방향을 바꾸는 것도 성장의 일부예요.\n"
        "지금 당장 완벽한 계획이 없어도 괜찮아요. 조금씩 나에 대해 알아가는 과정이 중요하니까요.\n"
        "조급해하지 않아도 돼요. 당신의 속도대로 충분히 잘 가고 있어요."
    ),
    "자존감/자기이해": (
        "스스로를 사랑하기 어렵다는 말, 그 말만으로도 얼마나 오랫동안 혼자 고민했는지 느껴져요.\n"
        "있는 그대로의 당신은 이미 충분히 소중해요. 남들과 비교하지 않아도, 당신만의 가치가 있어요.\n"
        "가끔은 나를 칭찬해 주는 연습을 해보세요. 작더라도 잘한 걸 알아봐 주세요.\n"
        "당신은 결코 부족하지 않아요. 지금의 모습도 아름다워요."
    ),
    "기타": (
        "이 공간에 고민을 털어놔줘서 정말 고마워요.\n"
        "당신의 이야기는 충분히 의미 있고, 누군가에게 털어놓는 것만으로도 큰 용기예요.\n"
        "무엇이든 당신이 겪는 일이면 그건 진짜예요. 여기선 어떤 감정도 부정하지 않을게요.\n"
        "필요하면 언제든 또 찾아와도 좋아요. 늘 여기 있을게요."
    )
}

# 입력 폼
with st.form("counsel_form"):
    age_group = st.selectbox(
        "당신의 나이대는?",
        ["초등학생", "중학생", "고등학생", "대학생", "청년 (20~30대)", "중장년 (40~50대)", "시니어 (60대 이상)"]
    )

    concern_type = st.selectbox(
        "고민의 주제는 무엇인가요?",
        ["학업", "감정/우울/불안", "인간관계", "가족 문제", "진로/미래", "자존감/자기이해", "기타"]
    )

    concern = st.text_area("고민을 자유롭게 적어주세요. (익명)", height=200)

    submitted = st.form_submit_button("보내기")

    if submitted:
        if concern.strip() == "":
            st.warning("고민 내용을 입력해 주세요.")
        else:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            new_data = pd.DataFrame({
                "시간": [timestamp],
                "나이대": [age_group],
                "고민 주제": [concern_type],
                "고민 내용": [concern]
            })

            try:
                old_data = pd.read_csv("counsel_data.csv")
                data = pd.concat([old_data, new_data], ignore_index=True)
            except FileNotFoundError:
                data = new_data

            data.to_csv("counsel_data.csv", index=False)

            st.success("고민을 나눠줘서 정말 고마워요.")
            st.markdown(f"**💬 상담 메시지:**\n\n{response_dict.get(concern_type, response_dict['기타'])}")

# 관리자용 다운로드
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
