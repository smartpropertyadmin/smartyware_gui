import csv
from abc import abstractclassmethod
from datetime import datetime,timedelta
import time
from lib2to3.pgen2.token import OP
import requests
import pandas as pd
import os
import html5lib
import glob
from bs4 import BeautifulSoup
from requests_html import HTML, HTMLSession
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options




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

class extract_copier_toshiba_5015ac():
    url = 'http://192.168.1.202/contentwebserver'
    url1 = ' http://192.168.1.202/?MAIN=TOPACCESS'
    PATH = f"{os.environ['USERPROFILE']}\Smart Property Management (S) Pte Ltd\SMART HQ ACCOUNTS - SMART HQ ACCOUNTS\SMARTYWARE\chromedriver.exe"
    DOWNLOAD_PATH = f"{os.environ['USERPROFILE']}\Downloads"
    options = Options()
    # options.add_argument("user-agent=whatever yourrrr want")
    # options.add_experimental_option("excludeSwitches", ["enable-automation"])
    # options.add_experimental_option('useAutomationExtension', False)
    def __init__(self) -> None:
        
        self.driver = webdriver.Chrome(self.PATH , options=self.options)
        self.driver.get(self.url1)
        # self.driver.switch_to.frame("TATopLevelFrameSet")

        self.driver.switch_to.frame("TopLevelFrame")
        WebDriverWait(self.driver, 30).until(
                    EC.presence_of_element_located((By.XPATH, "//frame[@name='topframe']")))
        self.driver.switch_to.frame("topframe")
        self.driver.find_element_by_link_text("Login").click()
        
        WebDriverWait(self.driver, 30).until(
                    EC.presence_of_element_located((By.XPATH, "//frame[@name='TopLevelFrame']")))
        self.driver.switch_to.frame("TopLevelFrame")
        
        self.driver.switch_to.frame("Loginframe")
        self.driver.find_element_by_name("USERNAME").send_keys("admin")
        self.driver.find_element_by_name("PASS").send_keys(123456)
        self.driver.find_element_by_name("Login").click()
        time.sleep(3)
      
    def get_counter_list(self):
        
        WebDriverWait(self.driver, 20).until(EC.frame_to_be_available_and_switch_to_it((By.XPATH, "//frame[@name='TopLevelFrame']")))
        # self.driver.switch_to.frame("TopLevelFrame")
        self.driver.switch_to.frame("topframe")
        self.driver.find_element_by_id("USERMGMT-anchor").click()
        self.driver.switch_to.parent_frame()
        self.driver.switch_to.frame("SubMenu")
        elem = WebDriverWait(self.driver, 30).until(
                    EC.presence_of_element_located((By.XPATH, "//td[@id='tdExprtImport']")))
        self.driver.find_element_by_id("tdExprtImport").click()
        self.driver.switch_to.parent_frame()
        self.driver.switch_to.frame("contents")
        self.driver.find_element_by_name("DeptInfoExprtSmlLr").click()
        WebDriverWait(self.driver, 30).until(
                    EC.element_to_be_clickable((By.XPATH, "//a[@id='DeptInfoExprtSmlLrgFileName']"))).click()
        # self.driver.find_element_by_id("DeptInfoExprtSmlLrgFileName").click()
        time.sleep(3)
        download_file_path = ""
        while not f'DEPT_SMALL_LARGE_COUNT_{datetime.today().strftime("%y%m%d")}' in download_file_path:
            download_file_path = max(glob.iglob(f'{self.DOWNLOAD_PATH}\*.csv'), key=os.path.getctime)
        
        today = datetime.today()
        TemplateFilePath = "{}\\Smart Property Management (S) Pte Ltd\\SMART HQ CORNER - SMART Invoice - STATIONERY PHOTOCOPY\\PHOTOCOPIER FRANKING REPORT\\PHOTOCOPIER\\{}\\{}\\"
        TemplateFilename = "{} - TOSHIBA 5015AC.csv"
        FilePath = TemplateFilePath.format(os.environ['Userprofile'],today.strftime("%Y"),
            "{:02d}".format((today - timedelta(days=5)).month) + " - " + (today - timedelta(days=5)).strftime(
                "%b-%y").upper())
        FileName = TemplateFilename.format(today.strftime("%Y%m%d"))
        try:
            os.makedirs(FilePath)
        except OSError:
            print ("Folder Exidummy_var"
                   "sted")

        FilePathName = os.path.join(FilePath,FileName)
        os.rename(download_file_path, FilePathName)
        self.driver.switch_to.parent_frame()
        time.sleep(2)
        self.update_log_list()

        

    def update_log_list(self):
        self.driver.switch_to.frame("topframe")
        self.driver.find_element_by_id("LOGS").click()
        self.driver.switch_to.parent_frame()
        self.driver.switch_to.frame("SubMenu")
        WebDriverWait(self.driver, 30).until(
                            EC.element_to_be_clickable((By.XPATH, "//a[@id='ExportLog']"))).click()
        self.driver.switch_to.parent_frame()
        self.driver.switch_to.frame("contents")
        self.driver.switch_to.frame("fraList")
        WebDriverWait(self.driver, 30).until(
                            EC.element_to_be_clickable((By.XPATH, "//input[@value='Create New File&Clear Log']"))).click()
        self.driver.switch_to.alert.accept()
        WebDriverWait(self.driver, 30).until(
                    EC.element_to_be_clickable((By.XPATH, "//a[@id='PrintJobFileName']"))).click()
        time.sleep(3)
        download_file_path = ""
        while not f'PRINT_LOG_{datetime.today().strftime("%y%m%d")}' in download_file_path:
            download_file_path = max(glob.iglob(f'{self.DOWNLOAD_PATH}\*.csv'), key=os.path.getctime)
        
        today = datetime.today()
        TemplateFilePath = "{}\\Smart Property Management (S) Pte Ltd\\SMART HQ CORNER - SMART Invoice - STATIONERY PHOTOCOPY\\PHOTOCOPIER FRANKING REPORT\\PHOTOCOPIER\\LOG LIST\\TOSHIBA\\"
        FilePath = TemplateFilePath.format(os.environ['Userprofile'],today.strftime("%Y"))
        FileName = f'PRINT_LOG_{datetime.today().strftime("%y%m%d")}.csv'
        try:
            os.makedirs(FilePath)
        except OSError:
            print ("Folder Exidummy_var"
                   "sted")

        FilePathName = os.path.join(FilePath,FileName)
        os.rename(download_file_path, FilePathName)
        self.driver.switch_to.parent_frame()
        self.driver.switch_to.parent_frame()
        time.sleep(2)
    
    def clear_counter_list(self):
        WebDriverWait(self.driver, 20).until(EC.frame_to_be_available_and_switch_to_it((By.XPATH, "//frame[@name='TopLevelFrame']")))
        self.driver.switch_to.frame("topframe")
        self.driver.find_element_by_id("USERMGMT-anchor").click()
        self.driver.switch_to.parent_frame()
        self.driver.switch_to.frame("SubMenu")
        WebDriverWait(self.driver, 30).until(
                                    EC.element_to_be_clickable((By.XPATH, "//a[@id='DeptMgmt']"))).click()
        self.driver.switch_to.parent_frame()
        self.driver.switch_to.frame("contents")
        self.driver.switch_to.frame("fraTitle")
        WebDriverWait(self.driver, 30).until(
                    EC.element_to_be_clickable((By.XPATH, "//input[@name='ResetAll']"))).click()
        self.driver.switch_to.alert.accept()
        self.driver.switch_to.parent_frame()
        self.driver.switch_to.parent_frame()
        time.sleep(2)
        








if __name__ == '__main' :
    extract_copier_toshiba_5015ac.get_counter_list()
