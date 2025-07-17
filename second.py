import streamlit as st
import pandas as pd
import requests
from io import StringIO

st.title("📊 2025년 5월 주민등록 인구 및 세대 현황 분석 대시보드")

# 🔧 여기에 본인의 GitHub CSV 경로를 입력하세요
CSV_URL = "https://raw.githubusercontent.com/사용자아이디/레포지토리명/main/202506_202506_주민등록인구및세대현황_월간.csv"

# 데이터 불러오기 함수
@st.cache_data
def load_csv(url):
    try:
        r = requests.get(url)
        r.encoding = 'EUC-KR'
        df = pd.read_csv(StringIO(r.text))
        df.columns = df.columns.str.strip()  # 열 이름 공백 제거
        return df
    except Exception as e:
        st.error(f"CSV 파일을 불러오는 중 오류 발생: {e}")
        return None

df = load_csv(CSV_URL)

if df is not None:
    # 🔍 주요 컬럼 추출
    col_candidates = list(df.columns)
    st.sidebar.write("🔎 CSV 파일 열 목록:")
    st.sidebar.write(col_candidates)

    if "행정구역" in df.columns and "2025년06월_세대수" in df.columns:
        df["행정구역"] = df["행정구역"].str.replace(r"\(.*\)", "", regex=True).str.strip()
        df["2025년06월_세대수"] = pd.to_numeric(df["2025년06월_세대수"], errors="coerce")

        # 연령별 컬럼만 추출
        age_cols = [col for col in df.columns if "세" in col and "계" in col]
        new_col_names = [col.split("_")[-1].replace("세", "") for col in age_cols]

        age_df = df[["행정구역", "2025년06월_세대수"] + age_cols].copy()
        age_df.columns = ["행정구역", "2025년06월_세대수"] + new_col_names

        # 상위 5개 지역만 시각화
        top5 = age_df.sort_values(by="2025년06월_세대수", ascending=False).head(5).set_index("행정구역")

        st.subheader("📈 상위 5개 지역의 연령별 인구 분포")
        st.line_chart(top5.drop(columns="2025년06월_세대수").T)

        st.subheader("🔍 전체 데이터 미리보기")
        st.dataframe(age_df)
    else:
        st.error("❌ CSV에 '행정구역' 또는 '2025년06월_세대수' 열이 없습니다. 열 이름을 확인해 주세요.")
