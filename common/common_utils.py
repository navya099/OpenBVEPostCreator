def format_station_km(number: float) -> str:
    """측점(m)을 km 단위 문자열로 변환 (예: 1234.5 → '1.234')"""
    return "{:.3f}".format(number * 0.001)
