import copernicusmarine
from datetime import datetime, timedelta, timezone

# 現在の日付（日本時間）を取得
jst = timezone(timedelta(hours=9))  # 日本標準時 (JST) UTC+9
today = datetime.now(jst).date()
target_dates = [today, today + timedelta(days=3), today + timedelta(days=7)]

# 今日から5日間のデータを取得（湧昇流データ）
for i, date in enumerate(target_dates):    
    output_filename = f"CMEMS_wo_{i}.nc"  
    
    copernicusmarine.subset(
        dataset_id="cmems_mod_glo_phy-wcur_anfc_0.083deg_P1D-m",  # 湧昇流データセットID
        variables=["wo"],  # 湧昇流（垂直速度）
        minimum_longitude=133,
        maximum_longitude=158,
        minimum_latitude=40,
        maximum_latitude=60,
        start_datetime=date.strftime("%Y-%m-%d"),
        end_datetime=date.strftime("%Y-%m-%d"),
        minimum_depth=55.76,  # 深度は必要に応じて変更
        maximum_depth=55.76,
        output_filename=output_filename,
        output_directory=r"C:\Users\suedakouta\Desktop\Horned Puffin\forecast_download"
    )
    
    print(f"Day {i+1} ({date}) - Download complete: {output_filename}")
