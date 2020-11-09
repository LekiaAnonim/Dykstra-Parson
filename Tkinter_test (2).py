#!/usr/bin/env python
# coding: utf-8

# In[4]:


from tkinter import*
from tkinter import filedialog
from tkinter import ttk
#from tkinter import askopenfilename
import pandas as pd
from tkinter.messagebox import*
from tkinter.filedialog import askopenfilename
import csv
import math
from decimal import*
from tkinter import*

getcontext().prec = 3

root = Tk()
root.iconbitmap('STRATV.ico')


style = ttk.Style()
style.theme_use('clam')

# list the options of the style
# (Argument should be an element of TScrollbar, eg. "thumb", "trough", ...)
print(style.element_options("Horizontal.TScrollbar.thumb"))

# configure the style
style.configure("Horizontal.TScrollbar", gripcount=0,
                background="Green", darkcolor="DarkGreen", lightcolor="LightGreen",
                troughcolor="gray", bordercolor="blue", arrowcolor="white")

#Create a main frame
main_frame = Frame(root,bg='#d6ebfb')
main_frame.pack(fill = BOTH, expand =1)

#Create a canvas

my_canvas = Canvas(main_frame,bg='#d6ebfb')
my_canvas.pack(side = LEFT, fill=BOTH, expand = 1)

#Add a scrollbar to the canvas
my_scrollbar = ttk.Scrollbar(main_frame, orient = VERTICAL, command = my_canvas.yview)
my_scrollbar.pack(side=RIGHT, fill = Y)
my_scrollbarx = ttk.Scrollbar(main_frame, orient=HORIZONTAL, command=my_canvas.xview)
my_scrollbarx.pack(side=BOTTOM, fill = X)
#Configure the canvas
my_canvas.configure(xscrollcommand=my_scrollbarx.set, yscrollcommand = my_scrollbar.set)
my_canvas.bind('<Configure>', lambda e: my_canvas.configure(scrollregion = my_canvas.bbox('all')))

#Create ANOTHER frame inside the canvas
second_frame = Frame(my_canvas, bg = '#c8f1f7')

#Add that frame to a windows in the canvas
my_canvas.create_window((0,0), window = second_frame, anchor = 'nw')







root.title('STRAT-V')
#frame_1 = LabelFrame(second_frame,text ='Input Data', bd = 2,bg = '#ebffd4', relief = GROOVE).place(height =750, width =6000)
#frame_2 = LabelFrame(second_frame,text = 'Calculate',bd = 2,bg ='#c8f1f7', relief = RAISED).place(height =750, width =500)


def donothing():
      x = 0

def quit():
       root.destroy 
        
        
def save():
    contents = Label.get(1.0,"end-1c") #store the contents of the text widget in a str
    try:                                       #this try/except block checks to
        with open(f, 'w') as outputFile:  #see if the str containing the output
            outputFile.write(contents)         #file (self.f) exists, and we can write to it,
    except AttributeError:                     #and if it doesn't,
        save_as()                         #call save_as

def save_as():
    contents = Label.get(1.0,"end-1c")
    f = tkFileDialog.asksaveasfilename(   #this will make the file path a string
        defaultextension=".z",                 #so it's easier to check if it exists
        filetypes = (("textfile", "*.txt"),    #in the save function
                     ("All files", "*.")))
    with open(f, 'w') as outputFile:
        outputFile.write(contents)        
        
        
        
        
