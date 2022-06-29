from Canon_IR5540_Extract import extract_copier_canon_ir5540 
from Canon_IR3320_Extract import extract_copier_canon_ir3320
from Ricoh_C3503_Extract import extract_copier_ricoh_c3503

# from Copier.Crimsion_intereq import crimsion_intereq_selenium
# from datetime import datetime
# report_date = datetime(2022,1,31)
# test =  crimsion_intereq_selenium()
# test.retrieve_monthly_report(report_month=report_date)

# extract_copier_canon_ir5540().post_new_account("4034")
# extract_copier_canon_ir3320().post_new_account("4034")
extract_copier_canon_ir5540().clear_counter_list()
extract_copier_canon_ir3320().clear_counter_list()

# extract_copier_canon_ir3320().get_counter_list()
# extract_copier_canon_ir5540().get_counter_list()
# extract_copier_ricoh_c3503().get_counter_list()
# extract_0218ricoh().get_counter_list()
# Konica_02_26_Extract.extract_0226konaica().get_counter_list()