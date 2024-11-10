import xarray as xr
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature

# NetCDFファイルのパスを指定
file_path = r"C:\Users\suedakouta\Downloads\glo12_rg_1d-m_20241107-20241107_3D-thetao_fcst_R20241106.nc"

# データセットを読み込む
ds = xr.open_dataset(file_path)

# 時間を固定（最初の時間ステップを選択）
time_fixed = ds.isel(time=0)

# 深度を9.57mに指定
depth_index = abs(time_fixed['depth'] - 9.57).argmin()
data_depth_fixed = time_fixed.isel(depth=depth_index)

# 緯度経度の範囲を指定
lat_min, lat_max = 40, 60
lon_min, lon_max = 133, 158
data_cropped = data_depth_fixed.sel(latitude=slice(lat_min, lat_max), longitude=slice(lon_min, lon_max))

# 温度データを抽出
temperature_data = data_cropped['thetao']

# 地図に描画
plt.figure(figsize=(6, 10))
ax = plt.axes(projection=ccrs.Mercator())
ax.set_extent([lon_min, lon_max, lat_min, lat_max], crs=ccrs.PlateCarree())

# 海岸線や陸地の追加
ax.add_feature(cfeature.COASTLINE)
ax.add_feature(cfeature.LAND, facecolor='lightgray')

# 温度データのプロット
temperature_data.plot(ax=ax, transform=ccrs.PlateCarree(), cmap='seismic', cbar_kwargs={'label': 'Temperature (°C)'})

# 等温線のプロット
lon, lat = temperature_data['longitude'], temperature_data['latitude']
contour = ax.contour(lon, lat, temperature_data, levels=10, colors='black', linewidths=0.5, transform=ccrs.PlateCarree())
ax.clabel(contour, inline=True, fontsize=8, fmt='%1.1f °C') 

# タイトルやラベル
plt.title(f"Sea Water Temperature at 1m Depth (Fixed Time)")
plt.xlabel("Longitude")
plt.ylabel("Latitude")

# 地図の表示
plt.show()
