echo "streamlit==1.25.0" >> requirements.txt
echo "pandas==2.1.0" >> requirements.txt
git init
git add requirements.txt
git commit -m "Add requirements file"
git branch -M main
git remote add origin https://github.com/jeeyikim/1.git
git push -u origin main
pip install -r requirements.txt

import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import datetime

# Google Sheets API 설정 함수
def get_google_sheet():
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    credentials = ServiceAccountCredentials.from_json_keyfile_name("your_google_credentials.json", scope)
    client = gspread.authorize(credentials)
    sheet = client.open_by_url("https://docs.google.com/spreadsheets/d/1m7dXCA5FML71PvMKPa1xL5zi0neg1QkhHLT0fTMNUjc/edit#gid=0").sheet1
    return sheet

# Google Sheets에 데이터 저장 함수
def save_to_google_sheet(data):
    sheet = get_google_sheet()
    sheet.append_row(data)

# Streamlit UI
st.title("대학생의 경제 상황과 소비 패턴에 따른 만족도 분석 설문지")

# 섹션 1: 기본 정보
st.header("1. 기본 정보")
name = st.text_input("이름을 입력하세요:")
gender = st.radio("성별을 선택하세요:", ("남성", "여성", "기타"))
age = st.number_input("만 나이를 입력하세요:", min_value=0, max_value=120, step=1)
major = st.text_input("학과를 입력하세요:")
residence = st.radio("주거 형태를 선택하세요:", ("자취", "기숙사", "통학", "기타"))

# 섹션 2: 수입원
st.header("2. 수입원")
work_hour = st.number_input("일주일 기준 총 알바 시간 (시간):")
salary = st.number_input("한달에 알바로 받는 돈 (만원):")
work_satisfaction = st.slider("알바 만족도 (1: 매우 불만족, 5: 매우 만족):", 1, 5)
pocketmoney = st.number_input("월 평균 용돈 (만원):")

# 섹션 3: 지출
st.header("3. 지출")
food = st.number_input("월 평균 식비 (만원):")
transportation = st.number_input("월 평균 교통비 (만원):")
house = st.number_input("월세 (관리비 포함, 만원):")
living_etc = st.number_input("기타 생활비 (만원):")
saving = st.number_input("월 저축 (만원):")
leisure = st.number_input("월 여가비 (만원):")
sudden = st.number_input("월 충동 구매 횟수:")

# 섹션 4: 만족도
st.header("4. 만족도")
satisfaction = st.slider("경제적 만족도 (1: 매우 불만족, 5: 매우 만족):", 1, 5)
reason = st.text_area("만족도에 대한 이유:")

if st.button("제출"):
    if name:
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        response_data = [
            timestamp, name, age, gender, major, residence, work_hour, salary,
            work_satisfaction, pocketmoney, food, transportation, house, living_etc,
            saving, leisure, sudden, satisfaction, reason
        ]

        # Google Sheets에 저장
        try:
            save_to_google_sheet(response_data)
            st.success("설문지가 제출되었습니다. 감사합니다!")
        except Exception as e:
            st.error(f"데이터 저장 중 오류가 발생했습니다: {e}")
    else:
        st.error("이름을 입력해주세요.")
