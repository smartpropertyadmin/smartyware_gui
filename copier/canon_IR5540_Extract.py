import csv
from abc import abstractclassmethod
from datetime import datetime,timedelta
import requests
import re
import os

from bs4 import BeautifulSoup
from requests_html import HTML, HTMLSession
# from flask_project.copier.Azure_connection  import Azureconnect, smart_project_listing, printerLog
# from sqlalchemy import desc

headers = {
    'user-agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'
}

class extract_copier_canon_ir5540():
    url = 'http://192.168.1.201:8000/login'
    dummy_var = int(datetime.timestamp(datetime.now()) * 1000)
    
    def __init__(self) -> None:
        self.s = HTMLSession()
        self.r = self.s.get(self.url, headers=headers)

        self.r = self.s.post(self.url,  data={
            'uri' : '/rps/',
            'deptid': "8888" ,
            'password': "9999"
        },verify=False)
    
    def clear_counter_list(self):
        url_2 = "http://192.168.1.201:8000/rps/csl.cgi"
        data = {
            'SecID': '0',
            'Page': '0',
            'Flag': 'AllClear_Data',
            'PageFlag':'',
            'CoreNXAction':'./ csl.cgi',
            'CoreNXPage': 'c_topsil.tpl',
            "Dummy": ""
        }

        dummy_var = int(datetime.timestamp(datetime.now()) * 1000)
        r2 = self.s.get('http://192.168.1.201:8000/usermode')
        data["Dummy"] = dummy_var
        r2 = self.s.post(url_2, data=data,headers = headers)
        print (r2.text )

    def get_counter_list(self):
        url_2 = 'http://192.168.1.201:8000/rps/pdeptid.csv?Flag=Csv_Data&LogType=8&Dummy='

        url_2 += str(self.dummy_var)
        r2 = self.s.get('http://192.168.1.201:8000/usermode')
        r = self.s.get(url_2, headers=headers).text

        new_r = str(r).split('\n')
        new_r[0] =new_r[0]+'\r'

        today = datetime.today()
        TemplateFilePath = "{}\\Smart Property Management (S) Pte Ltd\\SMART HQ CORNER - SMART Invoice - STATIONERY PHOTOCOPY\\PHOTOCOPIER FRANKING REPORT\\PHOTOCOPIER\\{}\\{}\\"
        TemplateFilename = "{} - CANON C5540.csv"
        FilePath = TemplateFilePath.format(os.environ['Userprofile'],today.strftime("%Y"),
            "{:02d}".format((today - timedelta(days=5)).month) + " - " + (today - timedelta(days=5)).strftime(
                "%b-%y").upper())
        FileName = TemplateFilename.format(today.strftime("%Y%m%d"))
        try:
            os.makedirs(FilePath)
        except OSError:
            print("Folder Existed")

        FilePathName = os.path.join(FilePath, FileName)

        with open(FilePathName , 'w', encoding= "utf-8") as csv_file:
            csv_writer = csv.writer(csv_file)
            for line in new_r:
                csv_file.write(line)
    
    def update_log_list(self):
        printerModel = "Canon_IR5540"
        url_2 = 'http://192.168.1.201:8000/rps/pprint.csv?LogType=0&Flag=Csv_Data&Dummy='
        headers = {
            'Accept': 'text / h     tml, application / xhtml + xml, application / xml;q = 0.9, image / webp, image / apng, * / *;q = 0.8, application / signed - exchange;v = b3',
            'Accept - Encoding' : 'gzip, deflate',
            'Accept - Language': 'en - US, en;q = 0.9',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'
        }
        data = {
            'LogType' : '0',
            'Flag' : 'Csv_Data',
            'Dummy' : str(self.dummy_var)
        }
    
    
        url_2 += str(self.dummy_var)
        r2 = self.s.get('http://192.168.1.201:8000/usermode')
        r = self.s.get(url_2, headers=headers, data= data)
        return (r)
    
    #
    #     # os.chdir(r'Z:\STATIONERY,POSTAGE,PHOTOCOPY\PHOTOCOPIER FRANKING REPORT\PHOTOCOPIER\LOG LIST')
    #     # def Timestamp_Endtime( Endtime):
    #     #     return datetime.strptime(Endtime['End Time '], '%d/%m %Y %X').timestamp()
    #     #
    #     # Old_log = pd.read_csv('CANON_PRINT_LOG_0218.csv')
    #     # Old_log['Time Stamp '] = Old_log.apply(lambda row: Timestamp_Endtime(row), axis=1)
    #     # Old_log = Old_log.sort_values('Time Stamp ',ascending= 0)
    #     session = Azureconnect().session
    #     lastEntry = session.query(printerLog).filter(printerLog.printerModel == "Canon_IR5540").order_by(desc(printerLog.printDateTime)).first()
    #     # Last_log = lastEntry
    #
    #     new_r = str(r.text).split('\n')
    #     new_r[0] = new_r[0] + '\r'
    #     IterNew_r =iter(new_r)
    #     next(IterNew_r)
    #
    #     for line in new_r[1:-1]:
    #         cell = str(line).split(',')
    #
    #         if cell[0] == "" :
    #             break
    #
    #         if datetime.strptime(cell[3], '%d/%m %Y %X' ).timestamp() > lastEntry.printDateTime.timestamp():
    #             MCST_id = cell[4]
    #             printerJobNo = cell[0]
    #             printType = cell[5]
    #             printFileName = cell[6]
    #             printUserName = cell[7]
    #             printedPages = re.search('"(.+) X (.+)"',cell[10])
    #             printSheetPages =  printedPages.group(1)
    #             printCopies = printedPages.group(2)
    #             printStatus = cell[11]
    #
    #             newEntryLog = printerLog(MCST_id=MCST_id, printerJobNo = printerJobNo, printType=printType, printFileName= printFileName,
    #                                      printUserName=printUserName, printSheetPages=printSheetPages, printCopies= printCopies,
    #                                      printStatus = printStatus)
    #
    #             session.add(newEntryLog)
    #
    #
    #             # Old_log=  Old_log.append(dicCell ,ignore_index=True)
    #
    #     # Old_log['Time Stamp '] = Old_log.apply(lambda row: Timestamp_Endtime(row), axis=1)
        # Old_log = Old_log.sort_values('Time Stamp ', ascending=0)
        #
        # Old_log.to_csv('CANON_PRINT_LOG_0218.csv',index= False)
        #
        #
        # session.commit()
    def post_new_account(self,New_account):
        url_2 = 'http://192.168.1.201:8000/rps/csp.cgi'
        headers = {
            'Accept': 'text / html, application / xhtml + xml, application / xml;q = 0.9, image / webp, image / apng, * / *;q = 0.8, application / signed - exchange;v = b3',
            'Accept - Encoding': 'gzip, deflate',
            'Accept - Language': 'en - US, en;q = 0.9',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'
        }
        data = {
            'SecID' : New_account,
            'Pswd' : New_account,
            'Pswd_Chk': '1',
            'ScanLimitCL' : '0',
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
        r2 = self.s.get('http://192.168.1.201:8000/usermode')
        r3 = self.s.post(url_2, headers= headers, data= data)
        # print (r3.text)+

