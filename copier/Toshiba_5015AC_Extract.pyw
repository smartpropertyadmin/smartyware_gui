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
    'Accept' : '*/*',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language' : 'en-US,en-SG;q=0.9,en;q=0.8,zh-CN;q=0.7,zh;q=0.6',
    'Cache-Control' : 'no-cache',
    'Connection' : 'keep-alive',
    'Content-Length' : '728',
    'Content-Type' : 'text/plain; charset=UTF-8',
    'csrfpId' : '192.168.1.240.15d67824a549b12339937084ccda4c82',
    'Host' : '192.168.1.202',
    'Origin' : 'http://192.168.1.202',
    'Pragma' : 'no-cache',
    'Referer' : 'http://192.168.1.202/Counters/DeptMngmntAdminList.html?v=1566946497ta',
    'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36'
}

class extract_copier():
    url = 'http://192.168.1.202/contentwebserver'
    url1 = ' http://192.168.1.202/?MAIN=TOPACCESS'

    s =  HTMLSession()

    payload= {
       'LOGINMODE': 'NORMAL',
       'SECURITYLEVEL': 'LOW',
       'USERCRED': ',USERNAME:admin,USERID:10002,',
       'DiagnosticMode': ',9963:2,8832:1,3656:1,3644:0,6080:0,3832:0,9337:0,9298:0,9299:0,8921:1,9001:1,9000:0,6080:0,9886:1,9817:2,9384:1,9227:1,9228:1,9229:1,9215:0,6084:0,8720:0,6091:1,8798:1.7,3683:0,970:0,',
       'USERROLE' : ':⇔Administrator:⇔AccountManager:⇔CopyOperator:⇔ScanOperator:⇔Print:⇔PrintOperator:⇔eFilingOperator:⇔ColorPrintCopyOperator:⇔FaxOperator:⇔Auditor:⇔Fax:⇔',
       'SESSID' : '123456789',
       'TAPERMISSIONS' : 'AddressBookRemoteAccess,ColorPrint,CopyJob,DeviceSetting,EWBAccess,FaxReceivedPrint,FaxTransmission,IPFaxTransmission,InternetFaxTransmission,JobOperation,LogExport,LogRead,PrintJob,PrintManagement,RemoteScan,SendEmail,StoreToLocalStorage,StoreToRemoteServer,StoreToUSBDevice,USBDirectPrint,UserDepartmentManagement,WSScanPush,eFilingAccess',
       'LOGINSTATUS' : 'Authenticated',
       'LocaleOrder': 'WesternOrder',
       'EFICtrlInstalled' : '0',
       'TA_SETTINGS' : 'YES~YES',
       'ADDR_BOOK_REMOTE_PERM' : 'AddressBookRemoteAccess',
       'AddressBkPerm' : 'NoRestriction',
       'AuthenticationType' : 'Local',
       'SYNCHOME' : 'false'

    }


    payload = {
        f"<DeviceInformationModel><GetValue><Accounting></Accounting></GetValue><SetValue><Accounting><BillingCodes><BillingCodeInfo></BillingCodeInfo></BillingCodes></Accounting></SetValue><Command><GetBillingCodes><commandNode>Accounting/BillingCodes</commandNode><Params><pageSize contentType='Value'>200</pageSize><pageNo contentType='Value'>1</pageNo><pagingType contentType='Value'>IndexNumberBase</pagingType><sortProperty contentType='Value'>ID</sortProperty><sortOrder contentType='Value'>Asc</sortOrder><includeCounterQuota>AgentTotalizedCounters</includeCounterQuota><billingCodesDetails contentType='XPath'>Accounting/BillingCodes/BillingCode</billingCodesDetails></Params></GetBillingCodes></Command></DeviceInformationModel>"
    }


    s.params = payload
    r = s.post(url, headers=headers)
    print (r.text)
    s.params = {'MAIN' : 'TOPACCESS'}
    # r2 = s.get(url1 )
    # print(r2.text)
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
        TemplateFilePath= "Z:\\STATIONERY,POSTAGE,PHOTOCOPY\PHOTOCOPIER FRANKING REPORT\PHOTOCOPIER\\2019\\{}\\"
        TemplateFilename = "{} - #02-26 CANON OPERATION.csv"
        FilePath = TemplateFilePath.format("{:02d}".format((today-timedelta(days=5)).month) + " - " + (today-timedelta(days=5)).strftime("%b'%y").upper())
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

            url_2 = 'http://192.168.1.202/Counters/DeptMngmntAdminList.html'
            dummy_var = int(datetime.timestamp(datetime.now()) * 1000)
            url_2 += str(dummy_var)
            r2 = self.s.get('http://192.168.1.202/Counters/DeptMngmntAdminList.html')
            print (r2.text)
            # for page_no in range(0,2):
            #     r = self.s.get(url_2.format(page_no), headers=headers)
            #     source = r.text
            #     html = HTML(html=source)
            #     html.render()
            #     soup = BeautifulSoup(html.html, 'html.parser')
            #
            #     Counter_table = soup.find('table')
            #     # print(Counter_table)
            #     Counter_body = Counter_table.find('tbody')
            #
            #
            #     row_value = []
            #     for tr in Counter_body.find_all('tr'):
            #
            #         for td in tr.find_all('td'):
            #
            #             cellValue = td.text.strip().split('\n',1)[0]
            #
            #
            #             if cellValue .isnumeric():
            #                 row_value.append(cellValue )
            #         csv_writer.writerow(row_value)
            #         row_value = []

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

if __name__ == '__main' :
    extract_copier.get_counter_list()
