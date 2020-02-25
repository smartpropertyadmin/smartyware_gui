import requests
import re
import json
from bs4 import BeautifulSoup
from flask_project.models import GL_listing
from flask_project import db

def decode_email(string):
    r = int(string[:2], 16)
    email = ''.join([chr(int(string[i:i+2], 16) ^ r)
                     for i in range(2, len(string), 2)])
    return email


def find_company_uen_no(company_name):
    company_name_replace =  re.sub('[^a-zA-Z0-9\n\.]', ' ', company_name)
    Search_records = []

    while not Search_records and re.search('\S+\s',company_name_replace):
        url = f'https://data.gov.sg/api/action/datastore_search?resource_id=' \
              f'bdb377b8-096f-4f86-9c4f-85bad80ef93c&q={company_name_replace.replace(" ","+")}'

        Search_company = requests.get(url).json()
        Search_records = Search_company['result']['records']

        company_name_replace= str(company_name_replace).rsplit(' ',1)[0]

    if not Search_records :
        print (company_name + ' <OTHERS>')
        return company_name + ' <OTHERS>'

    else:
        print (Search_records[0]['entity_name'])
        return Search_records[0]['entity_name']


def extract_all_payment_vendor():
    results = db.session.query(GL_listing.account_code, GL_listing.Mcst_no, GL_listing.debtor_creditor).\
        filter(GL_listing.account_code > 7000, GL_listing.debtor_creditor != "").\
        group_by(GL_listing.Mcst_no, GL_listing.debtor_creditor).all()

    for result in results:
        pass

def redefine_all_debtor_creditors():
    results = db.session.query(GL_listing.id,GL_listing.account_code, GL_listing.Mcst_no, GL_listing.debtor_creditor). \
        filter(GL_listing.account_code > 7000, GL_listing.debtor_creditor != "").\
        order_by(GL_listing.debtor_creditor).all()

    previous_debtor_creditor = ""
    for result in results:
        Gl_entry = GL_listing.query.get_or_404(result.id)

        if previous_debtor_creditor == Gl_entry.debtor_creditor:
            Gl_entry.debtor_creditor = previous_found_debtor_creditor

        else:
            previous_debtor_creditor = Gl_entry.debtor_creditor
            Gl_entry.debtor_creditor = find_company_uen_no(Gl_entry.debtor_creditor)
            previous_found_debtor_creditor = Gl_entry.debtor_creditor



        db.session.commit()
class get_vendor_info:
    def __init__(self,vendor_name,*soup):
        self.vendor_name = vendor_name

        search_name = re.sub('[^a-zA-Z0-9\n\s\-\.\@\&]', '', self.vendor_name)
        search_name = re.sub('[\.\@\&]',' ',search_name).rstrip()
        print (search_name)
        search_name = re.sub(' +',' ',search_name).replace(' ', '-').lower()
        search_url = f'https://sgpgrid.com/company-details/' + search_name
        print(search_url)

        Company_page = requests.get(search_url)
        self.soup = BeautifulSoup(Company_page.text, 'html.parser')


    def get_vendor_email_address(self):

        email = self.soup.find('img', attrs={'alt' : 'email' }).parent.find_next_sibling("p").findNext('span')['data-cfemail']
        print(decode_email(email))
        return decode_email(email)

    def get_vendor_address(self):

        address = self.soup.find('img', attrs={'alt' : 'address' }).parent.find_next_sibling("p").get_text()
        return address

    def get_vendor_phone(self):

        phone  = self.soup.find('img', attrs={'alt' : 'phone' }).parent.find_next_sibling("p").get_text()
        return phone




# print(get_vendor_info('FORGE M&E (S) PTE. LTD.').get_vendor_email_address())