# 仮想環境の変更
import pygrib

# GRIBファイルのパスを指定
file_path = r"C:\Users\suedakouta\Downloads\Z__C_RJTD_20241105120000_GSM_GPV_Rgl_FD0112_grib2.bin"

# GRIBファイルを開く
with pygrib.open(file_path) as grib_file:
    # ファイル内のメッセージ数を確認
    print(f"Total messages: {grib_file.messages}")

    # メッセージを順に読み込む（例として、最初のメッセージを取得）
    grib_message = grib_file.message(1)  # メッセージ番号で指定（例: 1）

    # データの基本情報を表示
    print("Parameter name:", grib_message.name)
    print("Parameter units:", grib_message.units)
    print("Date:", grib_message.validDate)
    print("Shape of values array:", grib_message.values.shape)

    # データ値を取得
    values = grib_message.values  # データの値の配列

    # 緯度と経度を取得
    lats, lons = grib_message.latlons()

# データの表示例
print("Values:", values)
print("Latitudes:", lats)
print("Longitudes:", lons)
