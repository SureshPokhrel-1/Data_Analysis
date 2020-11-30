# -*- coding: utf-8 -*-
"""
Created on Sat Nov 28 19:53:05 2020

@author: supokhrel
"""
Height = 400
Width = 600

Data_res_1_opt = [ "1", "2","3","5","10", "15", "20", "30", "45", "60"]
Data_res_2_opt = [ "Minute", "Hour","Day","Month","Year"]

Hour_opt = ["00", "01", "02", "03", "04", "05", "06", "07", "08", "09", "10",
            "11", "12", "13", "14", "15", "16", "17", "18", "19", "20", "21", "22", "23"]

Min_opt = ["00", "01", "02", "03", "04", "05", "06", "07", "08", "09",
           "10", "11", "12", "13", "14", "15", "16", "17", "18", "19",
           "20", "21", "22", "23", "24", "25", "26", "27", "28", "29",
           "30", "31", "32", "33", "34", "35", "36", "37", "38", "39",
           "40", "41", "42", "43", "44", "45", "46", "47", "48", "49",
           "50", "51", "52", "53", "54", "55", "56", "57", "58", "59"]

Slice_YES_NO = ["NO", "YES"]
Avg_YES_NO = ["NO", "YES"]

Avg_type_1_opt = [ "1", "2","3","5","10", "15", "20", "30", "45", "60"]
Avg_type_2_opt = [ "Minute", "Hour","Day","Month","Year"]


import tkinter as tkt
from tkinter import filedialog 
from tkcalendar import DateEntry
from tkinter import ttk
   
# Function for opening the  
# file explorer window
File_Path = '' 
def browseFiles(): 
    global File_Path
    filename = filedialog.askopenfilename(initialdir = "/", 
                                          title = "Select a File", 
                                          filetypes = (("CSV files", 
                                                        "*.csv*"), 
                                                       )) 
    if (filename != ''):
        label_file_explorer.configure(text = filename, fg = 'black') 
        File_Path = filename
    else:
        label_file_explorer.configure(text="!!!File Not Selected", fg = 'crimson')
#        File_Path = ''


window = tkt.Tk()
window.title("Data Analysis Tool  V1.2")

canvas = tkt.Canvas(window, height = Height , width = Width )
canvas.pack()

frame = tkt.Frame(window, bg = 'skyblue', bd = 0)
frame.place(relx = 0.05, rely = 0.05, relheight = 0.85, relwidth = 0.9)

var = tkt.StringVar()
var.set('Filling Entries...')
lbl_finish = tkt.Label(frame, textvariable=var)
lbl_finish.place(relx = 0.25, rely = 0.86, relheight = 0.05, relwidth = 0.65)

label_msz = ''

def Data_process():
#    global label_msz
##    label_msz.destroy()
#    label_msz.config(text = 'Processing... Please Wait')
#    label_msz.place(relx = 0.25, rely = 0.86, relheight = 0.05, relwidth = 0.65)
    var.set('')
    window.update()
#    sleep(5)
    var.set('Processing....')
    window.update()
    import pandas as pd
    import glob
    import numpy as np
    Data_res_1 = Data_res_1_.get()
    Data_res_2 = Data_res_2_.get()
    
    Slice_status = Slice_status_.get()
    Start_date_str = cal_start.get() + " " + Start_hour_Menu.get() + ":" + Start_min_Menu.get()
    End_date_str = cal_end.get() + " " + End_hour_Menu.get() + ":" + End_min_Menu.get()
    
    Avg_status = Avg_status_.get()
    Avg_type_1 = Avg_type_1_.get()
    Avg_type_2 = Avg_type_2_.get()
#    print(Data_res_1, Data_res_2, Slice_status, Start_date_str, End_date_str, Avg_status, Avg_type_1, Avg_type_2)
    
    
    if(Data_res_2 == 'Minute'):
        Data_res = Data_res_1 + 'T'
    elif(Data_res_2 == 'Hour'):
        Data_res = Data_res_1 + 'H'
    elif(Data_res_2 == 'Day'):
        Data_res = Data_res_1 + 'D'
    elif(Data_res_2 == 'Month'):
        Data_res = Data_res_1 + 'M'
    elif(Data_res_2 == 'Year'):
        Data_res = Data_res_1 + 'Y'
        
    File = glob.glob(File_Path)
#    print("Input file: ",File_Path)
    if not File:
        print("Empty Filename")
        window.destroy()
        import sys
        sys.exit()
        
    
    df = pd.concat([pd.read_csv(fp, low_memory=False) for fp in File], ignore_index=True)
    df.insert(0, 'Date_temp', pd.to_datetime(df[df.columns[0]]))
    df.drop(columns=[df.columns[1]], inplace = True)
    df.rename(columns = {'Date_temp':'Date'}, inplace = True)
    df.drop_duplicates(subset='Date', keep = 'last', inplace = True)
    df = df.sort_values(by='Date')
    df = df.set_index(['Date']).asfreq(Data_res)
