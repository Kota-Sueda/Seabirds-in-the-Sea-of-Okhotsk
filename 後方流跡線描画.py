import pandas as pd
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature

plt.rcParams['font.family'] = 'Meiryo'

# CSVファイルのパスを指定
file_path = r"C:\Users\suedakouta\Downloads\20241106232120.csv"

# 各解析の行範囲を指定
row_ranges = [(30, 102), (133, 205), (236, 308)]
print(row_ranges)

# 地図の作成
plt.figure(figsize=(8, 8))
ax = plt.axes(projection=ccrs.Mercator())
ax.set_extent([120, 170, 30, 60], crs=ccrs.PlateCarree())  # 日本周辺の範囲に設定

# 海岸線や国境の追加
ax.add_feature(cfeature.COASTLINE)
ax.add_feature(cfeature.BORDERS, linestyle=':')

# 各行範囲で流跡線データを読み込み、緯度と経度をプロット
highlight_rows = [0, 24, 48, 71] 
for start, end in row_ranges:
    # ファイルの指定範囲の行を読み込み（カンマ区切りで読み込み）
    df = pd.read_csv(file_path, sep=',', comment='#', header=None, skiprows=start, nrows=end - start)
    
    # 6列目と7列目を緯度と経度として取得してプロット
    latitudes = df.iloc[:, 5]  # 6列目
    longitudes = df.iloc[:, 6]  # 7列目
    ax.plot(longitudes, latitudes, marker='o', markersize=3, transform=ccrs.PlateCarree())

    # 指定された行のプロット（赤色）
    for row in highlight_rows:
        if row < len(df):  # データの範囲内か確認
            ax.plot(longitudes.iloc[row], latitudes.iloc[row], marker='o', color='red', markersize=5, transform=ccrs.PlateCarree())


# タイトルを追加
plt.title("3日間の後方流跡線解析")

# 地図の表示
plt.show()

