import xarray as xr
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from matplotlib.colors import TwoSlopeNorm
import os
from datetime import datetime


# 各変数のファイルパス
wo_base_path = r"C:\Users\suedakouta\Desktop\Horned Puffin\forecast_download\CMEMS_wo_{}.nc"
phyc_base_path = r"C:\Users\suedakouta\Desktop\Horned Puffin\forecast_download\CMEMS_phyc_{}.nc"
no3_base_path = r"C:\Users\suedakouta\Desktop\Horned Puffin\forecast_download\CMEMS_no3_{}.nc"

# 出力フォルダの設定
output_folder = r"C:\Users\suedakouta\Desktop\python\Puffin\images"
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# 緯度経度の範囲
lat_min, lat_max = 40, 60
lon_min, lon_max = 133, 158

# 描画と保存
for i in range(3): 
    # 湧昇流データの読み込みと描画
    ds_wo = xr.open_dataset(wo_base_path.format(i))
    vertical_velocity = ds_wo["wo"].isel(time=0)
    time_value = ds_wo["time"].isel(time=0).values 
    formatted_time = datetime.utcfromtimestamp(time_value.astype('O') / 1e9).strftime('%Y/%m/%d')
    data_cropped = vertical_velocity.sel(latitude=slice(lat_min, lat_max), longitude=slice(lon_min, lon_max))

    plt.figure(figsize=(8, 8))
    ax = plt.axes(projection=ccrs.Mercator())
    ax.set_extent([lon_min, lon_max, lat_min, lat_max], crs=ccrs.PlateCarree())
    ax.add_feature(cfeature.COASTLINE)
    ax.add_feature(cfeature.LAND, facecolor='lightgray')

    norm = TwoSlopeNorm(vmin=-0.0005, vcenter=0, vmax=0.0005)
    data_cropped.plot(
        ax=ax,
        transform=ccrs.PlateCarree(),
        cmap="seismic",
        norm=norm,
        cbar_kwargs={'label': 'Vertical Velocity (m/s)'}
    )
    plt.title(f"Vertical Velocity at 55m Depth (Day {i+1})")
    plt.suptitle(f"{formatted_time}", fontsize=25, y=0.96, fontweight='bold')
    plt.savefig(os.path.join(output_folder, f"Vertical_Velocity_Day_{i+1}.png"))
    plt.close()

    # 植物プランクトンデータの読み込みと描画
    ds_phyc = xr.open_dataset(phyc_base_path.format(i))
    phytoplankton = ds_phyc["phyc"].isel(time=0)
    time_value = ds_wo["time"].isel(time=0).values 
    formatted_time = datetime.utcfromtimestamp(time_value.astype('O') / 1e9).strftime('%Y/%m/%d')
    data_cropped = phytoplankton.sel(latitude=slice(lat_min, lat_max), longitude=slice(lon_min, lon_max))

    plt.figure(figsize=(8, 8))
    ax = plt.axes(projection=ccrs.Mercator())
    ax.set_extent([lon_min, lon_max, lat_min, lat_max], crs=ccrs.PlateCarree())
    ax.add_feature(cfeature.COASTLINE)
    ax.add_feature(cfeature.LAND, facecolor='lightgray')

    norm = TwoSlopeNorm(vmin=0.0, vcenter=1.75, vmax=3.5)
    data_cropped.plot(
        ax=ax,
        transform=ccrs.PlateCarree(),
        cmap="PRGn",
        norm=norm,
        cbar_kwargs={'label': 'Phytoplankton Concentration (mmol/m³)'}
    )
    plt.title(f"Phytoplankton Concentration at 25m Depth (Day {i+1})")
    plt.suptitle(f"{formatted_time}", fontsize=25, y=0.96, fontweight='bold')
    plt.savefig(os.path.join(output_folder, f"Phytoplankton_Concentration_Day_{i+1}.png"))
    plt.close()

    # 硝酸塩データの読み込みと描画
    ds_no3 = xr.open_dataset(no3_base_path.format(i))
    nitrate = ds_no3["no3"].isel(time=0)
    time_value = ds_wo["time"].isel(time=0).values 
    formatted_time = datetime.utcfromtimestamp(time_value.astype('O') / 1e9).strftime('%Y/%m/%d')
    data_cropped = nitrate.sel(latitude=slice(lat_min, lat_max), longitude=slice(lon_min, lon_max))

    max_value = data_cropped.max().values
    min_value = data_cropped.min().values

    plt.figure(figsize=(8, 8))
    ax = plt.axes(projection=ccrs.Mercator())
    ax.set_extent([lon_min, lon_max, lat_min, lat_max], crs=ccrs.PlateCarree())
    ax.add_feature(cfeature.COASTLINE)
    ax.add_feature(cfeature.LAND, facecolor='lightgray')

    norm = TwoSlopeNorm(vmin=min_value, vcenter=(max_value + min_value) / 2, vmax=max_value)
    data_cropped.plot(
        ax=ax,
        transform=ccrs.PlateCarree(),
        cmap="BrBG",
        norm=norm,
        cbar_kwargs={'label': 'Nitrate Concentration (mmol/m³)'}
    )
    plt.title(f"Nitrate Concentration at 25m Depth (Day {i+1})")
    plt.suptitle(f"{formatted_time}", fontsize=25, y=0.96, fontweight='bold')
    plt.savefig(os.path.join(output_folder, f"Nitrate_Concentration_Day_{i+1}.png"))
    plt.close()

print("All images have been saved.")
