import xarray as xr
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from matplotlib.colors import TwoSlopeNorm

# NetCDFファイルのパスを指定
file_path = r"C:\Users\suedakouta\Desktop\Horned Puffin\forecast_download\CMEMS_phyc_0.nc"

# データセットを読み込む
ds = xr.open_dataset(file_path)

# 植物プランクトンのデータを選択（深度と時間を固定）
phytoplankton = ds["phyc"]
time_fixed = phytoplankton.isel(time=0)  # 最初の時間ステップを選択

# 緯度経度の範囲を指定してデータを切り取る
lat_min, lat_max = 40, 60
lon_min, lon_max = 133, 158
data_cropped = time_fixed.sel(latitude=slice(lat_min, lat_max), longitude=slice(lon_min, lon_max))

# 植物プランクトンデータの最大値と最小値を計算
#max_value = data_cropped.max().values
#min_value = data_cropped.min().values
#print(f"Phytoplankton Concentration - Max: {max_value:.2f} mmol/m³, Min: {min_value:.2f} mmol/m³")

# 地図に描画
plt.figure(figsize=(8, 8))
ax = plt.axes(projection=ccrs.Mercator())
ax.set_extent([lon_min, lon_max, lat_min, lat_max], crs=ccrs.PlateCarree())

# 海岸線や陸地の追加
ax.add_feature(cfeature.COASTLINE)
ax.add_feature(cfeature.LAND, facecolor='lightgray')

# 植物プランクトンデータをカラーマップで描画
norm = TwoSlopeNorm(vmin=0.0, vcenter=1.75, vmax=3.5)  # 中心を0に設定し、値域を調整
cbar = data_cropped.plot(
    ax=ax, 
    transform=ccrs.PlateCarree(), 
    cmap="PRGn",  # 高濃度（赤）と低濃度（青）を区別
    norm=norm,
    cbar_kwargs={'label': 'Phytoplankton Concentration (mmol/m³)'}
)

# タイトルやラベル
plt.title("Phytoplankton Concentration at 25m Depth")
plt.xlabel("Longitude")
plt.ylabel("Latitude")

# 地図の表示
plt.show()

