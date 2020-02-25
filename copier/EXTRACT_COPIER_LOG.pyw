from flask_project.copier import Canon_IR5540_Extract
from flask_project.copier import Canon_IR3320_Extract
from flask_project.copier import Ricoh_C3503_Extract

# print ("Updating Canon_02_18 log ...... ")
# try:
Canon_IR5540_Extract.extract_0218canon().update_log_list()
#     # print ("Updating Canon_02_18 log sucessful!")
# except:
#     return
#     # print ("Updating Canon_02_18 log fail!")
#
# # print ("Updating Canon_02_26 log ...... ")
# try:
Canon_IR3320_Extract.extract_0226canon().update_log_list()
#     # print ("Updating Canon_02_26 log sucessful!")
# except:
#     return
#     # print ("Updating Canon_02_26 log fail!")
#     # continue
#     # print ("Updating Ricoh_02_18 log ...... ")
# try:
Ricoh_C3503_Extract.extract_0218ricoh().update_log_list()
#     # print ("Updating Ricoh_02_18 log sucessful!")
# except:
#     return
#     # print ("Updating Ricoh_02_18 log fail!")
#     # continue