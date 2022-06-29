import csv
from datetime import datetime,timedelta
import requests
import re
import os
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import pandas as pd


headers = {
    'user-agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'
}

class reallySg:
    url = 'https://rails-hasura-production-api.really.sg/graphsql'
    PATH = f"{os.environ['USERPROFILE']}\Smart Property Management (S) Pte Ltd\SMART HQ ACCOUNTS - SMART HQ ACCOUNTS\SMARTYWARE\chromedriver.exe"
    login_url = "https://app.really.sg/#/login?redirect=%2Fdashboard"
    def __init__(self) :
        self.driver = webdriver.Chrome(self.PATH)
        
    def sign_in(self, username, password):
        self.driver.get(self.login_url)
        self.driver.find_element_by_name("email").send_keys(username)
        self.driver.find_element_by_name("password").send_keys(password)
        self.driver.find_element_by_xpath("//span[text()='LOG IN']").click()



    def getVendorList(self):
        WebDriverWait(self.driver, 300).until(
            EC.element_to_be_clickable((By.XPATH, "//span[text()='Vendors']"))).click()
        time.sleep(2)
        WebDriverWait(self.driver, 300).until(
            EC.element_to_be_clickable((By.XPATH, "//span[text()='Vendors Directory']"))).click()
        time.sleep(3)
        pagination_span =  WebDriverWait(self.driver, 300).until(
            EC.element_to_be_clickable((By.XPATH,"//span[@class='el-pagination__sizes']")))
        WebDriverWait(pagination_span, 300).until(
            EC.element_to_be_clickable((By.TAG_NAME,"input"))).click()

        self.driver.find_element_by_xpath("//span[text()='50/page']").click()
    


    def extractVendorList(self):
        vendor_pages = int(self.driver.find_element_by_xpath("//ul[@class='el-pager']").find_elements_by_tag_name('li')[-1].text)
        vendor_pd = pd.DataFrame(columns=list(pd.read_html(self.driver.page_source)[0]))
        page_input = self.driver.find_element_by_xpath("//div[@class='el-input el-input--medium el-pagination__editor is-in-pagination']").find_element_by_tag_name("input")
        for vendor_page in range(1, vendor_pages+1):
            page_input.clear()
            page_input.send_keys(vendor_page, Keys.ENTER)
            
            vendor_pd.append(pd.read_html(self.driver.page_source)[1])
        return vendor_pd
    
    def extract_seabridge_dashboard(self, htmlString, outputfilepathname):
       
        soup = BeautifulSoup(htmlString, 'html.parser')
        with open(outputfilepathname, 'w', encoding='utf-8', newline='') as csv_file:
            csvWriter = csv.writer(csv_file)
            row_value= ['Vendor', 'Inv', 'Inv$','Budget', 'po-date', 'inv-due-date', 'match', 'pending with','status', 'inv-desc']
            for div in soup.find_all('div'):
                if div.attrs.get('class'):
                    if div.attrs.get('class')[0] == 'dashboard-list-item' : 
                        csvWriter.writerow(row_value)
                        row_value = []
                        
                if div.getText() and div.attrs.get('class'): 
                    if not div.attrs.get('class')[0] in ['row','result','dashboard-list-item']: 
                        print (div.attrs.get('class'))
                        row_value.append(div.getText())


if __name__ == '__main__':
    test = reallySg()
    print(test.url)
    test.test()
    
