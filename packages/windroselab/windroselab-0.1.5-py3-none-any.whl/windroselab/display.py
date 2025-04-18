



import numpy as np

from matplotlib import pyplot as plt
import matplotlib as mpl
import os


from windroselab.app_context import AppContext


def image_plotter(ctx:AppContext, wd, ws ,figname ='fig1', nd=8, ns=5, standard=True, color_number=0,
          title_font_size=30, angle_fontsize=10, dirction_fontsize=15,
          legend_fontsize=10, title1="WindRose",
          x1=1, y1=1.1, user_dpi=100, percent_angle=60,
          user_opening=0.6, figwidth=6, figheight=8,
          rectx = 1, Xlim=10, Linewidth=1,legx=0.5, legy=0.5,
          plot_length=20, image_length=5,
          title_font_color='black', angle_font_color='black',
          dirction_font_color='black', legend_font_color='black'
          ):
    
    
    
    
    # print(aa, (bb, cc))
    
    
    
    sizeOfLegend = legend_fontsize
   

    # nd = 8
    
    # ns = 5
    
    maxs = max(ws)
    
    speed_mean = (maxs - .5)/(ns - 1)
    
    speed_span = [0]
    
    speed_span1 = [0.5 + i*speed_mean for i in range(ns)]
    
    speed_span.extend(speed_span1)
    
    speed_span[-1] = speed_span[-1] + 0.01
    
    
    # standard = True
    
    standard_speed_span = [0, 0.5, 2.1, 3.6, 5.7, 8.8, 11.1, 1000]
    
    st = 0
    
    Calm = 1
    
    if standard:
            speed_span = standard_speed_span
            ns = 7
            st = 1
    
    direction_span = 360/nd
    
    
    ds = np.zeros((nd, ns))
    
    #m = 0
    
    
    
    for i in range(1, nd):
        
        for j in range(ns):
            k = 0
            for m in range(len(ws)):
            
                if (wd[m]>= direction_span*((2*i-1)/2) and wd[m]< direction_span*((2*i+1)/2)) and (ws[m]>=speed_span[j] and ws[m]< speed_span[j+1]):
                    
                    k += 1
                    
    #            m += 1
                
            ds[i, j] = k
    
    
    for j in range(ns):
        k = 0
        
        for m in range(len(ws)):
        
            if (wd[m]>= direction_span*((2*i+1)/2) or wd[m]< direction_span*(1/2)) and (ws[m]>=speed_span[j] and ws[m]< speed_span[j+1]):
                
                k += 1
                
    #            m += 1
            
        ds[0, j] = k
    
    
    
    rds = np.zeros((nd, ns+1))
    
    for i in range(nd):
        
        for j in range(ns):
            
            rds[i, j] = 100*ds[i, j]/len(ws)
            
        rds[i, j+1] = np.sum(rds[i, 0:j+1])
    
    
    
    
    
    maxrds = max(rds[:, -1])
    
    
    maxrds_mean = np.ceil(maxrds/5)
    
    r = [i*maxrds_mean for i in range(1,6)]
    
    
    
    
    
    new_rds = rds[:, 0:-1]
        
    total_calm = np.sum(new_rds[:,0])
    
    
    constant = 1000
    
    rr = r.copy()
    
    rrr = r.copy()
    
    
    for i in range(len(rrr)):
        
        rrr[i] = constant * rr[i]/rr[0]
        
    
    r = rrr.copy()
    
    
    
    new_rrds = new_rds.copy()
    
    new_rrrds = new_rds.copy()
    
    
    for i in range((np.shape(new_rds)[0])):
        
        for j in range((np.shape(new_rds)[1])):
            
            new_rrrds[i, j] = constant * new_rds[i, j]/rr[0]
    
    
    new_rds = new_rrrds
    
    
    
    ####
    
    
    
    
    
    
    
    # lw = 1
    
    color_strings = [ 'red', 'orange', 'yellow', 'green', 'cyan', 'blue', \
                     'brown', 'indigo', 'magenta', 'purple', 'black', \
                         'aquamarine', 'navy','olive', 'teal', 'violet',\
                             'tan', 'gold', 'lime', 'slateblue']
    
    
    colors = color_strings[color_number:]
    
    colors.extend(color_strings[0:color_number])
    
    
    vR = ctx.varR.get()
    
    if vR < 3:
        aa = 0
    else:
        aa = 1
        
        plot_length, image_length = image_length, plot_length
        
    bb = 1 - aa   
    
    cc = 1- (vR % 2)
    
     
    
    
    fig3 = plt.figure(figsize=(figwidth, figheight))#constrained_layout=True)
    gs = fig3.add_gridspec(2, 2, height_ratios=[plot_length, image_length], 
                           width_ratios=[plot_length, image_length])
    ax = fig3.add_subplot(gs[aa, :])
    
    
    
    
    
    adad = Xlim
    
    ax.set(xlim=(-(r[-1]+adad), (r[-1]+adad)), ylim = (-(r[-1]+adad), (r[-1]+adad)))
    
    plt.axis('off')
    
    
    
    
    for i in range(4):
        
    #    plt.axis('off')
        
        draw_circle = plt.Circle((0, 0), r[i], fill=False, color='gray', linewidth=Linewidth, linestyle='-')
        
        ax.set_aspect(1)
        ax.add_artist(draw_circle)
    
    
    draw_circle = plt.Circle((0, 0), r[-1], fill=False, color='black', linewidth=Linewidth, linestyle='-')
        
    ax.set_aspect(1)
    ax.add_artist(draw_circle)
    
    
    
    
    pi = np.pi
    
    
    x = lambda r, phi : r * np.cos(phi)
    
    y = lambda r, phi : r * np.sin(phi)
    
    
    
    # percent_angle = 60
    
    percent_angle_rad = percent_angle * pi / 180
    
    
    for i in range(len(r)):
        
        ax.text(x(r[i], percent_angle_rad), y(r[i], percent_angle_rad), str(int(rr[i]))+'%', fontsize=angle_fontsize, color=angle_font_color)
    
    
    
    x_values = np.array([0, 0, r[-1], -r[-1], x(r[-1], pi/4), x(r[-1], 5*pi/4), x(r[-1], 3*pi/4), x(r[-1], 7*pi/4)])
    
    y_values = np.array([r[-1], -r[-1], 0, 0, y(r[-1], pi/4), y(r[-1], 5*pi/4), y(r[-1], 3*pi/4), y(r[-1], 7*pi/4)])
    
    
    for i in range(4):
        
        draw_line = plt.plot(x_values[2*i: 2*i+2], y_values[2*i: 2*i+2], color ='gray', linewidth=Linewidth)
        
        ax.add_artist(draw_line[0])
    
    
    
    x_texts = np.array([0, 0, r[-1]+r[0]/2, -(r[-1]+r[0]), x(r[-1]+r[0]/2, pi/4), x(r[-1]+1.5*r[0], 5*pi/4), x(r[-1]+r[0], 3*pi/4), x(r[-1]+r[0]/2, 7*pi/4)])

    y_texts = np.array([r[-1]+r[0]/2, -(r[-1]+2*r[0]/3), 0, 0, y(r[-1]+r[0]/2, pi/4), y(r[-1]+1.5*r[0], 5*pi/4), y(r[-1]+r[0], 3*pi/4), y(r[-1]+r[0]/2, 7*pi/4)])

    texts = ['N', 'S', 'E', 'W', 'N-E', 'S-W', 'N-W', 'S-E']
    
    
    for i in range(len(texts)):
        
        ax.text(x_texts[i], y_texts[i], texts[i], fontsize=dirction_fontsize, color=dirction_font_color)#, rotation=135)
    
    
    
    
    
    
    opening = user_opening+pi/40
    
    theta = pi/2 #2*pi/nd
    
    #beta = pi/40 
    
    alpha = opening * (2*pi/nd)/2
    
    
    
    polygon = mpl.patches.Polygon
    
    Polygon = mpl.patches.Polygon
    
    ply = np.array([[polygon]*(ns-0)]*nd)
    
    
    
    for i in range(nd):
        
        k = 0
        
        r0 = new_rds[i, st]
        
        pts = np.array([ [x(0, 0), y(0, 0)], [x(r0, theta-alpha), y(r0, theta-alpha)],  [x(r0, theta+alpha), y(r0, theta+alpha)]])
    
        ply[i, st] = Polygon(pts, closed=True, color=colors[k], linewidth=.1)
    
        ax.add_artist(ply[i, st])
        
    #    del p
        
        for j in range(st, ns-1):
            
            
            
            r1 = r0 + new_rds[i, j+1]
            
            k += 1
            
            pts = np.array([ [x(r0, theta-alpha), y(r0, theta-alpha)], [x(r0, theta+alpha), y(r0, theta+alpha)], [x(r1, theta+alpha), y(r1, theta+alpha)], [x(r1, theta-alpha), y(r1, theta-alpha)]])
    
            ply[i, j+1] = Polygon(pts, closed=True, color=colors[k], linewidth=.1)
    
            ax.add_artist(ply[i, j+1])
            
    #        del p
            
            r0 = r1
            
        theta -= 2*pi/nd
        
    
    
    Labels = []
    
    if st != 1:
        Labels = ['Calm']
        
        Calm = 0
    
    for i in range(1, len(speed_span) - 1 ):
        
        str1 = str(np.round(speed_span[i], 1)) + '--' + str(np.round(speed_span[i+1], 1))
        
        
        
        Labels.append(str1)
        
    if standard:
            
        Labels = Labels[:-1]
        
        Labels.append('>= 11.1')
        
    
    ply1 = ply[0, Calm:]
    
    
    
    # reshaped_text = arabic_reshaper.reshape(title1)    # correct its shape
    # bidi_text = get_display(reshaped_text) 
    
    plt.title(title1,   x=x1, y=y1, fontsize=title_font_size, fontname='Times New Roman',
              color=title_font_color);
    
    
    ##@@@@%%%%%%%%%%%%%%%%%%%%%%%%%%
    
    
    
    try:
    
        im = plt.imread(get_sample_data(image_path))# + '\\Irimo.jpg'))
        ax2 = fig3.add_subplot(gs[bb, cc])
        
        # ax2 = plt.subplot(gs[1, 0])
        img = ax2.imshow(im)
        ax2.axis('off')
        
    except:
        pass
    
    
    
    font = mpl.font_manager.FontProperties(family='Times New Roman',
                                       weight='bold',
                                       style='normal', size=sizeOfLegend)
    
    lgd1 = plt.legend(ply1, Labels, bbox_to_anchor=(legx, legy),##(0,0) = right-bottom
               bbox_transform=plt.gcf().transFigure, prop=font)
    # lgd1.set_color("red")
    
    
    lgd1_title = 'Wind Speeds \n    (m/s)'
    
    if st == 1:
        
        lgd1_title += '\n\nCalms: ' + str(np.round(total_calm, 2)) + '%'
    
    lgd1.set_title(lgd1_title, prop={'size':legend_fontsize}) 
    
    # print((fig3).top, 344)
    plt.setp(lgd1.get_texts(), color=legend_font_color)
    lgd1._legend_title_box._text.set_color(legend_font_color)
    
    
    
    
    # plt.tight_layout(rect=[0, 0, rectx, recty])#, h_pad=-4)
    
    
    btm = float(ctx.Ent22.get())
    
    lft = float(ctx.Ent23.get())
    
    rgt = float(ctx.Ent24.get())
    
    tp = float(ctx.Ent25.get())
    
    wspc = float(ctx.Ent26.get())
    
    hspc = float(ctx.Ent27.get())
    
    if rgt == 0:
        rgt = None
        
    if tp == 0:
        tp = None
    
    plt.subplots_adjust(left=lft, bottom=btm, right=rgt, top=tp, wspace=wspc, hspace=hspc)
    
    L = ax.figure
    
     


    Number = 10000
     
    
    output = os.getcwd() + '\\' + figname + str(Number) + '.jpg'
    
    while os.path.isfile(output):
       Number +=  1
       output = os.getcwd() + '\\' + figname + str(Number) + '.jpg'
    

    # mpl.rcParams["figure.figsize"] = [5, 5]
    
    if bool(ctx.CheckVarT01.get()):
        L.savefig(output,   dpi=user_dpi)
    #, bbox_extra_artists=(lgd1,), bbox_inches='tight' , pad_inches=u_pad_inches,
    
    
    
    
    
    return(L, lgd1)
    