#    print(df)
    if(Slice_status == 'YES'):
        Start_date = pd.to_datetime(Start_date_str)
        End_date = pd.to_datetime(End_date_str)
        df = df.truncate(before=Start_date, after=End_date)
    
    Inital_cols = len(df.columns)
    for i in range(0, Inital_cols):
        df[df.columns[i]] = pd.to_numeric(df[df.columns[i]], errors='coerce')
        if(Avg_status == 'YES'):
            Data_Percent = 'Data_Availabiliy_Percentage_'
            DAP = Data_Percent+df.columns[i]
            df[DAP] = (~np.isnan(df[df.columns[i]])).astype(int)
            
            
    if(Avg_status == 'YES'):
        if(Avg_type_2 == 'Minute'):
            Avg_type = Avg_type_1 + 'T'
        elif(Avg_type_2 == 'Hour'):
            Avg_type = Avg_type_1 + 'H'
        elif(Avg_type_2 == 'Day'):
            Avg_type = Avg_type_1 + 'D'
        elif(Avg_type_2 == 'Month'):
            Avg_type = Avg_type_1 + 'M'
        elif(Avg_type_2 == 'Year'):
            Avg_type = Avg_type_1 + 'Y'
            
        df = df.resample(Avg_type).mean()
        Final_cols = len(df.columns)
        for i in range(Inital_cols, Final_cols):
            df[df.columns[i]] = df[df.columns[i]]*100
            df[df.columns[i]] = df[df.columns[i]].round(decimals = 1)
#        print(df)
     
#    print(Data_res, Avg_status, Avg_type)
            
    import os
    InputFolder_path = os.path.dirname(os.path.abspath(File_Path)) 
    InputFileName = os.path.basename(File_Path)
    #print(InputFolder_path)
    #print(InputFileName) 
    
    Output_FilePath = InputFolder_path+'\Processed_'+ InputFileName 
    #print(Output_FilePath)
    
    df.to_csv(Output_FilePath, index= True)
    
    
    var.set('')
    window.update()
#    sleep(5)
    var.set('Completed: Check your input folder')
    
#    label = tkt.Label(frame, text = "If you want to run again, then press Run button Else exit", fg = 'black')
#    label.place(relx = 0.25, rely = 0.92, relheight = 0.05, relwidth = 0.65)





########################################### GUI #########################################################
# Create a File Explorer label 
label_file_explorer = tkt.Label(frame,text = "", fg = "Green") 
label_file_explorer.place(relx = 0.12, rely = 0.01, relheight = 0.05, relwidth = 0.85) 

button_explore = tkt.Button(frame,  text = "Browse", command = browseFiles, fg = 'red') 
button_explore.place(relx = 0.01, rely = 0.01, relheight = 0.05, relwidth = 0.1)

label = tkt.Label(frame, text = 'Input Data Resolution', fg = 'black', bg = 'skyblue')
label.place(relx = 0.01, rely = 0.09, relheight = 0.05, relwidth = 0.22)

Data_res_1_ = tkt.StringVar(frame)
Data_res_1_.set(Data_res_1_opt[0])
Data_res_1_Menu = tkt.OptionMenu(frame, Data_res_1_, *Data_res_1_opt)
Data_res_1_Menu.place(relx = 0.25, rely = 0.09, relheight = 0.06, relwidth = 0.1)

Data_res_2_ = tkt.StringVar(frame)
Data_res_2_.set(Data_res_2_opt[0])
Data_res_2_Menu = tkt.OptionMenu(frame, Data_res_2_, *Data_res_2_opt)
Data_res_2_Menu.place(relx = 0.37, rely = 0.09, relheight = 0.06, relwidth = 0.15)

label = tkt.Label(frame, text = 'Data Slicing Required ?', fg = 'black', bg = 'skyblue')
label.place(relx = 0.01, rely = 0.32, relheight = 0.05, relwidth = 0.22)

Slice_status_= tkt.StringVar(frame)
Slice_status_.set(Slice_YES_NO[0])
Slice_status_Menu = tkt.OptionMenu(frame, Slice_status_, *Slice_YES_NO)
Slice_status_Menu.place(relx = 0.24, rely = 0.32, relheight = 0.06, relwidth = 0.10)

label = tkt.Label(frame, text = 'Start Date', fg = 'black', bg = 'skyblue')
label.place(relx =0.35, rely = 0.2, relheight = 0.05, relwidth = 0.20)

label = tkt.Label(frame, text = 'hh', fg = 'black', bg = 'skyblue')
label.place(relx =0.52, rely = 0.2, relheight = 0.05, relwidth = 0.05)

label = tkt.Label(frame, text = 'mm', fg = 'black', bg = 'skyblue')
label.place(relx =0.62, rely = 0.2, relheight = 0.05, relwidth = 0.05)

