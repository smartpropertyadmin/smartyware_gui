from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app
from flask_project import db, login_manager
from flask_login import UserMixin, current_user
from flask_security import RoleMixin, SQLAlchemyUserDatastore



@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class MCST_project(db.Model):
    __bind_key__ = 'MCST_Project_list'
    __tablename__ = 'MCST_project'
    id = db.Column(db.Integer, primary_key= True)
    MCST_no = db.Column(db.Integer, unique = True, nullable = False)
    Project_name = db.Column(db.String(120), nullable = False)
    MA_name = db.Column(db.String(120), nullable = False)
    Active_FY = db.Column(db.Text, nullable = False)
    Status = db.Column(db.String(120), nullable = False)
    Last_update_date = db.Column(db.Text, nullable = False)
    MCST_pending_list = db.relationship('MCST_pending_list', backref='pending_list', lazy=True)
    account_code_list =  db.relationship('audit_account_list', backref='pending_list', lazy=True)

class MCST_pending_list(db.Model):
    __bind_key__ = 'MCST_Project_list'

    id = db.Column(db.Integer, primary_key=True)
    MCST_id = db.Column(db.Integer, db.ForeignKey('MCST_project.id'))
    item = db.Column(db.String(120), nullable = False)
    Period_start =  db.Column(db.String(120))
    Period_end = db.Column(db.String(120))
    Date_requested = db.Column(db.String(120), nullable=False)
    Date_received = db.Column(db.String(120))
    File_uploaded = db.Column(db.String(120))

class MCST_declaration_list(db.Model):
    __bind_key__ = 'MCST_declaration_list'

    id = db.Column(db.Integer, primary_key=True)
    MCST_id = db.Column(db.Integer)
    name =  db.Column(db.String(120))
    contact_no = db.Column(db.String(120))
    date_registered = db.Column(db.String(120), nullable=False)
    unit_visted = db.Column(db.String(120))
    nric = db.Column(db.String(120))
    mainland_visit = db.Column(db.Boolean)
    family_visit = db.Column(db.Boolean)
    fever= db.Column(db.Boolean)
    respiratory=  db.Column(db.Boolean)
    contact_convid =   db.Column(db.Boolean)
    contact_place =   db.Column(db.String(120))
    declaration=   db.Column(db.Boolean)
    temperature = db.Column(db.String(120))
    time_taken = db.Column(db.String(120))


class Mcst_os_list(db.Model):
    # __bind_key__ = 'MCST_os_list'

    id = db.Column(db.Integer, primary_key=True)
    MCST_no = db.Column(db.Integer, db.ForeignKey('smart_project_listing.PRINTER_CODE'))
    item_group = db.Column(db.String(120), nullable = False)
    item_content = db.Column(db.String(120), nullable = False)
    created_date =  db.Column(db.String(120))
    attention_by = db.Column(db.String(120))
    last_reminder_date = db.Column(db.String(120), nullable=False)
    Date_received = db.Column(db.String(120))
    File_created = db.Column(db.String(120))
    File_uploaded = db.Column(db.String(120))

    def __repr__(self):
        return f"User('{self.MCST_no}', '{self.item_group}', '{self.item_content}')"





class RolesUsers (db.Model):
    __tablename__ = 'roles_users'
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column('user_id', db.Integer(), db.ForeignKey('user.id'))
    role_id = db.Column('role_id', db.Integer(), db.ForeignKey('role.id'))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)
    smart_project_listing = db.relationship('smart_project_listing', backref = 'user',lazy =True)
    role = db.relationship('Role', secondary= RolesUsers.__tablename__,
                            backref=db.backref('users', lazy='dynamic'))
    def get_reset_token(self, expires_sec=1800):
        s = Serializer(current_app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)


    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"


class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40))
    description = db.Column(db.String(255))

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"


