from PyPDF2 import PdfFileReader, PdfFileWriter,PdfFileMerger
import io
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from flask_project.models import smart_project_listing, bank_accounts_list,Mcst_os_list,db
from flask import render_template
from flask_weasyprint import HTML, render_pdf
from datetime import datetime
from flask_project.static.utils.common_func import qr_code_generate_smart
import re,os


def Update_DBS(Bank_acct):
    packet = io.BytesIO()
    # create a new PDF with Reportlab
    can = canvas.Canvas(packet, pagesize=A4)
    can.setFont("Helvetica",10)
    #draw MCST_No
    can.drawString(110, 737,f'MCST PLAN NO. {Bank_acct.MCST}')
    # Mcst_info = smart_project_listing.query.get(MCST_no)

    # draw Uen
    can.drawString(460, 737,  f'{Bank_acct.Bank_accts.UEN_NO}')
    # draw Office no
    Office_no = f'+65                                  6223 0169'
    can.drawString(200, 650, f'{Office_no}')
    # draw Email
    # Accts_email  = 'clarence.yeo@smartproperty.sg'

    can.drawString(200, 565, f'{Bank_acct.Bank_accts.user.email}')

    # draw Blk Level
    Block_add  = '38C                            03                      01                                                            577180'
    can.drawString(100, 480, f'{Block_add}')
    # draw street name
    Street_add = 'JALAN PEMIMPIN '
    can.drawString(100, 460, f'{Street_add}')
    # draw sg name
    Sg_add = 'SINGAPORE '
    can.drawString(450, 440, f'{Sg_add}')

    Mcst_os_item = Mcst_os_list(MCST_no=Bank_acct.Bank_accts.PRINTER_CODE, item_group="Change of Mailing", item_content="DBS",
                                created_date=datetime.now(), attention_by=Bank_acct.Bank_accts.ACCOUNTS_INCHARGE)

    db.session.add(Mcst_os_item)
    db.session.commit()

    Mcst_os_item.File_created = f'{Mcst_os_item.id:04d}_bank_change_of_mailing.pdf'
    db.session.commit()

    qrcode_reference_string = f'{Bank_acct.MCST}/{Bank_acct.BANK}/{Mcst_os_item.id:04d}'
    qrcode_reference = qr_code_generate_smart(qrcode_reference_string)
    QRImage = canvas.ImageReader(qrcode_reference)

    can.drawImage(QRImage,450,0,width=50,height=50)
    can.save()
    packet.seek(0)
    new_pdf = PdfFileReader(packet)


    DBS_template = open(r"Z:\ACCOUNTS\SMARTYWARE\TEMPLATE\BANKS_FORM\CHANGE_OF_MAILING\DBS_CHANGE_OF_MAILING.pdf",'rb')
    Pdf_read = PdfFileReader(DBS_template)
    output = PdfFileWriter()
    Pdf_first = Pdf_read.getPage(0)
    Pdf_first.mergePage(new_pdf.getPage(0))
    output.addPage(Pdf_first)
    # output_file = open(r'Z:\ACCOUNTS\SMARTYWARE\TEMPLATE\BANKS_FORM\CHANGE_OF_MAILING\testing.pdf','wb')
    # output.write(output_file)
    # output_file.close

    # subprocess.Popen(r'Z:\ACCOUNTS\SMARTYWARE\TEMPLATE\BANKS_FORM\CHANGE_OF_MAILING\testing.pdf', shell=True)
    pdf_bytes = io.BytesIO()
    output.write(pdf_bytes)
    pdf_bytes.seek(0)
    return pdf_bytes.read() , Mcst_os_item.id




