import sqlite3
import pandas as pd
conn = sqlite3.connect(r"Z:\CLARENCE\RESEARCH AND DEVELOPMENT\SOFTWARE\PYTHON\Flask_project\flask_project\site.db")
c = conn.cursor()
# with open('Z:\ACCOUNTS\9999 - CONSOLIDATION\OTHERS\PROJECT_LISTING.xlsx','r', encoding="utf-8") as f :
#     list_csv = csv.DictReader(f)
#     print (list_csv)
#     for csv_row in list_csv:
#         print (csv_row.items())
# Z:\ACCOUNTS\SMARTYWARE\TEMPLATE\EXCEL\ROLES.xlsx'
def import_spreadsheet_data(filename, table_name):

    list_csv = pd.read_excel(filename)
    excute_text = 'INSERT INTO {}('.format(table_name)
    excute_header =()
    excute_insert =()
    for column in list_csv.columns:
        excute_header += (str(column) ,)
        excute_insert += ('?' ,)
    excute_text +=  ','.join(excute_header) + ') VALUES (' + ','.join(excute_insert)+ ");"
    for index, row in list_csv.iterrows():
        excute_value =()
        for row_item in row :
            if str(row_item ) == 'nan'or str(row_item ) == 'NaT':
                excute_value += ('',)
            else:
                excute_value += (str(row_item),)

        print  (excute_text,excute_value)
        c.execute(excute_text,excute_value)
        print('submitted')
        conn.commit()

def import_spreadsheet_header(filename, table_name):

    list_csv = pd.read_excel(filename)
    excute_text = 'CREATE TABLE {}(id integer Primary Key'.format(table_name)
    excute_header = f''
    excute_insert =f''
    for column in list_csv.columns:

        excute_header += f', {column}  text'
    print (excute_header)
    excute_text +=  f'{excute_header});'
    print (excute_text)
    c.execute(excute_text)
    print('submitted')
    conn.commit()


if __name__ == '__main__' :
    # import_spreadsheet_header(r"Z:\ACCOUNTS\9999 - CONSOLIDATION\OTHERS\SMART_staff_details.xlsx",'user')
    import_spreadsheet_data(r"Z:\ACCOUNTS\9999 - CONSOLIDATION\OTHERS\role_user.xlsx",'roles_users')

#
# c.execute(""" CREATE TABLE smart_project_listing (
#             id integer Primary Key,
#             MCST_no text Not Null,
#             Printer_code integer Not Null,
#             PROPERTY_NAME text Not Null,
#             START_DATE text,
#             PREVIOUS_MA text,
#             TERMINATED_DATE text,
#             NEW_MA text,
#             YE text,
#             GST text,
#             GIRO text,
#             UNITS interger Not Null,
#             BILLINGS_CYCLE text Not Null,
#             DIRECTOR_HEAD text,
#             PORFORLIO_MANAGER text,
#             PROPERTY_OFFICIER text,
#             SITE_OFFICER text,
#             ROAD_NAME_ADDRESS text,
#             ACCOUNTS_INCHARGE text
#             );
#         """)
# c.execute("""INSERT INTO roles_users (user_id, role_id) VALUES
#     ( (SELECT id from user WHERE email ='clarence.yeo@smartproperty.sg'), (SELECT id from role WHERE name ='admin') )
#
# """ )
conn.commit()


# c.execute(""" select name from sqlite_master where type = 'table'
#   """)
# c.execute(""" Drop Table FILE_LISTING""")
# c.execute(""" SELECT * from FILE_LISTING
# """)
#
# print(c.fetchall())
#
