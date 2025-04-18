
import tkinter as tk

from windroselab.app_context import AppContext

from windroselab.display import image_plotter

from windroselab.draw_class import draw



def close_window(ctx:AppContext):
    ctx.app1.quit()
    ctx.app1.destroy()


def depict_fall(ctx:AppContext):
    
    
    # image(wd, ws ,figname ='fig19', nd=8, ns=5, standard=True, color_number=0,
    #       title_font_size=30, angle_fontsize=10, dirction_fontsize=15,
    #       legend_fontsize=10, title1="WindRose",
    #       x1=1, y1=1.1, user_dpi=100, percent_angle=60,
    #       user_opening=0.6, figwidth=6, figheight=8,
    #       rectx = 1, recty=1.2, legx=0.5, legy=0.5,
    #       plot_length=20, image_length=5,
    #       title_font_color='black', angle_font_color='black',
    #       dirction_font_color='black', legend_font_color='black'
    #       )
    
    
    
    try:
        figname1 = 'Fall'
        nd1 = ctx.spinT1.get()
        ns1 = ctx.spinT2.get()
        standard1 = bool(ctx.CheckVarT1.get())
        ColorsN = ctx.var2.get()#color_number
        tiFS = ctx.var4.get()#title_font_size
        aFS = ctx.var7.get()#angle_fontsize
        dFS = ctx.var6.get()#dirction_fontsize
        lFS = ctx.var5.get()#legend_fontsize
        t1 = ctx.Ent20.get() #title1
        xt = float(ctx.Ent2.get())#x position of title
        yt = float(ctx.Ent3.get())#x position of title
        udpi = int(ctx.var1.get())#user_dpi
        pa = int(ctx.var3.get())#percent_angle
        uo = float(ctx.Ent7.get())#user_opening
        fgW = float(ctx.Ent8.get())#figwidth
        fgH = float(ctx.Ent9.get())#figheight
        # rtx = float(Ent10.get())#rectx
        # rty = float(Ent11.get())#recty
        xlm = float(ctx.Ent10.get())
        lwidth = float(ctx.Ent11.get())
        lgX = float(ctx.Ent4.get())#legx
        lgY = float(ctx.Ent5.get())#legy
        pL = float(ctx.Ent16.get())#plot_length
        iL = float(ctx.Ent17.get()) #image_length
        tFC = ctx.var8.get()#title_font_color
        aFC = ctx.var11.get()#angle_font_color
        dFC = ctx.var10.get()#dirction_font_color
        lFC = ctx.var9.get()#legend_font_color
        
        
        L, lgd1 = image_plotter(ctx, ctx.awd_fa, ctx.aws_fa, figname =figname1, nd=int(nd1), ns=int(ns1),
                        standard=standard1, color_number=int(ColorsN),
                        title_font_size=tiFS, angle_fontsize=aFS,
                        dirction_fontsize=dFS, legend_fontsize=lFS,
                        title1=t1, x1=xt, y1=yt, user_dpi=udpi,
                        percent_angle=pa, user_opening=uo, figwidth=fgW,
                        figheight=fgH, Xlim=xlm, Linewidth=lwidth, legx=lgX, legy=lgY,
                        plot_length=pL, image_length=iL, title_font_color=tFC,
                        angle_font_color=aFC, dirction_font_color=dFC,
                        legend_font_color=lFC)
        
        
            
            
        app = draw(ctx, L, lgd1)
        app.protocol("WM_DELETE_WINDOW", func=lambda: close_window(ctx))
        app.mainloop()
        
        
          
        
    except:
        
        tk.messagebox.showinfo("Warning", 
                            'One or more of your input values is/are not valid. \n'+
                            'Or your data is not valid.')
