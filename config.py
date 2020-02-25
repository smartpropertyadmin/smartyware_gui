import os


class Config:
    SECRET_KEY = '123456789'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db'
    SQLALCHEMY_BINDS = {
        'Main' : 'sqlite:///site.db',
        'FILE_LISTING' : 'sqlite:///Z:\ACCOUNTS\9999 - CONSOLIDATION\DATABASE\FILE_LISTING.db',
        'audit_income_expenditure' : r'sqlite:///C:\project\flask_project\database\audit_income_expenditure.db',
        'MCST_Project_list' :  r'sqlite:///Z:\ACCOUNTS\9999 - CONSOLIDATION\DATABASE\MCST_Project_list.db',
        'MCST_os_list' : r'sqlite:///Z:\ACCOUNTS\9999 - CONSOLIDATION\DATABASE\MCST_os_list.db',
        'vendor_listing' : r'sqlite:///C:\project\flask_project\database\vendor_listing.db',
        'audit_list': r'sqlite:///Z:\ACCOUNTS\9999 - CONSOLIDATION\DATABASE\audit_list1.db',
        'MCST_declaration_list': 'sqlite:///MCST_declaration_list.db'
    }



    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    # MAIL_USERNAME = os.environ.get('EMAIL_USER')
    # MAIL_PASSWORD = os.environ.get('EMAIL_PASS')