class FILE_LISTING(db.Model):
    __bind_key__ = 'FILE_LISTING'
    id = db.Column(db.Integer, primary_key=True)
    ACCOUNTS_IN_CHARGE = db.Column(db.String(100),db.ForeignKey('user.username'), nullable=True)
    MCST = db.Column(db.String(100), nullable=False)
    NAME =  db.Column(db.String(100), nullable=False)
    START_DATE =  db.Column(db.String(100), nullable=True)
    FILE_TYPE=  db.Column(db.String(100), nullable=True)
    END_DATE= db.Column(db.String(100), nullable=True)
    COLOR = db.Column(db.String(100), nullable=True)
    BOX_ID = db.Column(db.String(100), nullable=True)

    def __repr__(self):
        return f"File_listing('{self.MCST}', '{self.FILE_TYPE}','{self.BOX_ID}')"



class smart_project_listing(db.Model):
    # id = db.Column(db.Integer, primary_key=True)
    ACCOUNTS_INCHARGE = db.Column(db.String(100),db.ForeignKey('user.username'), nullable=True)
    MCST_no = db.Column(db.Integer, primary_key=True)
    PRINTER_CODE = db.Column(db.Integer, nullable=False)
    PROPERTY_NAME =  db.Column(db.String(100), nullable=False)
    START_DATE =  db.Column(db.String(100), nullable=True, default=datetime.utcnow)
    PREVIOUS_MA =  db.Column(db.String(100), nullable=True)
    TERMINATED_DATE= db.Column(db.String(100), nullable=True, default=datetime.utcnow)
    NEW_MA = db.Column(db.String(100), nullable=True)
    YE = db.Column(db.String(100), nullable=True)
    GST =  db.Column(db.String(100), nullable=True)
    GIRO =  db.Column(db.String(100), nullable=True)
    UNITS =  db.Column(db.Integer, nullable=False)
    BILLINGS_CYCLE = db.Column(db.String(100), nullable=True)
    DIRECTOR_HEAD = db.Column(db.String(100), nullable=True)
    PORFORLIO_MANAGER = db.Column(db.String(100), nullable=True)
    PROPERTY_OFFICIER = db.Column(db.String(100), nullable=True)
    SITE_OFFICER = db.Column(db.String(100), nullable=True)
    ROAD_NAME_ADDRESS = db.Column(db.String(100), nullable=True)
    OFFICIAL_ADDRESS = db.Column(db.String(100), nullable=True)
    MAILING_ADDRESS = db.Column(db.String(100), nullable=True)
    SCHEDULE_TYPE= db.Column(db.String(100), nullable=True)
    UEN_NO = db.Column(db.String(100), nullable=True)
    BANK_ACCTS = db.relationship('bank_accounts_list', backref='Bank_accts', lazy="dynamic")
    Os_items = db.relationship('Mcst_os_list', backref='mcst_info', lazy="dynamic")
    # Convid_entry =  db.relationship('MCST_declaration_list', backref='mcst_info', lazy="dynamic")


    def __repr__(self):
        return f"Project_listing('{self.MCST_no}', '{self.PROPERTY_NAME}')"

class bank_accounts_list(db.Model):
    __tablename__ = 'bank_accounts_list'
    id = db.Column(db.Integer, primary_key=True)
    MCST = db.Column(db.Integer, db.ForeignKey('smart_project_listing.PRINTER_CODE'), nullable=False)
    TYPE =  db.Column(db.String(100), nullable=False)
    ACCOUNTNO =  db.Column(db.String(100), nullable=True, default=datetime.utcnow)
    AMOUNT =  db.Column(db.Text(100), nullable=True)
    DEPOSIT_NO= db.Column(db.String(100), nullable=True)
    START_DATE = db.Column(db.String(100), nullable=True)
    END_DATE = db.Column(db.String(100), nullable=True)
    RATE =  db.Column(db.Text(100), nullable=True)
    REFERENCE =  db.Column(db.String(100), nullable=True)
    BANK = db.Column(db.String(100), db.ForeignKey('bank_info.short_name'), nullable=False)

    def __repr__(self):
        return f"Bank_account('{self.MCST}', '{self.BANK}', '{self.TYPE}', '{self.ACCOUNTNO}')"


