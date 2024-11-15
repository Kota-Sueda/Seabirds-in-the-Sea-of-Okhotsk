import pygrib
import numpy as np
import xarray as xr
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import pytz
from datetime import datetime, timedelta
from matplotlib.colors import TwoSlopeNorm
from mpl_toolkits.axes_grid1.inset_locator import inset_axes

# 日本標準時で現在の日付と時刻を取得し、1日前の日付を設定
jst = pytz.timezone('Asia/Tokyo')
today = datetime.now(jst)
target_date = today - timedelta(days=3)

# データのベースパスと保存先フォルダを指定
temperature_base_path = r"C:\Users\suedakouta\Desktop\Horned Puffin\forecast_download\CMEMS_thetao_{}.nc"
current_base_path = r"C:\Users\suedakouta\Desktop\Horned Puffin\forecast_download\CMEMS_currents_{}.nc"
filename = f"Z__C_RJTD_{target_date.strftime('%Y%m%d120000')}"
wind_base_path = rf"C:\Users\suedakouta\Desktop\Horned Puffin\forecast_download\{filename}_GSM_GPV_Rgl_FD0{{}}12_grib2.bin"
output_folder = r"C:\Users\suedakouta\Desktop\python\Puffin\images"

# 抽出範囲の指定
lat_min, lat_max = 40, 60
lon_min, lon_max = 133, 158

# 5回繰り返してデータを読み込み、プロットを保存
for i in range(5):
    # 各データファイルのパスを設定
    temperature_file_path = temperature_base_path.format(i)
    current_file_path = current_base_path.format(i)
    wind_file_path = wind_base_path.format(i)
    output_file = f"{output_folder}\Weather_Map_{i}.png"

    plot_date = target_date + timedelta(days=i)
    plot_date_str = plot_date.strftime('%Y/%m/%d (%a)')

    # 海水温データの読み込み
    temperature_ds = xr.open_dataset(temperature_file_path)
    time_fixed_temperature = temperature_ds.isel(time=0)
    depth_index_temperature = abs(time_fixed_temperature['depth'] - 9.57).argmin()
    temperature_data = time_fixed_temperature.isel(depth=depth_index_temperature).sel(
        latitude=slice(40, 60), longitude=slice(133, 158))['thetao']

    # 海流データの読み込み
    current_ds = xr.open_dataset(current_file_path)
    time_fixed_current = current_ds.isel(time=0)
    depth_fixed_current = time_fixed_current.isel(depth=0).sel(
        latitude=slice(40, 60), longitude=slice(133, 158))
    uo = depth_fixed_current['uo'][::24, ::24].values
    vo = depth_fixed_current['vo'][::24, ::24].values
    lon = depth_fixed_current['longitude'][::24].values
    lat = depth_fixed_current['latitude'][::24].values

    # 風データの読み込み
    with pygrib.open(wind_file_path) as grb:
        u_wind_msg = grb.select(name='U component of wind', level=1000)[0]
        u_data = u_wind_msg.values
        v_wind_msg = grb.select(name='V component of wind', level=1000)[0]
        v_data = v_wind_msg.values
        lats, lons = u_wind_msg.latlons()

    # 緯度・経度で指定範囲をフィルタリング
    lat_mask = (lats >= lat_min) & (lats <= lat_max)
    lon_mask = (lons >= lon_min) & (lons <= lon_max)
    mask = lat_mask & lon_mask
    lats_filtered = lats[mask][::16]
    lons_filtered = lons[mask][::16]
    u_data_filtered = u_data[mask][::16]
    v_data_filtered = v_data[mask][::16]

    # プロットの作成
    plt.figure(figsize=(10, 10))
    ax = plt.axes(projection=ccrs.Mercator())
    ax.set_extent([133, 158, 40, 60], crs=ccrs.PlateCarree())

    # 海岸線や陸地の追加
    ax.add_feature(cfeature.COASTLINE)
    ax.add_feature(cfeature.LAND, facecolor='lightgray')

    # 海水温データを背景としてプロット
    norm = TwoSlopeNorm(vmin=-15, vcenter=5, vmax=25)
    temperature_data.plot(ax=ax, transform=ccrs.PlateCarree(), cmap='seismic', norm=norm, cbar_kwargs={'label': 'Temperature (°C)'})

    # 等温線のプロット
    contour = ax.contour(temperature_data['longitude'], temperature_data['latitude'], temperature_data,
                         levels=10, colors='black', linewidths=0.5, transform=ccrs.PlateCarree())
    ax.clabel(contour, inline=True, fontsize=8, fmt='%1.1f °C')

    # 海流データを矢羽根で重ねてプロット
    ax.quiver(lon, lat, uo, vo, transform=ccrs.PlateCarree(), scale=10, color='lime', width=0.005)

    # 風データを矢羽根記号で重ねてプロット
    ax.barbs(lons_filtered, lats_filtered, u_data_filtered, v_data_filtered, length=6, 
             transform=ccrs.PlateCarree(), barb_increments=dict(half=2, full=4, flag=20))

    # 凡例の表示位置を指定（例: 左上の緯度・経度）
    legend_x = 134.5
    legend_y = 59.6

    # 凡例の矢羽根の風速例（2, 4, 20 m/s）
    legend_u = np.array([2, 4, 20])
    legend_v = np.array([0, 0, 0])  # 水平方向の矢羽根にするためv成分は0

    # 凡例の位置を格納したnumpy配列を作成
    legend_x_positions = np.array([legend_x + i * 1.5 for i in range(len(legend_u))])
    legend_y_positions = np.full_like(legend_x_positions, legend_y)

    # 凡例の矢羽根とラベルを直接プロットに配置
    ax.barbs(legend_x_positions, legend_y_positions, legend_u, legend_v, 
             length=6, transform=ccrs.PlateCarree(),
             barb_increments=dict(half=2, full=4, flag=20), color='black')

    for i, speed in enumerate(legend_u):
        ax.text(legend_x_positions[i] - 0.5, legend_y_positions[i] - 0.3, f'{speed} m/s', 
                transform=ccrs.PlateCarree(), ha='center', fontsize=7, color='black')

    # タイトルとラベル
    plt.title(f"Wind (1000hPa) and Sea Water Temperature and Ocean Currents (9.57m)  day{i}")
    plt.suptitle(f"{plot_date_str}", fontsize=30, y=0.95, fontweight='bold')
    plt.xlabel("Longitude")
    plt.ylabel("Latitude")

    # プロットを保存
    plt.savefig(output_file, bbox_inches='tight')
    plt.close()
    print(f"Plot saved as: {output_file}")

