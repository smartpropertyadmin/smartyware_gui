from flask import render_template, request, Blueprint, redirect, url_for, flash, send_from_directory
from flask_project import db
from flask_login import login_required, current_user
from flask_project.models import MCST_pending_list,GL_listing, MCST_project, audit_account_list, smart_project_listing,MCST_declaration_list, Role
from flask_project.mcst.forms import Upload_pending_docs, convid_declaration, TemperatureForm
from flask_principal import Permission, RoleNeed
from flask_project.function import CheckRoleAccess
from flask_project.mcst.utils import save_file, create_accounts_file_checklist, import_mc_manager_gl
from flask_project.mcst.payment.payment_utils import extract_all_payment_vendor,redefine_all_debtor_creditors
from datetime import datetime
from decimal import Decimal
import os,re
mcst = Blueprint('mcst',__name__)

@mcst.route("/<int:MCST_no>/pending_documents", methods=['GET', 'POST'])
def pending_documents(MCST_no):
    pending_form = Upload_pending_docs()



    if pending_form.is_submitted():

        uploaded_file = save_file(pending_form.File_uploaded.data,str(MCST_no),pending_form.item.data)

        MCST_pending_item = MCST_pending_list.query.get_or_404(pending_form.item_id.data)
        MCST_pending_item.File_uploaded = uploaded_file
        MCST_pending_item.Date_received = datetime.now()


        if pending_form.item.data == 'QUOTATION':
            MCST_pending_list.pending_list.Status = "PENDING_DOCUMENTS"
            create_accounts_file_checklist(MCST_no, MCST_pending_item.Period_start, MCST_pending_item.Period_end)

        db.session.commit()

    Pending_items = db.session.query(MCST_pending_list).join(MCST_pending_list, MCST_project.MCST_pending_list)\
        .order_by(MCST_pending_list.Date_received, MCST_pending_list.id).filter(MCST_project.MCST_no == MCST_no).all()
    # for pending_item in Pending_items:
    #     print (pending_item)


    # print (url_for('mcst', filename=Pending_items[0].__dict__.get('File_uploaded')))
    return render_template('pending_documents.html', Pending_items = Pending_items, MCST_no= MCST_no, pending_form= pending_form)


@mcst.route("/letter_head/<path:filename>")
def letter_head(filename):
    letter_head_folder = r'Z:\ACCOUNTS\TEMPLATE\ESTATE LETTERHEAD\IMAGE HEADER'
    return send_from_directory(letter_head_folder,filename, as_attachment= True)

@mcst.route("/<int:MCST_no>/audit_report", methods=['GET'])
def audit_report(MCST_no):
    return render_template('audit_report.html')

@mcst.route("/<int:MCST_no>/<int:document_id>", methods=['GET'])
def mcst_docs(MCST_no,document_id):
    root_path = r'Z:\Mcst10\20200108_GL_EXTRACT'
    # import_mc_manager_gl (r"Z:\Mcst10\20200108_GL_EXTRACT\720_GL.txt",720)
    # for root, dirs, files in os.walk(root_path):
    #     for name in files:
    #         import_mc_manager_gl(os.path.join(root, name),
    #                       (re.search('(\d+)_' ,name).group(1)))
    # extract_all_payment_vendor()
    redefine_all_debtor_creditors()
    return ('home.html')


@mcst.route("/working_sheet/<int:MCST_no>", methods=['GET','POST'])
def working_sheet(MCST_no):

    audit_account_items = db.session.query(audit_account_list).join(audit_account_list, MCST_project.account_code_list)\
        .filter(MCST_project.MCST_no == MCST_no).group_by(audit_account_list.classify_type).all()
    for audit_account_item in audit_account_items:
        print (audit_account_item.current_fy_value )

    audit_account_breakdown_items = db.session.query(audit_account_list).join(audit_account_list, MCST_project.account_code_list)\
        .filter(MCST_project.MCST_no == MCST_no).all()
    return render_template('working_sheet.html', audit_account_items =audit_account_items , audit_account_breakdown_items = audit_account_breakdown_items , MCST_no= MCST_no )