#===========================================================================================================================
def Load_File():
    global label_file
    import_file=Tk()
    import_file.geometry('500x500')
    import_file.pack_propagate(False)
    import_file.resizable(0,0)

    #frame for Treeview
    frame3=LabelFrame(import_file,text='Data File')
    frame3.place(height=350, width=500)

    #Frame for open filedialog
    file_frame=LabelFrame(import_file, text='Open File')
    file_frame.place(height=100, width=500, rely=0.65, relx=0)

    #Buttons
    button1=Button(file_frame, text = 'Browse A File',command=lambda:file_dialog())
    button1.place(rely=0.65, relx=0.8)

    button2= Button(file_frame, text = 'Load Permeability-Porosity Data', command=lambda: Load_Permeability_Porosity_Data())
    button2.place(rely=0.65,relx=0.4)
    button3=Button(file_frame, text = 'Load Relative Permeability Data', command=lambda: Load_Relative_Permeability_Data())
    button3.place(rely=0.65, relx=0)

    label_file = ttk.Label(file_frame, text = 'No File Selected')
    label_file.place(rely=0,relx=0)

    #Treeview Widget
    tv1=ttk.Treeview(frame3)
    tv1.place(relheight=1, relwidth=1)

    treescrolly = Scrollbar(frame3, orient='vertical',command=tv1.yview)
    treescrollx = Scrollbar(frame3, orient='horizontal',command=tv1.xview)
    tv1.configure(xscrollcommand=treescrollx.set, yscrollcommand=treescrolly.set)
    treescrollx.pack(side='bottom', fill='x')
    treescrolly.pack(side='right', fill='y')

    def file_dialog():
        filename= filedialog.askopenfilename(initialdir="/", title = "Select A File", filetype=(("csvfiles","*.csv"),("All Files", "*.*")))
        label_file["text"]=filename

    def Load_Permeability_Porosity_Data():
        file_path=label_file['text']
        try:
            excel_filename=r"{}".format(file_path)
            bed_data=pd.read_csv(excel_filename)
        except ValueError:
            messagebox.showerror("Information","The file you have chosen is invalid")
            return None
        except FileNotFoundError:
            messagebox.showerror("Information", f"No such file as {file_path}")
            return None
        
        clear_data()
        tv1["column"]=list(bed_data.columns)
        tv1['show']='headings'
        for column in tv1['columns']:
            tv1.heading(column,text=column)
        bed_data_rows = bed_data.to_numpy().tolist()
        for row in bed_data_rows:
            tv1.insert("","end", values=row)
            
    def Load_Relative_Permeability_Data():
        file_path=label_file['text']
        try:
            excel_filename=r"{}".format(file_path)
            RPERM_data=pd.read_csv(excel_filename)
        except ValueError:
            messagebox.showerror("Information","The file you have chosen is invalid")
            return None
        except FileNotFoundError:
            messagebox.showerror("Information", f"No such file as {file_path}")
            return None

        clear_data()
        tv1["column"]=list(RPERM_data.columns)
        tv1['show']='headings'
        for column in tv1['columns']:
            tv1.heading(column,text=column)
        RPERM_data_rows = RPERM_data.to_numpy().tolist()
        for row in RPERM_data_rows:
            tv1.insert("","end", values=row)
        return None
    def clear_data():
        tv1.delete(*tv1.get_children())

    import_file.mainloop()
#===========================================================================================================================
    
def openfile():

    filename = askopenfilename(parent=root)
    f = open(filename)
    f.read()

#===========================================================================================================================    
    
import sviewgui.sview as sv
import pandas as pd
def results_and_graph_gui():
    sv.buildGUI(All_tables)

#============================================================================================================================
    
def front_location_plots_gui():
    get_ipython().run_line_magic('matplotlib', '')
    import matplotlib.pyplot as plt
    for i in Layer_table['LAYERS']:
        plt.figure(figsize = (4,3), dpi = 100)
        Flood_front_location_Time = plt.plot(Time_days_table, Front_Location_list_DataTable[i-1], label = 'Layer'+str(i))
        #plt.setp(Flood_front_location_Time, animated=False, color = 'b', label='Coverage Vs WOR',linestyle = '-', linewidth = 1, marker = 'o', markersize = 2)
        plt.title('Flood front location versus Time', fontdict ={'fontname': 'Arial', 'fontsize': 20})
        plt.xlabel(' Time (days)')
        plt.ylabel('Flood front location')
        plt.legend()
        plt.show()
        plt.savefig('Flood_front_location.pdf', dpi = 300)
        plt.savefig('Flood_front_location.png', dpi = 300)

    plt.ion()

#========================================================================================================================= 

menubar = Menu(root)
filemenu = Menu(menubar, tearoff=0)
filemenu.add_command(label="New", command=donothing)
filemenu.add_command(label="Open", command=openfile)
filemenu.add_command(label="Load", command=Load_File)
filemenu.add_command(label="Save", command=save)
filemenu.add_command(label="Save as...", command=save_as)

filemenu.add_separator()

filemenu.add_command(label="Exit", command=quit)
menubar.add_cascade(label="File", menu=filemenu)
editmenu = Menu(menubar, tearoff=0)
editmenu.add_command(label="Undo", command=donothing)

editmenu.add_separator()

editmenu.add_command(label="Cut", command=donothing)
editmenu.add_command(label="Copy", command=donothing)
editmenu.add_command(label="Paste", command=donothing)
editmenu.add_command(label="Delete", command=donothing)
editmenu.add_command(label="Select All", command=donothing)
menubar.add_cascade(label="Edit", menu=editmenu)

