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


class extract_copier_ricoh_c3503():
    url_login = 'http://192.168.1.200/web/guest/en/websys/webArch/authForm.cgi'
    url = 'http://192.168.1.200/web/guest/en/websys/webArch/login.cgi'
    s = HTMLSession()
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'en-US,en;q=0.9',
        'Connection': 'keep-alive',
        'Cookie': 'risessionid={}; cookieOnOffChecker=on; wimsesid={}',
        'Host': '192.168.1.200',
        'Upgrade-Insecure-Requests':'1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.87 Safari/537.36'
    }

    loginForm = s.get(url_login,headers= headers)
    soup = BeautifulSoup(loginForm.text, 'html.parser')

    wimToken = soup.find("input",attrs={"name": "wimToken"})


    dummy_var = int(datetime.timestamp(datetime.now()) * 1000)

    data = {
        'wimToken': '',
        'userid_work': '',
        'userid': 'YWRtaW4=',
        'password_work': '',
        'password': '',
        'open': ''}

    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'en-US,en;q=0.9',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Content-Length': '80',
        'Content-Type': 'application / x-www-form-urlencoded',
        'Cookie': 'risessionid={}; cookieOnOffChecker=on; wimsesid={}',
        'Host': '192.168.1.200',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.87 Safari/537.36'
    }
    headersCookie = headers['Cookie']
    headers['Cookie'] = headers['Cookie'].format(s.cookies['risessionid'], "--")
    data['wimToken']= wimToken['value']
    r = s.post(url,data=data, headers =headers)



    def post_new_account(self, New_account, Account_name):

        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7,ms-MY;q=0.6,ms;q=0.5',
            'Connection': 'keep-alive',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Cookie': 'risessionid={}; cookieOnOffChecker=on; wimsesid={}',
            'Host': '192.168.1.200',
            'Origin': 'http://192.168.1.200',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.87 Safari/537.36',

        }
        headers['Cookie'] = headers['Cookie'].format(self.s.cookies['risessionid'], self.s.cookies['wimsesid'])
        risessionid = self.s.cookies['risessionid']
        url_3 = 'http://192.168.1.200/web/entry/en/address/adrsList.cgi'
        url_2 = 'http://192.168.1.200/web/entry/en/address/adrsSetUser.cgi'

        r3 = self.s.get(url_3, headers=headers)

        # main page
        headers = {
            'Accept': 'text/plain, */*',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7,ms-MY;q=0.6,ms;q=0.5',
            'Connection': 'keep-alive',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Cookie': 'risessionid={}; cookieOnOffChecker=on; wimsesid={}',
            'Host': '192.168.1.200',
            'Origin': 'http://192.168.1.200',
            'Referer': 'http://192.168.1.200/web/entry/en/address/adrsList.cgi',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.87 Safari/537.36',
            'X-Requested-With' : 'XMLHttpRequest'
        }

        headers['Cookie'] = headers['Cookie'].format(risessionid, self.s.cookies['wimsesid'])

        # headers['Content-Length'] = '945'
        data = {
            'inputSpecifyModeIn': 'WRITE',
            'listUpdateIn': 'UPDATE',
            'wimToken': self.wimToken['value'],
            'mode': 'ADDUSER',
            'pageSpecifiedIn':'',
            'pageNumberIn':'',
            'outputSpecifyModeIn':'',
            'wayFrom':'adrsGetUser.cgi?outputSpecifyModeIn=SETTINGS',
            'wayTo': 'adrsList.cgiundefined',
            'isSelfPasswordEditMode': 'false',
            'entryIndexIn': '{:05d}'.format(int(New_account)),
            'entryNameIn': Account_name,
            'entryDisplayNameIn': '{:.10}'.format(Account_name),
            'priorityIn': '5',
            'entryTagInfoIn': '9,1,1,1',
            'userCodeIn': New_account,
            'smtpAuthAccountIn': 'AUTH_SYSTEM_O',
            'folderAuthAccountIn': 'AUTH_SYSTEM_O',
            'ldapAuthAccountIn': 'AUTH_SYSTEM_O',
            'availableFuncIn': 'COPY_FC,COPY_TC,COPY_MC,COPY_BW,PRT_FC,PRT_BW,DBX,FAX,SCAN,MFPBROWSER',
            'acsLimitationIn': 'ACSONLY_O',
            'entryUseIn': 'ENTRYUSE_TO_O,ENTRYUSE_FROM_O',
            'faxDestIn':'',
            'mailAddressIn':'',
            'isCertificateExist': 'false',
            'isEncryptAlways': 'false',
            'folderProtocolIn': 'SMB_O',
            'folderPathNameIn': ''
        }
        print(headers)
        print(data)

        r2 = self.s.post(url_2, headers=headers, data=data)
        print(r2.text)



    def get_counter_list(self):
        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'en-US,en;q=0.9',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'Cookie': 'cookieOnOffChecker=on; wimsesid={}',
            'Host': '192.168.1.200',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.87 Safari/537.36'
        }
        headers['Cookie'] =headers['Cookie'].format(self.s.cookies['wimsesid'])
        r2 = self.s.get('http://192.168.1.200/web/entry/en/websys/status/getUserCounter.cgi', headers = headers)
        soup = BeautifulSoup(r2 .text, 'html.parser')

        wimToken = soup.find("input", attrs={"name": "wimToken"})

        url_2 = 'http://192.168.1.200/web/entry/en/websys/status/downloadUserCounter.cgi'

        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'en-US,en;q=0.9',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'Content-Length': '69',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Cookie': 'cookieOnOffChecker=on; wimsesid={}',
            'Host': '192.168.1.200',
            'Origin': 'http://192.168.1.200',
            'Referer':'http://192.168.1.200/web/entry/en/websys/status/getUserCounter.cgi',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.87 Safari/537.36'
        }
        headers['Cookie'] = headers['Cookie'].format(self.s.cookies['wimsesid'])

        data = {
            'wimToken': wimToken['value'],
            'accessConf': '',
            'offset': '0',
            'userCounterListPage': '',
            'count': '10'
        }

        r = self.s.post(url_2, headers=headers,data= data)
        today = datetime.today()
        TemplateFilePath = "Z:\\STATIONERY,POSTAGE,PHOTOCOPY\PHOTOCOPIER FRANKING REPORT\PHOTOCOPIER\\{}\\{}\\"
        TemplateFilename = "{} - RICOH C3503.csv"
        FilePath = TemplateFilePath.format(today.strftime("%Y"),
            "{:02d}".format((today - timedelta(days=5)).month) + " - " + (today - timedelta(days=5)).strftime("%b'%y").upper())
        FileName = TemplateFilename.format(today.strftime("%Y%m%d"))
        try:
            os.makedirs(FilePath)
        except OSError:
            print("Folder Existed")

        FilePathName = os.path.join(FilePath, FileName)

        with open(FilePathName, 'w', encoding="utf-8", newline='') as csv_file:
            csv_writer = csv.writer(csv_file)
            for line in r.text:
                csv_file.write(line)

    def update_log_list(self):
        url_2 = 'http://192.168.1.200/web/entry/en/webprinter/jobHistory.cgi'

        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'en-US,en;q=0.9',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',

            'Cookie': 'cookieOnOffChecker=on; wimsesid={}',
            'Host': '192.168.1.200',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.87 Safari/537.36'
        }

        data ={
            'wimToken': self.wimToken['value'],
            'size': '20',
            'baseID': '',
            'baseIndex': '',
            'position': '0',
            'scene': '0',
            'operate': '0',
            'number': '20'

        }

        headers['Cookie'] = headers['Cookie'].format(self.s.cookies['wimsesid'])
        risessionid = self.s.cookies['risessionid']
        r = self.s.get(url_2, headers=headers)

        headers['Content-Length'] =  '90'
        headers['Content-Type']=  'application/x-www-form-urlencoded'
        headers['Referer']='http://192.168.1.200/web/entry/en/webprinter/jobHistory.cgi'
        soup = BeautifulSoup(r.text, 'html.parser')

        Log_table = soup.find('table',attrs={'class':"reportListCommon"})

        baseid= Log_table.find('td', attrs= {'class' : "listData"})

        data['baseID'] = baseid.text.strip()
        data['baseIndex'] = baseid.text.strip()

        headers['Cookie'] = 'risessionid={}; cookieOnOffChecker=on; wimsesid={}'.format(risessionid,self.s.cookies['wimsesid'])
        r = self.s.post(url_2, headers=headers,data=data)
        soup = BeautifulSoup(r.text, 'html.parser')
        Log_table = soup.find('table', attrs={'class': "reportListCommon"})

        os.chdir(r'Z:\STATIONERY,POSTAGE,PHOTOCOPY\PHOTOCOPIER FRANKING REPORT\PHOTOCOPIER\LOG LIST')

        def Timestamp_Endtime(Endtime):
            try :
                return datetime.strptime(Endtime['Created At'], '%d/%m/%y %H:%M').timestamp()
            except :
                print (Endtime['Created At'])




        Old_log = pd.read_csv('RICOH_PRINT_LOG_0218.csv', )
        # Old_log['Time Stamp '] = Old_log.apply(lambda row: Timestamp_Endtime(row), axis=1)
        Old_log = Old_log.sort_values('Time Stamp ', ascending=0)

        Last_log = Old_log.iloc[0]['Time Stamp ']
        cell = []
        for td in Log_table.find_all('td', attrs= {'class' : "listData"}):

            cell.append(td.text.strip())

            try :
                nobr = (td.previous_sibling.previous_sibling).find_all('nobr')
                cell[5] = nobr[0].text.strip() + " " + nobr[1].text.strip()
                cell.append(datetime.strptime(cell[5], '%d/%m/%Y %X').timestamp())
                if  cell[7] > Last_log:
                    dicCell = dict(zip(Old_log.head(-1), cell))
                    Old_log = Old_log.append(dicCell, ignore_index=True)

                cell = []
            except:
                continue
        #
        Old_log = Old_log.sort_values('Time Stamp ', ascending=0)
        Old_log.to_csv('RICOH_PRINT_LOG_0218.csv', index=False)

# extract_0218ricoh().post_new_account('1639','QUEENS ASTRID GARDENS')