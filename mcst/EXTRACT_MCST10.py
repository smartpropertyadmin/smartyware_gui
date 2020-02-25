import os
import csv
import pandas as pd
import shutil
import re
from datetime import datetime,timedelta


class MCExtract:

    def __init__(self):
        self.Mcmodules = ['AP', 'AR', 'GL']
        self.McRetrieveLog = ''
        self.McDattext = ''
        self.McDatMainText = ''
    def Update_Mcdat(self):
        with open("C:\Mcst10\mc.dat", 'w') as  McDatFile:
            McDatFile.writelines(self.McDatMainText)

    def MC_copy_file(self, Mc_name, Accts_Drive,Mcstindex, Mc_Property_name):
        Mc_Drive = os.path.join("C:\Mcst10", Mc_name)
        Mcstindex = str(Mcstindex)

        if not os.path.exists(Mc_Drive):
            os.makedirs(Mc_Drive)
        Server_Drive = os.path.join("\\\\" + Accts_Drive + '\mcst10', Mc_name + "\\")
        McDattext = ''
        try:
            Mcstindex_dat = (f"{int(Mcstindex):04d}")
        except:
            Mcstindex_dat = Mcstindex
        for Mcmodule in self.Mcmodules:
            McDattext += '"' + Mcstindex_dat + ' - ' + Mc_Property_name + ' - ' + Mcmodule + ' " "' + Mcmodule + '" "MC' + Mcstindex + Mcmodule + \
                         '" "MC' + Mcstindex + '" "Z:\MCBACK\MC' + Mcstindex + '" "' +  Mcstindex_dat + ' - ' + Mc_Property_name + ' - GL"'  + '\n'

        if McDattext not in self.McDatMainText:
            self.McDatMainText+= McDattext

        try:
            if os.path.exists(Server_Drive):

                for (dirpath, dirnames, filenames) in os.walk(Server_Drive):

                    for filename in filenames:

                        if re.search(filename, Mc_name, re.IGNORECASE) != -1:
                            shutil.copy(os.path.join(dirpath, filename), os.path.join(Mc_Drive, filename))

                self.McRetrieveLog += '\npath copied ,' + Server_Drive

            else:
                self.McRetrieveLog += '\ncant go path,' + Server_Drive
        except:
            self.McRetrieveLog += '\ncant go path,' + Server_Drive

    def Extract_single_Mcst(self, Mcstindex):
        Project_listing_file = "Z:\ACCOUNTS\9999 - CONSOLIDATION\OTHERS\Project_listing.xlsx"
        Staff_contact_file = "Z:\ACCOUNTS\9999 - CONSOLIDATION\OTHERS\SMART_staff_details.xlsx"
        Mc_list = pd.read_excel(Project_listing_file)
        Staff_list = pd.read_excel(Staff_contact_file)

        Mcstindex = int(Mcstindex)
        Mc_name = "MC" + str(Mcstindex)
        Mc_Property_name = Mc_list.loc[Mc_list['MCST_no'] == Mcstindex].iat[0,3]
        Accounts_incharge = Mc_list.loc[Mc_list['MCST_no'] == Mcstindex].iat[0,0]
        Accts_Drive = Staff_list.loc[Staff_list['NAME'] == Accounts_incharge].iat[0, 3]

        with open("C:\Mcst10\mc.dat", 'r') as  McDatFile:
            self.McDatMainText = McDatFile.read()
        try:
            # print (McDatFile.read())
            self.MC_copy_file(Mc_name=Mc_name, Accts_Drive=Accts_Drive, Mcstindex=Mcstindex,
                              Mc_Property_name=Mc_Property_name
                              )
            self.Update_Mcdat()
            print('MCST 10 Copied ', Mcstindex)
        except:

            print ('Unable to copy file', Mcstindex)

    def Push_MC_file(self, Mcstindex):
        Project_listing_file = "Z:\ACCOUNTS\9999 - CONSOLIDATION\OTHERS\Project_listing.xlsx"
        Staff_contact_file = "Z:\ACCOUNTS\9999 - CONSOLIDATION\OTHERS\SMART_staff_details.xlsx"
        Mc_list = pd.read_excel(Project_listing_file)
        Staff_list = pd.read_excel(Staff_contact_file)

        Mcstindex = int(Mcstindex)
        Mc_name = "MC" + str(Mcstindex)

        Accounts_incharge = Mc_list.loc[Mc_list['MCST_no'] == Mcstindex].iat[0,0]
        Accts_Drive = Staff_list.loc[Staff_list['NAME'] == Accounts_incharge].iat[0, 3]
        Mc_Drive = os.path.join("C:\Mcst10", Mc_name)
        Mcstindex = str(Mcstindex)
        Server_Drive = os.path.join("\\\\" + Accts_Drive + '\mcst10', Mc_name + "\\")

        try:
            if os.path.exists(Server_Drive):

                for (dirpath, dirnames, filenames) in os.walk(Mc_Drive):

                    for filename in filenames:
                        if Mc_name in filename:
                            shutil.copy(os.path.join(dirpath, filename),os.path.join(Server_Drive, filename))

                self.McRetrieveLog += '\npath copied ,' + Server_Drive

            else:
                self.McRetrieveLog += '\ncant go path,' + Server_Drive
        except:
            self.McRetrieveLog += '\ncant go path,' + Server_Drive



    def Extract_All_Mcst(self):
            Project_listing_file = "Z:\ACCOUNTS\9999 - CONSOLIDATION\OTHERS\Project_listing.xlsx"
            Staff_contact_file = "Z:\ACCOUNTS\9999 - CONSOLIDATION\OTHERS\SMART_staff_details.xlsx"
            Mc_list = pd.read_excel(Project_listing_file)
            Staff_list = pd.read_excel(Staff_contact_file)

            # with open("C:\Mcst10\mc.dat",'w') as  McDatFile :

            for Index, Mc_row in Mc_list.iterrows():
                try :
                    Accts_Drive = Staff_list.loc[Staff_list['NAME'] == Mc_row['ACCOUNTS INCHARGE']].iat[0,3]
                except:
                    continue

                Mcstindex = str(Mc_row['MCST_no'])
                Mc_name = "MC"+ str( Mc_row['MCST_no'])
                Mc_Property_name = Mc_row['PROPERTY']

                if Mc_row['TERMINATED DATE']  < datetime.today():
                    continue
                self.MC_copy_file(Mc_name= Mc_name, Accts_Drive= Accts_Drive,Mcstindex= Mcstindex, Mc_Property_name= Mc_Property_name)
            self.McDatMainText += '"Zsystem-10" "Zip Backup" "ZipBACKUP     #backdir\#db.zip    #defdir\#db.*" "" "" ""' + '\n' + \
                                '"Zsystem-12" "Zip Restore" "ZipRESTORE    #backdir\#db.zip    #defdir" "" "" ""' + '\n' + \
                                '"Zsystem-30" "Copy Backup" "cCOPY    #fulldb.*     #backdir " "" "" ""' + '\n' + \
                                '"Zsystem-32" "Copy Restore" "cRESTORE    #backdir\#db.*    #defdir " "" "" ""' + '\n' + \
                                '"Zsystem-40" "Screen Viewer" "" "" "" ""' + '\n' + \
                                '"Zsystem-50" "Printer DotMatrix" "" "" "" ""' + '\n' + \
                                '"Zsystem-52" "Printer Others Portrait" "" "" "" ""' + '\n' + \
                                '"Zsystem-54" "Printer Others Landscape" "" "" "" ""' + '\n' + \
                                '"Zsystem-62" "Print Statement Option" "Pre-printed-Stationery" "" "" ""' + '\n' + \
                                '"Zsysz-hid-80" "FileoutAll" "" "" "" ""'

            self.Update_Mcdat()

            self.McRetrieveLog = self.McRetrieveLog[self.McRetrieveLog.find('\n')+1:]
            with open(os.path.join("C:\Mcst10\MCRESTORELOG", datetime.today().strftime("%Y%m%d") + "_retrieve_log.csv"),'w') as csvfile:

                csvfile.write(self.McRetrieveLog)
    def Extract_MCST_List(self, File_path):
            Project_listing_file = "Z:\ACCOUNTS\9999 - CONSOLIDATION\OTHERS\Project_listing.xlsx"
            Staff_contact_file = "Z:\ACCOUNTS\9999 - CONSOLIDATION\OTHERS\SMART_staff_details.xlsx"
            Mc_list = pd.read_excel(Project_listing_file)
            Extract_list = pd.read_excel(File_path)
            Staff_list = pd.read_excel(Staff_contact_file)



            # with open("C:\Mcst10\mc.dat",'w') as  McDatFile :

            for Index, Mc_row in Extract_list.iterrows():

                Accts_ic = Mc_list.loc[Mc_list['MCST_no'] == Mc_row['MCST_no']].iat[0,0]

                try :
                    Accts_Drive = Staff_list.loc[Staff_list['NAME'] == Accts_ic].iat[0,3]

                except:
                    continue

                Mcstindex = str(Mc_row['MCST_no'])
                Mc_name = "MC"+ str( Mc_row['MCST_no'])
                Mc_Property_name = Mc_row['PROPERTY']
                self.Mcmodules = [Mc_row['Extract_type']]
                # if Mc_row['TERMINATED DATE']  < datetime.today():
                #     continue
                self.MC_copy_file(Mc_name= Mc_name, Accts_Drive= Accts_Drive,Mcstindex= Mcstindex, Mc_Property_name= Mc_Property_name)
            self.McDatMainText += '"Zsystem-10" "Zip Backup" "ZipBACKUP     #backdir\#db.zip    #defdir\#db.*" "" "" ""' + '\n' + \
                                '"Zsystem-12" "Zip Restore" "ZipRESTORE    #backdir\#db.zip    #defdir" "" "" ""' + '\n' + \
                                '"Zsystem-30" "Copy Backup" "cCOPY    #fulldb.*     #backdir " "" "" ""' + '\n' + \
                                '"Zsystem-32" "Copy Restore" "cRESTORE    #backdir\#db.*    #defdir " "" "" ""' + '\n' + \
                                '"Zsystem-40" "Screen Viewer" "" "" "" ""' + '\n' + \
                                '"Zsystem-50" "Printer DotMatrix" "" "" "" ""' + '\n' + \
                                '"Zsystem-52" "Printer Others Portrait" "" "" "" ""' + '\n' + \
                                '"Zsystem-54" "Printer Others Landscape" "" "" "" ""' + '\n' + \
                                '"Zsystem-62" "Print Statement Option" "Pre-printed-Stationery" "" "" ""' + '\n' + \
                                '"Zsysz-hid-80" "FileoutAll" "" "" "" ""'

            self.Update_Mcdat()

            self.McRetrieveLog = self.McRetrieveLog[self.McRetrieveLog.find('\n')+1:]

            with open(os.path.join("C:\Mcst10\MCRESTORELOG", datetime.today().strftime("%Y%m%d") + "_retrieve_log.csv"),'w') as csvfile:

                csvfile.write(self.McRetrieveLog)



# MCExtract().Extract_MCST_List(r"Z:\ACCOUNTS\9999 - CONSOLIDATION\PAYMENT\AP MODULE\GL EXTRACT MODULE.xlsx")
