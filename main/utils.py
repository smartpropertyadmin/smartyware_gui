import pandas as pd
import csv

def export_data_base_to_excel (data_base, export_file_path):
    with open(export_file_path, 'w', newline='') as csv_file:
        csv_write = csv.writer(csv_file)
        for data_row in data_base:
            print (data_row)
            csv_write.writerow(data_row)

