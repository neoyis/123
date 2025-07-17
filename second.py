import streamlit as st
import pandas as pd
import requests
from io import StringIO

# 앱 제목
st.title("2025년 5월 행정구역별 연령별 인구 현황 대시보드")

# GitHub에 업로드한 CSV 파일 주소 입력
# ★ 이곳을 본인 GitHub 주소로 바꿔주세요!
CSV_URL = "https://raw.githubusercontent.com/사용자아이디/레포지토리명/main/202506_202506_주민등록인구및세대현황_월간.csv"

# 데이터 불러오기
@st.cache_data
def load_data(url):
    response = requests.get(url)
    response.encoding = 'EUC-KR'  # 행정안전부 자료는 EUC-KR 인코딩
    data = StringIO(response.text)
    df = pd.read_csv(data)
    return df

try:
    df = load_data(CSV_URL)

    # 컬럼 정리
    df.columns = df.columns.str.strip()
    df["행정구역"] = df["행정구역"].str.split("(").str[0]

    # 연령별 컬럼만 추출
    age_cols = [col for col in df.columns if "2025년05월_계_" in col and "세" in col]
    df["총인구수"] = df["총인구수"].astype(int)
    df_age = df[["행정구역", "총인구수"] + age_cols].copy()

    # 연령 컬럼 이름 정리
    new_cols = ["행정구역", "총인구수"] + [col.replace("2025년05월_계_", "").replace("세", "") for col in age_cols]
    df_age.columns = new_cols

    # 시각화: 상위 5개 행정구역의 연령별 인구
    top5 = df_age.sort_values(by="총인구수", ascending=False).head(5).set_index("행정구역")

    st.subheader("📈 상위 5개 행정구역의 연령별 인구 변화 (선 그래프)")
    st.line_chart(top5.drop(columns="총인구수").T)

    st.subheader("🔍 원본 데이터 미리보기")
    st.dataframe(df.head())

except Exception as e:
    st.error(f"❌ 데이터를 불러오는 데 문제가 발생했습니다:\n\n{e}")
