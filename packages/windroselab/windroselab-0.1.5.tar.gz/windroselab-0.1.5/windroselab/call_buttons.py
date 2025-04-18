
from windroselab.app_context import AppContext

from tkinter import filedialog as fd

import tkinter as tk

from windroselab.opener import excel_reader


def enable(context:AppContext):
    
    context.TAB_CONTROL.tab(context.TAB2, state="normal")




def read_data(ctx:AppContext):
    
    ftypes = [('excel files', '*.xls'),('excel files', '*.xlsx'), ('All files', '*')]
    ctx.TAB_CONTROL.add(ctx.TAB2, text='Tab 2', state="disabled")
    #global file_path, wd, ws
    name = fd.askopenfilename(filetypes = ftypes) 
    
    ctx.txt1.delete("1.0", "end")
    ctx.txt1.insert(tk.END, name)
    
    
    
    ctx.file_path = name


   

    
    try :
        
        ctx.colDi = int(ctx.Ent12.get()) - 1
        ctx.colSp = int(ctx.Ent13.get()) - 1
        ctx.rowSt = int(ctx.Ent14.get()) - 1
        
        mx = int(ctx.spinT3.get())
        
        try:
            rowEn = int(ctx.Ent15.get()) - 1
            
        except:
            rowEn = '-'
            

        
        ctx.wd, ctx.ws, ctx.j = excel_reader(ctx, name, colDirection=ctx.colDi, colSpeed=ctx.colSp,
                                             rowStart=ctx.rowSt, rowEnd=rowEn, Max=mx)
        
        if ctx.j >0 :
            
            enable(ctx)

        
    except:
        tk.messagebox.showinfo("Warning", 
                           'One or more of your input values is/are not valid. \n'+
                           'Or your data is not valid.')
        print('Exception in read_data')


    
    
    

def add_mark(ctx:AppContext):
    #global image_path
    ftypes = [('Joint Photographic Experts Group', '*.jpg'),
              ('Joint Photographic Experts Group', '*.jpeg'),
              ('Portable Network Graphics', '*.png'),
              ('Tagged Image File Format', '*.tif'),
              ('Tagged Image File Format','*.tiff'),
              ('bitmap image file', '*.bmp'),
              ('All files', '*')]

    ctx.image_path = fd.askopenfilename(filetypes = ftypes) 
    
    
    ctx.txt2.insert(tk.END, ctx.image_path)
    
    # a = txt1.get(1.0, tk.END)
    
    # txt2.insert(tk.END, a)
    
    # print(a)
