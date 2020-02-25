import pyqrcode
from PIL import Image
import pycrc.algorithms


def qr_code_generate_smart(Qrcode_string, logo_file=None, logo_size = 1000):

    url = pyqrcode.QRCode(Qrcode_string,error = 'H')
    url.png('test.png',scale=100)
    img = Image.open('test.png')
    img = img.convert("RGBA")
    width, height = img.size
    # How big the logo we want to put in the qr code png


    # Open the logo image
    if not logo_file:
        logo = Image.open(r"Z:\CLARENCE\RESEARCH AND DEVELOPMENT\OTHERS\SMART_LOGO_square.png",'r')
    else:
        print(logo_file)
        logo = Image.open(logo_file,'r')

    # Calculate xmin, ymin, xmax, ymax to put the logo
    xmin = ymin = int((width / 2) - (logo_size / 2))
    xmax = ymax = int((width / 2) + (logo_size / 2))

    # resize the logo as calculated
    logo = logo.resize((xmax - xmin, ymax - ymin))

    # put the logo in the qr code
    img.paste(logo, (xmin, ymin, xmax, ymax))

    return img

# test_qr ='00020101021126940009SGPAYNOW010120210S98MC2189C030112080408202012310510TESTING123'
# qr_code_generate_smart(test_qr).show()
# qr_code_generate_smart('00020101021126370009SG.PAYNOW010120210201617935C030115204000053037025802SG5919KARIO GLASS PTE LTD6009Singapore630458F3').show()

def paynow_qrcode(PayNow_ID, Merchant_name, Bill_number, Transaction_amount):


    # module from https://pycrc.org

    Can_edit_amount = "0"
    Merchant_category = "0000"
    Transaction_currency = "702"
    Country_code = "SG"
    Merchant_city = "Singapore"
    Globally_Unique_ID = "SG.PAYNOW"
    Proxy_type = "2"

    start_string = "010212"
    Dynamic_PayNow_QR = "000201"
    Globally_Unique_ID_field = "00"
    Globally_Unique_ID_length = str(len(Globally_Unique_ID)).zfill(2)
    Proxy_type_field = "01"
    Proxy_type_length = str(len(Proxy_type)).zfill(2)
    PayNow_ID_field = "02"
    PayNow_ID_Length = str(len(PayNow_ID)).zfill(2)
    Can_edit_amount_field = "03"
    Can_edit_amount_length = str(len(Can_edit_amount)).zfill(2)
    Merchant_category_field = "52"
    Merchant_category_length = str(len(Merchant_category)).zfill(2)
    Transaction_currency_field = "53"
    Transaction_currency_length = str(len(Transaction_currency)).zfill(2)
    Merchant_Account_Info_field = "26"
    Merchant_Account_Info_length = str(len(Globally_Unique_ID_field + Globally_Unique_ID_length + Globally_Unique_ID + \
                                           Proxy_type_field + Proxy_type_length + Proxy_type + \
                                           PayNow_ID_field + PayNow_ID_Length + PayNow_ID + \
                                           Can_edit_amount_field + Can_edit_amount_length + Can_edit_amount)).zfill(2)

    Transaction_amount_field = "54"
    Transaction_amount_length = str(len(Transaction_amount)).zfill(2)
    Country_code_field = "58"
    Country_code_length = str(len(Country_code)).zfill(2)
    Merchant_name_field = "59"
    Merchant_name_length = str(len(Merchant_name)).zfill(2)
    Merchant_city_field = "60"
    Merchant_city_length = str(len(Merchant_city)).zfill(2)
    Bill_number_field = "62"
    Bill_number_sub_length = str(len(Bill_number)).zfill(2)
    Bill_number_length = str(len("01" + Bill_number_sub_length + Bill_number)).zfill(2)

    data_for_crc = Dynamic_PayNow_QR + start_string + Merchant_Account_Info_field + Merchant_Account_Info_length + \
                   Globally_Unique_ID_field + Globally_Unique_ID_length + Globally_Unique_ID + \
                   Proxy_type_field + Proxy_type_length + Proxy_type + \
                   PayNow_ID_field + PayNow_ID_Length + PayNow_ID + \
                   Can_edit_amount_field + Can_edit_amount_length + Can_edit_amount + \
                   Merchant_category_field + Merchant_category_length + Merchant_category + \
                   Transaction_currency_field + Transaction_currency_length + Transaction_currency + \
                   Transaction_amount_field + Transaction_amount_length + Transaction_amount + \
                   Country_code_field + Country_code_length + Country_code + \
                   Merchant_name_field + Merchant_name_length + Merchant_name + \
                   Merchant_city_field + Merchant_city_length + Merchant_city + \
                   Bill_number_field + Bill_number_length + "01" + Bill_number_sub_length + Bill_number + \
                   "6304"

    # print (data_for_crc)

    # Sample code from https://pycrc.org
    crc = pycrc.algorithms.Crc(width=16, poly=0x1021,
                               reflect_in=False, xor_in=0xffff,
                               reflect_out=False, xor_out=0x0000)

    my_crc = crc.bit_by_bit_fast(data_for_crc)  # calculate the CRC, using the bit-by-bit-fast algorithm.
    crc_data_upper = ('{:04X}'.format(my_crc))
    # crc_data_upper = crc_data[-4:].upper()

    final_string = data_for_crc + crc_data_upper

    # print (final_string)

    # example code from the following link.
    # https://ourcodeworld.com/articles/read/554/how-to-create-a-qr-code-image-or-svg-in-python

    # Create qr code instance
    # qr = pyqrcode.QRCode(
    #     version = 1,
    #     error_correction = qrcode.constants.ERROR_CORRECT_H,
    #     box_size = 5,
    #     border = 2,
    # )

    # print(final_string)
    # Add data

    Paynow_logo_file = r'Z:\CLARENCE\RESEARCH AND DEVELOPMENT\SOFTWARE\PYTHON\Flask_project\flask_project\static\img\PAYNOW_LOGO.png'
    # print (Paynow_logo_file)
    # url = pyqrcode.QRCode(final_string, error='H')
    #
    #
    #
    # url.png('test.png', scale=100, module_color=(124,26,120))
    # # url.show()
    # img = Image.open('test.png')
    # img = img.convert("RGBA")
    # width, height = img.size
    return qr_code_generate_smart(final_string,Paynow_logo_file, logo_size=2000)

if __name__ == "__main__":
    paynow_qrcode('S98MC2189C','MCST PLAN NO. 2189','001-02-05','100.23')