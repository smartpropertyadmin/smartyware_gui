from asyncore import loop
import time
from selenium import webdriver
from selenium.webdriver import ChromeOptions
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime
from dateutil.relativedelta import relativedelta
import pandas as pd
import glob
import os
import re

class crimsion_intereq_selenium():
    PATH = f"{os.environ['USERPROFILE']}\Smart Property Management (S) Pte Ltd\SMART HQ ACCOUNTS - SMART HQ ACCOUNTS\SMARTYWARE\chromedriver.exe"
    USERNAME_1 = "smsta001"
    USERNAME_2 = "smsta002"
    
    DOWNLOAD_PATH = f"{os.environ['USERPROFILE']}\Downloads"
    main_page_url = "https://www.mcstintereq.com.sg/mcstweb/AgencyReplyServlet?action=list"
    folder_search_path = f'{os.environ["USERPROFILE"]}\Smart Property Management (S) Pte Ltd\SMART HQ ACCOUNTS - SMART HQ ACCOUNTS\99999 - CONSOLIDATION\CRIMSON SEC 47\SECTION 47C REPLY'
    def __init__(self, PASSWORD = "SmartProp800") :
        self.driver = webdriver.Chrome(self.PATH)
        self.driver.get(self.main_page_url)
        self.PASSWORD = PASSWORD
        
    def sign_in(self, username):
        self.driver.find_element_by_id("txtUserId").send_keys(username)
        self.driver.find_element_by_id("txtPassword").send_keys(self.PASSWORD, Keys.TAB ,Keys.ENTER)

    def retrieve_monthly_report(self, report_month):
        self.sign_in(self.USERNAME_1)
        search_start_date = (report_month - relativedelta(months=6, days=-1)).strftime("%d/%m/%Y")
        search_end_date = report_month.strftime("%d/%m/%Y")
        self.driver.get('https://www.mcstintereq.com.sg/mcstweb/ReportServlet?action=search')
        self.driver.find_element_by_id("txtDateFrom").clear()
        self.driver.find_element_by_id("txtDateFrom").send_keys(search_start_date)
        self.driver.find_element_by_id("txtDateTo").clear()
        self.driver.find_element_by_id("txtDateTo").send_keys(search_end_date)
        self.driver.find_element_by_id("btn").click()
        self.driver.find_element_by_link_text('Excel').click()
        download_file_path = ""
        while not f'Bill Summary Dated {datetime.today().strftime("%d-%m-%Y")}' in download_file_path:
            download_file_path = max(glob.iglob(f'{self.DOWNLOAD_PATH}\*.xlsx'), key=os.path.getctime)
        report_pd = pd.read_excel(download_file_path)
        report_pd['REPLIED / BILLING DATE'] = pd.to_datetime(report_pd['REPLIED / BILLING DATE'] )
        filter_pd  = report_pd[report_pd['REPLIED / BILLING DATE'].dt.month == report_month.month]
        report_file_path = f"{os.environ['USERPROFILE']}\Smart Property Management (S) Pte Ltd\SMART HQ ACCOUNTS - SMART HQ ACCOUNTS\99999 - CONSOLIDATION\CRIMSON SEC 47\CRIMSON LOGIC BILLING.xlsx"
        existing_pd= pd.read_excel(report_file_path)
        combine_pd = pd.concat([existing_pd, filter_pd]).reset_index(drop=True)
        combine_pd.to_excel(report_file_path, index=False, columns=['LF CONTROL NO','LAW FIRM NAME','MCST / SUB-MCST NO','DEVELOPMENT NAME','BLOCK NO','UNIT NO','FEE','GST','RECEIVED DATE','REPLIED / BILLING DATE'])
    
    def upload_sec_cert(self, crimsion_list):
        self.sign_in(self.USERNAME_1)
        search_start_date = (datetime.today() - relativedelta(months=18)).strftime("%d/%m/%Y")
        if not self.driver.current_url == self.main_page_url: self.driver.get(self.main_page_url)
        self.driver.find_element_by_id("txtDateFrom").clear()
        self.driver.find_element_by_id("txtDateFrom").send_keys(search_start_date,Keys.ENTER,Keys.TAB,Keys.TAB)
        self.driver.find_element_by_xpath("//button[@onclick='goSearch()']").click()
        
        
        for crimsion_id in crimsion_list: 

            upload_file = glob.glob(f'{self.folder_search_path}\*{crimsion_id}*.pdf')
            search_bar = self.driver.find_element_by_xpath("//input[@type='search']")
            search_bar.clear()
            search_bar.send_keys(crimsion_id)
            self.driver.find_element_by_link_text(crimsion_id).click()
            self.driver.find_element_by_name("fileCertificateName").send_keys(upload_file)
            
            self.driver.find_element_by_name("lrSubmit").click()
            WebDriverWait(self.driver, 20)
            self.driver.switch_to.alert.accept()
            try:
                elem = WebDriverWait(self.driver, 30).until(
                    EC.presence_of_element_located((By.XPATH, "//input[@value='CONTINUE']")))
            finally:
                self.driver.back()
                self.driver.back()
    
    def sign_out(self):
        self.driver.find_element_by_class_name('fa-sign-out').click()
    
    def approve_sec_cert(self, crimsion_list):
        
        search_start_date = (datetime.today() - relativedelta(months=18)).strftime("%d/%m/%Y")
        self.driver.find_element_by_id("txtDateFrom").clear()
        self.driver.find_element_by_id("txtDateFrom").send_keys(search_start_date,Keys.ENTER,Keys.TAB,Keys.TAB)
        self.driver.find_element_by_xpath("//button[@onclick='goSearch()']").click()
        for crimsion_id in crimsion_list: 
            search_bar = self.driver.find_element_by_xpath("//input[@type='search']")
            search_bar.clear()
            search_bar.send_keys(crimsion_id)
            self.driver.find_element_by_link_text(crimsion_id).click()
            self.driver.find_element_by_name("lrApprove").click()
            self.driver.back()
            self.driver.back()

    def upload_outstanding_sec(self):
        outstanding_file = glob.glob(f'{self.folder_search_path}\*.pdf')
        crimsion_list = [re.search(r'.+(01\-\d+)\s\-.+\.pdf', filename).group(1) for filename in outstanding_file]
        self.upload_sec_cert(crimsion_list=crimsion_list)
        self.sign_out()
        self.sign_in(self.USERNAME_2)
        self.approve_sec_cert(crimsion_list)


if __name__ == '__main__':
    test = crimsion_intereq_selenium()
    test.upload_outstanding_sec()