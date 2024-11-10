import copernicusmarine
from datetime import datetime, timedelta, timezone

# 現在の日付（日本時間）を取得
jst = timezone(timedelta(hours=9))  # 日本標準時 (JST) UTC+9
today = datetime.now(jst).date()

# 今日から5日間のデータを取得　海水温
for i in range(5):
    date = today + timedelta(days=i)
    output_filename = f"CMEMS_thetao_{i}.nc"  
    
    copernicusmarine.subset(
        dataset_id="cmems_mod_glo_phy-thetao_anfc_0.083deg_P1D-m",
        variables=["thetao"],
        minimum_longitude=133,
        maximum_longitude=158,
        minimum_latitude=40,
        maximum_latitude=60,
        start_datetime=date.strftime("%Y-%m-%d"),
        end_datetime=date.strftime("%Y-%m-%d"),
        minimum_depth=9.57,
        maximum_depth=9.57,
        output_filename=output_filename,
        output_directory=r"C:\Users\suedakouta\Desktop\Horned Puffin\forecast_download"
    )
    
    print(f"Day {i+1} ({date}) - Download complete: {output_filename}")

# 今日から5日間のデータを取得　海流
for i in range(5):
    date = today + timedelta(days=i)
    output_filename = f"CMEMS_currents_{i}.nc" 
    
    copernicusmarine.subset(
        dataset_id="cmems_mod_glo_phy-cur_anfc_0.083deg_P1D-m",
        variables=["uo", "vo"],
        minimum_longitude=133,
        maximum_longitude=158,
        minimum_latitude=40,
        maximum_latitude=60,
        start_datetime=date.strftime("%Y-%m-%d"),
        end_datetime=date.strftime("%Y-%m-%d"),
        minimum_depth=9.57,
        maximum_depth=9.57,
        output_filename=output_filename,
        output_directory=r"C:\Users\suedakouta\Desktop\Horned Puffin\forecast_download"
    )
    
    print(f"Day {i+1} ({date}) - Download complete: {output_filename}")



