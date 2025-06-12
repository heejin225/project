import streamlit as st
import folium
from streamlit_folium import st_folium
import requests

st.title("근처 치킨집")

keyword = st.text_input("검색할 키워드를 입력하세요 (예: 치킨)")

# 기본 지도 중심 (서울특별시교육청 융합과학교육원 근처)
m = folium.Map(location=[37.4688, 126.9595], zoom_start=13)

KAKAO_REST_API_KEY = "80e7fec3a76f98ee84b20d5ff29886b6"

def search_places(query):
    url = "https://dapi.kakao.com/v2/local/search/keyword.json"
    headers = {"Authorization": f"KakaoAK {KAKAO_REST_API_KEY}"}
    params = {"query": query, "size": 15}  # 최대 15개 결과
    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        return response.json().get("documents")
    else:
        st.error("API 요청 실패: " + str(response.status_code))
        return None

if keyword:
    places = search_places(keyword)
    if places:
        for place in places:
            lat = float(place['y'])
            lon = float(place['x'])
            name = place['place_name']
            folium.Marker([lat, lon], popup=name).add_to(m)
        # 지도 중심을 첫 번째 장소로 이동
        m.location = [float(places[0]['y']), float(places[0]['x'])]
    else:
        st.warning("검색 결과가 없습니다.")

st_folium(m, width=700, height=500)
