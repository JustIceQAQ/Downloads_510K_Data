import io
import os
import re
import sys
import urllib.request
import zipfile
from datetime import datetime
import pandas as pd
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm
import tkinter as tk

x = datetime.now()
DateTimeSTR = '{}{}{}'.format(x.year,
                              str(x.month).zfill(2) if len(str(x.month)) < 2 else str(x.month),
                              str(x.day).zfill(2) if len(str(x.day)) < 2 else str(x.day))

def filetypesSelect(filedf, fileName, filetypesStr, check):
    if 'csv' in filetypesStr:
        filedf.to_csv('{}_{}.csv'.format(check, fileName), index=False, encoding='utf-8')
    elif 'json' in filetypesStr:
        filedf.to_json('{}_{}.json'.format(check, fileName), orient="records")
    elif 'xlsx' in filetypesStr:
        writer = pd.ExcelWriter('{}_{}.xlsx'.format(check, fileName), engine='xlsxwriter',
                                options={'strings_to_urls': False})
        filedf.to_excel(writer, index=False, encoding='utf-8')
        writer.close()
    elif 'msgpack' in filetypesStr:
        filedf.to_msgpack("{}_{}.msg".format(check, fileName), encoding='utf-8')
    elif 'feather' in filetypesStr:
        filedf.to_feather('{}_{}.feather'.format(check, fileName))
    elif 'parquet' in filetypesStr:
        filedf.to_parquet('{}_{}.parquet'.format(check, fileName), engine='pyarrow', encoding='utf-8')
    elif 'pickle' in filetypesStr:
        filedf.to_pickle('{}_{}.pkl'.format(check, fileName))



def change_label_number():
    strLabel = tk.Label(window, text='處理中...')
    strLabel.pack(anchor='center')
    window.update()
    global url
    global zipfileName
    global comboExample
    comboExampleget = fileTypeListbox.get(fileTypeListbox.curselection())
    url = 'https://www.fda.gov/MedicalDevices/ProductsandMedicalProcedures/DeviceApprovalsandClearances/510kClearances/ucm089428.htm'
    req = requests.get(url)
    soup = BeautifulSoup(req.text, 'html5lib')
    OBDataUrl = {i.a.text: i.a['href'] for i in soup.findAll('p') if i.find(text=re.compile('-'))}
    strLabel2 = tk.Label(window, text='Downloads 510K Data.')
    strLabel2.pack(anchor='center')
    window.update()
    for K, v in tqdm(OBDataUrl.items(), total=len(OBDataUrl), ascii=True, desc='Downloads 510K Data.'):
        urllib.request.urlretrieve(v, K)
    strLabel3 = tk.Label(window, text='Downloads 510K Data Done.')
    strLabel3.pack(anchor='center')
    window.update()
    all510kdatalist = []
    for j in tqdm(OBDataUrl, ascii=True, desc='Loading 510K Data'):
        with zipfile.ZipFile(j, 'r') as zipFile:
            txtfile = j.lower().replace('.zip', '.txt')
            fileio = io.StringIO(zipFile.read(txtfile).decode('cp1252'))
            test01 = pd.read_csv(fileio, sep='|', encoding='utf8')
            all510kdatalist.extend(test01.to_dict('records'))
    strLabel4 = tk.Label(window, text='Loading 510K Data to {}'.format(comboExampleget))
    strLabel4.pack(anchor='center')
    window.update()
    all510kDF = pd.DataFrame(all510kdatalist)
    all510kDf = all510kDF.rename(dict(zip(all510kDF.columns, [i.title() for i in all510kDF.columns])), axis=1)
    with open('{}.txt'.format(str(len(all510kDF))), 'w') as txt:
        pass


    # print('510K 額外資訊merge')
    # # 510K 額外資訊merge
    # urllib.request.urlretrieve('http://www.accessdata.fda.gov/premarket/ftparea/foiclass.zip', 'foiclass.zip')
    # with zipfile.ZipFile('foiclass.zip', 'r') as zipFile:
    #     fileio = io.StringIO(zipFile.read('foiclass.txt').decode('cp1252'))
    #     test01 = pd.read_csv(fileio, sep='|', encoding='utf8')
    # test01.rename(
    #     {'REVIEW_PANEL': 'Reviewadvisecomm', 'PRODUCTCODE': 'Productcode', 'DEVICENAME': 'DEVICENAME_ADJ'},
    #     axis=1, inplace=True)
    # full510k = pd.merge(all510kDf, test01, how='left', on=['Reviewadvisecomm', 'Productcode'])
    try:
        filetypesSelect(all510kDf, '510k', comboExampleget, DateTimeSTR)
        window.quit()
    except Exception:
        window2 = tk.Tk()
        window2.title('錯誤提示')
        window2.geometry('400x300')
        error_Text = ''
        e_type, e_value, e_traceback = sys.exc_info()
        error_Text += f'''錯誤訊息如下：
                        Errortype ==> {e_type.__name__}
                        ErrorInfo ==> {e_value}
                        ErrorFileName ==> {e_traceback.tb_frame.f_code.co_filename}
                        ErrorLineOn ==> {e_traceback.tb_lineno}
                        ErrorFunctionName ==> {e_traceback.tb_frame.f_code.co_name}'''
        with open('errorFileLog.log', 'w+') as errorFileLog:
            errorFileLog.write(error_Text)
        strLabel2 = tk.Label(window2, text='{}\n{}\n{}'.format(e_type, e_value, e_traceback))
        strLabel2.pack(anchor='center')
        window2.mainloop()

    finally:
        pass


window = tk.Tk()
window.title('請選擇 510K 資料輸出檔案格式(Select File Type)')
window.geometry('400x300')
try:
    path = './{}_510K'.format(DateTimeSTR)
    if not os.path.isdir(path):
        os.mkdir(path)
        os.chdir(path)
    else:
        os.chdir(path)
    fileTypeVar = tk.StringVar()
    fileTypeVar.set(('csv', 'json', 'xlsx', 'msgpack', 'feather', 'parquet', 'pickle'))
    fileTypeListbox = tk.Listbox(window, listvariable=fileTypeVar)
    fileTypeListbox.pack(anchor='center')
    saveButton = tk.Button(window, text='儲存(Save)', command=change_label_number)
    saveButton.pack(anchor='center')
    window.mainloop()
except Exception:
    window2 = tk.Tk()
    window2.title('錯誤提示')
    window2.geometry('400x300')
    error_Text = ''
    e_type, e_value, e_traceback = sys.exc_info()
    error_Text += f'''錯誤訊息如下：
                    Errortype ==> {e_type.__name__}
                    ErrorInfo ==> {e_value}
                    ErrorFileName ==> {e_traceback.tb_frame.f_code.co_filename}
                    ErrorLineOn ==> {e_traceback.tb_lineno}
                    ErrorFunctionName ==> {e_traceback.tb_frame.f_code.co_name}'''
    with open('errorFileLog.log', 'w+') as errorFileLog:
        errorFileLog.write(error_Text)
    strLabel2 = tk.Label(window2, text='{}\n{}\n{}'.format(e_type, e_value, e_traceback))
    strLabel2.pack(anchor='center')
    window2.mainloop()
finally:
    pass