def Update_OCBC(Bank_acct):


    packet = io.BytesIO()
    Mcst_os_item = Mcst_os_list(MCST_no=Bank_acct.Bank_accts.PRINTER_CODE, item_group="Change of Mailing", item_content="OCBC",
                                created_date=datetime.now(), attention_by=Bank_acct.Bank_accts.ACCOUNTS_INCHARGE)

    db.session.add(Mcst_os_item)
    db.session.commit()
    Mcst_os_item.File_created = f'{Mcst_os_item.id:04d}_bank_change_of_mailing.pdf'
    db.session.commit()

    # create a new PDF with Reportlab
    can_page1 = canvas.Canvas(packet, pagesize=A4)
    qrcode_reference_string = f'{Bank_acct.MCST}/{Bank_acct.BANK}/{Mcst_os_item.id:04d}'
    qrcode_reference = qr_code_generate_smart(qrcode_reference_string)
    QRImage = canvas.ImageReader(qrcode_reference)
    can_page1.drawImage(QRImage,450,0,width=50,height=50)
    can_page1.save()
    packet.seek(0)
    new_pdf_1 = PdfFileReader(packet)

    packet = io.BytesIO()
    can_page2 = canvas.Canvas(packet, pagesize=A4)
    can_page2.setFont("Helvetica",10)
    can_page2.drawString(128, 740,f'{Bank_acct.MCST}')
    can_page2.drawString(382, 740,f'{Bank_acct.Bank_accts.UEN_NO}')
    can_page2.save()
    packet.seek(0)
    new_pdf_2 = PdfFileReader(packet)

    packet = io.BytesIO()
    can_page3 = canvas.Canvas(packet, pagesize=A4)
    can_page3.setFont("Helvetica", 10)
    can_page3.drawString(180, 734, f'{Bank_acct.MCST}')
    can_page3.drawString(187, 723, f'{Bank_acct.Bank_accts.UEN_NO}')
    can_page3.save()
    packet.seek(0)
    new_pdf_3 = PdfFileReader(packet)

    packet = io.BytesIO()
    can_page4 = canvas.Canvas(packet, pagesize=A4)
    can_page4.setFont("Helvetica", 10)
    can_page4.drawString(175, 734, f'{Bank_acct.MCST}')
    can_page4.drawString(187, 723, f'{Bank_acct.Bank_accts.UEN_NO}')
    can_page4.save()
    packet.seek(0)
    new_pdf_4 = PdfFileReader(packet)

    packet = io.BytesIO()
    can_page5 = canvas.Canvas(packet, pagesize=A4)
    can_page5.setFont("Helvetica", 10)
    can_page5.drawString(180, 752, f'{Bank_acct.MCST}')
    can_page5.drawString(187, 740, f'{Bank_acct.Bank_accts.UEN_NO}')


    can_page5.save()
    packet.seek(0)
    new_pdf_5 = PdfFileReader(packet)

    with  open(r'Z:\ACCOUNTS\SMARTYWARE\TEMPLATE\BANKS_FORM\CHANGE_OF_MAILING\OCBC_CHANGE_OF_MAILING1.pdf','rb') as OCBC_template:
        Pdf_read = PdfFileReader(OCBC_template)
        output = PdfFileWriter()
        Pdf_first = Pdf_read.getPage(0)
        Pdf_first.mergePage(new_pdf_1.getPage(0))
        output.addPage(Pdf_first)
        Pdf_second = Pdf_read.getPage(1)
        Pdf_second.mergePage(new_pdf_2.getPage(0))
        output.addPage(Pdf_second)
        Pdf_third = Pdf_read.getPage(2)
        Pdf_third.mergePage(new_pdf_3.getPage(0))
        output.addPage(Pdf_third)
        Pdf_forth = Pdf_read.getPage(3)
        Pdf_forth.mergePage(new_pdf_4.getPage(0))
        output.addPage(Pdf_forth)
        Pdf_fifth = Pdf_read.getPage(4)
        Pdf_fifth.mergePage(new_pdf_5.getPage(0))
        output.addPage(Pdf_fifth)
        with open(r'Z:\ACCOUNTS\SMARTYWARE\TEMPLATE\BANKS_FORM\CHANGE_OF_MAILING\testing.pdf','wb') as output_file :
            output.write(output_file)


    pdf_bytes = io.BytesIO()
    output.write(pdf_bytes)
    pdf_bytes.seek(0)
    return pdf_bytes.read(), Mcst_os_item.id
