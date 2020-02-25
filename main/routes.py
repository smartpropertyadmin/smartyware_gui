from flask import render_template, request, Blueprint, redirect, url_for, flash, make_response
from flask_login import current_user, login_required
from flask_project.models import Post, smart_project_listing, RolesUsers, FILE_LISTING, MCST_project, GL_listing, vendor_listing, Mcst_os_list, User
from datetime import datetime
from flask_principal import Permission, RoleNeed
from flask_project.function import CheckRoleAccess
from flask_project.main.forms import RetrivalForm
from flask_project.main.utils import export_data_base_to_excel
from flask_project.mcst.utils import Mcst_func_generate
from flask_project.mcst.change_of_mailing import Generate_update_mailing
from flask_project.mcst.payment.payment_utils import get_vendor_info
from flask_project import db,bcrypt
import pandas as pd
from time import sleep
import os,io
from flask_weasyprint import HTML, render_pdf
main = Blueprint('main', __name__)



admin_permission = Permission(RoleNeed('admin'))

@main.route("/home")
def home():
    if not current_user.is_authenticated:
        return redirect(url_for('main.about'))
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template('home.html', posts=posts)

@main.route("/")
@main.route("/about")
def about():
    return render_template('about.html', title='About')



@main.route("/main_dashboard")
@login_required
def main_dashboard():
    MCST_project_items= MCST_project.query.order_by(MCST_project.Status, MCST_project.Active_FY, MCST_project.MA_name, MCST_project.MCST_no ).all()

    active_username =  current_user.username

    Mcst_pending_items = Mcst_os_list.query.join(smart_project_listing).filter(smart_project_listing.ACCOUNTS_INCHARGE == active_username).\
        filter(Mcst_os_list.Date_received == None).order_by(Mcst_os_list.MCST_no).all()

    profile_pic=  url_for('static', filename= 'profile_pics/' + current_user.image_file)
    # Mcst_pending_items= MCST_pending_list.query.filter(MCST_pending_list.File_uploaded == '').order_by(MCST_pending_list.MCST_id).all()
    return render_template('main_dashboard.html', title='main_dashboard', MCST_project_items= MCST_project_items, Mcst_pending_items= Mcst_pending_items,
                           profile_pic= profile_pic)



@main.route("/Projectlisting")
# @admin_permission.require(http_exception=401)

def Projectlisting():

    if not current_user.is_authenticated :
        flash('Please login before accessing the page', 'danger')
        return redirect(url_for('main.about'))
    elif CheckRoleAccess('admin') == False:
        flash('You have no authorization to the website', 'danger')
        return redirect(url_for('main.about'))

    Project_items = smart_project_listing.query.order_by(smart_project_listing.PRINTER_CODE).filter\
    ((smart_project_listing.TERMINATED_DATE == "")| (smart_project_listing.TERMINATED_DATE >= datetime.now())).all()

    Project_headers =  smart_project_listing.__table__.columns.keys()

    return render_template('Projectlisting.html',Project_items = Project_items, Project_headers=  Project_headers )


@main.route('/testing')

def testing():
    return render_template('testing.html')

@main.route('/File_listing')

def File_listing():

    if not current_user.is_authenticated :
        flash('Please login before accessing the page', 'danger')
        return redirect(url_for('main.about'))
    elif CheckRoleAccess('admin') == False:
        flash('You have no authorization to the website', 'danger')
        return redirect(url_for('main.about'))

    File_listing_items = FILE_LISTING.query.order_by(FILE_LISTING.MCST, FILE_LISTING.BOX_ID).all()

    File_listing_headers= FILE_LISTING.__table__.columns.keys()

    return render_template('File_listing.html',File_listing_items = File_listing_items , File_listing_headers=  File_listing_headers)

