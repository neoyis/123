import streamlit as st
import pandas as pd

st.title("2025년 6월 기준 연령별 인구 분석")

# ✅ GitHub CSV raw URL을 아래에 입력하세요!
csv_url = "https://raw.githubusercontent.com/사용자명/레포지토리명/브랜치명/경로/파일명.csv"

try:
    # GitHub에서 직접 불러오기 (EUC-KR 인코딩)
    df = pd.read_csv(csv_url, encoding="euc-kr")

    # 열 이름 자동 확인
    region_col = [col for col in df.columns if "행정구역" in col][0]
    total_col = [col for col in df.columns if "총인구수" in col][0]
    age_columns = [col for col in df.columns if col.startswith("2025년06월_계_")]

    # 필요한 열만 추출
    age_data = df[[region_col, total_col] + age_columns].copy()
    age_data.rename(columns={col: col.replace("2025년06월_계_", "") for col in age_columns}, inplace=True)

    # 숫자형 변환
    for col in age_data.columns[2:]:
        age_data[col] = pd.to_numeric(age_data[col], errors="coerce")

    # 총인구수 기준 상위 5개
    top5 = age_data.sort_values(total_col, ascending=False).head(5)

    # 시각화용 데이터 변환
    chart_data = top5.set_index(region_col).drop(columns=[total_col]).T
    chart_data.index.name = "연령"

    st.subheader("상위 5개 행정구역 연령별 인구 변화")
    st.line_chart(chart_data)

    st.subheader("개별 행정구역 인구 그래프 보기")
    selected_region = st.selectbox("행정구역을 선택하세요", chart_data.columns)
    st.line_chart(chart_data[[selected_region]])

    st.subheader("원본 데이터")
    st.dataframe(df)

except Exception as e:
    st.error(f"데이터를 불러오는 데 문제가 발생했습니다: {e}")
