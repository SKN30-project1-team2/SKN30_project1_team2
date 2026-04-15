"""
서울특별시 시군구별 전기자동차 등록 현황 샘플 데이터
실제 데이터: 국토교통부 자동차 등록 현황 (공공데이터포털)
"""
import pandas as pd
import glob

# 서울 25개 자치구 좌표
DISTRICT_COORDS = {
    "종로구": (37.5730, 126.9794),
    "중구": (37.5640, 126.9975),
    "용산구": (37.5384, 126.9654),
    "성동구": (37.5635, 127.0369),
    "광진구": (37.5384, 127.0823),
    "동대문구": (37.5744, 127.0396),
    "중랑구": (37.6063, 127.0927),
    "성북구": (37.5894, 127.0167),
    "강북구": (37.6396, 127.0256),
    "도봉구": (37.6688, 127.0471),
    "노원구": (37.6542, 127.0568),
    "은평구": (37.6027, 126.9291),
    "서대문구": (37.5791, 126.9368),
    "마포구": (37.5663, 126.9014),
    "양천구": (37.5170, 126.8664),
    "강서구": (37.5509, 126.8495),
    "구로구": (37.4955, 126.8875),
    "금천구": (37.4600, 126.9001),
    "영등포구": (37.5264, 126.8963),
    "동작구": (37.5124, 126.9393),
    "관악구": (37.4784, 126.9516),
    "서초구": (37.4837, 127.0324),
    "강남구": (37.5172, 127.0473),
    "송파구": (37.5145, 127.1059),
    "강동구": (37.5301, 127.1238),
}

def get_ev_data():
    """시군구별 전기차 등록 현황 데이터 생성"""
    import numpy as np
    np.random.seed(42)
    
    districts = list(DISTRICT_COORDS.keys())
    vehicle_types = ["승용", "승합", "화물", "특수"]
    
    # 강남/서초/송파는 높게, 외곽은 낮게 설정
    base_counts = {
        "종로구": 1200, "중구": 900, "용산구": 1800,
        "성동구": 1600, "광진구": 1400, "동대문구": 1100,
        "중랑구": 950, "성북구": 1300, "강북구": 800,
        "도봉구": 700, "노원구": 1500, "은평구": 1100,
        "서대문구": 1000, "마포구": 2000, "양천구": 1700,
        "강서구": 1900, "구로구": 1300, "금천구": 900,
        "영등포구": 1800, "동작구": 1400, "관악구": 1200,
        "서초구": 3200, "강남구": 3800, "송파구": 3100,
        "강동구": 2100,
    }
    
    # 차량 종류 비율: 승용 75%, 승합 10%, 화물 12%, 특수 3%
    type_ratios = {"승용": 0.75, "승합": 0.10, "화물": 0.12, "특수": 0.03}
    
    rows = []
    for district in districts:
        base = base_counts[district]
        for vtype in vehicle_types:
            count = int(base * type_ratios[vtype] * (1 + np.random.uniform(-0.1, 0.1)))
            rows.append({
                "시군구명": district,
                "연료명": "전기",
                "차량종류": vtype,
                "등록대수": count,
                "위도": DISTRICT_COORDS[district][0],
                "경도": DISTRICT_COORDS[district][1],
            })
    
    df = pd.DataFrame(rows)
    return df


def get_charging_station_data():
    """전기차 충전소 샘플 데이터"""
    import numpy as np
    np.random.seed(123)
    
    stations = []
    station_types = ["급속", "완속", "초급속"]
    
    for district, (lat, lon) in DISTRICT_COORDS.items():
        n = np.random.randint(15, 60)
        for i in range(n):
            dlat = np.random.uniform(-0.025, 0.025)
            dlon = np.random.uniform(-0.025, 0.025)
            stype = np.random.choice(station_types, p=[0.3, 0.6, 0.1])
            places = ["주차장", "공공기관", "쇼핑몰", "아파트", "주유소", "병원"]
            place = np.random.choice(places)
            stations.append({
                "시군구명": district,
                "설치장소명": f"{district} {place} {i+1}호 충전소",
                "주소": f"서울특별시 {district} {np.random.randint(1,200)}번지",
                "충전기종류": stype,
                "위도": lat + dlat,
                "경도": lon + dlon,
                "운영시간": "24시간" if np.random.random() > 0.3 else "09:00-22:00",
            })
    
    return pd.DataFrame(stations)


def get_load_faq_data():
    # data 폴더 안의 모든 csv 파일 가져오기
    file_list = glob.glob("data/*.csv")  # 또는 "data/*.csv"

    df_list = []
    for file in file_list:
        df = pd.read_csv(file)
        df_list.append(df)

    # 하나로 합치기
    df_faq = pd.concat(df_list, ignore_index=True)
    df_faq = df_faq.fillna("")

    # 기존 구조에 맞게 변환
    faqs = []
    for _, row in df_faq.iterrows():
        faqs.append({
            "category": "전기차",   # 일단 기본값 (원하면 나중에 컬럼 추가 가능)
            "question": row["question"],
            "answer": row["answer"],
            "tags": []  # CSV에 없으니까 빈 리스트
        })
    return faqs
