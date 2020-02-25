import os
from flask import url_for, current_app
import re
from decimal import Decimal
from datetime import datetime
from flask_project import db
from flask_project.models import MCST_pending_list, GL_listing
from datetime import datetime
from flask_project.mcst import EXTRACT_MCST10,change_of_mailing

def save_file(file_upload,MCST_no, file_type):
    _, f_ext = os.path.splitext(file_upload.filename)

    file_path = os.path.join(r'Z:\CLARENCE\RESEARCH AND DEVELOPMENT\SOFTWARE\PYTHON\Flask_project\mcst\datafile', MCST_no)
    if not os.path.exists(file_path):
        os.makedirs(file_path)
    file_path = os.path.join(file_path, file_type + f_ext)
    if os.path.exists(file_path):
        os.remove(file_path)
    print(file_path)
    file_upload.save(file_path)

    return os.path.join('datafile',MCST_no, file_type + f_ext)

def create_accounts_file_checklist(MCST_no, Fy_start , Fy_period):
    checklist_items = ['GL listing', 'Balance Sheet', 'I&E monthly', 'I&E budget', 'Schedule', 'Ageing', 'advances', 'AGM minutes', 'Insurance Policy']
    for checklist_item in checklist_items:
        MCST_pending_item = MCST_pending_list(MCST_no= MCST_no, item = checklist_item, Period_start= Fy_start ,
                                              Period_end= Fy_period, Date_requested = datetime.now())
        db.session.add(MCST_pending_item)
        db.session.commit()

def convert_gl_text_to_database(MCSt_no, gl_file):
    with open(gl_file,'w', encoding="utf-8", newline='') as gl_file_text:
        pass

def Generate_report(Mcst_no):
    pass

def Mcst_func_generate(Mcst_no, Mcst_func):
    if Mcst_func == 'MCST retrival':
        EXTRACT_MCST10.MCExtract().Extract_single_Mcst(str(Mcst_no))
    elif Mcst_func == 'MCST Push restore':
       EXTRACT_MCST10.MCExtract().Push_MC_file(str(Mcst_no))
    elif Mcst_func == 'Change of mailing':
        change_of_mailing.Generate_update_mailing(Mcst_no)


def extract_debtor_creditor_from_desc (description):
    if re.search("^(.+?)\s[:-](.+?)\Z", description):
        debtor_creditor_spilt = re.search("^(.+?)\s[:-](.+?)\Z", description)
        debtor_creditor = debtor_creditor_spilt.group(1)
        description = debtor_creditor_spilt.group(2)

        # with space after  of : or -
    elif re.search("^(.+?)[:-]\s(.+?)\Z", description):
        debtor_creditor_spilt = re.search("^(.+?)[:-]\s(.+?)\Z", description)
        debtor_creditor = debtor_creditor_spilt.group(1)
        description = debtor_creditor_spilt.group(2)
    else:
        debtor_creditor = ""

    return description, debtor_creditor


def extract_credit_debit_string(amount_string):
    if "C" in amount_string:
        amount_string = -Decimal(amount_string.replace(',', '').replace('C', ''))
    elif amount_string.isspace():
        amount_string= 0
    else:
        amount_string = Decimal(amount_string.replace(',', ''))
    return amount_string

    # if 'C' in



def post_gl_entry(Mcst_no,account_code,account_description,item_date, debit_credit_amt,reference,
                  debtor_creditor, description,audit_description):
    gl_entry = GL_listing(Mcst_no=Mcst_no, account_code=account_code, account_description=account_description,
                          item_date=item_date, debit_credit_amt=str(debit_credit_amt), reference=reference,
                          debtor_creditor=debtor_creditor, description=description,
                          audit_description=audit_description)

    db.session.add(gl_entry)
    db.session.commit()


def import_mc_manager_gl(gl_textfile, Mcst_no):
    with open(gl_textfile, "r") as gl_file:
        debit_credit_amt = 0
        account_code = 1000
        debtor_creditor = ""
        FY_opening_date = ""
        for index, gl_line in enumerate(gl_file):
            if re.search('^\s+(.+?)\s+[-]\s+(.+?)\s+',gl_line) and not FY_opening_date :
                FY_opening_date = datetime.strptime(re.search('\s+(.+?)\s+[-]\s+(.+?)\s+',gl_line).group(1),
                                                    "%b %Y")

            if re.search('\d\d[/]\d\d[/]\d\d', gl_line[9:17]):

                if not account_code == 1000 and not Decimal(debit_credit_amt) == 0 :
                    # with space before of : or -
                    description, debtor_creditor = extract_debtor_creditor_from_desc(description)
                    post_gl_entry(Mcst_no, account_code, account_description, item_date, debit_credit_amt, reference,
                                  debtor_creditor, description, "")
                    debtor_creditor=""
                    reference = ""


                item_date = gl_line[9:17]

                if not gl_line[84:97].isspace() and gl_line[84:97]:

                    debit_credit_amt = -Decimal(gl_line[84:97].replace(',',''))
                elif not gl_line[67:83].isspace() and gl_line[67:83]:

                    debit_credit_amt = Decimal(gl_line[67:83].replace(',',''))
                else:
                    debit_credit_amt = 0

                reference = gl_line[18:30].strip()
                description = gl_line[31:66].strip()

            else:
                if re.search("^\s+(.+?)\s\Z", gl_line):
                    add_on_desc = re.search("^\s+(.+?)\s\Z", gl_line).group(1)
                    if re.search("^(\S+)\s", add_on_desc) :
                        if re.search("^(\S+)\s", add_on_desc).group(1) == "Period" or \
                                re.search("^(\S+)\s", add_on_desc).group(1) == "G/L" or \
                                re.search("^(\S+)\s", add_on_desc).group(1) == "Date:" or \
                                re.search("\d+\s+[-]\s+", add_on_desc):
                            continue
                        else:
                            description += add_on_desc
                # changing account code
                if "Account:" in gl_line and re.search('Type: .+?\s+(.+)\s+(\d)', gl_line):


                    if not Decimal(debit_credit_amt) == 0 :
                        description, debtor_creditor = extract_debtor_creditor_from_desc(description)
                        post_gl_entry(Mcst_no, account_code, account_description, item_date, debit_credit_amt,
                                      reference,
                                      debtor_creditor, description, "")
                        debit_credit_amt = 0
                    account_code = re.search('Account: (.+?)\s+', gl_line).group(1).strip()
                    account_description = re.search('Type: .+?\s+(.+)\s+(\d)', gl_line).group(1).strip()
                    print (gl_line[110:130])
                    if not gl_line[110:130].isspace():
                        opening_balance = extract_credit_debit_string(gl_line[110:130])


                        post_gl_entry(Mcst_no, account_code, account_description, FY_opening_date,
                                      str(opening_balance),"B/F BALANCE",""
                                          ,"B/F BALANCE AS ON " + FY_opening_date.strftime('%d\%m\%y')
                                          , "")

        post_gl_entry(Mcst_no, account_code, account_description, item_date, debit_credit_amt, reference,
                      debtor_creditor, description, "")

