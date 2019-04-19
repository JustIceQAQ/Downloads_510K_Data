# Downloads_510K_Data
Downloads 510K Data

# 前言
下載美國 FDA [510K](https://www.fda.gov/MedicalDevices/ProductsandMedicalProcedures/DeviceApprovalsandClearances/510kClearances/ucm089428.htm) 檔案

- 510K 線上查詢： https://www.accessdata.fda.gov/scripts/cdrh/cfdocs/cfPMN/pmn.cfm
- 510K 檔案下載： https://www.fda.gov/MedicalDevices/ProductsandMedicalProcedures/DeviceApprovalsandClearances/510kClearances/ucm089428.htm
- 510K 欄位說明： https://www.fda.gov/MedicalDevices/ProductsandMedicalProcedures/DeviceApprovalsandClearances/510kClearances/ucm089452.htm

# 使用套件

- pandas
- requests
- BeautifulSoup

# 檔案更新時間
每月更新(當月更新上個月資料)
官方表示: These files are replaced monthly usually on the 5th of each month.

# 支援輸出

- .csv
- .json (records)
- .xlsx (Excel)
- .msgpack
- .feather
- .parquet

基於 pandas 的檔案格式
http://pandas.pydata.org/pandas-docs/stable/user_guide/io.html#io-tools-text-csv-hdf5