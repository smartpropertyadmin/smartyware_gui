from flask_project.copier.Canon_IR5540_Extract import extract_copier_canon_ir5540
from flask_project.copier.Canon_IR3320_Extract import extract_copier_canon_ir3320
from flask_project.copier.Ricoh_C3503_Extract import extract_copier_ricoh_c3503

# import Konica_02_26_Extract


extract_copier_canon_ir5540().post_new_account(4648)
extract_copier_canon_ir3320().post_new_account(4648)
# extract_copier_ricoh_c3503().get_counter_list()
# # extract_0218ricoh().get_counter_list()
# Konica_02_26_Extract.extract_0226konaica().get_counter_list()