helpmenu = Menu(menubar, tearoff=0)
helpmenu.add_command(label="Help Index", command=donothing)
helpmenu.add_command(label="About...", command=donothing)
menubar.add_cascade(label="Help", menu=helpmenu)

# create the Output menu
outputmenu = Menu(menubar, tearoff=0)
outputmenu.add_command(label="Tabular results and graphs",command = results_and_graph_gui)
outputmenu.add_command(label="Flood front location plot", command = front_location_plots_gui)
#added "file" to our menu
menubar.add_cascade(label="Output", menu=outputmenu)

#Create a load menu
loadmenu = Menu(menubar, tearoff=0)
loadmenu.add_command(label="Load Data",command =  Load_File)

#added "file" to our menu
menubar.add_cascade(label="Load", menu=loadmenu)

root.config(menu=menubar)


#===============================================================================================================================        

    
    # Creating Heading
Input_header = Label(second_frame, text = ('Enter Input Variables'),fg = '#b22222', bg = '#d6ebfb').grid(row =0, column = 0, columnspan = 3, sticky = W+E+N+S)

#===========================================================================================================================

def enter_inputs():
    global Length_of_bed_ft
    global width_of_bed_ft
    global average_porosity
    global VISO
    global VISW
    global OFVF
    global WFVF
    global SWI
    global SGI
    global SOI
    global SOR
    global Constant_injection_rate
    global Inj_Pressure_differential
    global Residual_gas_saturation_unswept_area
    global Residual_gas_saturation_swept_area
    global Residual_gas_saturation
    
    fields = ('Length_of_bed_ft', 'width_of_bed_ft', 'average_porosity','VISO', 'VISW','OFVF','WFVF','SWI', 'SGI','SOI','SOR','Constant_injection_rate',
    'Inj_Pressure_differential','Residual_gas_saturation_unswept_area','Residual_gas_saturation_swept_area','Residual_gas_saturation')


    
    def residual_gas_saturation(entries):

        global RGSU
        global RGSS
        global RGS
        # period rate:
        RGSU = float(entries['Residual_gas_saturation_unswept_area'].get())

        # principal loan:
        RGSS =  float(entries['Residual_gas_saturation_swept_area'].get())
        Residual_gas_saturation = float(entries['Residual_gas_saturation'].get())

        RGS = RGSU+RGSS
        RGS = ("%8.2f" % RGS).strip()
        entries['Residual_gas_saturation'].delete(0, END)
        entries['Residual_gas_saturation'].insert(0, RGS)
       # print("Monthly Payment: %f" % float(monthly))


    def makeform(inputs, fields):
        global entries
        entries = {}
        for field in fields:
           # print(field)
            row = Frame(inputs)
            lab = Label(row, width=22, text=field+": ", anchor='w')
            ent = Entry(row)
            ent.insert(0, "0")
            row.pack(side=TOP, 
                     fill=X, 
                     padx=5, 
                     pady=5)
            lab.pack(side=LEFT)
            ent.pack(side=RIGHT, 
                     expand=YES,padx = 50, 
                     fill=X)
            entries[field] = ent
        return entries
    def quit():
        inputs.quit
    if __name__ == '__main__':
        inputs = Tk()
        ents = makeform(inputs, fields)
        b1 = Button(inputs, text='Residual gas saturation',
               command=(lambda e=ents:residual_gas_saturation(e)))
        b1.pack(side=LEFT, padx=5, pady=5)
        b3 = Button(inputs, text='Quit', command=quit)
        b3.pack(side=LEFT, padx=5, pady=5)
        inputs.mainloop() 
Enter_input_button = Button(second_frame, text = 'Enter input data',justify = LEFT,relief= RAISED, command = enter_inputs).grid(row=2,column =0,padx=5,pady=10)    





#==========================================================================================================================
Label(second_frame, text='Calculate',bg = '#2196f3',justify = CENTER,relief= FLAT).grid(row=0, column=4, columnspan = 8,padx = 40,pady=10, sticky = W+E+N+S)

bed_data = pd.read_csv('Permeability_Porosity_distribution_data.csv')

#===========================================================================================================================      


# ARRANGING THE DATA IN ORDER OF DECREASING PERMEABILITY.
bed_data_sort = bed_data.sort_values(by='PERMEABILITY', ascending=False)


#==========================================================================================================================