def Update_others(Bank_acct):

    mcst_info = smart_project_listing.query.get(f'{Bank_acct.MCST}')
    property_name = mcst_info.PROPERTY_NAME

    header_source = f'{Bank_acct.MCST:04d}_{Bank_acct.Bank_accts.PROPERTY_NAME}.png'

    Mcst_os_item = Mcst_os_list(MCST_no=Bank_acct.Bank_accts.PRINTER_CODE, item_group="Change of Mailing", item_content=Bank_acct.BANK,
                                created_date=datetime.now(), attention_by= Bank_acct.Bank_accts.ACCOUNTS_INCHARGE)

    db.session.add(Mcst_os_item)
    db.session.commit()
    Mcst_os_item.File_created = f'{Mcst_os_item.id:04d}_bank_change_of_mailing.pdf'
    db.session.commit()
    bank_account_digit = re.sub('[^a-zA-Z0-9]', '', Bank_acct.ACCOUNTNO)

    qrcode_reference_string =  f'{Bank_acct.MCST}/{Bank_acct.BANK}/{Mcst_os_item.id:04d}'
    qrcode_reference = qr_code_generate_smart(qrcode_reference_string)

    # update_barcode = barcode.get('code39',
    #                              code= f'{mcst_info.MCST_no}-{mcst_info.PROPERTY_NAME}-{bank_account.ACCOUNTNO}-{Mcst_os_item.id}')
    filename = f'temp_barcode_{datetime.timestamp(datetime.now())}{Mcst_os_item.id}.png'
    filefolder =r'Z:\CLARENCE\RESEARCH AND DEVELOPMENT\SOFTWARE\PYTHON\Flask_project\flask_project\temp'

    filepath = os.path.join(filefolder, filename)

    qrcode_reference.save(filepath)


    # print(bank_account.bank_accounts_details)
    letter_date =datetime.now().strftime('%d %B %Y')

    change_of_mailing_html =  render_template ('change_of_mailing.html', mcst_info=mcst_info , bank_account=Bank_acct,
                     header_source = header_source, Mcst_os_item= Mcst_os_item, letter_date= letter_date, filename=filename)

    pdf = HTML(string=change_of_mailing_html).write_pdf()
    return pdf , Mcst_os_item.id




def Generate_update_mailing(Mcst_no, pdffile = None):


    Project_info =  bank_accounts_list.query.join(smart_project_listing).filter(smart_project_listing.PRINTER_CODE == int(Mcst_no)).\
        group_by(bank_accounts_list.BANK).all()
    if not pdffile:
        pdffile = r"Z:\ACCOUNTS\9999 - CONSOLIDATION\BANK ACCOUNTS\testing.pdf"

    pdfmerger = PdfFileMerger()

    output_path = r'Z:\CLARENCE\RESEARCH AND DEVELOPMENT\SOFTWARE\PYTHON\Flask_project\flask_project\posts\outstanding_docs'

    for index, Bank_acct in enumerate(Project_info):

        if Bank_acct.BANK == "DBS":
            mailing_pdf = Update_DBS(Bank_acct)
        elif Bank_acct.BANK == "OCBC":

            mailing_pdf =  Update_OCBC(Bank_acct)
        else:
            mailing_pdf =  Update_others(Bank_acct)

        pdf = mailing_pdf[0]
        output_file = os.path.join(output_path, f'{mailing_pdf[1]:04d}_bank_change_of_mailing.pdf')

        with open(output_file,'wb') as f:
            f.write(pdf)


    #     pdfmerger.append(pdf)
    # pdf_bytes = io.BytesIO()
    # pdfmerger.write(pdf_bytes)
    # pdf_bytes.seek(0)

    return mailing_pdf
        # pdfmerger.append(mailing_pdf)
    # with open(pdffile,'rb') as pdf :
    #     pdfmerger.write(pdf)
    # return pdfmerger


