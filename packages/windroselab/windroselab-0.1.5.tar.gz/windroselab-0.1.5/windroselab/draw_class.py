import tkinter

import tkinter as tk

from windroselab.app_context import AppContext

import matplotlib as mpl

from tkinter import filedialog as fd 



Pics_Formats = {'eps': 'Encapsulated Postscript',
 'jpg': 'Joint Photographic Experts Group',
 'jpeg': 'Joint Photographic Experts Group',
 'pdf': 'Portable Document Format',
 'pgf': 'PGF code for LaTeX',
 'png': 'Portable Network Graphics',
 'ps': 'Postscript',
 'raw': 'Raw RGBA bitmap',
 'rgba': 'Raw RGBA bitmap',
 'svg': 'Scalable Vector Graphics',
 'svgz': 'Scalable Vector Graphics',
 'tif': 'Tagged Image File Format',
 'tiff': 'Tagged Image File Format',
 #'bmp': 'Bitmap File Format'
 }

files = [('All Files', '*.*')]
    
for i in Pics_Formats:
    
    s = ( Pics_Formats[i], '*.' + i)
    
    files.append(s)






button_fontsize = 20


class draw( tk.Tk):

    def __init__(self, ctx:AppContext, f, lgd1, *args, **kwargs):
        
        tk.Tk.__init__(self, *args, **kwargs)

        tk.Tk.iconbitmap(self)#, default='clienticon.ico')
        
        
        tk.Tk.wm_title(self, "Graph Page!")

        self.ctx = ctx


        
        self.f = f
        
        self.lgd1 = lgd1
        
        
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand = True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
#    
            
        F = view

        frame = F(ctx, f, lgd1,container, self)
        

        self.frames[F] = frame
        
        self.geometry("800x700+0+0")

        frame.grid(row=0, column=0, sticky="nsew")
    

        self.show_frame(view)

    def show_frame(self, cont):

        frame = self.frames[cont]
        frame.tkraise()
        
    def close_frames(self):
        
        self.quit()
                        
        self.destroy()
            



class view( tk.Frame):

    def __init__(self, ctx:AppContext, f, lgd1, parent, controller):
        tk.Frame.__init__(self, parent)
        # self.geometry("500x500")
        # label = tk.Label(self, text="Graph Page!", font=LARGE_FONT)
        # label.pack(pady=1,padx=1)

#        button1 = ttk.Button(self, text="Back to Home",
#                            command=lambda: controller.show_frame(StartPage))
#        button1.pack()




        self.f = f

        self.ctx = ctx
        
        self.lgd1 = lgd1
        
        frame1 = tk.Frame(self, borderwidth=2)
        frame1.pack(side=tk.TOP)
        button2=tk.Button(frame1, text='Quit',
                          font=button_fontsize,
                          height = 1, 
                          width = 4,
                          command= lambda: controller.close_frames() )
        
#        button2.winfo_pixels(1000)
        
        button2.pack(side=tk.LEFT)
        

        udpi = int(self.ctx.var1.get())#user_dpi
        
        def save(): 
            
            file = fd.asksaveasfile(filetypes=files, 
        defaultextension='.png', title="Window-2") 
            
            if file:
                if file.name:
                    canvas.figure.savefig(file.name, bbox_extra_artists=(lgd1,), pad_inches=.5, dpi=udpi)
                    # canvas.print_figure(file.name, bbox_extra_artists=(lgd1,), bbox_inches='tight',pad_inches=.5, dpi=100)
                    
            
            
        
        button3=tk.Button(frame1, text='Save',
                          font=button_fontsize,
                          height = 1, 
                          width = 4,
                          command= save )
        
        button3.pack(side=tk.LEFT)

        FigureCanvasTkAgg = mpl.backends.backend_tkagg.FigureCanvasTkAgg
        NavigationToolbar2Tk = mpl.backends.backend_tkagg.NavigationToolbar2Tk

        

        canvas = FigureCanvasTkAgg(f, self)
        # canvas.resize(self, w = 14, h=9)
#        canvas.show()
        canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=0)

        toolbar = NavigationToolbar2Tk(canvas, frame1)
        toolbar.update()
        toolbar.pack(side="left", fill=tk.X, expand=True)
        
        canvas._tkcanvas.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)
        
        # print(toolbar.save_figure)
        
