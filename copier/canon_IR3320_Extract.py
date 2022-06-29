import csv
from abc import abstractclassmethod
from datetime import datetime,timedelta
from lib2to3.pgen2 import driver
import requests
import pandas as pd
import os
import html5lib
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from requests_html import HTML, HTMLSession




headers = {
    'user-agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'
}

class extract_copier_canon_ir3320():
    PATH = f"{os.environ['USERPROFILE']}\Smart Property Management (S) Pte Ltd\SMART HQ ACCOUNTS - SMART HQ ACCOUNTS\SMARTYWARE\chromedriver.exe"
    def __init__(self) -> None:
        self.driver = webdriver.Chrome(self.PATH)
        self.driver.get("http://192.168.1.203")
        self.driver.find_element_by_id("details-button").click()
        self.driver.find_element_by_id("proceed-link").click()
        self.driver.find_element_by_id("deptid").send_keys("8888")
        self.driver.find_element_by_id("password").send_keys("9999", Keys.TAB, Keys.ENTER)
        self.driver.find_element_by_link_text('Settings/Registration').click()
        dummy_var = self.driver.current_url.split('Dummy=')[1]
    # url = 'https://192.168.1.203:8443/login'
    # nest_asyncio.apply()
    # session = HTMLSession()

    # dummy_var = int(datetime.timestamp(datetime.now()) * 1000)
    # r = session.get(url, headers=headers,verify=False)

    # r = session.post(url,  data={
    #     'uri' : '/rps/',
    #     'deptid': "8888" ,
    #     'password': "9999"
    # },verify=False)

    def clear_counter_list(self):
        url_2= "https://192.168.1.203:8443/rps/csmp.cgi"
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

        # dummy_var = int(datetime.timestamp(datetime.now()) * 1000)
        # r2 = self.s.get('http://192.168.1.203:8443/usermode', verify=False)
        # data["Dummy"]= dummy_var
        # r2 = self.s.post(url_2,data= data, headers= headers, verify=False)
        url_2 = 'https://192.168.1.203:8443/rps/csl.cgi?Flag=Init_Data&SecID=0&Page=0&Dummy='+str(self.dummy_var)
        if not self.driver.current_url == url_2 : self.driver.get(url_2)
        self.driver.find_element_by_xpath("//input[@value='Settings...']").click()
        self.driver.find_element_by_id("Reset").click()
        self.driver.switch_to.alert.accept()
    
    def get_counter_list(self):
        today = datetime.today()
        TemplateFilePath= "{}\\Smart Property Management (S) Pte Ltd\\SMART HQ CORNER - SMART Invoice - STATIONERY PHOTOCOPY\\PHOTOCOPIER FRANKING REPORT\\PHOTOCOPIER\\{}\\{}\\"
        TemplateFilename = "{} - CANON C3320.csv"
        FilePath = TemplateFilePath.format(os.environ['Userprofile'], today.strftime("%Y"),
                   "{:02d}".format((today-timedelta(days=5)).month) + " - " + (today-timedelta(days=5)).strftime("%b-%y").upper())
        FileName = TemplateFilename.format(today.strftime("%Y%m%d"))
        try:
            os.makedirs(FilePath)
        except OSError:
            print ("Folder Exist dummy_var")

        FilePathName = os.path.join(FilePath,FileName)

        with open(FilePathName, 'w', encoding="utf-8", newline='') as csv_file:
            headersRow = ['Dept. ID','Total Prints','Color Total','Black & White Total',
                          'Color Copy','Color Scan','Color Print','Black & White Copy','Black & White Scan',
                          'Black & White Print']
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow(headersRow)
            
            dummy_var = int(datetime.timestamp(datetime.now()) * 1000)
            # r2 = self.session.get('https://192.168.1.203:8443/usermode', verify=False)
            
            # WebDriverWait(self.driver, 300).until(
            # EC.presence_of_element_located((By.LINK_TEXT, "User Management"))).click()
            # WebDriverWait(self.driver, 300).until(
            # EC.presence_of_element_located((By.LINK_TEXT, "Department ID Management"))).click()
            
            
            url_2 = 'https://192.168.1.203:8443/rps/csl.cgi?Flag=Init_Data&SecID=0&Page={}&Dummy='+str(dummy_var)

            for page_no in range(0,2):
                # r = self.session.get(url_2.format(page_no), headers=headers, verify=False)
                # source = r.text
                # html = HTML(html=source)
                # html.render()

                # page_request_url = request_url.replace("Page=0",f"Page={page_no}")
                # print (url_2, self.driver.current_url)
                if not url_2 == self.driver.current_url: self.driver.get(url_2.format(page_no))
                soup = BeautifulSoup(self.driver.page_source, 'html.parser')

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
        url_2 = 'http://192.168.1.203:8000/rps/csp.cgi'
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
        r2 = self.s.get('http://192.168.1.203:8000/usermode')
        r3 = self.s.post(url_2, headers=headers, data=data)
        # print(r3.text)

    def update_log_list(self):
        url_2 = ' http://192.168.1.203:8000/rps/pprint.csv?LogType=0&Flag=Csv_Data&Dummy='
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
        r2 = self.s.get('http://192.168.1.203:8000/usermode')
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
