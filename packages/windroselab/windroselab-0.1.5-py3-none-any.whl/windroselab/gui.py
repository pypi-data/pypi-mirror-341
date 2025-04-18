

from tkinter import ttk, Menu

import tkinter
import tkinter as tk

import tkvalidate #pip install tkvalidate

from windroselab.call_buttons import read_data, add_mark

from windroselab.depictFunc import depict

from windroselab.spring import depict_spring

from windroselab.summer import depict_summer

from windroselab.fall import depict_fall

from windroselab.winter import depict_winter

from windroselab.app_context import AppContext



def close_window(ctx:AppContext):
    ctx.app1.quit()
    ctx.app1.destroy()
    




def activate_speeds(context:AppContext):
    
    if context.spinT2.config()['state'][4] == 'disabled':
        context.spinT2.config ( state = "readonly")
        
    else:
        
        context.spinT2.config ( state = "disabled")
    

    
def activate_buttons(context:AppContext):
    
    buttonList = [context.button2, context.button3, context.button4, context.button5]
    
    for button in buttonList:
        
    
        if button.config()['state'][4] == 'disabled':
            button.config ( state = "normal")
            
        else:
            
            button.config ( state = "disabled")
    
    entList = [context.Ent18, context.Ent19, context.Ent20, context.Ent21]
    
    textList = ["Spring", "Summer", "Autumn", "Winter"]
    
    i = 0
    
    for ent in entList:
        
    
        if ent.config()['state'][4] == 'disabled':
            ent.config ( state = "normal")
            ent.delete(0, tk.END)
            ent.insert(0, textList[i])
            
            i += 1
            
        else:
            
            ent.config ( state = "disabled")
    
#    print(Ent18.config()['state'][4])





def func(context:AppContext, _event=None):
        depict(context)



def About():
    tk.messagebox.showinfo("About", 
                           'This software is written by'+
                           '  "Seyed Abdolvahab Taghavi (s.av.taghavi@gmail.com)".'+'\nIt plots windrose'+
                           ' of data.')




def NewCommand(ctx:AppContext):
    
    ctx.txt1.delete("1.0", "end")
    ctx.txt2.delete("1.0", "end")
    

    ctx.ChT0.deselect()
    
    buttonList = [ctx.button2, ctx.button3, ctx.button4, ctx.button5]
    
    for button in buttonList:
        
        button.config ( state = "disabled")
    
    entList = [ctx.Ent18, ctx.Ent19, ctx.Ent20, ctx.Ent21]
    
    
         
    for ent in entList:
        
    
        ent.config ( state = "disabled")
    
    ctx.TAB_CONTROL.add(ctx.TAB2, text='Tab 2', state="disabled")
    
#    TAB_CONTROL.focus_force()
    ctx.TAB_CONTROL.select(ctx.TAB1)
    
    #global ws, wd, awd_sp, aws_sp, awd_su, aws_su, awd_fa, aws_fa, awd_wi, aws_wi, image_path
    
    
    try:
        
        
       # del image_path, ws, wd, awd_sp, aws_sp, awd_su, aws_su, awd_fa, aws_fa, awd_wi, aws_wi

        ctx.image_path = None
        ctx.ws = None
        ctx.wd = None
        ctx.awd_sp = None
        ctx.aws_sp = None
        ctx.awd_su = None
        ctx.aws_su = None
        ctx.awd_fa = None
        ctx.aws_fa = None
        ctx.awd_wi = None
        ctx.aws_wi = None
        
        


        
         
    except :
        pass



