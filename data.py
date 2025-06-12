# streamlit_app.py

import streamlit as st
import pandas as pd
import folium
from urllib.parse import quote
from streamlit_folium import st_folium

st.set_page_config(page_title="서울시 상권 지도", layout="wide")

st.title("📍 서울시 상권 지도 시각화")
st.markdown("GitHub에 올린 CSV 데이터를 불러와 folium으로 지도에 표시합니다.")

# 1. GitHub 파일명과 경로 설정
filename = "서울시 상권분석서비스(영역-상권).csv"
base_url = "https://raw.githubusercontent.com/heejin225/project/main/"
encoded_url = base_url + quote(filename)

# 2. CSV 불러오기 (인코딩 시도)
try:
    df = pd.read_csv(encoded_url, encoding='cp949')
except UnicodeDecodeError:
    df = pd.read_csv(encoded_url, encoding='utf-8-sig')

df.columns = df.columns.str.strip()

# 3. 지도 중심 설정
map_center = [df["와이좌표_값"].mean(), df["엑스좌표_값"].mean()]
m = folium.Map(location=map_center, zoom_start=12)

# 4. 자치구 선택 필터 추가
gu_list = df["자치구_코드_명"].dropna().unique()
selected_gu = st.selectbox("자치구를 선택하세요", ["전체"] + sorted(gu_list.tolist()))

# 5. 필터링
if selected_gu != "전체":
    df = df[df["자치구_코드_명"] == selected_gu]

# 6. 지도에 마커 추가
for _, row in df.iterrows():
    popup = f"""<b>상권명:</b> {row['상권_코드_명']}<br>
                <b>행정동:</b> {row['행정동_코드_명']}<br>
                <b>자치구:</b> {row['자치구_코드_명']}<br>
                <b>면적:</b> {row['영역_면적']:,}㎡"""
    folium.CircleMarker(
        location=[row["와이좌표_값"], row["엑스좌표_값"]],
        radius=5,
        popup=popup,
        color="blue",
        fill=True,
        fill_color="cyan",
        fill_opacity=0.7
    ).add_to(m)

# 7. Streamlit에서 지도 출력
st_data = st_folium(m, width=900, height=600)