@main.route("/MCST_retrival", methods=['GET', 'POST'])
def MCST_retrival():
    form = RetrivalForm()
    Project_items = smart_project_listing.query.order_by(smart_project_listing.PRINTER_CODE).filter \
        ((smart_project_listing.TERMINATED_DATE == "") | (
                    smart_project_listing.TERMINATED_DATE >= datetime.now())).all()

    if form.is_submitted():

        Mcst_func_generate(request.form['Mcst_no'],request.form['Mcst_func'])
        flash(f'{form.MCST_no.data} have been retrived','success')

    return render_template('MCST_retrival.html', title='Login', form=form, Project_items = Project_items)

@main.route("/vendors_listing")
def vendors_listing():

    if not current_user.is_authenticated :
        flash('Please login before accessing the page', 'danger')
        return redirect(url_for('main.about'))
    elif CheckRoleAccess('admin') == False:
        flash('You have no authorization to the website', 'danger')
        return redirect(url_for('main.about'))

    vendors_list = db.session.query(GL_listing.account_code, GL_listing.Mcst_no, GL_listing.debtor_creditor,
                                    GL_listing.account_description).\
        filter(GL_listing.account_code > 7000, GL_listing.debtor_creditor != "").\
        order_by(GL_listing.account_code, GL_listing.debtor_creditor,GL_listing.Mcst_no).\
        group_by(GL_listing.Mcst_no, GL_listing.debtor_creditor).all()
    # data_import = pd.read_sql(db.session.query.statement,db.session.bind)
    # data_import.to_csv(r'C:\project\flask_project\database\testing.csv')

    for vendor in vendor_listing.query.all():

        if not vendor.ADDRESS :

            sleep(5)
            vendor_entry = vendor_listing.query.get_or_404(vendor.id)
            try:
                vendor_contacts = get_vendor_info(vendor.VENDOR)
                vendor_entry.ADDRESS = vendor_contacts.get_vendor_address()
                vendor_entry.CONTACT_NO = vendor_contacts.get_vendor_phone()
                vendor_entry.EMAIL =  vendor_contacts.get_vendor_email_address()
            except:
                pass

    db.session.commit()


    return render_template('Vendors_listing.html',vendors_list = vendors_list)






@main.route('/outstanding_docs/<string:outstanding_file>')
def outstanding_docs(outstanding_file):
    output_path = r'Z:\CLARENCE\RESEARCH AND DEVELOPMENT\SOFTWARE\PYTHON\Flask_project\flask_project\posts\outstanding_docs'
    change_mailing_pdf_path = os.path.join(output_path, outstanding_file)
    with open(change_mailing_pdf_path,'rb') as f:


        response = make_response(f.read())
        response.headers['Content-Type'] = 'application/pdf'
        response.headers['Content-Disposition'] = \
            'inline; filename=%s.pdf' % 'yourfilename'
        return response



@main.route('/bank_change_of_mailing/<int:mcst_no>')
def bank_change_of_mailing(mcst_no):
    return Generate_update_mailing(str(mcst_no))


@main.route('/change_of_mailing')
def change_of_mailing():


    # options = {'page-size': 'A4', 'dpi': 400}
    # print(redirect(url_for('main.change_of_mailing_generate',mcst_no= 2329)).headers)

    active_projects = smart_project_listing.query.filter(smart_project_listing.TERMINATED_DATE == '').\
        filter(smart_project_listing.MAILING_ADDRESS == "HQ").all()


    for active_project in active_projects:
        if int(active_project.PRINTER_CODE) >3235:
           pass
            # pdf = Generate_update_mailing(str(active_project.PRINTER_CODE))



    return redirect(url_for('main.main_dashboard'))
            # change_mailing_pdf_path = os.path.join(output_path, )
            # with open(output_path,'wb') as f:
            #
            #     f.write(pdf)
            #     response = make_response(pdf)
            #     response.headers['Content-Type'] = 'application/pdf'
            #     response.headers['Content-Disposition'] = \
            #         'inline; filename=%s.pdf' % 'yourfilename'
            #     return response