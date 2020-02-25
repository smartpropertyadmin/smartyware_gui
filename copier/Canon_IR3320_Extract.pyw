import csv
from abc import abstractclassmethod
from datetime import datetime,timedelta
import requests
import pandas as pd
import os
import html5lib
from bs4 import BeautifulSoup
from requests_html import HTML, HTMLSession



headers = {
    'user-agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'
}

class extract_copier_canon_ir3320():
    url = 'http://192.168.1.156:8000/login'

    s =  HTMLSession()

    # r = s.get(url, headers=headers)

    r = s.post(url,  data={
        'uri' : '/rps/',
        'deptid': '8888' ,
        'password': '9999'
    })
    dummy_var = int(datetime.timestamp(datetime.now()) * 1000)
    def clear_counter_list(self):
        url_2= "http://192.168.1.156:8000/rps/csmp.cgi"
        data = {
            "Manage": "1",
            "FLimit": "0",
            "Default" : "0",
            "DefScan" : "0",
            "BWCopy" : "0",
            "BWPrint" : "0",
            "BWPDLPrint" : "0",
            "LargeCount" : "0",
            "SecID" :"",
            "Flag" : "Clear_Data",
            "Page": "0",
            "PageFlag" : "c_topsib.tpl",
            "FuncTypeFlag" :"",
            "CoreNXAction" :"./ csmp.cgi",
            "CoreNXPage" : "c_topsis.tpl",
            "Dummy" : ""
        }

        dummy_var = int(datetime.timestamp(datetime.now()) * 1000)
        r2 = self.s.get('http://192.168.1.156:8000/usermode')
        data["Dummy"]= dummy_var
        r2 = self.s.post(url_2,data= data, headers= headers)


    def get_counter_list(self):
        today = datetime.today()
        TemplateFilePath= "Z:\\STATIONERY,POSTAGE,PHOTOCOPY\PHOTOCOPIER FRANKING REPORT\PHOTOCOPIER\\{}\\{}\\"
        TemplateFilename = "{} - CANON C3320.csv"
        FilePath = TemplateFilePath.format( today.strftime("%Y"),
                   "{:02d}".format((today-timedelta(days=5)).month) + " - " + (today-timedelta(days=5)).strftime("%b'%y").upper())
        FileName = TemplateFilename.format(today.strftime("%Y%m%d"))
        try:
            os.makedirs(FilePath)
        except OSError:
            print ("Folder Exidummy_var"
                   "sted")

        FilePathName = os.path.join(FilePath,FileName)

        with open(FilePathName, 'w', encoding="utf-8", newline='') as csv_file:
            headersRow = ['Dept. ID','Total Prints','Color Total','Black & White Total',
                          'Color Copy','Color Scan','Color Print','Black & White Copy','Black & White Scan',
                          'Black & White Print']
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow(headersRow)

            url_2 = 'http://192.168.1.156:8000/rps/csl.cgi?Flag=Init_Data&SecID=0&Page={}&Dummy='
            dummy_var = int(datetime.timestamp(datetime.now()) * 1000)
            url_2 += str(dummy_var)
            r2 = self.s.get('http://192.168.1.156:8000/usermode')

            for page_no in range(0,2):
                r = self.s.get(url_2.format(page_no), headers=headers)
                source = r.text
                html = HTML(html=source)
                html.render()
                soup = BeautifulSoup(html.html, 'html.parser')

                Counter_table = soup.find('table')
                # print(Counter_table)
                Counter_body = Counter_table.find('tbody')


                row_value = []
                for tr in Counter_body.find_all('tr'):

                    for td in tr.find_all('td'):

                        cellValue = td.text.strip().split('\n',1)[0]


                        if cellValue .isnumeric():
                            row_value.append(cellValue )
                    csv_writer.writerow(row_value)
                    row_value = []

    def post_new_account(self, New_account):
        url_2 = 'http://192.168.1.156:8000/rps/csp.cgi'
        headers = {
            'Accept': 'text / html, application / xhtml + xml, application / xml;q = 0.9, image / webp, image / apng, * / *;q = 0.8, application / signed - exchange;v = b3',
            'Accept - Encoding': 'gzip, deflate',
            'Accept - Language': 'en - US, en;q = 0.9',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'
        }
        data = {
            'SecID': New_account,
            'Pswd': New_account,
            'Pswd_Chk': '1',
            'ScanLimitCL': '0',
            'ScanLimitBW': '0',
            'CopyLimitCL': '0',
            'CopyLimitBW': '0',
            'PrntLimitCL': '0',
            'PrntLimitBW': '0',
            'TotalLimit': '0',
            'TotalLimitCL': '0',
            'TotalLimitBW': '0',
            'ScanCheckCL': '0',
            'ScanCheckBW': '0',
            'CopyCheckCL': '0',
            'CopyCheckBW': '0',
            'PrntCheckCL': '0',
            'PrntCheckBW': '0',
            'TotalCheck': '0',
            'TotalCheckCL': '0',
            'TotalCheckBW': '0',
            'Page': '0',
            'Flag': 'Exec_Data',
            'PageFlag': 'c_topsib.tpl',
            'CoreNXAction': './csp.cgi',
            'CoreNXPage': 'c_topsie.tpl',
            'CoreNXFlag': 'Init_Data',
            'Dummy': self.dummy_var

        }
        r2 = self.s.get('http://192.168.1.156:8000/usermode')
        r3 = self.s.post(url_2, headers=headers, data=data)
        # print(r3.text)

    def update_log_list(self):
        url_2 = ' http://192.168.1.156:8000/rps/pprint.csv?LogType=0&Flag=Csv_Data&Dummy='
        headers = {
            'Accept': 'text / h     tml, application / xhtml + xml, application / xml;q = 0.9, image / webp, image / apng, * / *;q = 0.8, application / signed - exchange;v = b3',
            'Accept - Encoding': 'gzip, deflate',
            'Accept - Language': 'en - US, en;q = 0.9',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'
        }
        data = {
            'LogType': '0',
            'Flag': 'Csv_Data',
            'Dummy': str(self.dummy_var)
        }

        url_2 += str(self.dummy_var)
        r2 = self.s.get('http://192.168.1.156:8000/usermode')
        r = self.s.get(url_2, headers=headers, data=data)

        os.chdir(r'Z:\STATIONERY,POSTAGE,PHOTOCOPY\PHOTOCOPIER FRANKING REPORT\PHOTOCOPIER\LOG LIST')

        def Timestamp_Endtime(Endtime):
            return datetime.strptime(Endtime['End Time '], '%d/%m %Y %X').timestamp()

        Old_log = pd.read_csv('CANON_PRINT_LOG_0226.csv')
        Old_log['Time Stamp '] = Old_log.apply(lambda row: Timestamp_Endtime(row), axis=1)
        Old_log = Old_log.sort_values('Time Stamp ', ascending=0)

        Last_log = Old_log.iloc[0]['End Time ']

        new_r = str(r.text).split('\n')
        new_r[0] = new_r[0] + '\r'
        IterNew_r = iter(new_r)
        next(IterNew_r)

        for line in new_r[1:-1]:
            cell = str(line).split(',')

            if cell[0] == "":
                break

            if datetime.strptime(cell[3], '%d/%m %Y %X').timestamp() > datetime.strptime(Last_log,
                                                                                         '%d/%m %Y %X').timestamp():
                dicCell = dict(zip(Old_log.head(-1), cell))

                Old_log = Old_log.append(dicCell, ignore_index=True)

        Old_log['Time Stamp '] = Old_log.apply(lambda row: Timestamp_Endtime(row), axis=1)
        Old_log = Old_log.sort_values('Time Stamp ', ascending=0)

        Old_log.to_csv('CANON_PRINT_LOG_0226.csv', index=False)
