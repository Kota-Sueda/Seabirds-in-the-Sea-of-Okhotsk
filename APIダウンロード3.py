import copernicusmarine
from datetime import datetime, timedelta, timezone

# 現在の日付（日本時間）を取得
jst = timezone(timedelta(hours=9))  # 日本標準時 (JST) UTC+9
today = datetime.now(jst).date()
target_dates = [today, today + timedelta(days=3), today + timedelta(days=7)]


for i, date in enumerate(target_dates):
    output_filename = f"CMEMS_phyc_{i}.nc"  
    
    copernicusmarine.subset(
        dataset_id="cmems_mod_glo_bgc-pft_anfc_0.25deg_P1D-m",  # 栄養塩やプランクトンに関連するデータセットID
        variables=["phyc"],  
        minimum_longitude=133,
        maximum_longitude=158,
        minimum_latitude=40,
        maximum_latitude=60,
        start_datetime=date.strftime("%Y-%m-%d"),
        end_datetime=date.strftime("%Y-%m-%d"),
        minimum_depth=25.21,  # 表層のデータを取得
        maximum_depth=25.21,  # 必要に応じて深度を調整
        output_filename=output_filename,
        output_directory=r"C:\Users\suedakouta\Desktop\Horned Puffin\forecast_download"
    )
    
    print(f"Day {i+1} ({date}) - Download complete: {output_filename}")

for i, date in enumerate(target_dates):
    date = today + timedelta(days=i)
    output_filename = f"CMEMS_no3_{i}.nc"  
    
    copernicusmarine.subset(
        dataset_id="cmems_mod_glo_bgc-nut_anfc_0.25deg_P1D-m",  # 栄養塩やプランクトンに関連するデータセットID
        variables=["no3"],  
        minimum_longitude=133,
        maximum_longitude=158,
        minimum_latitude=40,
        maximum_latitude=60,
        start_datetime=date.strftime("%Y-%m-%d"),
        end_datetime=date.strftime("%Y-%m-%d"),
        minimum_depth=25.21,  # 表層のデータを取得
        maximum_depth=25.21,  # 必要に応じて深度を調整
        output_filename=output_filename,
        output_directory=r"C:\Users\suedakouta\Desktop\Horned Puffin\forecast_download"
    )
    
    print(f"Day {i+1} ({date}) - Download complete: {output_filename}")