#Importing the Relative permeability Data
import pandas as pd
RPERM_data = pd.read_csv('Oil_Water_Relative_Permeability_data.csv')

#==========================================================================================================================


# Extracting input variables from data table.
import numpy as np
PORO = np.array(bed_data_sort['POROSITY'])
permeability_array = np.array(bed_data_sort['PERMEABILITY'])
h = np.array(bed_data_sort['THICKNESS'])
SW = np.array(RPERM_data['SW'])
KRW = np.array(RPERM_data['KRW'])
KRO = np.array(RPERM_data['KRO'])


#==========================================================================================================================


#This code calculates the permeability ratio, ki/kn
List_of_permeability_ratio = []
for permeability_index in range(len(permeability_array)):
    List_of_permeability_ratio_subset = [][:-permeability_index]
    for index,permeability in enumerate(permeability_array):
        if permeability_index <= index:
            permaebility_ratio = permeability/permeability_array[permeability_index]
            List_of_permeability_ratio_subset.append(permaebility_ratio)
    List_of_permeability_ratio.append(List_of_permeability_ratio_subset)

List_of_permeability_ratio_DataTable = pd.DataFrame(List_of_permeability_ratio).transpose()


#==========================================================================================================================

def average_porosity():
    #global Average_porosity
    Average_porosity = '%.3f' % np.mean(bed_data_sort.POROSITY)
    Label(second_frame, text= str(Average_porosity),justify = LEFT, relief = SUNKEN).grid(row = 3, column = 6,padx = 40,pady=5, sticky =W)
Button(second_frame,text='Average Porosity',bg = '#337ab7',fg = 'white', command=average_porosity).grid(row=2,column=6,padx = 40,pady=10, sticky =W)

# RELATIVE PERMEABILITY OF WATER AT 1-SOR.
def relative_perm_1_SOR(entries):
    global SOR
    SOR = float(entries['SOR'].get())
    KRW_1_SOR = '%.3f' % RPERM_data.loc[RPERM_data.SW == 1-SOR,'KRW'].values[0]
    Label(second_frame, text=  str(KRW_1_SOR),justify = LEFT, relief = SUNKEN).grid(row = 3, column = 7,padx = 40,pady=5, sticky =W)
Button(second_frame,text='Relative Permeability at 1-SOR',bg = '#337ab7',fg = 'white',command=(lambda: relative_perm_1_SOR(entries))).grid(row=2,column=7,padx = 40,pady=10, sticky =W)    



# RELATIVE PERMEABILITY OF OIL AT INITIAL WATER SATURATION.
def relative_perm_SWI(entries):
    global SWI
    SWI = float(entries['SWI'].get())
    KRO_SWI = '%.3f' % RPERM_data.loc[RPERM_data.SW == SWI,'KRO'].values[0]
    Label(second_frame, text= str(KRO_SWI),justify = LEFT, relief = SUNKEN).grid(row = 5, column = 6,padx = 40,pady=5, sticky =W)
Button(second_frame,text='Relative Permeability at Initial Water Saturation',bg = '#337ab7',fg = 'white',command=(lambda: relative_perm_SWI(entries))).grid(row=4,column=6,padx = 40,pady=10, sticky =W)

#CALCULATING THE WATER MOBILITY
def water_mobilty(entries):
    global VISW
    VISW = float(entries['VISW'].get())
    Water_Mobility =  permeability_array*KRW_1_SOR/VISW
    Label(second_frame, text=str(Water_Mobility),justify = LEFT, relief = SUNKEN).grid(row = 11, column = 6,padx = 40,pady=5, sticky =W)
Button(second_frame,text='Water Mobility',bg = '#337ab7',fg = 'white',command=(lambda: water_mobilty(entries))).grid(row=10,column=6,padx = 40,pady=10, sticky =W)


#CALCULATING THE WATER MOBILITY
def oil_mobilty(entries):
    global VISO
    VISO = float(entries['VISO'].get())
    Oil_Mobility =  permeability_array*KRO_SWI/VISO
    Label(second_frame, text=str(Oil_Mobility),justify = LEFT, relief = SUNKEN).grid(row = 11, column = 7,padx = 40,pady=5, sticky =W)
Button(second_frame,text='Oil Mobility',bg = '#337ab7',fg = 'white',command=(lambda: oil_mobilty(entries))).grid(row=10,column=7,padx = 40,pady=10, sticky =W)




