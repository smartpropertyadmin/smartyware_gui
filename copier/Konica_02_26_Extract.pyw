import csv
from abc import abstractclassmethod
from datetime import datetime,timedelta
import requests
import pandas as pd
import os
import html5lib
import re
from bs4 import BeautifulSoup
from requests_html import HTML, HTMLSession

class extract_0226konica():
    url =     "http://192.168.1.253/wcd/login.cgi"
    headers = { 'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
                'Accept-Encoding':'gzip, deflate',
                'Accept-Language':'en-US,en;q=0.9',
                'Cache-Control':'max-age=0',
                'Connection':'keep-alive',
                'Content-Length':'34',
                'Content-Type':'application/x-www-form-urlencoded',
                'Cookie':'wd=n; help=off,off,off; selno=En; vm=Flash; uatype=NN; lang=En; access=; param=; usr=S_INF; adm=AS_COU',
                'Host':'192.168.1.253',
                'Origin':'http://192.168.1.253',
                'Upgrade-Insecure-Requests':'1',
                'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.87 Safari/537.36}'
                }
    data = {
        'func': 'PSL_LP1_LOG',
        'password': '12345678'
    }

    s = HTMLSession()
    r = s.post(url,headers= headers, data=data)
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'en-US,en;q=0.9',
        'Connection': 'keep-alive',
        'Cookie': '',
        'Host': '192.168.1.253',
        'Origin': 'http://192.168.1.253',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.87 Safari/537.36}'
        }
    headers['Cookie'] = 'wd=n; help=off,off,off; selno=En; vm=Flash; uatype=NN; lang=En; access=; param=; usr=S_INF; ID={}; adm=AS_CNLExport'.format(s.cookies['ID'])
    a_system =  s.get('http://192.168.1.253/wcd/a_system.xml',headers= headers)
    soup = BeautifulSoup (a_system.text)

    Token_Id = soup.token.text.strip()

    def get_counter_list(self):
        url2 = 'http://192.168.1.253/wcd/a_user.cgi'
        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'en-US,en;q=0.9',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'Content-Length': '111',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Cookie': 'wd=n; help=off,off,off; selno=En; vm=Flash; uatype=NN; lang=En; access=; param=; usr=S_INF; ID={}; adm=AS_CNLExport',
            'Host': '192.168.1.253',
            'Origin': 'http://192.168.1.253',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.87 Safari/537.36}'
        }
        headers['Cookie'] = headers['Cookie'].format(self.s.cookies['ID'])
        data = {
            'func': 'PSL_AS_CNL_EXP',
            'h_token': self.Token_Id,
            'AS_CNL_R_SEL': 'Track'
        }
        r2 = self.s.post(url2, headers=headers, data=data)

        url2 = 'http://192.168.1.253/wcd/a_filedownload'
        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'en-US,en;q=0.9',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'Content-Length': '75',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Cookie': 'wd=n; help=off,off,off; selno=En; vm=Flash; uatype=NN; lang=En; access=; param=; usr=S_INF; ID={}; adm=AS_CNLExport',
            'Host': '192.168.1.253',
            'Origin': 'http://192.168.1.253',
            'Referer': 'http://192.168.1.253/wcd/a_user.cgi',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.87 Safari/537.36}'
            }
        headers['Cookie'] = headers['Cookie'].format(self.s.cookies['ID'])
        data = {
            'func': 'PSL_AS_CNL_CNK',
            'cginame1': 'a_filedownload',
            'cginame2': 'a_filedownload',
            'H_BAK': '0'
        }

        today = datetime.today()
        TemplateFilePath = "Z:\\STATIONERY,POSTAGE,PHOTOCOPY\PHOTOCOPIER FRANKING REPORT\PHOTOCOPIER\\2019\\{}\\"
        TemplateFilename = "{} - #02-26 KONICA OPERATION.csv"
        FilePath = TemplateFilePath.format(
            "{:02d}".format((today - timedelta(days=5)).month) + " - " + (today - timedelta(days=5)).strftime(
                "%b'%y").upper())
        FileName = TemplateFilename.format(today.strftime("%Y%m%d"))
        try:
            os.makedirs(FilePath)
        except OSError:
            print("Folder Existed")

        FilePathName = os.path.join(FilePath, FileName)
        os.chdir(FilePath)

        r2 = self.s.post(url2, headers=headers, data=data, allow_redirects= True)
        print(r2.content)

        # Counter_text_file =  r2.headers.['Content-Disposition'].replace('attachment;filename=','')
        Counter_text_file = r2.headers.get('Content-Disposition')

        fname = re.findall('filename=(.+)',Counter_text_file)
        print (fname[0])
        # CounterFile = self.s.get('http://192.168.1.253/wcd/a_filedownload/{}'.format(Counter_text_file), allow_redirects=True).content
        # CounterFile  = open(fname[0], 'wb').write(r2.content)
        #  os.path.join(FilePath, fname[0]),delimiter="\t")
        # pd.to_csv(FilePathName, index=False)

        with open(fname[0], 'r', encoding="utf-16" ) as text_file:
            reader = csv.reader(text_file,delimiter= "\t")
            with open(FilePathName,'w',encoding="utf-8") as csv_file:
                for row in reader:
                    for cell in row :
                        csv_file.write(cell + ",")
                    csv_file.write('\r')


extract_0226konica().get_counter_list()