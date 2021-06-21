import os
import pandas as pd
import xlsxwriter
import zipfile
import itertools
from zipfile import ZipFile
from datetime import datetime

import automation_helpers.globalconstants as gc

def sheet_creation(workbook,sheet_name, headings):
    """ Creating and returning sheet for each message """
    worksheet = workbook.add_worksheet(sheet_name)
    worksheet.set_column('A:C', 70)
    worksheet.set_row(0, 30)

    worksheet.set_column('A:A', 13)
    worksheet.set_column('B:B', 17)
    worksheet.set_column('C:C', 17)
    worksheet.set_column('D:D', 17)
    worksheet.set_column('E:E', 30)
    worksheet.set_column('F:F', 30)
    bold = workbook.add_format({'bold': 1, 'align': 'right'})
    worksheet.write_row('A1', headings, bold)
    return worksheet

def create_excel(log_type):
    path = gc.IMAGE_FOLDER+"/../../../Merged_Output/"
    if os.path.isdir(path) == False:
        os.makedirs(path)
    workbook = xlsxwriter.Workbook("{0}/Robot_Results.xlsx".format(path))

    headings = ['S.No', 'TestCaseId', 'IterationNo', "PASS/FAIL", "Android Logs", "Modem Logs"]
    worksheet = sheet_creation(workbook, "Result", headings)
    Values1 = []
    center = workbook.add_format({'align': 'center'})
    Values1 = gc.EXCEL_DATA.values()
    exec_status = []
    android_log_path = []
    output_path = []
    for v in Values1:
        exec_status.append(v[0])
        android_log_path.append(v[1])
        output_path.append((v[1]+"/../"))

    print(output_path)
    iter_no = []
    tc_name = []
    for key_name in list(gc.EXCEL_DATA.keys()):
        y = key_name.rsplit("_", 1) 
        it = "Iteration_"+str(y[1])
        iter_no.append(it)
        tc_name.append(y[0])

    row = 1
    col = 0
    for (a,b,c,d,e) in itertools.zip_longest(tc_name, iter_no, exec_status, android_log_path, output_path):        
            if b != None: 
                worksheet.write(row , col, row, center)
                worksheet.write(row , col + 1, a, center)
                worksheet.write(row , col + 2, b, center)
                worksheet.write(row , col + 3, c, center)
                worksheet.write(row , col + 4, d, center)
                
                if int(log_type) == 0:
                    worksheet.write(row , col + 5, d, center)
                elif int(log_type) == 1:
                    worksheet.write(row , col + 5, e, center)

            row += 1
    
    workbook.close()