# CALCULATING THE MOBILITY RATIO, M.
def mobility_ratio(entries):
    global SWI
    global VISW
    global VISO
    global SOR
    SWI = float(entries['SWI'].get())
    VISW = float(entries['VISW'].get())
    VISO = float(entries['VISO'].get())
    SOR = float(entries['SOR'].get())
    KRW_1_SOR = RPERM_data.loc[RPERM_data.SW == 1-SOR,'KRW'].values[0]
    KRO_SWI = RPERM_data.loc[RPERM_data.SW == SWI,'KRO'].values[0]
    Mobility_Ratio =  KRW_1_SOR*VISO/(KRO_SWI*VISW)
    Label(second_frame, text= str(Mobility_Ratio),justify = LEFT, relief = SUNKEN).grid(row = 7, column = 7,padx = 40,pady=5, sticky =W)
Button(second_frame,text='Mobility Ratio',bg = '#337ab7',fg = 'white',command=(lambda: mobility_ratio(entries))).grid(row=6,column=7,padx = 40,pady=10, sticky =W)


#CALCULATING THE AREAL SWEEP EFFICIENCY AT BREAKTHROUGH
def areal_sweep_efficiency_at_breakthrough(entries):
    global SWI
    global VISW
    global VISO
    global SOR
    SWI = float(entries['SWI'].get())
    VISW = float(entries['VISW'].get())
    VISO = float(entries['VISO'].get())
    SOR = float(entries['SOR'].get())
    KRW_1_SOR = RPERM_data.loc[RPERM_data.SW == 1-SOR,'KRW'].values[0]
    KRO_SWI = RPERM_data.loc[RPERM_data.SW == SWI,'KRO'].values[0]
    Mobility_Ratio = KRW_1_SOR*VISO/(KRO_SWI*VISW)
    Areal_sweep_efficiency_at_breakthrough =  0.54602036+(0.03170817/Mobility_Ratio)+(0.30222997/math.exp(Mobility_Ratio)-0.0050969*Mobility_Ratio)
    Label(second_frame, text= str(Areal_sweep_efficiency_at_breakthrough),justify = LEFT,relief = SUNKEN).grid(row = 9, column = 6,padx = 40,pady=5, sticky =W)
Button(second_frame,text='Areal sweep efficiency at breakthrough',bg = '#337ab7',fg = 'white',command=(lambda: areal_sweep_efficiency_at_breakthrough(entries))).grid(row=8,column=6,padx = 40,pady=10, sticky =W)


#CALCULATING AREA OF RESERVOIR IN ACRES.
def area_acres(entries):
    global Length_of_bed_ft
    global width_of_bed_ft
    Length_of_bed_ft = float(entries['Length_of_bed_ft'].get())
    width_of_bed_ft = float(entries['width_of_bed_ft'].get())
    Area_acres =  Length_of_bed_ft*width_of_bed_ft/43560
    Label(second_frame, text= str(Area_acres)+ ' acres',justify = LEFT,relief = SUNKEN).grid(row = 9, column = 7,padx = 40,pady=5, sticky =W)
Button(second_frame,text='Area of the reservoir bed',bg = '#337ab7',fg = 'white',command=(lambda: area_acres(entries))).grid(row=8,column=7,padx = 40,pady=10, sticky =W)


#CALCULATING THE GROSS ROCK VOLUME.
def gross_rock_volume(entries):
    global Length_of_bed_ft
    global width_of_bed_ft
    Length_of_bed_ft = float(entries['Length_of_bed_ft'].get())
    width_of_bed_ft = float(entries['width_of_bed_ft'].get())
    Area_acres = Length_of_bed_ft*width_of_bed_ft/43560
    Gross_rock_volume_acre_ft =  Area_acres*bed_data_sort.THICKNESS.sum()
    Label(second_frame, text= str(Gross_rock_volume_acre_ft)+ ' acres-ft',justify = LEFT,relief = SUNKEN).grid(row = 5, column = 7,padx = 40,pady=5, sticky =W)
Button(second_frame,text='Gross rock volume',bg = '#337ab7',fg = 'white',command=(lambda: gross_rock_volume(entries))).grid(row=4,column=7,padx = 40,pady=10, sticky =W)



#CALCULATING DISPLACEMENT EFFICIENCY
def displacement_efficiency(entries):
    global SGI
    global SWI
    global SOR
    SWI = float(entries['SWI'].get())
    SOR = float(entries['SOR'].get())
    SGI = float(entries['SGI'].get())
    Displacement_efficiency =  (1-SWI-SGI-SOR)/(1-SWI-SGI)
    Label(second_frame, text= str(Displacement_efficiency),justify = LEFT,relief = SUNKEN).grid(row = 7, column = 6,padx = 40,pady=5, sticky =W)
