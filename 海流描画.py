import xarray as xr
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature

# NetCDFファイルのパスを指定
file_path = r"C:\Users\suedakouta\Downloads\cmems_mod_glo_phy-cur_anfc_0.083deg_P1D-m_1730900648088.nc"

# データセットを読み込む
ds = xr.open_dataset(file_path)

# 時間を固定（最初の時間ステップを選択）
time_fixed = ds.isel(time=0)

# 深度を指定（1層しかない場合はそのまま取得）
depth_fixed = time_fixed.isel(depth=0)

# 緯度経度の範囲を指定
lat_min, lat_max = 40, 60
lon_min, lon_max = 133, 158
data_cropped = depth_fixed.sel(latitude=slice(lat_min, lat_max), longitude=slice(lon_min, lon_max))

# 東向き速度(uo)と北向き速度(vo)を抽出
uo = data_cropped['uo'][::24, ::24].values  # 24間隔でデータをサブセット
vo = data_cropped['vo'][::24, ::24].values  # 24間隔でデータをサブセット

# 緯度と経度の値を24間隔で取得
lon = data_cropped['longitude'][::24].values
lat = data_cropped['latitude'][::24].values

# 地図に描画
plt.figure(figsize=(6, 10))
ax = plt.axes(projection=ccrs.Mercator())
ax.set_extent([lon_min, lon_max, lat_min, lat_max], crs=ccrs.PlateCarree())

# 海岸線や陸地の追加
ax.add_feature(cfeature.COASTLINE)
ax.add_feature(cfeature.LAND, facecolor='lightgray')

# quiver関数でベクトルをプロット
#plt.quiver(lon, lat, uo, vo, transform=ccrs.PlateCarree(), scale=8, color='blue', width=0.006)
# 中抜き矢印の描画
plt.quiver(lon, lat, uo, vo, transform=ccrs.PlateCarree(), scale=10, color='lime', width=0.005,
               facecolor='none', edgecolor='lime', linewidth=0.6)

# タイトルやラベル
plt.title("Ocean Currents (Eastward and Northward velocity)")
plt.xlabel("Longitude")
plt.ylabel("Latitude")

# 地図の表示
plt.show()
