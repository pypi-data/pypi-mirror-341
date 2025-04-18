import xlrd 

import win32com.client



import tkvalidate #pip install tkvalidate

import os

import numpy as np

from windroselab.app_context import AppContext

from windroselab.seasons import seasons_determiner


def excel_reader(ctx:AppContext, fileName, colDirection=4, colSpeed=5, rowStart=1, rowEnd=100, Max=40, ):
    
    

    # name_reverse = fileName[::-1]
    
    # index1 = name_reverse.find('\\')
    
    # name_reverse1 = name_reverse[index1+1:]
    
    # path = name_reverse1[::-1]


    Number = 10000
    
    
    output = os.getcwd() + '\\' + 'Data' + str(Number) + '.xlsx'
    
    while os.path.isfile(output):
       Number +=  1
       output = os.getcwd() + '\\' + 'Data' + str(Number) + '.xlsx'
       
    
    
    try :
        wb = xlrd.open_workbook(fileName) 
        
        
    except:
        
        wbc = o.Workbooks.Open(fileName)
        wbc.ActiveSheet.SaveAs(output,51)
        o.Workbooks.Close()
        
        wb = xlrd.open_workbook(output) 
        

    
    sheet = wb.sheet_by_index(0) 
    
    row = sheet.nrows
    
    if rowEnd =='-':
        rowEnd = row
        
    
    wd = np.zeros((row, 1))
    
    ws = np.zeros((row, 1))
    
    j = 0
    
    #for date: xlrd.xldate_as_tuple(sheet.cell(3,1).value,wb.datemode)
    
    for i in range(rowStart, rowEnd):
         vel = sheet.cell_value(i, colSpeed)
         dr = sheet.cell_value(i, colDirection)
         
        # if(isinstance(vel, float) or isinstance(vel, int)) and 
        
         # if (not( (int(dr) == dr) and (vel == 0 or vel == 0.0))) and ((int(dr) == dr) and (isinstance(vel, float) or isinstance(vel, int))):
         try:
             
             wd[j, 0] = dr
             
             ws[j, 0] = vel
             
             if vel <= Max: 
                 j += 1
         
         except:
             pass
    
    wd = wd[0:j, 0]
    
    ws = ws[0:j, 0]
    #print(ws.shape)
    
    if bool(ctx.CheckVarT0.get()):
        
        
        seasons_determiner(ctx, wb, colDirection, colSpeed, rowStart, rowEnd, Max_speed=Max)
    
    return(wd, ws, j)
