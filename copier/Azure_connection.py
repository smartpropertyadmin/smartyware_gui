import pyodbc
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, ForeignKey,desc
from sqlalchemy.orm import relationship, sessionmaker
import urllib
from sqlalchemy.ext.declarative import declarative_base


class Azureconnect():
    connectString = "DRIVER={SQL Server};SERVER=smartpropertysingapore.database.windows.net;DATABASE=smartpropertyadmin;UID=smartpropertyadmin;PWD=tB96HB2jsywsRvw"
    params = urllib.parse.quote_plus (connectString)
    conn_str= f"mssql+pyodbc:///?odbc_connect={params}"
    engine_azure= create_engine(conn_str,echo=True)
    Base = declarative_base()
    Session = sessionmaker(bind=engine_azure)
    session = Session()


class printerLog(Azureconnect().Base):
    __tablename__ = "printer_log"
    id = Column(Integer, primary_key=True)
    MCST_id = Column(Integer, ForeignKey('smart_project_listing.PRINTER_CODE'), nullable=False)
    printerModel = Column(String(120))
    printerJobNo = Column(String(120))
    printDateTime = Column(String(120))
    printType = Column(String(120))
    printFileName = Column(String(120))
    printUserName = Column(String(120))
    printSheetPages = Column(Integer)
    printCopies = Column(Integer)
    printStatus = Column(String(120))


class smart_project_listing(Azureconnect().Base):
    # id = Column(Integer, primary_key=True)
    # ACCOUNTS_INCHARGE = Column(String(100),nullable=True)
    __tablename__ = "smart_project_listing"
    MCST_no = Column(String(100), nullable=False)
    PRINTER_CODE = Column(Integer, nullable=False,primary_key=True)
    PROPERTY_NAME =  Column(String(100), nullable=False)
    START_DATE =  Column(String(100), nullable=True)
    PREVIOUS_MA =  Column(String(100), nullable=True)
    TERMINATED_DATE= Column(String(100), nullable=True)
    NEW_MA = Column(String(100), nullable=True)
    YE = Column(String(100), nullable=True)
    GST =  Column(String(100), nullable=True)
    GIRO =  Column(String(100), nullable=True)
    UNITS =  Column(Integer, nullable=False)
    BILLINGS_CYCLE = Column(String(100), nullable=True)
    SHAREPOINT_ID = Column(String(100), nullable=True)
    # DIRECTOR_HEAD = Column(String(100), nullable=True)
    # PORFORLIO_MANAGER = Column(String(100), nullable=True)
    # PROPERTY_OFFICIER = Column(String(100), nullable=True)
    # SITE_OFFICER = Column(String(100), nullable=True)
    ROAD_NAME_ADDRESS = Column(String(100), nullable=True)
    OFFICIAL_ADDRESS = Column(String(100), nullable=True)
    MAILING_ADDRESS = Column(String(100), nullable=True)
    SCHEDULE_TYPE= Column(String(100), nullable=True)
    UEN_NO = Column(String(100), nullable=True)
    # SITE_EMAIL = Column(String(100), nullable=True)
    # User_list = relationship('user_project', backref= 'mcst_info', lazy ='dynamic')
    # gl_listing = relationship('gl_listing', backref= 'mcst_info', lazy ='dynamic')
    # BANK_ACCTS = relationship('bank_accounts_list', backref='Bank_accts', lazy="dynamic")
    # strata_roll_list = relationship('strata_roll', backref='mcst_info', lazy="dynamic")
    # Os_items = relationship('mcst_os_list', backref='mcst_info', lazy="dynamic")
    # Convid_entry =  relationship('MCST_declaration_list', backref='mcst_info', lazy="dynamic")
    printerLogList = relationship('printerLog', backref='projectDetails', lazy='dynamic')


session = Azureconnect().session
lastEntry = session.query(printerLog).filter(printerLog.printerModel == "Canon_IR5540").order_by(desc(printerLog.printDateTime)).first()
lastEntry.printDateTime = "2021-03-05"
session.commit()
print (lastEntry.MCST_id, lastEntry.printDateTime)