Button(second_frame,text='Displacement efficiency',bg = '#337ab7',fg = 'white',command=(lambda: displacement_efficiency(entries))).grid(row=6,column=6,padx = 40,pady=10, sticky =W)


#CALCULATING THE AREAL SWEEP EFFICIENCY
def areal_sweep_efficiency(entries):
    global SGI
    global SWI
    global SOR
    global SGI
    global Constant_injection_rate 
    global Inj_Pressure_differential
    SWI = float(entries['SWI'].get())
    SOR = float(entries['SOR'].get())
    SGI = float(entries['SGI'].get())
    VISW = float(entries['VISW'].get())
    VISO = float(entries['VISO'].get())
    Constant_injection_rate = float(entries['Constant_injection_rate'].get())
    Inj_Pressure_differential = float(entries['Inj_Pressure_differential'].get())
    KRW_1_SOR = RPERM_data.loc[RPERM_data.SW == 1-SOR,'KRW'].values[0]
    KRO_SWI = RPERM_data.loc[RPERM_data.SW == SWI,'KRO'].values[0]
    Mobility_Ratio = KRW_1_SOR*VISO/(KRO_SWI*VISW)
    Areal_sweep_efficiency_at_breakthrough = 0.54602036+(0.03170817/Mobility_Ratio)+(0.30222997/math.exp(Mobility_Ratio)-0.0050969*Mobility_Ratio)
    Displacement_efficiency = (1-SWI-SGI-SOR)/(1-SWI-SGI)
    Areal_sweep_efficiency =  Areal_sweep_efficiency_at_breakthrough+0.2749*np.log((1/Displacement_efficiency))
    Label(second_frame, text= str(Areal_sweep_efficiency),justify = LEFT,relief = SUNKEN).grid(row = 13, column = 6,padx = 40,pady=10, sticky =W)
Button(second_frame,text='Areal sweep efficiency',bg = '#337ab7',fg = 'white',command=(lambda: areal_sweep_efficiency(entries))).grid(row=12,column=6,padx = 40,pady=10, sticky =W)


#============================================================================================================================================================



# EXTRACTING THE SORTED LAYER COLUMN
Layer_column = bed_data_sort['LAYER'].to_numpy()
Layer_table =  pd.DataFrame(Layer_column, columns = ['LAYERS'])


#This code calculates the list of waterflood front location as each layer breaksthrough




KRW_1_SOR = RPERM_data.loc[RPERM_data.SW == 1-SOR,'KRW'].values[0]
KRO_SWI = RPERM_data.loc[RPERM_data.SW == SWI,'KRO'].values[0]
Mobility_Ratio = KRW_1_SOR*VISO/(KRO_SWI*VISW)
Areal_sweep_efficiency_at_breakthrough = 0.54602036+(0.03170817/Mobility_Ratio)+(0.30222997/math.exp(Mobility_Ratio)-0.0050969*Mobility_Ratio)
Displacement_efficiency = (1-SWI-SGI-SOR)/(1-SWI-SGI)
Areal_sweep_efficiency =  Areal_sweep_efficiency_at_breakthrough+0.2749*np.log((1/Displacement_efficiency))
Area_acres = Length_of_bed_ft*width_of_bed_ft/43560
Gross_rock_volume_acre_ft =  Area_acres*bed_data_sort.THICKNESS.sum()

Front_Location_list = []
for permeability_index1 in range(len(permeability_array)):
    #Front_Location_list = []
    Front_Location = (Mobility_Ratio - np.sqrt(Mobility_Ratio**2+List_of_permeability_ratio_DataTable[permeability_index1]*(1-Mobility_Ratio**2)))/(Mobility_Ratio-1)
    Front_Location_list.append(Front_Location)

#This code generates table of flood front location as the layers breakthrough
Front_Location_list_DataTable = pd.DataFrame(Front_Location_list).transpose().rename(columns={0:'FLOOD FRONT LOCATION OF EACH BED'})

#==========================================================================================================================


# CALCULATING THE OIL FLOW RATE IN EACH BED AS EACH BED BREAKS THROUGH

Water_Mobility = permeability_array*KRW_1_SOR/VISW
Water_Flowrate_per_bed = (width_of_bed_ft*bed_data_sort['THICKNESS']*Inj_Pressure_differential/Length_of_bed_ft)*Water_Mobility
    