@mcst.route("/coviddeclaration/<int:mcst_no>", methods=['GET', 'POST'])
def coviddeclaration(mcst_no):
    form =  convid_declaration()
    mcst_info = smart_project_listing.query.filter(smart_project_listing.PRINTER_CODE == mcst_no).first()
    smartpropertylogo = url_for('static', filename= 'img/SMART LOGO.png')
    today_date = datetime.strftime(datetime.today(),"%Y-%m-%d")

    if form.validate_on_submit():
        print(form.mainland_visit.data)
        print(form.respiratory.data)


        MCST_declaration = MCST_declaration_list(MCST_id=mcst_no, name = form.full_name.data, contact_no = form.contact_no.data, date_registered = form.date_registered.data,
                                                 unit_visted = form.unit_visted.data,nric = form.nric.data, mainland_visit= form.mainland_visit.data,
                                                 family_visit = form.family_visit.data, fever= form.fever.data, respiratory= form.respiratory.data,
                                                 contact_convid= form.contact_convid.data,
                                                  contact_place= ','.join(request.form.getlist('place_visited')),declaration= form.declaration.data)
        db.session.add(MCST_declaration)
        db.session.commit()


        flash('Thank You for the declaration, Please approach to management for temperature taking', 'success')
        return redirect(url_for('mcst.coviddeclaration', mcst_no=mcst_no))


    title = f'{mcst_info.MCST_no} - {mcst_info.PROPERTY_NAME}  Covid-19 Declaration'
    return render_template('covid_health_declaration.html' , mcst_info= mcst_info , form= form,
                           smartpropertylogo= smartpropertylogo, today_date= today_date, title= title)



@mcst.route("/covid_listing/<int:MCST_no>", methods=['GET', 'POST'])
@login_required
def covid_listing(MCST_no):
    MCST_role = Role.query.filter(Role.name ==  MCST_no).first()
    if not MCST_role in current_user.role:
        return redirect(url_for('mcst.covid_listing' , MCST_no=current_user.role[0].name))



    Temperature_form = TemperatureForm()
    mcst_info = smart_project_listing.query.filter(smart_project_listing.PRINTER_CODE== MCST_no).first()
    title = f'MCST {mcst_info.MCST_no} - {mcst_info.PROPERTY_NAME} covid listing'

    if Temperature_form.submit():
        if Temperature_form.submit.data == True :
            selected_declaration =  MCST_declaration_list.query.get_or_404(Temperature_form.id.data)
            selected_declaration.temperature = Temperature_form.Temperature.data
            selected_declaration.time_taken = datetime.today().strftime("%Y/%m/%d %H:%M:%S")
            db.session.commit()
        elif Temperature_form.delete.data == True :
            selected_declaration = MCST_declaration_list.query.get_or_404(Temperature_form.id.data)
            db.session.delete(selected_declaration)
            db.session.commit()
    #
    #     if pending_form.item.data == 'QUOTATION':
    #         MCST_pending_list.pending_list.Status = "PENDING_DOCUMENTS"
    #         create_accounts_file_checklist(MCST_no, MCST_pending_item.Period_start, MCST_pending_item.Period_end)
    #
    #     db.session.commit()

    covid_listing = MCST_declaration_list.query.filter((MCST_declaration_list.temperature == None)| (MCST_declaration_list.temperature == "")).filter(MCST_declaration_list.MCST_id== MCST_no ).\
        order_by(MCST_declaration_list.id).all()
    # for pending_item in Pending_items:
    #     print (pending_item)


    # print (url_for('mcst', filename=Pending_items[0].__dict__.get('File_uploaded')))
    return render_template('covid_listing.html', covid_listing =covid_listing, mcst_info= mcst_info, title= title, Temperature_form= Temperature_form)

