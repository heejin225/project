import pandas as pd
import folium

# GitHub raw CSV 링크
url = "https://raw.githubusercontent.com/사용자명/리포지토리명/브랜치명/파일이름.csv"

# CSV 파일 불러오기
df = pd.read_csv(url, encoding='utf-8')

# 열 이름 확인 (혹시 공백이 있을 수 있으니 strip 처리)
df.columns = df.columns.str.strip()

# folium 지도 중심을 전체 좌표의 평균으로 설정
map_center = [df["와이좌표값"].mean(), df["엑스좌표값"].mean()]
m = folium.Map(location=map_center, zoom_start=12)

# 마커 추가
for _, row in df.iterrows():
    popup_text = f"""
    상권명: {row['상권코드명']}<br>
    행정동: {row['행정동코드명']}<br>
    자치구: {row['자치구코드명']}
    """
    folium.Marker(
        location=[row["와이좌표값"], row["엑스좌표값"]],
        popup=folium.Popup(popup_text, max_width=300),
        icon=folium.Icon(color="green", icon="info-sign")
    ).add_to(m)

# 지도 저장
m.save("commercial_area_map.html")
print("✅ 지도 저장 완료: commercial_area_map.html")
