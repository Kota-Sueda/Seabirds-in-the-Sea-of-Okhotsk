import pygrib
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.lines as mlines
import cartopy.crs as ccrs
from mpl_toolkits.axes_grid1.inset_locator import inset_axes

# GRIBファイルのパス
file_path = r"C:\Users\suedakouta\Downloads\Z__C_RJTD_20241105120000_GSM_GPV_Rgl_FD0112_grib2.bin"

# 抽出範囲の指定
lat_min, lat_max = 40, 60
lon_min, lon_max = 133, 158

# GRIBファイルを開く
with pygrib.open(file_path) as grb:
    # U風成分を取得
    u_wind_msg = grb.select(name='U component of wind', level=1000)[0]  # 10 m高度のデータ
    u_data = u_wind_msg.values
    lats, lons = u_wind_msg.latlons()

    # V風成分を取得
    v_wind_msg = grb.select(name='V component of wind', level=1000)[0]
    v_data = v_wind_msg.values

# 指定した緯度・経度範囲でデータをフィルタリング
lat_mask = (lats >= lat_min) & (lats <= lat_max)
lon_mask = (lons >= lon_min) & (lons <= lon_max)
mask = lat_mask & lon_mask

# マスキングしたデータの作成
lats_filtered = lats[mask]
lons_filtered = lons[mask]
u_data_filtered = u_data[mask]
v_data_filtered = v_data[mask]

# データを一つおきに間引き
lats_filtered = lats_filtered[::16]
lons_filtered = lons_filtered[::16]
u_data_filtered = u_data_filtered[::16]
v_data_filtered = v_data_filtered[::16]

# プロット
plt.figure(figsize=(8, 8))
ax = plt.axes(projection=ccrs.PlateCarree())
ax.set_extent([lon_min, lon_max, lat_min, lat_max], crs=ccrs.PlateCarree())

# 矢羽根プロット
#ax.quiver(lons_filtered, lats_filtered, u_data_filtered, v_data_filtered, transform=ccrs.PlateCarree())

# 矢羽根記号（barbs）プロット
ax.barbs(lons_filtered, lats_filtered, u_data_filtered, v_data_filtered, 
         length=6,  # 矢羽根のサイズを調整
         transform=ccrs.PlateCarree(), 
         barb_increments=dict(half=2, full=4, flag=20))  # 風速の表示を設定  

# 地図の特徴を追加
ax.coastlines()
ax.gridlines(draw_labels=True)

# タイトルを設定
plt.title('10 m Wind Components (U and V) over Specified Region')

# 凡例用の四角形のAxesを地図の左上隅に追加
legend_ax = inset_axes(ax, width="19%", height="12%", loc="upper left", borderpad=0)

# 凡例に表示する風速の例（2, 4, 20 m/s）
legend_u = [2, 4, 20]
legend_v = [0, 0, 0]  # 水平に表示するためのv成分

# 凡例の矢羽根をプロット
legend_ax.barbs([0.35, 1.35, 2.35], [0, 0, 0], legend_u, legend_v, 
                length=6, 
                barb_increments=dict(half=2, full=4, flag=20), color='black')
legend_ax.set_xlim(-0.5, 2.5)
legend_ax.set_ylim(-1, 1)

# 矢羽根の下にラベルを追加
for i, speed in enumerate(legend_u):
    legend_ax.text(i, -0.5, f'{speed} m/s', ha='center', fontsize=7, color='black')


# 表示
plt.show()
