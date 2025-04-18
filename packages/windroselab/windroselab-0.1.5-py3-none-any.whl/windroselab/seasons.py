
import numpy as np

import xlrd

from windroselab.app_context import AppContext



def seasons_determiner(ctx:AppContext, wb, colDirection, colSpeed, rowStart, rowEnd, Max_speed=40):
    
    #print(55)
    
    # wb = xlrd.open_workbook(f_name) 
    
    date_col = int(ctx.Ent11p.get()) - 1
    
    
    
    sheet = wb.sheet_by_index(0) 
    
    row = sheet.nrows
    
    ctx.wd = np.zeros((row, 1))

    #print("np.shape(ctx.wd) = ")
    
    #print(np.shape(ctx.wd))
    
    ctx.ws = np.zeros((row, 1))
    
    j = 0
    
    wd_sp = [] ; ws_sp = []
    
    wd_su = [] ; ws_su = []
    
    wd_fa = [] ; ws_fa = []
    
    wd_wi = [] ; ws_wi = []
    
    
    
    for i in range(rowStart, rowEnd):
        
        try:
            
            vel = sheet.cell_value(i, colSpeed)
            dr = sheet.cell_value(i, colDirection)
         
            date = xlrd.xldate_as_tuple(sheet.cell(i, date_col).value,wb.datemode)
         
        # if(isinstance(vel, float) or isinstance(vel, int)) and 
        
         # if (not( (int(dr) == dr) and (vel == 0 or vel == 0.0))) and ((int(dr) == dr) and (isinstance(vel, float) or isinstance(vel, int))):
         # try:
            ctx.wd[j, 0] = dr
            ctx.ws[j, 0] = vel
            
            if vel > Max_speed :
                
                continue
   
            j += 1
        
        
        
            if date[1]==4 or date[1]==5 or (date[1]==3 and date[2]>20 ) or (date[1]==6 and date[2]<21 ):
                
                wd_sp.append(dr) ; ws_sp.append(vel)
        
            elif date[1]==7 or date[1]==8 or (date[1]==6 and date[2]>20 ) or (date[1]==9 and date[2]<23 ):
           
                wd_su.append(dr) ; ws_su.append(vel)
           
            elif date[1]==10 or date[1]==11 or (date[1]==9 and date[2]>22 ) or (date[1]==12 and date[2]<21 ):
           
                wd_fa.append(dr) ; ws_fa.append(vel)
           
            elif date[1]==1 or date[1]==2 or (date[1]==12 and date[2]>20 ) or (date[1]==3 and date[2]<21 ):
           
                wd_wi.append(dr) ; ws_wi.append(vel)
            
                
            
             
              
         
        except Exception as e:
            
            pass
    
    ctx.wd = ctx.wd[0:j, 0]

    #print("np.shape(ctx.wd) = ")
    
    #print(np.shape(ctx.wd))
    
    ctx.ws = ctx.ws[0:j, 0]   
    
    #global awd_sp, aws_sp, awd_su, aws_su, awd_fa, aws_fa, awd_wi, aws_wi
    
    ctx.awd_sp = np.array(wd_sp) ; ctx.aws_sp = np.array(ws_sp)
    
    ctx.awd_su = np.array(wd_su) ; ctx.aws_su = np.array(ws_su)
    
    ctx.awd_fa = np.array(wd_fa) ; ctx.aws_fa = np.array(ws_fa)
    
    ctx.awd_wi = np.array(wd_wi) ; ctx.aws_wi = np.array(ws_wi)
    
    #print(j, j)