Water_Flowrate_per_bed_table = pd.DataFrame(Water_Flowrate_per_bed).rename(columns={'THICKNESS':'INJECTED WATER FLOWRATE(STB/D)'})
Water_Flowrate_per_bed_table


#===========================================================================================================================


# CALCULATING THE OIL FLOW RATE IN EACH BED AS EACH BED BREAKS THROUGH
Oil_Flowrate_per_bed_list = []
for bed in Front_Location_list_DataTable.columns:
    Oil_Flowrate_per_bed = (width_of_bed_ft*bed_data_sort['THICKNESS']*Inj_Pressure_differential/Length_of_bed_ft)*Water_Mobility/((1-Mobility_Ratio)*Front_Location_list_DataTable[bed]+Mobility_Ratio)
    Oil_Flowrate_per_bed_list.append(Oil_Flowrate_per_bed)
    
    
Oil_Flowrate_per_bed_table = pd.DataFrame(Oil_Flowrate_per_bed_list).transpose().rename(columns={0:'OIL FLOWRATE  IN EACH BED (STB/D)'})


#==========================================================================================================================


# CALCULATING THE VERTICAL COVERAGE
coverage_list = []
Total_Number_of_layers = len(permeability_array)-1
for number_layer_breakthrough in range(len(permeability_array)):
    coverage_individual = (number_layer_breakthrough+((Total_Number_of_layers-number_layer_breakthrough)*Mobility_Ratio/(Mobility_Ratio-1))-(1/(Mobility_Ratio-1))*np.sqrt(Mobility_Ratio**2+List_of_permeability_ratio_DataTable[number_layer_breakthrough][1:]*(1-Mobility_Ratio**2)).sum())/Total_Number_of_layers
    coverage_list.append(coverage_individual)

#Table of vertical coverage of the reservoir when a given layer just broke through.
coverage_table = pd.DataFrame(coverage_list, columns=['VERTICAL COVERAGE (FRACTION)'])

#============================================================================================================================

WOR_denominator_ratio_list = []
for denominator_index in range(len(permeability_array)):
    WOR_denominator_ratio = permeability_array/np.sqrt(Mobility_Ratio**2+List_of_permeability_ratio_DataTable[denominator_index]*(1-Mobility_Ratio**2))
    WOR_denominator_ratio_list.append(WOR_denominator_ratio)
WOR_denominator_ratio_table = pd.DataFrame(WOR_denominator_ratio_list).transpose()

# CALCULATING THE WATER OIL RATIO, WORn and generate table
WOR_list = []
sum_of_permeability = sum(bed_data_sort.PERMEABILITY)
for number_layer_breakthrough in range(len(permeability_array)):
    WOR = sum_of_permeability/(WOR_denominator_ratio_table[number_layer_breakthrough].sum())
    WOR_list.append(WOR)
WOR_table = pd.DataFrame(WOR_list,columns=['WATER-OIL RATIO'])


#==========================================================================================================================


#CALCULATING THE CUMULATIVE OIL RECOVERY AS EACH BED BREAKSTHROUGH.

Average_porosity = np.mean(bed_data_sort.POROSITY)

Area_acres = Length_of_bed_ft*width_of_bed_ft/43560
Gross_rock_volume_acre_ft = Area_acres*bed_data_sort.THICKNESS.sum()

#KRW_1_SOR = RPERM_data.loc[RPERM_data.SW == 1-SOR,'KRW'].values[0]
#KRO_SWI = RPERM_data.loc[RPERM_data.SW == SWI,'KRO'].values[0]
Mobility_Ratio = KRW_1_SOR*VISO/(KRO_SWI*VISW)

Areal_sweep_efficiency_at_breakthrough = 0.54602036+(0.03170817/Mobility_Ratio)+(0.30222997/math.exp(Mobility_Ratio)-0.0050969*Mobility_Ratio)
Cumulative_oil_recovery = (7758*Areal_sweep_efficiency_at_breakthrough*Gross_rock_volume_acre_ft*Average_porosity*(SOI-SOR)*coverage_table/OFVF).rename(columns={'VERTICAL COVERAGE (FRACTION)':'CUMULATIVE OIL RECOVERY (BARRELS)'})



#============================================================================================================================

