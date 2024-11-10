from netCDF4 import Dataset

file_path = r"C:\Users\suedakouta\Downloads\cmems_mod_glo_phy-cur_anfc_0.083deg_P1D-m_1730900648088.nc"
dataset = Dataset(file_path, "r")

# ファイル全体の情報を確認
print(dataset)

# 各変数の名前とその情報を確認
for var_name in dataset.variables:
    print(f"Variable: {var_name}")
    print(dataset.variables[var_name])

# グローバル属性を確認
print("\nGlobal attributes:")
for attr_name in dataset.ncattrs():
    print(f"{attr_name}: {getattr(dataset, attr_name)}")

# 必要があれば特定の変数データを確認
# temp_data = dataset.variables['temperature'][:]
# print(temp_data)

# ファイルを閉じる
dataset.close()