cal_start = DateEntry(frame,bg="darkblue",fg="white",year=2020, month = 1, day = 1, date_pattern = 'm/d/y')
cal_start.place(relx =0.37, rely = 0.255, relheight = 0.05, relwidth = 0.138)

Start_hour_= tkt.StringVar(frame)
Start_hour_.set(Hour_opt[0])
Start_hour_Menu = ttk.Combobox(frame, textvariable = Start_hour_, values =  Hour_opt)
Start_hour_Menu.place(relx = 0.52, rely = 0.25, relheight = 0.06, relwidth = 0.07)

label = tkt.Label(frame, text = ':', fg = 'black', bg = 'skyblue')
label.place(relx =0.595, rely = 0.25, relheight = 0.06, relwidth = 0.02)

Start_min_= tkt.StringVar(frame)
Start_min_.set(Min_opt[0])
Start_min_Menu = ttk.Combobox(frame, textvariable = Start_min_, values =  Min_opt)
Start_min_Menu.place(relx = 0.62, rely = 0.25, relheight = 0.06, relwidth = 0.07)


label = tkt.Label(frame, text = 'End Date', fg = 'black', bg = 'skyblue')
label.place(relx =0.35, rely = 0.35, relheight = 0.05, relwidth = 0.20)

label = tkt.Label(frame, text = 'hh', fg = 'black', bg = 'skyblue')
label.place(relx =0.52, rely = 0.35, relheight = 0.05, relwidth = 0.05)

label = tkt.Label(frame, text = 'mm', fg = 'black', bg = 'skyblue')
label.place(relx =0.62, rely = 0.35, relheight = 0.05, relwidth = 0.05)

cal_end = DateEntry(frame,bg="darkblue",fg="white",year=2020, month = 1, day = 31, date_pattern = 'm/d/y')
cal_end.place(relx =0.37, rely = 0.4, relheight = 0.05, relwidth = 0.138)

End_hour_= tkt.StringVar(frame)
End_hour_.set(Hour_opt[23])
End_hour_Menu = ttk.Combobox(frame, textvariable = End_hour_, values =  Hour_opt)
End_hour_Menu.place(relx = 0.52, rely = 0.395, relheight = 0.06, relwidth = 0.07)

label = tkt.Label(frame, text = ':', fg = 'black', bg = 'skyblue')
label.place(relx =0.595, rely = 0.395, relheight = 0.06, relwidth = 0.02)

End_min_= tkt.StringVar(frame)
End_min_.set(Min_opt[59])
End_min_Menu = ttk.Combobox(frame, textvariable = End_min_, values =  Min_opt)
End_min_Menu.place(relx = 0.62, rely = 0.395, relheight = 0.06, relwidth = 0.07)

label = tkt.Label(frame, text = 'Averaging Required ?', fg = 'black', bg = 'skyblue')
label.place(relx = 0.01, rely = 0.62, relheight = 0.05, relwidth = 0.22)

Avg_status_= tkt.StringVar(frame)
Avg_status_.set(Avg_YES_NO[0])
Avg_status_Menu = tkt.OptionMenu(frame, Avg_status_, *Avg_YES_NO)
Avg_status_Menu.place(relx = 0.24, rely = 0.62, relheight = 0.06, relwidth = 0.10)


Avg_type_1_ = tkt.StringVar(frame)
Avg_type_1_.set(Avg_type_1_opt[0])
Avg_type_1_Menu = tkt.OptionMenu(frame, Avg_type_1_, *Avg_type_1_opt)
Avg_type_1_Menu.place(relx = 0.4, rely = 0.62, relheight = 0.06, relwidth = 0.1)

Avg_type_2_ = tkt.StringVar(frame)
Avg_type_2_.set(Avg_type_2_opt[0])
Avg_type_2_Menu = tkt.OptionMenu(frame, Avg_type_2_, *Avg_type_2_opt)
Avg_type_2_Menu.place(relx = 0.52, rely = 0.62, relheight = 0.06, relwidth = 0.15)


bt = tkt.Button(frame, text = 'RUN', bg = 'coral', fg = 'blue', command = Data_process )
bt.place(relx = 0.05, rely = 0.84, relheight = 0.08, relwidth = 0.08)

label = tkt.Label(frame, text = 'Current Status', fg = 'black', bg = 'skyblue')
label.place(relx = 0.45, rely = 0.80, relheight = 0.05, relwidth = 0.22)

#label_msz = tkt.Label(frame, text = 'Filling Entries', fg = 'black')
#label_msz.place(relx = 0.25, rely = 0.86, relheight = 0.05, relwidth = 0.65)

label = tkt.Label(window, text = 'Developed by Suresh-ICIMOD', fg = 'grey')
label.place(relx = 0.64, rely = 0.95, relheight = 0.05, relwidth = 0.45)

window.mainloop()

