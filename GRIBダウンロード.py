import requests
from datetime import datetime, timedelta
import os
import glob
import pytz

# === 設定 ===
# 外付けHDDの保存先パス 
save_dir = r"C:\Users\suedakouta\Desktop\Horned Puffin\forecast_download"

jst = pytz.timezone('Asia/Tokyo')
today = datetime.now(jst)

base_url = "https://database.rish.kyoto-u.ac.jp/arch/jmadata/data/gpv/original"

# ダウンロード対象の日付を指定（例：昨日のデータ）
target_date = today - timedelta(days=1)

# FD0012, 0112, 0212, 0312, 0412 のファイルを取得
file_variants = ["0012", "0112", "0212", "0312", "0412"]

# === ダウンロード処理 ===
for variant in file_variants:
    # 日付に基づいて URL とファイル名を生成
    date_str = target_date.strftime("%Y/%m/%d")
    filename = f"Z__C_RJTD_{target_date.strftime('%Y%m%d120000')}_GSM_GPV_Rgl_FD{variant}_grib2.bin"
    download_url = f"{base_url}/{date_str}/{filename}"

    # ダウンロード先のファイルパスを生成
    output_file = os.path.join(save_dir, filename)

    # ファイルをダウンロード
    try:
        print(f"ダウンロード中: {download_url}")
        response = requests.get(download_url, stream=True)

        if response.status_code == 200:
            # バイナリモードでファイルを保存
            with open(output_file, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            print(f"ダウンロード完了: {output_file}")
        else:
            print(f"エラー: {response.status_code} - ファイルが見つかりませんでした")

    except Exception as e:
        print(f"エラーが発生しました: {e}")