#CALCULATING THE VOLUME OF WATER REQUIRED TO FILL-UP THE GAS SPACE.
Water_volume_to_fillup_gas_space = 7758*Area_acres*bed_data_sort.THICKNESS*bed_data_sort.POROSITY*(SGI-Residual_gas_saturation)
Water_volume_to_fillup_gas_space_table=pd.DataFrame(Water_volume_to_fillup_gas_space, columns = ['WATER VOLUME FOR GAS SPACE FILL-UP'])


#============================================================================================================================


#CALCULATING THE PRODUCING WATER-OIL RATIO
Producing_water_oil_ratio = (WOR_table*OFVF).rename(columns={'WATER-OIL RATIO':'PRODUCING WATER-OIL RATIO'})
Producing_water_oil_ratio


#===========================================================================================================================


# Note that the integration for the calculation of the cumulative oil produced starts from 0
# Hence, a new row will have to be inserted at the first row with element 0
# this is done for both the producing water-oil ratio and the cumulative oil produced.

# for the cumulative oil recovery
Cumulative_oil_recovery.loc[-1] = [0]  # adding a row
#Cumulative_oil_recovery.index = Cumulative_oil_recovery.index + 1  # shifting index
Cumulative_oil_recovery_Starting_from_0 = Cumulative_oil_recovery.sort_index()  # sorting by index

# for the producing water-oil ratio
Producing_water_oil_ratio.loc[-1] = [0]  # adding a row
#Producing_water_oil_ratio.index = Producing_water_oil_ratio.index + 1  # shifting index
Producing_water_oil_ratio_Starting_from_0 = Producing_water_oil_ratio.sort_index()  # sorting by index

# CALCULATING THE CUMULATIVE WATER PRODUCTION

# To determine the cumulative water production, the produced water oil ratio is ingreated against the cumulative oil recovery.
# The integration uses a cumulative trapezoidal row by row integration.

# import numpy and scipy.integrate.cumtrapz 
import numpy as np 
from scipy import integrate

# Preparing the Integration variables y, x.
   # the to.numpy() method converts from dataframe to numpy array which appears in the form of list of lists in the array. 
   #The concatenate function helps to bring the list of lists together.
x = np.concatenate(Cumulative_oil_recovery_Starting_from_0.to_numpy(),axis=0)
y = np.concatenate(Producing_water_oil_ratio_Starting_from_0.to_numpy(),axis=0) 

# using scipy.integrate.cumtrapz() method 
Cumulative_water_produced = pd.DataFrame(integrate.cumtrapz(y, x), columns = ['CUMULATIVE WATER PRODUCED'])


#==============================================================================================================================


# CALCULATING THE CUMULATIVE WATER INJECTED, Wi
Cumulative_water_injected = (Cumulative_water_produced['CUMULATIVE WATER PRODUCED'] + OFVF*Cumulative_oil_recovery['CUMULATIVE OIL RECOVERY (BARRELS)'] + Water_volume_to_fillup_gas_space_table['WATER VOLUME FOR GAS SPACE FILL-UP']).drop([-1])
Cumulative_water_injected_table = pd.DataFrame(Cumulative_water_injected,columns = ['CUMULATIVE WATER INJECTED (BARRELS)'])


#===================================================================================================================================


# CALCULATING THE TIME REQUIRED FOR INJECTION TO REACH A GIVEN RECOVERY.
Time_days = Cumulative_water_injected_table['CUMULATIVE WATER INJECTED (BARRELS)']/Constant_injection_rate
Time_days_table = pd.DataFrame(Time_days).rename(columns ={'CUMULATIVE WATER INJECTED (BARRELS)': 'Time (Days)'}, inplace = False)
#print(Time_days_table)
Time_years = Time_days_table/365
Time_years_table = Time_years.rename(columns ={'Time (Days)': 'Time (Years)'}, inplace = False)


#=======================================================================================================================================


# TABLE OF ALL OBTAINED VALUES.
All_tables =pd.concat([Layer_table,Water_Flowrate_per_bed_table, coverage_table, WOR_table, Cumulative_oil_recovery, Water_volume_to_fillup_gas_space_table, Producing_water_oil_ratio, Cumulative_water_produced, Cumulative_water_injected_table, Time_days_table, Time_years_table,Front_Location_list_DataTable,Oil_Flowrate_per_bed_table], axis = 1).drop([-1])


#====================================================================================================================================================





#================================================================================================================================




#root = Tk()

root.geometry("1200x600")


#creation of an instance
#app = Window(root)

#mainloop 
root.mainloop() 


# In[63]:





# In[23]:





# In[ ]:





# In[ ]:





# In[ ]:




