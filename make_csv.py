import pandas as pd

# 엑셀 파일 읽기
xlsx = pd.read_excel("50 Deutsche Lieder.xlsx", dtype=str)  # 문자열로 읽기

# 모든 열에 대해 문자열 앞뒤 공백 제거
xlsx = xlsx.apply(lambda col: col.map(lambda x: x.strip() if isinstance(x, str) else x))

# CSV 파일로 저장
xlsx.to_csv("50 Deutsche Lieder.csv", index=False, encoding="utf-8-sig")