def lunch_app(ctx:AppContext) :
    
    
    app1 = tkinter.Tk()
    app1.geometry("800x600")
    app1.title('Plotting of Windrose Graphs')

    ctx.app1 = app1


    ctx.TAB_CONTROL = ttk.Notebook(app1)
    #Tab1
    ctx.TAB1 = ttk.Frame(ctx.TAB_CONTROL)
    ctx.TAB_CONTROL.add(ctx.TAB1, text='Tab 1')

    # button1=tk.Button(TAB1,text='Quit',command=close_window   )
    # button1.grid(row=1,column=0,sticky='W',padx=50,pady=6)




    frameT0 = tk.Frame(ctx.TAB1, height=1, borderwidth=2)#, bg='red')
    frameT0.grid(row=0, column=0, sticky='W' ,padx=50,pady=4)#.pack(side=tk.TOP)

    ctx.CheckVarT0 = tk.IntVar()
    ctx.ChT0 = tk.Checkbutton(frameT0, text = "Seasons", variable = ctx.CheckVarT0, \
                     onvalue = 1, offvalue = 0, height=2, \
                     width = 7, bg='red' , command=lambda:activate_buttons(ctx))

    ctx.ChT0.grid(row=0, column=0, sticky='W')


    ctx.CheckVarT01 = tk.IntVar()
    ChT01 = tk.Checkbutton(frameT0, text = "Autosave Plots", variable = ctx.CheckVarT01, \
                     onvalue = 1, offvalue = 0, height=2, \
                     width = 10, bg='lightgreen' )

    ChT01.grid(row=0, column=1, sticky='W')


    Lb11 = tk.Label(frameT0, text="Columns of Data:  ")
    Lb11.grid(row=0,column=2,sticky='W')#,padx=5, pady=4)

    Lb11p = tk.Label(frameT0, text="Date:  ")
    Lb11p.grid(row=0,column=3,sticky='W')#,padx=5, pady=4)


    ctx.Ent11p = tk.Entry(frameT0, width=4)
    ctx.Ent11p.grid(row=0, column=4, sticky='w')#,padx=5, pady=4)
    #Ent5.place(x=225, y=85)

    ctx.Ent11p.delete(0, tk.END)
    ctx.Ent11p.insert(0, "2")


    Lb12 = tk.Label(frameT0, text="Directions:  ")
    Lb12.grid(row=0,column=5,sticky='W')#,padx=5, pady=4)


    ctx.Ent12 = tk.Entry(frameT0, width=4)
    ctx.Ent12.grid(row=0, column=6, sticky='w')#,padx=5, pady=4)
    #Ent5.place(x=225, y=85)

    ctx.Ent12.delete(0, tk.END)
    ctx.Ent12.insert(0, "4")


    Lb13 = tk.Label(frameT0, text="Speeds:  ")
    Lb13.grid(row=0,column=7,sticky='W')#,padx=5, pady=4)


    ctx.Ent13 = tk.Entry(frameT0, width=4)
    ctx.Ent13.grid(row=0, column=8, sticky='w')#,padx=5, pady=4)
    #Ent5.place(x=225, y=85)

    ctx.Ent13.delete(0, tk.END)
    ctx.Ent13.insert(0, "3")


    Lb36 = tk.Label(frameT0, text=" Maximum:  ")
    Lb36.grid(row=0, column=9, sticky='W')



    varT3 = tk.StringVar(frameT0)
    varT3.set("40")

    ctx.spinT3 = tk.Spinbox(frameT0, width=4, from_= 10, to = 40, textvariable=varT3, state='readonly')#, textvariable=text_variable)  

    tkvalidate.int_validate(ctx.spinT3, from_=10, to=40)
      
    ctx.spinT3.grid(row=0,column=10,sticky='W',padx=5,pady=4)




    frameT00 = tk.Frame(ctx.TAB1, height=1, borderwidth=2)#, bg='red')
    frameT00.grid(row=1, column=0, sticky='W' ,padx=50,pady=4)#.pack(side=tk.TOP)


    Lb14 = tk.Label(frameT00, text="Rows of data:  ")
    Lb14.grid(row=0,column=0,sticky='W')#,padx=5, pady=4)

    Lb15 = tk.Label(frameT00, text="Start:  ")
    Lb15.grid(row=0,column=1,sticky='W')#,padx=5, pady=4)


    ctx.Ent14 = tk.Entry(frameT00, width=4)
    ctx.Ent14.grid(row=0, column=2, sticky='w')#,padx=5, pady=4)
    #Ent5.place(x=225, y=85)

    ctx.Ent14.delete(0, tk.END)
    ctx.Ent14.insert(0, "2")



    Lb16 = tk.Label(frameT00, text="End:  ")
    Lb16.grid(row=0,column=3,sticky='W')#,padx=5, pady=4)




    Ent15 = tk.Entry(frameT00, width=4)
    Ent15.grid(row=0, column=4, sticky='w')#,padx=5, pady=4)
    #Ent5.place(x=225, y=85)

    Ent15.delete(0, tk.END)
    Ent15.insert(0, "-")


    Lb17 = tk.Label(frameT00, text="Ratios:  ")
    Lb17.grid(row=0,column=5,sticky='W',padx=1)#, pady=4)

    Lb18 = tk.Label(frameT00, text="Length of Plot:  ")
    Lb18.grid(row=0,column=6,sticky='W')#,padx=5, pady=4)


    ctx.Ent16 = tk.Entry(frameT00, width=4)
    ctx.Ent16.grid(row=0, column=7, sticky='w')#,padx=5, pady=4)
    #Ent5.place(x=225, y=85)

    ctx.Ent16.delete(0, tk.END)
    ctx.Ent16.insert(0, "20")



    Lb19 = tk.Label(frameT00, text="  Length of Image:  ")
    Lb19.grid(row=0,column=8,sticky='W')#,padx=5, pady=4)


    ctx.Ent17 = tk.Entry(frameT00, width=4)
    ctx.Ent17.grid(row=0, column=9, sticky='w',padx=7)#, pady=4)
    #Ent5.place(x=225, y=85)

    ctx.Ent17.delete(0, tk.END)
    ctx.Ent17.insert(0, "4")








    frameT2 = tk.Frame(ctx.TAB1, height=1, borderwidth=2)#, bg='red')
    frameT2.grid(row=2, column=0, sticky='W' ,padx=40,pady=4)#.pack(side=tk.TOP)





    btn1 = tk.Button(frameT2, text='Open Data File', 
           command=lambda:read_data(ctx))

    btn1.grid(row=0, column=0, padx=12,pady=4)

    ctx.txt1 = tk.Text(frameT2, height=1, width=52)

    ctx.txt1.grid(row=0, column=1, sticky='E')


    frameT3 = tk.Frame(ctx.TAB1, height=1, borderwidth=2)#, bg='red')
    frameT3.grid(row=3, column=0, sticky='W' ,padx=42,pady=4)#.pack(side=tk.TOP)


    btn2 = tk.Button(frameT3, text='Open Image File', 
           command=lambda: add_mark(ctx))

    btn2.grid(row=0, column=0, padx=10,pady=4)

    ctx.txt2 = tk.Text(frameT3, height=1, width=51)

    ctx.txt2.grid(row=0, column=1)




    Lbf4 = tk.LabelFrame(ctx.TAB1, text="Titles:")
    Lbf4.grid(row=4, column=0, sticky='W',padx=50)


    Lb1 = tk.Label(Lbf4, text="Title of Total Plot:")
    Lb1.grid(row=0,column=0,sticky='W')#,padx=5, pady=4)

    ctx.Ent1 = tk.Entry(Lbf4, width=67)
    ctx.Ent1.grid(row=0,column=1,sticky='W')#,padx=5, pady=4)

    ctx.Ent1.delete(0, tk.END)
    ctx.Ent1.insert(0, "Windrose")



    Lb26 = tk.Label(Lbf4, text="Title of Spring Plot:", bg='lawngreen', anchor="w")
    Lb26.grid(row=1,column=0,sticky='W', ipadx=5)#,padx=5, pady=4)

    ctx.Ent18 = tk.Entry(Lbf4, width=67, state="disabled")
    ctx.Ent18.grid(row=1,column=1,sticky='W')#,padx=5, pady=4)



    Lb27 = tk.Label(Lbf4, text="Title of Summer Plot:", bg='salmon')
    Lb27.grid(row=2,column=0,sticky='W')#,padx=5, pady=4)

    ctx.Ent19 = tk.Entry(Lbf4, width=67, state="disabled")
    ctx.Ent19.grid(row=2,column=1,sticky='W')#,padx=5, pady=4)




    Lb28 = tk.Label(Lbf4, text="Title of Autumn Plot:", bg='yellow')
    Lb28.grid(row=3,column=0,sticky='W')#,padx=5, pady=4)

    ctx.Ent20 = tk.Entry(Lbf4, width=67, state="disabled")
    ctx.Ent20.grid(row=3,column=1,sticky='W')#,padx=5, pady=4)




    Lb29 = tk.Label(Lbf4, text="Title of Winter Plot:", bg='skyblue', anchor="w")
    Lb29.grid(row=4,column=0,sticky='W', ipadx=5)#,padx=5, pady=4)

    ctx.Ent21 = tk.Entry(Lbf4, width=67, state="disabled")
    ctx.Ent21.grid(row=4,column=1,sticky='W')#,padx=5, pady=4)



    Lbf5 = tk.LabelFrame(ctx.TAB1, text="Location of Image:")
    Lbf5.grid(row=5, column=0, sticky='W',padx=50)



    ctx.varR = tk.IntVar()

    ctx.varR.set(1)

    R1 = tk.Radiobutton(Lbf5, text="Bottom Left", variable=ctx.varR, value=1)
    R1.grid(row=0, column=0, sticky='W',padx=22)

    R2 = tk.Radiobutton(Lbf5, text="Bottom Right", variable=ctx.varR, value=2)
    R2.grid(row=0, column=1, sticky='W',padx=22)

    R3 = tk.Radiobutton(Lbf5, text="Top Left", variable=ctx.varR, value=3)
    R3.grid(row=0, column=2, sticky='W',padx=23)

    R4 = tk.Radiobutton(Lbf5, text="Top Right", variable=ctx.varR, value=4)
    R4.grid(row=0, column=3, sticky='W',padx=23)



    # btn3=tkinter.Button(TAB1,text='Tab 2',width=10,
    #                             height=4,
    #                             command=enable   )

    # btn3.grid(row=6,column=0,sticky='W',padx=50,pady=4)











    ####################Tab2####################
    ############################################


    ctx.TAB2 = ttk.Frame(ctx.TAB_CONTROL)
    ctx.TAB_CONTROL.add(ctx.TAB2, text='Tab 2', state="disabled")
    ctx.TAB_CONTROL.pack(expand=1, fill="both")




    frame1 = tk.Frame(ctx.TAB2, borderwidth=2)
    frame1.grid(row=0, column=0, sticky='W',padx=50,pady=4)#.pack(side=tk.TOP)

    #Lb0 = tk.Label(frame1, text="Name of Figure:  ")
    #Lb0.grid(row=0,column=0,sticky='W')#,padx=5, pady=4)
    #
    #Ent0 = tk.Entry(frame1, width=50)
    #Ent0.grid(row=0,column=1,sticky='W')#,padx=5, pady=4)
    #
    #Ent0.delete(0, tk.END)
    #Ent0.insert(0, "Fig1")






    frameT1 = tk.Frame(ctx.TAB2, height=1, borderwidth=2)#, bg='red')
    frameT1.grid(row=1, column=0, sticky='w' ,padx=50,pady=4)#.pack(side=tk.TOP)


    ctx.CheckVarT1 = tk.IntVar()
    ChT1 = tk.Checkbutton(frameT1, text = "Standard", variable = ctx.CheckVarT1, \
                     onvalue = 1, offvalue = 0, height=2, \
                     width = 6, bg='red' , command=lambda:activate_speeds(ctx))

    ChT1.grid(row=0, column=0, sticky='W')


    LbT0 = tk.Label(frameT1, text="  Directions:  ")
    LbT0.grid(row=0,column=1,sticky='W')#,padx=5, pady=4)

    varT1 = tk.StringVar(frameT1)
    varT1.set("4")
    ctx.spinT1 = tk.Spinbox(frameT1, width=4, values=(4,8,16,32), textvariable=varT1,
                        state='readonly')#, textvariable=text_variable)  

    tkvalidate.int_validate(ctx.spinT1, from_=4, to=32)
      
    ctx.spinT1.grid(row=0,column=2,sticky='W',padx=5,pady=4) 




    LbT1 = tk.Label(frameT1, text="  Speeds:  ")
    LbT1.grid(row=0,column=3,sticky='W')#,padx=5, pady=4)

    varT2 = tk.StringVar(frameT1)
    varT2.set("4")
    ctx.spinT2 = tk.Spinbox(frameT1, width=4, from_= 2, to = 20, textvariable=varT2, state='readonly')#, textvariable=text_variable)  

    tkvalidate.int_validate(ctx.spinT2, from_=2, to=20)
      
    ctx.spinT2.grid(row=0,column=4,sticky='W',padx=5,pady=4) 






    Lb5 = tk.Label(frameT1, text="     dpi: ")
    Lb5.grid(row=0, column=7, sticky='W')



    ctx.var1 = tk.StringVar(ctx.TAB2)
    ctx.var1.set("100")
    spin1 = tk.Spinbox(frameT1, width=4, from_= 10, to = 1000, textvariable=ctx.var1)#, textvariable=text_variable)  

    tkvalidate.int_validate(spin1, from_=0, to=1000)
      
    spin1.grid(row=0,column=8,sticky='W',padx=5,pady=4) 








    frame2 = tk.Frame(ctx.TAB2, borderwidth=2, height=10)
    frame2.grid(row=2, column=0, sticky='W',padx=50,pady=4)#.pack(side=tk.TOP)



    Lb2 = tk.Label(frame2, text="Position of Title: ")
    Lb2.grid(row=0,column=0,sticky='W')#,padx=5, pady=4)

    Lb3 = tk.Label(frame2, text="X =")
    Lb3.grid(row=0,column=1,sticky='W')

    ctx.Ent2 = tk.Entry(frame2, width=4)
    ctx.Ent2.grid(row=0, column=2, sticky='W',padx=13, pady=4)

    ctx.Ent2.delete(0, tk.END)
    ctx.Ent2.insert(0, "0.5")

    Lb4 = tk.Label(frame2, text="Y =")
    Lb4.grid(row=0, column=3, sticky='W')


    ctx.Ent3 = tk.Entry(frame2, width=4)
    ctx.Ent3.grid(row=0, column=4, sticky='W',padx=13, pady=4)

    ctx.Ent3.delete(0, tk.END)
    ctx.Ent3.insert(0, "1.1")



    Lb8 = tk.Label(frame2, text="  Legend Position: ")
    Lb8.grid(row=0, column=5, sticky='W')



    Lb9 = tk.Label(frame2, text="  X =  ")
    Lb9.grid(row=0,column=6,sticky='W')

    ctx.Ent4 = tk.Entry(frame2, width=4)
    ctx.Ent4.grid(row=0, column=7, sticky='W',padx=12, pady=4)
    #Ent4.place(x=135, y=85)

    ctx.Ent4.delete(0, tk.END)
    ctx.Ent4.insert(0, "1")

    Lb10 = tk.Label(frame2, text="Y =  ")
    Lb10.grid(row=0, column=8, sticky='W')


    ctx.Ent5 = tk.Entry(frame2, width=4)
    ctx.Ent5.grid(row=0, column=9, sticky='',padx=12, pady=4)
    #Ent5.place(x=225, y=85)

    ctx.Ent5.delete(0, tk.END)
    ctx.Ent5.insert(0, "0.5")






    frame3 = tk.Frame(ctx.TAB2, height=1, borderwidth=2)#, bg='red')
    frame3.grid(row=4, column=0, sticky='N' ,padx=50,pady=4)#.pack(side=tk.TOP)




    Lb12 = tk.Label(frame3, text=" Width of Sectors:  ")
    Lb12.grid(row=0, column=0, sticky='W')



    ctx.Ent7 = tk.Entry(frame3, width=4)
    ctx.Ent7.grid(row=0, column=1, sticky='w',padx=20, pady=4)
    #Ent5.place(x=225, y=85)

    ctx.Ent7.delete(0, tk.END)
    ctx.Ent7.insert(0, 0.3)

    tkvalidate.float_validate(ctx.Ent7, from_=0, to=1)

    Lb6 = tk.Label(frame3, text="Colors:")
    Lb6.grid(row=0, column=2, sticky='W')



    ctx.var2 = tk.StringVar(ctx.TAB2)
    ctx.var2.set("0")
    spin2 = tk.Spinbox(frame3, width =4,from_= 0, to = 19, textvariable=ctx.var2)#, textvariable=text_variable)  

    tkvalidate.int_validate(spin2, from_=0, to=19)
      
    spin2.grid(row=0,column=3,sticky='W',padx=20,pady=4) 



    Lb7 = tk.Label(frame3, text="   Writing_Percent_Angles")
    Lb7.grid(row=0, column=4, sticky='W')


    ctx.var3 = tk.StringVar(ctx.TAB2)
    ctx.var3.set("60")
    spin3 = tk.Spinbox(frame3, width =4, from_= 0, to = 359, textvariable=ctx.var3)#, textvariable=text_variable)  

    tkvalidate.int_validate(spin3, from_=0, to=359)
      
    spin3.grid(row=0,column=5,sticky='W',padx=20,pady=4) 


    Lbalaki1 = tk.Label(frame3, text="                            ")
    Lbalaki1.grid(row=0, column=6, sticky='W')








    # Lbalaki2 = tk.Label(frame4, text="                               ")
    # Lbalaki2.grid(row=0, column=7, sticky='W')


    Lbf0 = tk.LabelFrame(ctx.TAB2, text="Adjusting Size of Plot:", fg='orange')
    Lbf0.grid(row=5, column=0, sticky='W',padx=50)



    Lb13 = tk.Label(Lbf0, text="Width of Figure: ")
    Lb13.grid(row=0, column=0, sticky='W')


    ctx.Ent8 = tk.Entry(Lbf0, width=4)
    ctx.Ent8.grid(row=0, column=1, sticky='w',padx=8, pady=4)
    #Ent5.place(x=225, y=85)

    ctx.Ent8.delete(0, tk.END)
    ctx.Ent8.insert(0, "8")




    Lb14 = tk.Label(Lbf0, text="Height of Figure: ")
    Lb14.grid(row=0, column=2, sticky='W')


    ctx.Ent9 = tk.Entry(Lbf0, width=4)
    ctx.Ent9.grid(row=0, column=3, sticky='w',padx=8, pady=4)
    #Ent5.place(x=225, y=85)

    ctx.Ent9.delete(0, tk.END)
    ctx.Ent9.insert(0, "6")


    # Lb19 = tk.Label(Lbf0, text="  Bounding Box:  ")
    # Lb19.grid(row=0, column=4, sticky='W')

    Lb20 = tk.Label(Lbf0, text="XLimit ")
    Lb20.grid(row=0, column=5, sticky='W')


    ctx.Ent10 = tk.Entry(Lbf0, width=4)
    ctx.Ent10.grid(row=0, column=6, sticky='w',padx=8, pady=4)
    #Ent5.place(x=225, y=85)

    ctx.Ent10.delete(0, tk.END)
    ctx.Ent10.insert(0, "10")

    Lb21 = tk.Label(Lbf0, text="Circles' Line-Width")
    Lb21.grid(row=0, column=7, sticky='W')

    ctx.Ent11 = tk.Entry(Lbf0, width=4)
    ctx.Ent11.grid(row=0, column=8, sticky='w',padx=8, pady=4)
    #Ent5.place(x=225, y=85)

    ctx.Ent11.delete(0, tk.END)
    ctx.Ent11.insert(0, "1")



    Lbf00 = tk.LabelFrame(ctx.TAB2, text="Configure subplots:", fg='blue')
    Lbf00.grid(row=6, column=0, sticky='W',padx=50)

    #plt.subplots_adjust(left=None, bottom=None, right=None, top=None, wspace=2, hspace=.5)


    Lb30 = tk.Label(Lbf00, text="Bottom:  ")
    Lb30.grid(row=0, column=0, sticky='W')

    ctx.Ent22 = tk.Entry(Lbf00, width=4)
    ctx.Ent22.grid(row=0, column=1, sticky='w',padx=1, pady=4)
    #Ent5.place(x=225, y=85)

    ctx.Ent22.delete(0, tk.END)
    ctx.Ent22.insert(0, "0")


    Lb31 = tk.Label(Lbf00, text="Left:  ")
    Lb31.grid(row=0, column=2, sticky='W')

    ctx.Ent23 = tk.Entry(Lbf00, width=4)
    ctx.Ent23.grid(row=0, column=3, sticky='w',padx=1, pady=4)
    #Ent5.place(x=225, y=85)

    ctx.Ent23.delete(0, tk.END)
    ctx.Ent23.insert(0, "0")


    Lb32 = tk.Label(Lbf00, text="Right:  ")
    Lb32.grid(row=0, column=4, sticky='W')

    ctx.Ent24 = tk.Entry(Lbf00, width=4)
    ctx.Ent24.grid(row=0, column=5, sticky='w',padx=1, pady=4)
    #Ent5.place(x=225, y=85)

    ctx.Ent24.delete(0, tk.END)
    ctx.Ent24.insert(0, "1")


    Lb33 = tk.Label(Lbf00, text="Top:  ")
    Lb33.grid(row=0, column=6, sticky='W')

    ctx.Ent25 = tk.Entry(Lbf00, width=4)
    ctx.Ent25.grid(row=0, column=7, sticky='w',padx=1, pady=4)
    #Ent5.place(x=225, y=85)

    ctx.Ent25.delete(0, tk.END)
    ctx.Ent25.insert(0, ".9")


    Lb34 = tk.Label(Lbf00, text="Width Space:  ")
    Lb34.grid(row=0, column=8, sticky='W')

    ctx.Ent26 = tk.Entry(Lbf00, width=4)
    ctx.Ent26.grid(row=0, column=9, sticky='w',padx=1, pady=4)
    #Ent5.place(x=225, y=85)

    ctx.Ent26.delete(0, tk.END)
    ctx.Ent26.insert(0, "1")



    Lb35 = tk.Label(Lbf00, text="Height Space:  ")
    Lb35.grid(row=0, column=10, sticky='W')

    ctx.Ent27 = tk.Entry(Lbf00, width=4)
    ctx.Ent27.grid(row=0, column=11, sticky='w',padx=1, pady=4)
    #Ent5.place(x=225, y=85)

    ctx.Ent27.delete(0, tk.END)
    ctx.Ent27.insert(0, "0.5")
        




    Lbf1 = tk.LabelFrame(ctx.TAB2, text="Fonts:", fg='green')
    Lbf1.grid(row=7, column=0, sticky='W', padx=50)

    Lb15 = tk.Label(Lbf1, text="Title: ")
    Lb15.grid(row=0, column=0, sticky='N')


    ctx.var4 = tk.StringVar(ctx.TAB2)
    ctx.var4.set("20")
    spin4 = tk.Spinbox(Lbf1, width=4, from_= 1, to = 100, textvariable=ctx.var4)#, textvariable=text_variable)  

    tkvalidate.int_validate(spin4, from_=1, to=100)
      
    spin4.grid(row=0,column=1,sticky='W',padx=17,pady=4) 




    Lb16 = tk.Label(Lbf1, text="Legend: ")
    Lb16.grid(row=0, column=2, sticky='N')


    ctx.var5 = tk.StringVar(ctx.TAB2)
    ctx.var5.set("12")
    spin5 = tk.Spinbox(Lbf1, width=4, from_= 1, to = 100, textvariable=ctx.var5)#, textvariable=text_variable)  

    tkvalidate.int_validate(spin5, from_=1, to=100)
      
    spin5.grid(row=0, column=3, sticky='W', padx=17, pady=4) 




    Lb17 = tk.Label(Lbf1, text="Directions: ")
    Lb17.grid(row=0, column=4, sticky='N')


    ctx.var6 = tk.StringVar(ctx.TAB2)
    ctx.var6.set("12")
    spin6 = tk.Spinbox(Lbf1, width=4, from_= 1, to = 100, textvariable=ctx.var6)#, textvariable=text_variable)  

    tkvalidate.int_validate(spin6, from_=1, to=100)
      
    spin6.grid(row=0, column=5, sticky='W', padx=17, pady=4) 






    Lb18 = tk.Label(Lbf1, text="Percentage: ")
    Lb18.grid(row=0, column=6, sticky='N')


    ctx.var7 = tk.StringVar(ctx.TAB2)
    ctx.var7.set("12")
    spin7 = tk.Spinbox(Lbf1, width=4, from_= 1, to = 100, textvariable=ctx.var7)
    #, textvariable=text_variable)  

    tkvalidate.int_validate(spin7, from_=1, to=100)
      
    spin7.grid(row=0, column=7, sticky='W', padx=17, pady=4) 






    Lbf2 = tk.LabelFrame(ctx.TAB2, text="Colors of Fonts:")
    Lbf2.grid(row=8, column=0, sticky='W',padx=50)




    Lb22 = tk.Label(Lbf2, text="Title: ")
    Lb22.grid(row=0, column=0, sticky='N')


    fontColorRange = ['black', 'blue',  'cyan', 'green', 'indigo',  'magenta',  
                      'orange', 'purple', 'red',  'yellow']
    ctx.var8 = tk.StringVar(ctx.TAB2)
    ctx.var8.set("black")

    spin8 = tk.Spinbox(Lbf2, width=max(len(i) for i in (fontColorRange))+1, 
                       values=fontColorRange, textvariable=ctx.var8, state='readonly')#, textvariable=text_variable)  

    # tkvalidate.string_validate(spin8, values=fontColorRange)
      
    spin8.grid(row=0,column=1,sticky='W',padx=5,pady=4) 


    Lb23 = tk.Label(Lbf2, text="Legend: ")
    Lb23.grid(row=0, column=2, sticky='N')

    ctx.var9 = tk.StringVar(ctx.TAB2)
    ctx.var9.set("black")

    spin9 = tk.Spinbox(Lbf2, width=max(len(i) for i in (fontColorRange))+1, 
                       values=fontColorRange, textvariable=ctx.var9, state='readonly')#, textvariable=text_variable)  

    # tkvalidate.string_validate(spin8, values=fontColorRange)
      
    spin9.grid(row=0,column=3,sticky='W',padx=5,pady=4) 


    Lb24 = tk.Label(Lbf2, text="Directions: ")
    Lb24.grid(row=0, column=4, sticky='N')

    ctx.var10 = tk.StringVar(ctx.TAB2)
    ctx.var10.set("black")
    spin10 = tk.Spinbox(Lbf2, width=max(len(i) for i in (fontColorRange))+1, 
                        values=fontColorRange, textvariable=ctx.var10, state='readonly')#, textvariable=text_variable)  

    # tkvalidate.string_validate(spin8, values=fontColorRange)
      
    spin10.grid(row=0,column=5,sticky='W',padx=5,pady=4) 


    Lb25 = tk.Label(Lbf2, text="Percentage: ")
    Lb25.grid(row=0, column=6, sticky='N')

    ctx.var11 = tk.StringVar(ctx.TAB2)
    ctx.var11.set("black")

    spin11 = tk.Spinbox(Lbf2, width=max(len(i) for i in (fontColorRange))+1,
                        values=fontColorRange, textvariable=ctx.var11, state='readonly')#, textvariable=text_variable)  

    # tkvalidate.string_validate(spin8, values=fontColorRange)
      
    spin11.grid(row=0,column=7,sticky='W',padx=5,pady=4) 







    Lbf3 = tk.LabelFrame(ctx.TAB2, text="Plot Buttons:")
    Lbf3.grid(row=9, column=0, sticky='W',padx=50)




    button1 = tkinter.Button(Lbf3,
                                text="Plot",
                                width=10,
                                height=4,  command = lambda: depict(ctx))


    button1.grid(row=0,column=0,sticky='W',padx=12,pady=4)




    ##############shortcut key in Tab2





    ctx.TAB2.bind('<F5>', lambda event : func(ctx, event))


    ######################



    ctx.button2 = tkinter.Button(Lbf3,
                                text="Spring",
                                width=10,
                                height=4, bg='lawngreen',  command = lambda: depict_spring(ctx),
                                state="disabled")


    ctx.button2.grid(row=0,column=1,sticky='W',padx=12,pady=4)



    ctx.button3 = tkinter.Button(Lbf3,
                                text="Summer",
                                width=10,
                                height=4, bg='salmon',  command = lambda: depict_summer(ctx),
                                state="disabled")


    ctx.button3.grid(row=0,column=2,sticky='W',padx=12,pady=4)




    ctx.button4 = tkinter.Button(Lbf3,
                                text="Fall",
                                width=10,
                                height=4, bg='yellow',  command = lambda: depict_fall(ctx),
                                state="disabled")


    ctx.button4.grid(row=0,column=3,sticky='W',padx=11,pady=4)



    ctx.button5 = tkinter.Button(Lbf3,
                                text="Winter",
                                width=10,
                                height=4, bg='skyblue',  command = lambda: depict_winter(ctx),
                                state="disabled")


    ctx.button5.grid(row=0,column=4,sticky='W',padx=11,pady=4)






    button6=tkinter.Button(ctx.TAB2,text='Quit',width=10,
                                height=4,
                                command=lambda: close_window(ctx)  )

    button6.grid(row=10,column=0,sticky='W',padx=50,pady=4)






    menuBar = Menu(app1) # 1
    app1.config(menu=menuBar)
    # Now we add a menu to the bar and also assign a menu item to the menu.
    fileMenu = Menu(menuBar, tearoff=0) # 2


    fileMenu.add_command(label="New", command=lambda:NewCommand(ctx))
    fileMenu.add_separator()
    fileMenu.add_command(label="Exit", command=lambda: close_window(ctx)) # 3

    menuBar.add_cascade(label="File", menu=fileMenu)


    helpMenu = Menu(menuBar, tearoff=0) # 6
    helpMenu.add_command(label="About", command=About)
    menuBar.add_cascade(label="Help", menu=helpMenu)


    # style = ttk.Style(app1)
    # style.configure('TLabel', background='black', foreground='white')
    # style.configure('TFrame', background='lightblue')
    app1.resizable(0, 0)
    #app1.mainloop()

    app1.protocol("WM_DELETE_WINDOW", func=lambda: close_window(ctx))

    app1.mainloop()

'''for date in xlrd: asp = xlrd.xldate_as_tuple(sheet.cell(3,1).value,wb.datemode)

start of spring : 21 March (3, 21)

end of spring : 20 June (6, 20)

start of summer : 21 June (6, 21)

end of summer : 22 September (9, 22)f

start of fall : 23 September (9, 23)

end of fall : 22 December (12, 20)

start of winter : 23 December (12, 21)

end of winter : 22 March (3, 20)

'''




