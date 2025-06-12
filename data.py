import streamlit as st
import folium
from streamlit_folium import st_folium
import requests

# ✅ 사용자 설정 부분
KAKAO_API_KEY = "80e7fec3a76f98ee84b20d5ff29886b6"  # 예: KakaoAK abcdef1234567890

# 카카오 장소 검색 함수
def search_places(query):
    url = "https://dapi.kakao.com/v2/local/search/keyword.json"
    headers = {
        "Authorization": f"KakaoAK {KAKAO_API_KEY}"  # ← 중요!
    }
    params = {
        "query": query,
        "size": 10  # 최대 15개까지 가능
    }
    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        return response.json().get("documents", [])
    else:
        st.error(f"카카오 API 요청 실패 (코드: {response.status_code})")
        return []

# 👉 스트림릿 UI
st.title("📍 카카오 API로 음식점 검색하기")

keyword = st.text_input("검색할 음식 키워드를 입력하세요 (예: 치킨, 피자, 삼겹살 등)", value="치킨")

# 초기 지도: 서울 시청
m = folium.Map(location=[37.4688, 126.9595], zoom_start=13)

if keyword:
    results = search_places(keyword)
    if results:
        first = results[0]
        m.location = [float(first['y']), float(first['x'])]  # 첫 장소 중심
        for place in results:
            name = place['place_name']
            lat = float(place['y'])
            lon = float(place['x'])
            addr = place.get('road_address_name', '')
            folium.Marker(
                [lat, lon],
                popup=f"{name}<br>{addr}",
                tooltip=name
            ).add_to(m)
    else:
        st.warning("검색 결과가 없습니다.")

# 지도 출력
st_folium(m, width=700, height=500)
