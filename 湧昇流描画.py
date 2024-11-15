import xarray as xr
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from matplotlib.colors import TwoSlopeNorm

# NetCDFファイルのパスを指定
file_path = r"C:\Users\suedakouta\Desktop\Horned Puffin\forecast_download\CMEMS_wo_0.nc"

# データセットを読み込む
ds = xr.open_dataset(file_path)

# 湧昇流（垂直速度）のデータを選択（深度と時間を固定）
vertical_velocity = ds["wo"]  # 深度55.76m
time_fixed = vertical_velocity.isel(time=0)  # 最初の時間ステップを選択

# 緯度経度の範囲を指定してデータを切り取る
lat_min, lat_max = 40, 60
lon_min, lon_max = 133, 158
data_cropped = time_fixed.sel(latitude=slice(lat_min, lat_max), longitude=slice(lon_min, lon_max))

# 地図に描画
plt.figure(figsize=(8, 8))
ax = plt.axes(projection=ccrs.Mercator())
ax.set_extent([lon_min, lon_max, lat_min, lat_max], crs=ccrs.PlateCarree())

# 海岸線や陸地の追加
ax.add_feature(cfeature.COASTLINE)
ax.add_feature(cfeature.LAND, facecolor='lightgray')

# 湧昇流データをカラーマップで描画
norm = TwoSlopeNorm(vmin=-0.0005, vcenter=0, vmax=0.0005)  # 中心を0に設定
cbar = data_cropped.plot(
    ax=ax, 
    transform=ccrs.PlateCarree(), 
    cmap="seismic",  # 上昇流と下降流を区別
    norm=norm,
    cbar_kwargs={'label': 'Vertical Velocity (m/s)'}
)

# タイトルやラベル
plt.title("Vertical Velocity at 55m Depth")
plt.xlabel("Longitude")
plt.ylabel("Latitude")

# 地図の表示
plt.show()