class bank_info(db.Model):
    __tablename__ = 'bank_info'
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(100), nullable=False)
    short_name = db.Column(db.String(100), primary_key=True, nullable=False)
    mailing_address =  db.Column(db.String(100), nullable=False)
    rm_name = db.Column(db.String(100))
    contact_no =db.Column(db.String(100))
    contact_email = db.Column(db.String(100))
    bank_accounts = db.relationship('bank_accounts_list', backref='bank_accounts_details', lazy="dynamic")

    def __repr__(self):
        return f"Bank_info('{self.full_name}', '{self.short_name}')"





class audit_income_expenditure(db.Model):
    __bind_key__ = 'audit_income_expenditure'
    id = db.Column(db.Integer, primary_key=True)
    income_expenditure = db.Column(db.String(20),  nullable=False)
    audit_description =  db.Column(db.String(20),  nullable=False)
    gl_listing =   db.relationship('GL_listing', backref='gl_listing', lazy=True)
    year_start = db.Column(db.String(20), nullable=False)
    year_end = db.Column(db.String(20), nullable=False)
    amount = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"Audit_IE('{self.audit_description, self.amount})'"


class GL_listing(db.Model):
    __bind_key__ = 'audit_income_expenditure'
    id = db.Column(db.Integer, primary_key=True)
    Mcst_no = db.Column(db.Integer, nullable = False)
    account_code =  db.Column(db.Integer, nullable=False)
    account_description = db.Column(db.String(50), nullable=False)
    item_date = db.Column(db.String(50), nullable=False)
    debit_credit_amt = db.Column(db.Text, nullable=False)
    reference = db.Column(db.String(50))
    debtor_creditor = db.Column(db.String(50))
    description = db.Column(db.String(50), nullable=False)
    audit_description = db.Column(db.String(50), db.ForeignKey('audit_income_expenditure.audit_description'))

    def __repr__(self):
        return f"GL listing('{self.Mcst_no, self.account_code, self.account_description, self.debit_credit_amt})'"

class account_code_current(db.Model):
    __bind_key__ = 'audit_income_expenditure'
    id = db.Column(db.Integer, primary_key=True)
    account_code =  db.Column(db.Integer, nullable=False)
    account_description = db.Column(db.String(50), nullable=False)
    debit_credit_amt = db.Column(db.Text)
    audit_description = db.Column(db.String(50), db.ForeignKey('audit_income_expenditure.audit_description'))

    def __repr__(self):
        return f"GL listing('{self.account_code, self.account_description, self.debit_credit_amt})'"


class audit_account_list(db.Model):
    __bind_key__ = 'MCST_Project_list'
    __tablename__ = 'audit_account_list'
    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('MCST_project.id'))
    item =  db.Column(db.Integer, nullable=False)
    current_fy_value = db.Column(db.Text)
    last_fy_value = db.Column(db.Text)
    classify_type= db.Column(db.String(50))

    def __repr__(self):
        return f"audit_account('{self.item, self.classify_type})'"



class account_code_last(db.Model):
    __bind_key__ = 'audit_income_expenditure'
    id = db.Column(db.Integer, primary_key=True)
    account_code =db.Column(db.Integer, nullable=False)
    account_description = db.Column(db.String(50), nullable=False)
    debit_credit_amt = db.Column(db.Text)
    audit_description = db.Column(db.String(50), db.ForeignKey('audit_income_expenditure.audit_description'))

    def __repr__(self):
        return f"GL listing('{self.account_code, self.account_description, self.debit_credit_amt})'"

class vendor_listing(db.Model):
    __bind_key__ = 'vendor_listing'
    id = db.Column(db.Integer, primary_key=True)
    ACCOUNT_CODE =db.Column(db.Integer, nullable=False)
    VENDOR = db.Column(db.String(50), nullable=False)
    ADDRESS = db.Column(db.String(50))
    CONTACT_NO = db.Column(db.String(50))
    EMAIL = db.Column(db.String(50))

    def __repr__(self):
        return f"Vendor_listing('{self.VENDOR}')"
