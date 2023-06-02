# -*- coding: utf-8 -*-
"""
@paper: Komprese 360° obrazu založená na hlubokém učení
@author: Adam Budáč
@thesis: Diplomová práca 2022/2023
@organisation: VUT Brno, FEKT, UREL
"""


import tkinter as tk
from tkinter import ttk, filedialog, Canvas, Button
import time
from timeit import default_timer as timer
from PIL import Image, ImageTk
import os
import subprocess
import shutil
import matlab.engine
import csv
import glob

WorkDirWindows = os.getcwd()
WorkDirPython = WorkDirWindows.replace("\\", "/" )
WorkDirWindows = WorkDirWindows.replace("\\", "\\\\" )

# Definicia kvality a kvantizacnych parametrov
Q_min_JPEG = 0
Q_max_JPEG = 100
Q_min_JPEGXL = 5
Q_max_JPEGXL = 100
Q_min_HEIC = 0
Q_max_HEIC = 51
Q_min_AVIF = 1
Q_max_AVIF = 63
Q_min_VVCIntra = 1
Q_max_VVCIntra = 63
Q_min_FRICwRNN = 0
Q_max_FRICwRNN = 15
Q_min_CAEMfE2EOIC = 1
Q_max_CAEMfE2EOIC = 9
Q_min_HiFiC = 1
Q_max_HiFiC = 3
Q_min_LIC360 = 1
Q_max_LIC360 = 8

def LoadFile():
    global Path, Head, Tail, Filename, Extension, obrazok, width, height, img
    Path = main.tk.splitlist(filedialog.askopenfilename(title = "Vyberte obrázok"))
    Path = ''.join(Path)
    Head, Tail = os.path.split(Path)
    Filename = Tail.split(".")[0]
    Extension = Tail.split(".")[-1]
    ttk.Label(main, text=Tail).grid(column=ColumnShift + 1, row=RowShift, columnspan = 3)
    shutil.copy(Path, Tail)
    obrazok = Image.open(Tail)
    imagewidth, imageheight = obrazok.size
    width = imagewidth
    height = imageheight
    ttk.Label(main, text=str(imagewidth) + " x " + str(imageheight)).grid(column=1 + ColumnShift, row = 1 + RowShift, columnspan = 3)
    obrazok = obrazok.resize((512, 256))
    obrazok = ImageTk.PhotoImage(obrazok)
    canvas.create_image(0,0,anchor=tk.NW,image=obrazok)
        
def NewEntry(r,c,w):
    entry = tk.Entry(main,width = w)
    entry.grid(row=r,column=c)
    return entry

CheckCodecList = [1,1,1,1,1,1,1,1,1]
def CheckCodec():

    if CheckCodecJPEG.get() == 1:
        CheckCodecList[0] = 1
    else:
        CheckCodecList[0] = 0

    if CheckCodecJPEGXL.get() == 1:
        CheckCodecList[1] = 1
    else:
        CheckCodecList[1] = 0

    if CheckCodecAVIF.get() == 1:
        CheckCodecList[2] = 1
    else:
        CheckCodecList[2] = 0

    if CheckCodecHEIC.get() == 1:
        CheckCodecList[3] = 1
    else:
        CheckCodecList[3] = 0

    if CheckCodecVVCIntra.get() == 1:
        CheckCodecList[4] = 1
    else:
        CheckCodecList[4] = 0

    if CheckCodecFRICwRNN.get() == 1:
        CheckCodecList[5] = 1
    else:
        CheckCodecList[5] = 0

    if CheckCodecCAEMfE2EOIC.get() == 1:
        CheckCodecList[6] = 1
    else:
        CheckCodecList[6] = 0

    if CheckCodecHiFiC.get() == 1:
        CheckCodecList[7] = 1
    else:
        CheckCodecList[7] = 0

    if CheckCodecLIC360.get() == 1:
        CheckCodecList[8] = 1
    else:
        CheckCodecList[8] = 0

CheckMetricList = [1,1,1,1,1,1,1]
def CheckMetric():

    if CheckMetricPSNRHVSM.get() == 1:
        CheckMetricList[0] = 1
    else:
        CheckMetricList[0] = 0

    if CheckMetricWSPSNR.get() == 1:
        CheckMetricList[1] = 1
    else:
        CheckMetricList[1] = 0

    if CheckMetricMSSSIM.get() == 1:
        CheckMetricList[2] = 1
    else:
        CheckMetricList[2] = 0

    if CheckMetricVIFp.get() == 1:
        CheckMetricList[3] = 1
    else:
        CheckMetricList[3] = 0

    if CheckMetricVMAF.get() == 1:
        CheckMetricList[4] = 1
    else:
        CheckMetricList[4] = 0

    if CheckMetricFSIMc.get() == 1:
        CheckMetricList[5] = 1
    else:
        CheckMetricList[5] = 0

    if CheckMetricGMSD.get() == 1:
        CheckMetricList[6] = 1
    else:
        CheckMetricList[6] = 0

def Process():
    global Quality_JPEG, Quality_JPEGXL, Quality_AVIF, Quality_HEIC, Quality_VVC, Quality_FRICwRNN, Quality_CAEMfE2EOIC, Quality_HiFiC, Quality_LIC360, Q, kodek, CasovacStart, CasovacEnd
    
# Nacitanie kvality kodekov
    Quality_JPEG        = int(Quality_JPEG_Entry.get())
    Quality_JPEGXL      = int(Quality_JPEGXL_Entry.get())
    Quality_AVIF        = int(Quality_AVIF_Entry.get())
    Quality_HEIC        = int(Quality_HEIC_Entry.get())
    Quality_VVC         = int(Quality_VVC_Entry.get())
    Quality_FRICwRNN    = int(Quality_FRICwRNN_Entry.get())
    Quality_CAEMfE2EOIC = int(Quality_CAEMfE2EOIC_Entry.get())
    Quality_HiFiC       = int(Quality_HiFiC_Entry.get())
    Quality_LIC360      = int(Quality_LIC360_Entry.get())
    Compress_Reference()

# Kompresia a dekompresia
    if CheckCodecList[0] == 1:
        Compress_JPEG()
    if CheckCodecList[1] == 1:
        Compress_JPEG_XL()
    if CheckCodecList[2] == 1:
        Compress_AVIF()
    if CheckCodecList[3] == 1:
        Compress_HEIC()
    if CheckCodecList[4] == 1:
        Compress_VVC_Intra()
    if CheckCodecList[5] == 1:
        Compress_FRICwRNN()
    if CheckCodecList[6] == 1:
        Compress_CAEMfE2EOIC()
    if CheckCodecList[7] == 1:
        Compress_HiFiC()
    if CheckCodecList[8] == 1:
        Compress_LIC360()

# Vypocet metrik a BPP
    for kodek in ["jpg","jxl","avif","heic","vvc","FRICwRNN","CAEMfE2EOIC","HiFiC","LIC360"]:

        if CheckCodecList[0] == 1 and kodek == "jpg":
            Q = Quality_JPEG
            if CheckMetricList[0] == 1:
                Calculate_PSNR_HVS_M()
            if CheckMetricList[1] == 1:
                Calculate_WS_PSNR()
            if CheckMetricList[2] == 1:
                Calculate_MS_SSIM()
            if CheckMetricList[3] == 1:
                Calculate_VIFp()
            if CheckMetricList[4] == 1:
                Calculate_VMAF()
            if CheckMetricList[5] == 1:
                Calculate_FSIMc()
            if CheckMetricList[6] == 1:
                Calculate_GMSD()
            Calculate_BPP()
                
        elif CheckCodecList[1] == 1 and kodek == "jxl":
            Q = Quality_JPEGXL
            if CheckMetricList[0] == 1:
                Calculate_PSNR_HVS_M()
            if CheckMetricList[1] == 1:
                Calculate_WS_PSNR()
            if CheckMetricList[2] == 1:
                Calculate_MS_SSIM()
            if CheckMetricList[3] == 1:
                Calculate_VIFp()
            if CheckMetricList[4] == 1:
                Calculate_VMAF()
            if CheckMetricList[5] == 1:
                Calculate_FSIMc()
            if CheckMetricList[6] == 1:
                Calculate_GMSD()
            Calculate_BPP()
                
        elif CheckCodecList[2] == 1 and kodek == "avif":
            Q = Quality_AVIF
            if CheckMetricList[0] == 1:
                Calculate_PSNR_HVS_M()
            if CheckMetricList[1] == 1:
                Calculate_WS_PSNR()
            if CheckMetricList[2] == 1:
                Calculate_MS_SSIM()
            if CheckMetricList[3] == 1:
                Calculate_VIFp()
            if CheckMetricList[4] == 1:
                Calculate_VMAF()
            if CheckMetricList[5] == 1:
                Calculate_FSIMc()
            if CheckMetricList[6] == 1:
                Calculate_GMSD()
            Calculate_BPP()
                
        elif CheckCodecList[3] == 1 and kodek == "heic":
            Q = Quality_HEIC
            if CheckMetricList[0] == 1:
                Calculate_PSNR_HVS_M()
            if CheckMetricList[1] == 1:
                Calculate_WS_PSNR()
            if CheckMetricList[2] == 1:
                Calculate_MS_SSIM()
            if CheckMetricList[3] == 1:
                Calculate_VIFp()
            if CheckMetricList[4] == 1:
                Calculate_VMAF()
            if CheckMetricList[5] == 1:
                Calculate_FSIMc()
            if CheckMetricList[6] == 1:
                Calculate_GMSD()
            Calculate_BPP()
                
        elif CheckCodecList[4] == 1 and kodek == "vvc":
            Q = Quality_VVC
            if CheckMetricList[0] == 1:
                Calculate_PSNR_HVS_M()
            if CheckMetricList[1] == 1:
                Calculate_WS_PSNR()
            if CheckMetricList[2] == 1:
                Calculate_MS_SSIM()
            if CheckMetricList[3] == 1:
                Calculate_VIFp()
            if CheckMetricList[4] == 1:
                Calculate_VMAF()
            if CheckMetricList[5] == 1:
                Calculate_FSIMc()
            if CheckMetricList[6] == 1:
                Calculate_GMSD()
            Calculate_BPP()
                
        elif CheckCodecList[5] == 1 and kodek == "FRICwRNN":
            Q = Quality_FRICwRNN
            if CheckMetricList[0] == 1:
                Calculate_PSNR_HVS_M()
            if CheckMetricList[1] == 1:
                Calculate_WS_PSNR()
            if CheckMetricList[2] == 1:
                Calculate_MS_SSIM()
            if CheckMetricList[3] == 1:
                Calculate_VIFp()
            if CheckMetricList[4] == 1:
                Calculate_VMAF()
            if CheckMetricList[5] == 1:
                Calculate_FSIMc()
            if CheckMetricList[6] == 1:
                Calculate_GMSD()
            Calculate_BPP()
                
        elif CheckCodecList[6] == 1 and kodek == "CAEMfE2EOIC":
            Q = Quality_CAEMfE2EOIC
            if CheckMetricList[0] == 1:
                Calculate_PSNR_HVS_M()
            if CheckMetricList[1] == 1:
                Calculate_WS_PSNR()
            if CheckMetricList[2] == 1:
                Calculate_MS_SSIM()
            if CheckMetricList[3] == 1:
                Calculate_VIFp()
            if CheckMetricList[4] == 1:
                Calculate_VMAF()
            if CheckMetricList[5] == 1:
                Calculate_FSIMc()
            if CheckMetricList[6] == 1:
                Calculate_GMSD()
            Calculate_BPP()
                
        elif CheckCodecList[7] == 1 and kodek == "HiFiC":
            Q = Quality_HiFiC
            if CheckMetricList[0] == 1:
                Calculate_PSNR_HVS_M()
            if CheckMetricList[1] == 1:
                Calculate_WS_PSNR()
            if CheckMetricList[2] == 1:
                Calculate_MS_SSIM()
            if CheckMetricList[3] == 1:
                Calculate_VIFp()
            if CheckMetricList[4] == 1:
                Calculate_VMAF()
            if CheckMetricList[5] == 1:
                Calculate_FSIMc()
            if CheckMetricList[6] == 1:
                Calculate_GMSD()
            Calculate_BPP()
                
        elif CheckCodecList[8] == 1 and kodek == "LIC360":
            Q = Quality_LIC360
            if CheckMetricList[0] == 1:
                Calculate_PSNR_HVS_M()
            if CheckMetricList[1] == 1:
                Calculate_WS_PSNR()
            if CheckMetricList[2] == 1:
                Calculate_MS_SSIM()
            if CheckMetricList[3] == 1:
                Calculate_VIFp()
            if CheckMetricList[4] == 1:
                Calculate_VMAF()
            if CheckMetricList[5] == 1:
                Calculate_FSIMc()
            if CheckMetricList[6] == 1:
                Calculate_GMSD()
            Calculate_BPP()
        
# Kvalita/QP
    ttk.Label(main, text="          " + str(Quality_JPEG)).grid(column=ColumnVysledky + 1, row=2 + RowShift)
    ttk.Label(main, text=str(Quality_JPEGXL)             ).grid(column=ColumnVysledky + 2, row=2 + RowShift)
    ttk.Label(main, text=str(Quality_AVIF)               ).grid(column=ColumnVysledky + 3, row=2 + RowShift)
    ttk.Label(main, text=str(Quality_HEIC)               ).grid(column=ColumnVysledky + 4, row=2 + RowShift)
    ttk.Label(main, text=str(Quality_VVC)                ).grid(column=ColumnVysledky + 5, row=2 + RowShift)
    ttk.Label(main, text=str(Quality_FRICwRNN)           ).grid(column=ColumnVysledky + 6, row=2 + RowShift)
    ttk.Label(main, text=str(Quality_CAEMfE2EOIC)        ).grid(column=ColumnVysledky + 7, row=2 + RowShift)
    ttk.Label(main, text=str(Quality_HiFiC)              ).grid(column=ColumnVysledky + 8, row=2 + RowShift)
    ttk.Label(main, text=str(Quality_LIC360)             ).grid(column=ColumnVysledky + 9, row=2 + RowShift)

# Vysledky metrik
# JPEG
    # PSNR-HVS-M
    MetricResultPath = WorkDirWindows + "\\Score_jpg_Q" + str(Quality_JPEG) + "_psnrhvsm.csv"
    if os.path.isfile(MetricResultPath) == True:
        with open(MetricResultPath) as file:
            DataReadCSV = csv.DictReader(file, delimiter=',')
            for csvcolumn in DataReadCSV:
                Data = csvcolumn['value'][0:6]
                ttk.Label(main, text="          " + Data).grid(column=ColumnVysledky + 1, row=4 + RowShift)
    # WS-PSNR
    MetricResultPath = WorkDirWindows + "\\ScoreWSPSNR_jpg_Q" + str(Quality_JPEG) + ".txt"
    if os.path.isfile(MetricResultPath) == True:
        with open(MetricResultPath,'r') as file:
            txtvalue = file.readline()
            Data = txtvalue[8:14]
            file.close()
            ttk.Label(main, text="          " + Data).grid(column=ColumnVysledky + 1, row=5 + RowShift)
    # MS-SSIM
    MetricResultPath = WorkDirWindows + "\\Score_jpg_Q" + str(Quality_JPEG) + "_msssim.csv"
    if os.path.isfile(MetricResultPath) == True:
        with open(MetricResultPath) as file:
            DataReadCSV = csv.DictReader(file, delimiter=',')
            for csvcolumn in DataReadCSV:
                Data = csvcolumn['value'][0:6]
                ttk.Label(main, text="          " + Data).grid(column=ColumnVysledky + 1, row=6 + RowShift)
    # VIFp
    MetricResultPath = WorkDirWindows + "\\Score_jpg_Q" + str(Quality_JPEG) + "_vifp.csv"
    if os.path.isfile(MetricResultPath) == True:
        with open(MetricResultPath) as file:
            DataReadCSV = csv.DictReader(file, delimiter=',')
            for csvcolumn in DataReadCSV:
                Data = csvcolumn['value'][0:6]
                ttk.Label(main, text="          " + Data).grid(column=ColumnVysledky + 1, row=7 + RowShift)
    # VMAF
    MetricResultPath = WorkDirWindows + "\\ScoreVMAF_jpg_Q" + str(Quality_JPEG) + ".txt"
    if os.path.isfile(MetricResultPath) == True:
        with open(MetricResultPath,'r') as file:
            txtvalue = file.readline()
            txtvalue = txtvalue[txtvalue.find('vmaf: '):]
            Data = txtvalue[6:12]
            file.close()
            ttk.Label(main, text="          " + Data).grid(column=ColumnVysledky + 1, row=8 + RowShift)
    # FSIMc
    MetricResultPath = WorkDirWindows + "\\ScoreFSIMc_jpg_Q" + str(Quality_JPEG) + ".txt"
    if os.path.isfile(MetricResultPath) == True:
        with open(MetricResultPath,'r') as file:
            Data = file.readline()
            file.close()
            ttk.Label(main, text="          " + Data).grid(column=ColumnVysledky + 1, row=9 + RowShift)
    # GMSD
    MetricResultPath = WorkDirWindows + "\\ScoreGMSD_jpg_Q" + str(Quality_JPEG) + ".txt"
    if os.path.isfile(MetricResultPath) == True:
        with open(MetricResultPath,'r') as file:
            Data = file.readline()
            file.close()
            ttk.Label(main, text="          " + Data).grid(column=ColumnVysledky + 1, row=10 + RowShift)
# JPEG XL  
    # PSNR-HVS-M
    MetricResultPath = WorkDirWindows + "\\Score_jxl_Q" + str(Quality_JPEGXL) + "_psnrhvsm.csv"
    if os.path.isfile(MetricResultPath) == True:
        with open(MetricResultPath) as file:
            DataReadCSV = csv.DictReader(file, delimiter=',')
            for csvcolumn in DataReadCSV:
                Data = csvcolumn['value'][0:6]
                ttk.Label(main, text=Data).grid(column=ColumnVysledky + 2, row=4 + RowShift)
    # WS-PSNR
    MetricResultPath = WorkDirWindows + "\\ScoreWSPSNR_jxl_Q" + str(Quality_JPEGXL) + ".txt"
    if os.path.isfile(MetricResultPath) == True:
        with open(MetricResultPath,'r') as file:
            txtvalue = file.readline()
            Data = txtvalue[8:14]
            file.close()
            ttk.Label(main, text=Data).grid(column=ColumnVysledky + 2, row=5 + RowShift)
    # MS-SSIM
    MetricResultPath = WorkDirWindows + "\\Score_jxl_Q" + str(Quality_JPEGXL) + "_msssim.csv"
    if os.path.isfile(MetricResultPath) == True:
        with open(MetricResultPath) as file:
            DataReadCSV = csv.DictReader(file, delimiter=',')
            for csvcolumn in DataReadCSV:
                Data = csvcolumn['value'][0:6]
                ttk.Label(main, text=Data).grid(column=ColumnVysledky + 2, row=6 + RowShift)
    # VIFp
    MetricResultPath = WorkDirWindows + "\\Score_jxl_Q" + str(Quality_JPEGXL) + "_vifp.csv"
    if os.path.isfile(MetricResultPath) == True:
        with open(MetricResultPath) as file:
            DataReadCSV = csv.DictReader(file, delimiter=',')
            for csvcolumn in DataReadCSV:
                Data = csvcolumn['value'][0:6]
                ttk.Label(main, text=Data).grid(column=ColumnVysledky + 2, row=7 + RowShift)
    # VMAF
    MetricResultPath = WorkDirWindows + "\\ScoreVMAF_jxl_Q" + str(Quality_JPEGXL) + ".txt"
    if os.path.isfile(MetricResultPath) == True:
        with open(MetricResultPath,'r') as file:
            txtvalue = file.readline()
            txtvalue = txtvalue[txtvalue.find('vmaf: '):]
            Data = txtvalue[6:12]
            file.close()
            ttk.Label(main, text=Data).grid(column=ColumnVysledky + 2, row=8 + RowShift)
    # FSIMc
    MetricResultPath = WorkDirWindows + "\\ScoreFSIMc_jxl_Q" + str(Quality_JPEGXL) + ".txt"
    if os.path.isfile(MetricResultPath) == True:
        with open(MetricResultPath,'r') as file:
            Data = file.readline()
            file.close()
            ttk.Label(main, text=Data).grid(column=ColumnVysledky + 2, row=9 + RowShift)
    # GMSD
    MetricResultPath = WorkDirWindows + "\\ScoreGMSD_jxl_Q" + str(Quality_JPEGXL) + ".txt"
    if os.path.isfile(MetricResultPath) == True:
        with open(MetricResultPath,'r') as file:
            Data = file.readline()
            file.close()
            ttk.Label(main, text=Data).grid(column=ColumnVysledky + 2, row=10 + RowShift)
# AVIF
    # PSNR-HVS-M
    MetricResultPath = WorkDirWindows + "\\Score_avif_Q" + str(Quality_AVIF) + "_psnrhvsm.csv"
    if os.path.isfile(MetricResultPath) == True:
        with open(MetricResultPath) as file:
            DataReadCSV = csv.DictReader(file, delimiter=',')
            for csvcolumn in DataReadCSV:
                Data = csvcolumn['value'][0:6]
                ttk.Label(main, text=Data).grid(column=ColumnVysledky + 3, row=4 + RowShift)
    # WS-PSNR
    MetricResultPath = WorkDirWindows + "\\ScoreWSPSNR_avif_Q" + str(Quality_AVIF) + ".txt"
    if os.path.isfile(MetricResultPath) == True:
        with open(MetricResultPath,'r') as file:
            txtvalue = file.readline()
            Data = txtvalue[8:14]
            file.close()
            ttk.Label(main, text=Data).grid(column=ColumnVysledky + 3, row=5 + RowShift)
    # MS-SSIM
    MetricResultPath = WorkDirWindows + "\\Score_avif_Q" + str(Quality_AVIF) + "_msssim.csv"
    if os.path.isfile(MetricResultPath) == True:
        with open(MetricResultPath) as file:
            DataReadCSV = csv.DictReader(file, delimiter=',')
            for csvcolumn in DataReadCSV:
                Data = csvcolumn['value'][0:6]
                ttk.Label(main, text=Data).grid(column=ColumnVysledky + 3, row=6 + RowShift)
    # VIFp
    MetricResultPath = WorkDirWindows + "\\Score_avif_Q" + str(Quality_AVIF) + "_vifp.csv"
    if os.path.isfile(MetricResultPath) == True:
        with open(MetricResultPath) as file:
            DataReadCSV = csv.DictReader(file, delimiter=',')
            for csvcolumn in DataReadCSV:
                Data = csvcolumn['value'][0:6]
                ttk.Label(main, text=Data).grid(column=ColumnVysledky + 3, row=7 + RowShift)
    # VMAF
    MetricResultPath = WorkDirWindows + "\\ScoreVMAF_avif_Q" + str(Quality_AVIF) + ".txt"
    if os.path.isfile(MetricResultPath) == True:
        with open(MetricResultPath,'r') as file:
            txtvalue = file.readline()
            txtvalue = txtvalue[txtvalue.find('vmaf: '):]
            Data = txtvalue[6:12]
            file.close()
            ttk.Label(main, text=Data).grid(column=ColumnVysledky + 3, row=8 + RowShift)
    # FSIMc
    MetricResultPath = WorkDirWindows + "\\ScoreFSIMc_avif_Q" + str(Quality_AVIF) + ".txt"
    if os.path.isfile(MetricResultPath) == True:
        with open(MetricResultPath,'r') as file:
            Data = file.readline()
            file.close()
            ttk.Label(main, text=Data).grid(column=ColumnVysledky + 3, row=9 + RowShift)
    # GMSD
    MetricResultPath = WorkDirWindows + "\\ScoreGMSD_avif_Q" + str(Quality_AVIF) + ".txt"
    if os.path.isfile(MetricResultPath) == True:
        with open(MetricResultPath,'r') as file:
            Data = file.readline()
            file.close()
            ttk.Label(main, text=Data).grid(column=ColumnVysledky + 3, row=10 + RowShift)
# HEIC
    # PSNR-HVS-M
    MetricResultPath = WorkDirWindows + "\\Score_heic_Q" + str(Quality_HEIC) + "_psnrhvsm.csv"
    if os.path.isfile(MetricResultPath) == True:
        with open(MetricResultPath) as file:
            DataReadCSV = csv.DictReader(file, delimiter=',')
            for csvcolumn in DataReadCSV:
                Data = csvcolumn['value'][0:6]
                ttk.Label(main, text=Data).grid(column=ColumnVysledky + 4, row=4 + RowShift)
    # WS-PSNR
    MetricResultPath = WorkDirWindows + "\\ScoreWSPSNR_heic_Q" + str(Quality_HEIC) + ".txt"
    if os.path.isfile(MetricResultPath) == True:
        with open(MetricResultPath,'r') as file:
            txtvalue = file.readline()
            Data = txtvalue[8:14]
            file.close()
            ttk.Label(main, text=Data).grid(column=ColumnVysledky + 4, row=5 + RowShift)
    # MS-SSIM
    MetricResultPath = WorkDirWindows + "\\Score_heic_Q" + str(Quality_HEIC) + "_msssim.csv"
    if os.path.isfile(MetricResultPath) == True:
        with open(MetricResultPath) as file:
            DataReadCSV = csv.DictReader(file, delimiter=',')
            for csvcolumn in DataReadCSV:
                Data = csvcolumn['value'][0:6]
                ttk.Label(main, text=Data).grid(column=ColumnVysledky + 4, row=6 + RowShift)
    # VIFp
    MetricResultPath = WorkDirWindows + "\\Score_heic_Q" + str(Quality_HEIC) + "_vifp.csv"
    if os.path.isfile(MetricResultPath) == True:
        with open(MetricResultPath) as file:
            DataReadCSV = csv.DictReader(file, delimiter=',')
            for csvcolumn in DataReadCSV:
                Data = csvcolumn['value'][0:6]
                ttk.Label(main, text=Data).grid(column=ColumnVysledky + 4, row=7 + RowShift)
    # VMAF
    MetricResultPath = WorkDirWindows + "\\ScoreVMAF_heic_Q" + str(Quality_HEIC) + ".txt"
    if os.path.isfile(MetricResultPath) == True:
        with open(MetricResultPath,'r') as file:
            txtvalue = file.readline()
            txtvalue = txtvalue[txtvalue.find('vmaf: '):]
            Data = txtvalue[6:12]
            file.close()
            ttk.Label(main, text=Data).grid(column=ColumnVysledky + 4, row=8 + RowShift)
    # FSIMc
    MetricResultPath = WorkDirWindows + "\\ScoreFSIMc_heic_Q" + str(Quality_HEIC) + ".txt"
    if os.path.isfile(MetricResultPath) == True:
        with open(MetricResultPath,'r') as file:
            Data = file.readline()
            file.close()
            ttk.Label(main, text=Data).grid(column=ColumnVysledky + 4, row=9 + RowShift)
    # GMSD
    MetricResultPath = WorkDirWindows + "\\ScoreGMSD_heic_Q" + str(Quality_HEIC) + ".txt"
    if os.path.isfile(MetricResultPath) == True:
        with open(MetricResultPath,'r') as file:
            Data = file.readline()
            file.close()
            ttk.Label(main, text=Data).grid(column=ColumnVysledky + 4, row=10 + RowShift)
# VVC Intra
    # PSNR-HVS-M
    MetricResultPath = WorkDirWindows + "\\Score_vvc_Q" + str(Quality_VVC) + "_psnrhvsm.csv"
    if os.path.isfile(MetricResultPath) == True:
        with open(MetricResultPath) as file:
            DataReadCSV = csv.DictReader(file, delimiter=',')
            for csvcolumn in DataReadCSV:
                Data = csvcolumn['value'][0:6]
                ttk.Label(main, text=Data).grid(column=ColumnVysledky + 5, row=4 + RowShift)
    # WS-PSNR
    MetricResultPath = WorkDirWindows + "\\ScoreWSPSNR_vvc_Q" + str(Quality_VVC) + ".txt"
    if os.path.isfile(MetricResultPath) == True:
        with open(MetricResultPath,'r') as file:
            txtvalue = file.readline()
            Data = txtvalue[8:14]
            file.close()
            ttk.Label(main, text=Data).grid(column=ColumnVysledky + 5, row=5 + RowShift)
    # MS-SSIM
    MetricResultPath = WorkDirWindows + "\\Score_vvc_Q" + str(Quality_VVC) + "_msssim.csv"
    if os.path.isfile(MetricResultPath) == True:
        with open(MetricResultPath) as file:
            DataReadCSV = csv.DictReader(file, delimiter=',')
            for csvcolumn in DataReadCSV:
                Data = csvcolumn['value'][0:6]
                ttk.Label(main, text=Data).grid(column=ColumnVysledky + 5, row=6 + RowShift)
    # VIFp
    MetricResultPath = WorkDirWindows + "\\Score_vvc_Q" + str(Quality_VVC) + "_vifp.csv"
    if os.path.isfile(MetricResultPath) == True:
        with open(MetricResultPath) as file:
            DataReadCSV = csv.DictReader(file, delimiter=',')
            for csvcolumn in DataReadCSV:
                Data = csvcolumn['value'][0:6]
                ttk.Label(main, text=Data).grid(column=ColumnVysledky + 5, row=7 + RowShift)
    # VMAF
    MetricResultPath = WorkDirWindows + "\\ScoreVMAF_vvc_Q" + str(Quality_VVC) + ".txt"
    if os.path.isfile(MetricResultPath) == True:
        with open(MetricResultPath,'r') as file:
            txtvalue = file.readline()
            txtvalue = txtvalue[txtvalue.find('vmaf: '):]
            Data = txtvalue[6:12]
            file.close()
            ttk.Label(main, text=Data).grid(column=ColumnVysledky + 5, row=8 + RowShift)
    # FSIMc
    MetricResultPath = WorkDirWindows + "\\ScoreFSIMc_vvc_Q" + str(Quality_VVC) + ".txt"
    if os.path.isfile(MetricResultPath) == True:
        with open(MetricResultPath,'r') as file:
            Data = file.readline()
            file.close()
            ttk.Label(main, text=Data).grid(column=ColumnVysledky + 5, row=9 + RowShift)
    # GMSD
    MetricResultPath = WorkDirWindows + "\\ScoreGMSD_vvc_Q" + str(Quality_VVC) + ".txt"
    if os.path.isfile(MetricResultPath) == True:
        with open(MetricResultPath,'r') as file:
            Data = file.readline()
            file.close()
            ttk.Label(main, text=Data).grid(column=ColumnVysledky + 5, row=10 + RowShift)
# FRICwRNN
    # PSNR-HVS-M
    MetricResultPath = WorkDirWindows + "\\Score_FRICwRNN_Q" + str(Quality_FRICwRNN) + "_psnrhvsm.csv"
    if os.path.isfile(MetricResultPath) == True:
        with open(MetricResultPath) as file:
            DataReadCSV = csv.DictReader(file, delimiter=',')
            for csvcolumn in DataReadCSV:
                Data = csvcolumn['value'][0:6]
                ttk.Label(main, text=Data).grid(column=ColumnVysledky + 6, row=4 + RowShift)
    # WS-PSNR
    MetricResultPath = WorkDirWindows + "\\ScoreWSPSNR_FRICwRNN_Q" + str(Quality_FRICwRNN) + ".txt"
    if os.path.isfile(MetricResultPath) == True:
        with open(MetricResultPath,'r') as file:
            txtvalue = file.readline()
            Data = txtvalue[8:14]
            file.close()
            ttk.Label(main, text=Data).grid(column=ColumnVysledky + 6, row=5 + RowShift)
    # MS-SSIM
    MetricResultPath = WorkDirWindows + "\\Score_FRICwRNN_Q" + str(Quality_FRICwRNN) + "_msssim.csv"
    if os.path.isfile(MetricResultPath) == True:
        with open(MetricResultPath) as file:
            DataReadCSV = csv.DictReader(file, delimiter=',')
            for csvcolumn in DataReadCSV:
                Data = csvcolumn['value'][0:6]
                ttk.Label(main, text=Data).grid(column=ColumnVysledky + 6, row=6 + RowShift)
    # VIFp
    MetricResultPath = WorkDirWindows + "\\Score_FRICwRNN_Q" + str(Quality_FRICwRNN) + "_vifp.csv"
    if os.path.isfile(MetricResultPath) == True:
        with open(MetricResultPath) as file:
            DataReadCSV = csv.DictReader(file, delimiter=',')
            for csvcolumn in DataReadCSV:
                Data = csvcolumn['value'][0:6]
                ttk.Label(main, text=Data).grid(column=ColumnVysledky + 6, row=7 + RowShift)
    # VMAF
    MetricResultPath = WorkDirWindows + "\\ScoreVMAF_FRICwRNN_Q" + str(Quality_FRICwRNN) + ".txt"
    if os.path.isfile(MetricResultPath) == True:
        with open(MetricResultPath,'r') as file:
            txtvalue = file.readline()
            txtvalue = txtvalue[txtvalue.find('vmaf: '):]
            Data = txtvalue[6:12]
            file.close()
            ttk.Label(main, text=Data).grid(column=ColumnVysledky + 6, row=8 + RowShift)
    # FSIMc
    MetricResultPath = WorkDirWindows + "\\ScoreFSIMc_FRICwRNN_Q" + str(Quality_FRICwRNN) + ".txt"
    if os.path.isfile(MetricResultPath) == True:
        with open(MetricResultPath,'r') as file:
            Data = file.readline()
            file.close()
            ttk.Label(main, text=Data).grid(column=ColumnVysledky + 6, row=9 + RowShift)
    # GMSD
    MetricResultPath = WorkDirWindows + "\\ScoreGMSD_FRICwRNN_Q" + str(Quality_FRICwRNN) + ".txt"
    if os.path.isfile(MetricResultPath) == True:
        with open(MetricResultPath,'r') as file:
            Data = file.readline()
            file.close()
            ttk.Label(main, text=Data).grid(column=ColumnVysledky + 6, row=10 + RowShift)
# CAEMfE2EOIC
    # PSNR-HVS-M
    MetricResultPath = WorkDirWindows + "\\Score_CAEMfE2EOIC_Q" + str(Quality_CAEMfE2EOIC) + "_psnrhvsm.csv"
    if os.path.isfile(MetricResultPath) == True:
        with open(MetricResultPath) as file:
            DataReadCSV = csv.DictReader(file, delimiter=',')
            for csvcolumn in DataReadCSV:
                Data = csvcolumn['value'][0:6]
                ttk.Label(main, text=Data).grid(column=ColumnVysledky + 7, row=4 + RowShift)
    # WS-PSNR
    MetricResultPath = WorkDirWindows + "\\ScoreWSPSNR_CAEMfE2EOIC_Q" + str(Quality_CAEMfE2EOIC) + ".txt"
    if os.path.isfile(MetricResultPath) == True:
        with open(MetricResultPath,'r') as file:
            txtvalue = file.readline()
            Data = txtvalue[8:14]
            file.close()
            ttk.Label(main, text=Data).grid(column=ColumnVysledky + 7, row=5 + RowShift)
    # MS-SSIM
    MetricResultPath = WorkDirWindows + "\\Score_CAEMfE2EOIC_Q" + str(Quality_CAEMfE2EOIC) + "_msssim.csv"
    if os.path.isfile(MetricResultPath) == True:
        with open(MetricResultPath) as file:
            DataReadCSV = csv.DictReader(file, delimiter=',')
            for csvcolumn in DataReadCSV:
                Data = csvcolumn['value'][0:6]
                ttk.Label(main, text=Data).grid(column=ColumnVysledky + 7, row=6 + RowShift)
    # VIFp
    MetricResultPath = WorkDirWindows + "\\Score_CAEMfE2EOIC_Q" + str(Quality_CAEMfE2EOIC) + "_vifp.csv"
    if os.path.isfile(MetricResultPath) == True:
        with open(MetricResultPath) as file:
            DataReadCSV = csv.DictReader(file, delimiter=',')
            for csvcolumn in DataReadCSV:
                Data = csvcolumn['value'][0:6]
                ttk.Label(main, text=Data).grid(column=ColumnVysledky + 7, row=7 + RowShift)
    # VMAF
    MetricResultPath = WorkDirWindows + "\\ScoreVMAF_CAEMfE2EOIC_Q" + str(Quality_CAEMfE2EOIC) + ".txt"
    if os.path.isfile(MetricResultPath) == True:
        with open(MetricResultPath,'r') as file:
            txtvalue = file.readline()
            txtvalue = txtvalue[txtvalue.find('vmaf: '):]
            Data = txtvalue[6:12]
            file.close()
            ttk.Label(main, text=Data).grid(column=ColumnVysledky + 7, row=8 + RowShift)
    # FSIMc
    MetricResultPath = WorkDirWindows + "\\ScoreFSIMc_CAEMfE2EOIC_Q" + str(Quality_CAEMfE2EOIC) + ".txt"
    if os.path.isfile(MetricResultPath) == True:
        with open(MetricResultPath,'r') as file:
            Data = file.readline()
            file.close()
            ttk.Label(main, text=Data).grid(column=ColumnVysledky + 7, row=9 + RowShift)
    # GMSD
    MetricResultPath = WorkDirWindows + "\\ScoreGMSD_CAEMfE2EOIC_Q" + str(Quality_CAEMfE2EOIC) + ".txt"
    if os.path.isfile(MetricResultPath) == True:
        with open(MetricResultPath,'r') as file:
            Data = file.readline()
            file.close()
            ttk.Label(main, text=Data).grid(column=ColumnVysledky + 7, row=10 + RowShift)
# HiFiC
    # PSNR-HVS-M
    MetricResultPath = WorkDirWindows + "\\Score_HiFiC_Q" + str(Quality_HiFiC) + "_psnrhvsm.csv"
    if os.path.isfile(MetricResultPath) == True:
        with open(MetricResultPath) as file:
            DataReadCSV = csv.DictReader(file, delimiter=',')
            for csvcolumn in DataReadCSV:
                Data = csvcolumn['value'][0:6]
                ttk.Label(main, text=Data).grid(column=ColumnVysledky + 8, row=4 + RowShift)
    # WS-PSNR
    MetricResultPath = WorkDirWindows + "\\ScoreWSPSNR_HiFiC_Q" + str(Quality_HiFiC) + ".txt"
    if os.path.isfile(MetricResultPath) == True:
        with open(MetricResultPath,'r') as file:
            txtvalue = file.readline()
            Data = txtvalue[8:14]
            file.close()
            ttk.Label(main, text=Data).grid(column=ColumnVysledky + 8, row=5 + RowShift)
    # MS-SSIM
    MetricResultPath = WorkDirWindows + "\\Score_HiFiC_Q" + str(Quality_HiFiC) + "_msssim.csv"
    if os.path.isfile(MetricResultPath) == True:
        with open(MetricResultPath) as file:
            DataReadCSV = csv.DictReader(file, delimiter=',')
            for csvcolumn in DataReadCSV:
                Data = csvcolumn['value'][0:6]
                ttk.Label(main, text=Data).grid(column=ColumnVysledky + 8, row=6 + RowShift)
    # VIFp
    MetricResultPath = WorkDirWindows + "\\Score_HiFiC_Q" + str(Quality_HiFiC) + "_vifp.csv"
    if os.path.isfile(MetricResultPath) == True:
        with open(MetricResultPath) as file:
            DataReadCSV = csv.DictReader(file, delimiter=',')
            for csvcolumn in DataReadCSV:
                Data = csvcolumn['value'][0:6]
                ttk.Label(main, text=Data).grid(column=ColumnVysledky + 8, row=7 + RowShift)
    # VMAF
    MetricResultPath = WorkDirWindows + "\\ScoreVMAF_HiFiC_Q" + str(Quality_HiFiC) + ".txt"
    if os.path.isfile(MetricResultPath) == True:
        with open(MetricResultPath,'r') as file:
            txtvalue = file.readline()
            txtvalue = txtvalue[txtvalue.find('vmaf: '):]
            Data = txtvalue[6:12]
            file.close()
            ttk.Label(main, text=Data).grid(column=ColumnVysledky + 8, row=8 + RowShift)
    # FSIMc
    MetricResultPath = WorkDirWindows + "\\ScoreFSIMc_HiFiC_Q" + str(Quality_HiFiC) + ".txt"
    if os.path.isfile(MetricResultPath) == True:
        with open(MetricResultPath,'r') as file:
            Data = file.readline()
            file.close()
            ttk.Label(main, text=Data).grid(column=ColumnVysledky + 8, row=9 + RowShift)
    # GMSD
    MetricResultPath = WorkDirWindows + "\\ScoreGMSD_HiFiC_Q" + str(Quality_HiFiC) + ".txt"
    if os.path.isfile(MetricResultPath) == True:
        with open(MetricResultPath,'r') as file:
            Data = file.readline()
            file.close()
            ttk.Label(main, text=Data).grid(column=ColumnVysledky + 8, row=10 + RowShift)
# LIC360
    # PSNR-HVS-M
    MetricResultPath = WorkDirWindows + "\\Score_LIC360_Q" + str(Quality_LIC360) + "_psnrhvsm.csv"
    if os.path.isfile(MetricResultPath) == True:
        with open(MetricResultPath) as file:
            DataReadCSV = csv.DictReader(file, delimiter=',')
            for csvcolumn in DataReadCSV:
                Data = csvcolumn['value'][0:6]
                ttk.Label(main, text=Data).grid(column=ColumnVysledky + 9, row=4 + RowShift)
    # WS-PSNR
    MetricResultPath = WorkDirWindows + "\\ScoreWSPSNR_LIC360_Q" + str(Quality_LIC360) + ".txt"
    if os.path.isfile(MetricResultPath) == True:
        with open(MetricResultPath,'r') as file:
            txtvalue = file.readline()
            Data = txtvalue[8:14]
            file.close()
            ttk.Label(main, text=Data).grid(column=ColumnVysledky + 9, row=5 + RowShift)
    # MS-SSIM
    MetricResultPath = WorkDirWindows + "\\Score_LIC360_Q" + str(Quality_LIC360) + "_msssim.csv"
    if os.path.isfile(MetricResultPath) == True:
        with open(MetricResultPath) as file:
            DataReadCSV = csv.DictReader(file, delimiter=',')
            for csvcolumn in DataReadCSV:
                Data = csvcolumn['value'][0:6]
                ttk.Label(main, text=Data).grid(column=ColumnVysledky + 9, row=6 + RowShift)
    # VIFp
    MetricResultPath = WorkDirWindows + "\\Score_LIC360_Q" + str(Quality_LIC360) + "_vifp.csv"
    if os.path.isfile(MetricResultPath) == True:
        with open(MetricResultPath) as file:
            DataReadCSV = csv.DictReader(file, delimiter=',')
            for csvcolumn in DataReadCSV:
                Data = csvcolumn['value'][0:6]
                ttk.Label(main, text=Data).grid(column=ColumnVysledky + 9, row=7 + RowShift)
    # VMAF
    MetricResultPath = WorkDirWindows + "\\ScoreVMAF_LIC360_Q" + str(Quality_LIC360) + ".txt"
    if os.path.isfile(MetricResultPath) == True:
        with open(MetricResultPath,'r') as file:
            txtvalue = file.readline()
            txtvalue = txtvalue[txtvalue.find('vmaf: '):]
            Data = txtvalue[6:12]
            file.close()
            ttk.Label(main, text=Data).grid(column=ColumnVysledky + 9, row=8 + RowShift)
    # FSIMc
    MetricResultPath = WorkDirWindows + "\\ScoreFSIMc_LIC360_Q" + str(Quality_LIC360) + ".txt"
    if os.path.isfile(MetricResultPath) == True:
        with open(MetricResultPath,'r') as file:
            Data = file.readline()
            file.close()
            ttk.Label(main, text=Data).grid(column=ColumnVysledky + 9, row=9 + RowShift)
    # GMSD
    MetricResultPath = WorkDirWindows + "\\ScoreGMSD_LIC360_Q" + str(Quality_LIC360) + ".txt"
    if os.path.isfile(MetricResultPath) == True:
        with open(MetricResultPath,'r') as file:
            Data = file.readline()
            file.close()
            ttk.Label(main, text=Data).grid(column=ColumnVysledky + 9, row=10 + RowShift)


ColumnShift = 1
ColumnKodek = ColumnShift
ColumnKvalita = ColumnKodek + 3
ColumnMetrika = ColumnKvalita + 3
ColumnVysledky = ColumnMetrika + 3
RowShift = 1


main = tk.Tk()
main.title ("Deep Learning based 360° Image Compression and Quality Evaluation Framework by Adam Budac")


ttk.Label(main, text="        "        ).grid(column=0, row=0) # Gap: pravy horny roh
ttk.Label(main, text=""                ).grid(column=ColumnShift, row=2 + RowShift) # Gap: Image width - Kodek
ttk.Label(main, text="                ").grid(column=ColumnKvalita + 2, row=2 + RowShift) # Gap: Kvalita - Metrika
ttk.Label(main, text="                ").grid(column=ColumnMetrika + 2, row=2 + RowShift) # Gap: Metrika - 


#ttk.Label(main, text="Vybrať obrázok:").grid(column=ColumnShift, row=RowShift)
action = ttk.Button(main, text="Vybrať obrázok", command=LoadFile)
action.grid(column=ColumnShift, row=RowShift)
ttk.Label(main, text="Rozmery obrázku:").grid(column=ColumnShift, row=RowShift + 1)

#Filename = NewEntry(0 + ColumnShift, 1 + RowShift, 10)
#ImageWidth = NewEntry(1 + ColumnShift, 1 + RowShift, 4)


ttk.Label(main, text="Kodek"      ).grid(column=ColumnKodek, row=3 + RowShift)
ttk.Label(main, text="JPEG"       ).grid(column=ColumnKodek, row=4 + RowShift)
ttk.Label(main, text="JPEG XL"    ).grid(column=ColumnKodek, row=5 + RowShift)
ttk.Label(main, text="AVIF"       ).grid(column=ColumnKodek, row=6 + RowShift)
ttk.Label(main, text="HEIC"       ).grid(column=ColumnKodek, row=7 + RowShift)
ttk.Label(main, text="VVC Intra"  ).grid(column=ColumnKodek, row=8 + RowShift)
ttk.Label(main, text="FRICwRNN"   ).grid(column=ColumnKodek, row=9 + RowShift)
ttk.Label(main, text="CAEMfE2EOIC").grid(column=ColumnKodek, row=10 + RowShift)
ttk.Label(main, text="HiFiC"      ).grid(column=ColumnKodek, row=11 + RowShift)
ttk.Label(main, text="LIC360"     ).grid(column=ColumnKodek, row=12 + RowShift)

CheckCodecJPEG        = tk.IntVar()
CheckCodecJPEGXL      = tk.IntVar()
CheckCodecAVIF        = tk.IntVar()
CheckCodecHEIC        = tk.IntVar()
CheckCodecVVCIntra    = tk.IntVar()
CheckCodecFRICwRNN    = tk.IntVar()
CheckCodecCAEMfE2EOIC = tk.IntVar()
CheckCodecHiFiC       = tk.IntVar()
CheckCodecLIC360      = tk.IntVar()

CheckJPEG        = tk.Checkbutton(main, variable=CheckCodecJPEG,        onvalue=1, offvalue=0, command=CheckCodec)
CheckJPEGXL      = tk.Checkbutton(main, variable=CheckCodecJPEGXL,      onvalue=1, offvalue=0, command=CheckCodec)
CheckAVIF        = tk.Checkbutton(main, variable=CheckCodecAVIF,        onvalue=1, offvalue=0, command=CheckCodec)
CheckHEIC        = tk.Checkbutton(main, variable=CheckCodecHEIC,        onvalue=1, offvalue=0, command=CheckCodec)
CheckVVCIntra    = tk.Checkbutton(main, variable=CheckCodecVVCIntra,    onvalue=1, offvalue=0, command=CheckCodec)
CheckFRICwRNN    = tk.Checkbutton(main, variable=CheckCodecFRICwRNN,    onvalue=1, offvalue=0, command=CheckCodec)
CheckCAEMfE2EOIC = tk.Checkbutton(main, variable=CheckCodecCAEMfE2EOIC, onvalue=1, offvalue=0, command=CheckCodec)
CheckHiFiC       = tk.Checkbutton(main, variable=CheckCodecHiFiC,       onvalue=1, offvalue=0, command=CheckCodec)
CheckLIC360      = tk.Checkbutton(main, variable=CheckCodecLIC360,      onvalue=1, offvalue=0, command=CheckCodec)

CheckJPEG.select()
CheckJPEGXL.select()
CheckAVIF.select()
CheckHEIC.select()
CheckVVCIntra.select()
CheckFRICwRNN.select()
CheckCAEMfE2EOIC.select()
CheckHiFiC.select()
CheckLIC360.select()

CheckJPEG.grid        (column=ColumnKodek + 1, row=4 + RowShift, sticky=tk.W)
CheckJPEGXL.grid      (column=ColumnKodek + 1, row=5 + RowShift, sticky=tk.W)
CheckAVIF.grid        (column=ColumnKodek + 1, row=6 + RowShift, sticky=tk.W)
CheckHEIC.grid        (column=ColumnKodek + 1, row=7 + RowShift, sticky=tk.W)
CheckVVCIntra.grid    (column=ColumnKodek + 1, row=8 + RowShift, sticky=tk.W)
CheckFRICwRNN.grid    (column=ColumnKodek + 1, row=9 + RowShift, sticky=tk.W)
CheckCAEMfE2EOIC.grid (column=ColumnKodek + 1, row=10 + RowShift, sticky=tk.W)
CheckHiFiC.grid       (column=ColumnKodek + 1, row=11 + RowShift, sticky=tk.W)
CheckLIC360.grid      (column=ColumnKodek + 1, row=12 + RowShift, sticky=tk.W)

ttk.Label(main, text="Kvalita/QP").grid(column=ColumnKvalita, row=3 + RowShift)
ttk.Label(main, text= str(Q_min_JPEG)        + " - " + str(Q_max_JPEG)        + ":").grid(column=ColumnKvalita, row=4 + RowShift)
ttk.Label(main, text= str(Q_min_JPEGXL)      + " - " + str(Q_max_JPEGXL)      + ":").grid(column=ColumnKvalita, row=5 + RowShift)
ttk.Label(main, text= str(Q_min_AVIF)        + " - " + str(Q_max_AVIF)        + ":").grid(column=ColumnKvalita, row=6 + RowShift)
ttk.Label(main, text= str(Q_min_HEIC)        + " - " + str(Q_max_HEIC)        + ":").grid(column=ColumnKvalita, row=7 + RowShift)
ttk.Label(main, text= str(Q_min_VVCIntra)    + " - " + str(Q_max_VVCIntra)    + ":").grid(column=ColumnKvalita, row=8 + RowShift)
ttk.Label(main, text= str(Q_min_FRICwRNN)    + " - " + str(Q_max_FRICwRNN)    + ":").grid(column=ColumnKvalita, row=9 + RowShift)
ttk.Label(main, text= str(Q_min_CAEMfE2EOIC) + " - " + str(Q_max_CAEMfE2EOIC) + ":").grid(column=ColumnKvalita, row=10 + RowShift)
ttk.Label(main, text= str(Q_min_HiFiC)       + " - " + str(Q_max_HiFiC)       + ":").grid(column=ColumnKvalita, row=11 + RowShift)
ttk.Label(main, text= str(Q_min_LIC360)      + " - " + str(Q_max_LIC360)      + ":").grid(column=ColumnKvalita, row=12 + RowShift)

Quality_JPEG_Entry        = NewEntry(4 + RowShift,  ColumnKvalita + 1, 3)
Quality_JPEGXL_Entry      = NewEntry(5 + RowShift,  ColumnKvalita + 1, 3)
Quality_AVIF_Entry        = NewEntry(6 + RowShift,  ColumnKvalita + 1, 3)
Quality_HEIC_Entry        = NewEntry(7 + RowShift,  ColumnKvalita + 1, 3)
Quality_VVC_Entry         = NewEntry(8 + RowShift,  ColumnKvalita + 1, 3)
Quality_FRICwRNN_Entry    = NewEntry(9 + RowShift,  ColumnKvalita + 1, 3)
Quality_CAEMfE2EOIC_Entry = NewEntry(10 + RowShift, ColumnKvalita + 1, 3)
Quality_HiFiC_Entry       = NewEntry(11 + RowShift, ColumnKvalita + 1, 3)
Quality_LIC360_Entry      = NewEntry(12 + RowShift, ColumnKvalita + 1, 3)

Quality_JPEG_Entry.insert(0,Q_max_JPEG)
Quality_JPEGXL_Entry.insert(0,Q_max_JPEGXL)
Quality_AVIF_Entry.insert(0,Q_min_AVIF)
Quality_HEIC_Entry.insert(0,Q_min_HEIC)
Quality_VVC_Entry.insert(0,Q_min_VVCIntra)
Quality_FRICwRNN_Entry.insert(0,Q_max_FRICwRNN)
Quality_CAEMfE2EOIC_Entry.insert(0,Q_max_CAEMfE2EOIC)
Quality_HiFiC_Entry.insert(0,Q_max_HiFiC)
Quality_LIC360_Entry.insert(0,Q_max_LIC360)

ttk.Label(main, text="Metrika"   ).grid(column=ColumnMetrika, row=3 + RowShift)
ttk.Label(main, text="PSNR-HVS-M").grid(column=ColumnMetrika, row=4 + RowShift)
ttk.Label(main, text="WS-PSNR"   ).grid(column=ColumnMetrika, row=5 + RowShift)
ttk.Label(main, text="MS-SSIM"   ).grid(column=ColumnMetrika, row=6 + RowShift)
ttk.Label(main, text="VIFp"      ).grid(column=ColumnMetrika, row=7 + RowShift)
ttk.Label(main, text="VMAF"      ).grid(column=ColumnMetrika, row=8 + RowShift)
ttk.Label(main, text="FSIMc"     ).grid(column=ColumnMetrika, row=9 + RowShift)
ttk.Label(main, text="GMSD"      ).grid(column=ColumnMetrika, row=10 + RowShift)

CheckMetricPSNRHVSM = tk.IntVar()
CheckMetricWSPSNR   = tk.IntVar()
CheckMetricMSSSIM   = tk.IntVar()
CheckMetricVIFp     = tk.IntVar()
CheckMetricVMAF     = tk.IntVar()
CheckMetricFSIMc    = tk.IntVar()
CheckMetricGMSD     = tk.IntVar()

CheckPSNRHVSM = tk.Checkbutton(main, variable=CheckMetricPSNRHVSM, onvalue=1, offvalue=0, command=CheckMetric)
CheckWSPSNR   = tk.Checkbutton(main, variable=CheckMetricWSPSNR,   onvalue=1, offvalue=0, command=CheckMetric)
CheckMSSSIM   = tk.Checkbutton(main, variable=CheckMetricMSSSIM,   onvalue=1, offvalue=0, command=CheckMetric)
CheckVIFp     = tk.Checkbutton(main, variable=CheckMetricVIFp,     onvalue=1, offvalue=0, command=CheckMetric)
CheckVMAF     = tk.Checkbutton(main, variable=CheckMetricVMAF,     onvalue=1, offvalue=0, command=CheckMetric)
CheckFSIMc    = tk.Checkbutton(main, variable=CheckMetricFSIMc,    onvalue=1, offvalue=0, command=CheckMetric)
CheckGMSD     = tk.Checkbutton(main, variable=CheckMetricGMSD,     onvalue=1, offvalue=0, command=CheckMetric)

CheckPSNRHVSM.select()
CheckWSPSNR.select()
CheckMSSSIM.select()
CheckVIFp.select()
CheckVMAF.select()
CheckFSIMc.select()
CheckGMSD.select()

CheckPSNRHVSM.grid (column=ColumnMetrika + 1, row=4 + RowShift, sticky=tk.W)
CheckWSPSNR.grid   (column=ColumnMetrika + 1, row=5 + RowShift, sticky=tk.W)
CheckMSSSIM.grid   (column=ColumnMetrika + 1, row=6 + RowShift, sticky=tk.W)
CheckVIFp.grid     (column=ColumnMetrika + 1, row=7 + RowShift, sticky=tk.W)
CheckVMAF.grid     (column=ColumnMetrika + 1, row=8 + RowShift, sticky=tk.W)
CheckFSIMc.grid    (column=ColumnMetrika + 1, row=9 + RowShift, sticky=tk.W)
CheckGMSD.grid     (column=ColumnMetrika + 1, row=10 + RowShift, sticky=tk.W)


ttk.Label(main, text="Výsledky"   ).grid(column=ColumnVysledky, row=RowShift)
ttk.Label(main, text="Kodek:"     ).grid(column=ColumnVysledky, row=1 + RowShift)
ttk.Label(main, text="Kvalita/QP:").grid(column=ColumnVysledky, row=2 + RowShift)
ttk.Label(main, text="BPP:"       ).grid(column=ColumnVysledky, row=3 + RowShift)

ttk.Label(main, text="              JPEG    ").grid(column=ColumnVysledky + 1, row=1 + RowShift)
ttk.Label(main, text="    JPEGXL    "        ).grid(column=ColumnVysledky + 2, row=1 + RowShift)
ttk.Label(main, text="    AVIF    "          ).grid(column=ColumnVysledky + 3, row=1 + RowShift)
ttk.Label(main, text="    HEIC    "          ).grid(column=ColumnVysledky + 4, row=1 + RowShift)
ttk.Label(main, text="    VVC Intra    "     ).grid(column=ColumnVysledky + 5, row=1 + RowShift)
ttk.Label(main, text="    FRICwRNN    "      ).grid(column=ColumnVysledky + 6, row=1 + RowShift)
ttk.Label(main, text="    CAEMfE2EOIC    "   ).grid(column=ColumnVysledky + 7, row=1 + RowShift)
ttk.Label(main, text="    HiFiC    "         ).grid(column=ColumnVysledky + 8, row=1 + RowShift)
ttk.Label(main, text="    LIC360    "        ).grid(column=ColumnVysledky + 9, row=1 + RowShift)

ttk.Label(main, text="PSNR-HVS-M:").grid(column=ColumnVysledky, row=4 + RowShift)
ttk.Label(main, text="WS-PSNR:"   ).grid(column=ColumnVysledky, row=5 + RowShift)
ttk.Label(main, text="MS-SSIM:"   ).grid(column=ColumnVysledky, row=6 + RowShift)
ttk.Label(main, text="VIFp:"      ).grid(column=ColumnVysledky, row=7 + RowShift)
ttk.Label(main, text="VMAF:"      ).grid(column=ColumnVysledky, row=8 + RowShift)
ttk.Label(main, text="FSIMc:"     ).grid(column=ColumnVysledky, row=9 + RowShift)
ttk.Label(main, text="GMSD:"      ).grid(column=ColumnVysledky, row=10 + RowShift)

ttk.Label(main, text="Čas kompresie:").grid(column=ColumnVysledky, row=11 + RowShift)

ttk.Label(main, text=" "                 ).grid(column=ColumnVysledky, row=13 + RowShift)
ttk.Label(main, text="Referenčný obrázok").grid(column=ColumnVysledky, row=14 + RowShift)
canvas = Canvas(main, width = 512, height = 256)
canvas.grid(column=ColumnShift, row=15 + RowShift, columnspan=16)

action = ttk.Button(main, text="Spracovať", command=Process)
action.grid(column=ColumnMetrika, row=RowShift)

exit_button = Button(main, text="Koniec", command=main.destroy).grid(column=ColumnShift, row=RowShift + 14)

# Definicia funkcii kompresie a dekompresie
# Priprava referencneho suboru
def Compress_Reference():
    # Priprava BMP
    command = "ffmpeg -y -i " + Filename + ".png -pix_fmt rgb24 " + Filename + ".bmp"
    subprocess.call(command,shell=True)
    # Priprava Y4M 444
    command = "ffmpeg -y -i " + Filename + ".png -pix_fmt yuv444p " + Filename + "_444.y4m"
    subprocess.call(command,shell=True)
    # Priprava YUV 444
    command = "ffmpeg -y -i " + Filename + ".png -pix_fmt yuv444p " + Filename + "_444.yuv"
    subprocess.call(command,shell=True)
    # Priprava YUV 420
    command = "ffmpeg -y -i " + Filename + ".png -pix_fmt yuv420p " + Filename + "_420.yuv"
    subprocess.call(command,shell=True)
    # Priprava PGM
    command = "ffmpeg -y -i " + Filename + ".png " + Filename + ".pgm"
    subprocess.call(command,shell=True)

# Kompresia a dekompresia JPEG
def Compress_JPEG():
    global Q
    Q = Quality_JPEG
    # JPEG kompresia
    command = "cjpeg -quality " + str(Q) + " -optimize -outfile " + Filename + "jpg_Q" + str(Q) + ".jpg " + Filename + ".bmp"
    CasovacStart = timer()
    subprocess.call(command,shell=True)
    CasovacEnd = timer()
    # JPEG dekompresia
    command = "djpeg -bmp -outfile " + Filename + "jpg_Q" + str(Q) + ".bmp " + Filename + "jpg_Q" + str(Q) + ".jpg"
    subprocess.call(command,shell=True)
    # PNG
    command = "ffmpeg -y -i " + Filename + "jpg_Q" + str(Q) + ".bmp -pix_fmt rgb24 " + Filename + "jpg_Q" + str(Q) + ".png"
    subprocess.call(command,shell=True)
    # Y4M 444
    command = "ffmpeg -y -i " + Filename + "jpg_Q" + str(Q) + ".png -pix_fmt yuv444p " + Filename + "jpg_Q" + str(Q) + "_444.y4m"
    subprocess.call(command,shell=True)
    # YUV 444
    command = "ffmpeg -y -i " + Filename + "jpg_Q" + str(Q) + ".png -pix_fmt yuv444p " + Filename + "jpg_Q" + str(Q) + "_444.yuv"
    subprocess.call(command,shell=True)
    # YUV 420
    command = "ffmpeg -y -i " + Filename + "jpg_Q" + str(Q) + ".png -pix_fmt yuv420p " + Filename + "jpg_Q" + str(Q) + "_420.yuv"
    subprocess.call(command,shell=True)
    # PGM
    command = "ffmpeg -y -i " + Filename + "jpg_Q" + str(Q) + ".png " + Filename + "jpg_Q" + str(Q) + ".pgm"
    subprocess.call(command,shell=True)
    Casovac = CasovacEnd - CasovacStart
    Cas = time.strftime("%H:%M:%S", time.gmtime(Casovac))
    ttk.Label(main, text="          " + Cas).grid(column=ColumnVysledky + 1, row=11 + RowShift)

# Kompresia a dekompresia JPEG XL
def Compress_JPEG_XL():
    global Q
    Q = Quality_JPEGXL
    # JPEG_XL kompresia
    command = "cjxl " + Filename + ".png " + Filename + "jxl_Q" + str(Q) + ".jxl -q " + str(Q) + " -e 9 --brotli_effort 11 --num_threads=-1 -P 15"
    CasovacStart = timer()
    subprocess.call(command,shell=True)
    CasovacEnd = timer()
    # JPEG_XL dekompresia
    command = "djxl " + Filename + "jxl_Q" + str(Q) + ".jxl " + Filename + "jxl_Q" + str(Q) + ".png --num_threads=12 --bits_per_sample=8"
    subprocess.call(command,shell=True)
    # Y4M 444
    command = "ffmpeg -y -i " + Filename + "jxl_Q" + str(Q) + ".png -pix_fmt yuv444p " + Filename + "jxl_Q" + str(Q) + "_444.y4m"
    subprocess.call(command,shell=True)
    # YUV 444
    command = "ffmpeg -y -i " + Filename + "jxl_Q" + str(Q) + ".png -pix_fmt yuv444p " + Filename + "jxl_Q" + str(Q) + "_444.yuv"
    subprocess.call(command,shell=True)
    # YUV 420
    command = "ffmpeg -y -i " + Filename + "jxl_Q" + str(Q) + ".png -pix_fmt yuv420p " + Filename + "jxl_Q" + str(Q) + "_420.yuv"
    subprocess.call(command,shell=True)
    # PGM
    command = "ffmpeg -y -i " + Filename + "jxl_Q" + str(Q) + ".png " + Filename + "jxl_Q" + str(Q) + ".pgm"
    subprocess.call(command,shell=True)
    Casovac = CasovacEnd - CasovacStart
    Cas = time.strftime("%H:%M:%S", time.gmtime(Casovac))
    ttk.Label(main, text=Cas).grid(column=ColumnVysledky + 2, row=11 + RowShift)

# Kompresia a dekompresia AVIF
def Compress_AVIF():
    global Q
    Q = Quality_AVIF
    # AVIF kompresia
    command = "avifenc -j all -d 8 -y 420 -r f --min " + str(Q) + " --max " + str(Q) + " -s 0 -c aom --ignore-exif --ignore-xmp --ignore-icc -a enable-chroma-deltaq=1 -a tune=ssim " + Filename + ".png " + Filename + "avif_Q" + str(Q) + ".avif"
    CasovacStart = timer()
    subprocess.call(command,shell=True)
    CasovacEnd = timer()
    # AVIF dekompresia
    command = "avifdec -j all -c aom -d 8 --png-compress 0 -u best -- " + Filename + "avif_Q" + str(Q) + ".avif " + Filename + "avif_Q" + str(Q) + ".png"
    subprocess.call(command,shell=True)
    # Y4M 444
    command = "ffmpeg -y -i " + Filename + "avif_Q" + str(Q) + ".png -pix_fmt yuv444p " + Filename + "avif_Q" + str(Q) + "_444.y4m"
    subprocess.call(command,shell=True)
    # YUV 444
    command = "ffmpeg -y -i " + Filename + "avif_Q" + str(Q) + ".png -pix_fmt yuv444p " + Filename + "avif_Q" + str(Q) + "_444.yuv"
    subprocess.call(command,shell=True)
    # YUV 420
    command = "ffmpeg -y -i " + Filename + "avif_Q" + str(Q) + ".png -pix_fmt yuv420p " + Filename + "avif_Q" + str(Q) + "_420.yuv"
    subprocess.call(command,shell=True)
    # PGM
    command = "ffmpeg -y -i " + Filename + "avif_Q" + str(Q) + ".png " + Filename + "avif_Q" + str(Q) + ".pgm"
    subprocess.call(command,shell=True)
    Casovac = CasovacEnd - CasovacStart
    Cas = time.strftime("%H:%M:%S", time.gmtime(Casovac))
    ttk.Label(main, text=Cas).grid(column=ColumnVysledky + 3, row=11 + RowShift)

# Kompresia a dekompresia HEIC
def Compress_HEIC():
    global Q
    Q = Quality_HEIC
    # HEIC kompresia
    command = "TAppEncoder -c c:\HEIC\cfg\encoder_intra_main.cfg -i " + Filename + "_444.yuv -b " + Filename + "heic_Q" + str(Q) + ".bin -o " + Filename + "heic_Q" + str(Q) + "_420.yuv -wdt " + str(width) + " -hgt " + str(height) + " --InputBitDepth=8 --OutputBitDepth=8 --InputChromaFormat=444 -cf 420 -fr 1 -f 1 --Profile=main --Level=6.2 -q " + str(Q) + " --VideoFullRange"
    CasovacStart = timer()
    subprocess.call(command,shell=True)
    CasovacEnd = timer()
    # HEIC dekompresia
    command = "TAppDecoder -b " + Filename + "heic_Q" + str(Q) + ".bin -o " + Filename + "heic_Q" + str(Q) + "_420.yuv"
    subprocess.call(command,shell=True)
    # YUV 444
    command = "ffmpeg -y -f rawvideo -video_size " + str(width) + "x" + str(height) + " -pix_fmt yuv420p -i " + Filename + "heic_Q" + str(Q) + "_420.yuv -pix_fmt yuv444p " + Filename + "heic_Q" + str(Q) + "_444.yuv"    
    subprocess.call(command,shell=True)
    # Y4M 444
    command = "ffmpeg -y -f rawvideo -video_size " + str(width) + "x" + str(height) + " -pix_fmt yuv444p -i " + Filename + "heic_Q" + str(Q) + "_444.yuv " + Filename + "heic_Q" + str(Q) + "_444.y4m"
    subprocess.call(command,shell=True)
    # PNG
    command = "ffmpeg -y -i " + Filename + "heic_Q" + str(Q) + "_444.y4m " + Filename + "heic_Q" + str(Q) + ".png"
    subprocess.call(command,shell=True)
    # PGM
    command = "ffmpeg -y -i " + Filename + "heic_Q" + str(Q) + ".png " + Filename + "heic_Q" + str(Q) + ".pgm"
    subprocess.call(command,shell=True)
    Casovac = CasovacEnd - CasovacStart
    Cas = time.strftime("%H:%M:%S", time.gmtime(Casovac))
    ttk.Label(main, text=Cas).grid(column=ColumnVysledky + 4, row=11 + RowShift)

# Kompresia a dekompresia VVC_Intra
def Compress_VVC_Intra():
    global Q
    Q = Quality_VVC
    # VVC_Intra kompresia
    command = "vvencapp -i " + Filename + "_420.yuv -s " + str(width) + "x" + str(height) + " -c yuv420 -r 1 -f 1 -o " + Filename + "vvc_Q" + str(Q) + ".266 --preset=slower -b 0 -q " + str(Q) + " -t 8 --tiles 4x4 --profile=main_10_still_picture --level=6.2"
    CasovacStart = timer()
    subprocess.call(command,shell=True)
    CasovacEnd = timer()
    # VVC_Intra dekompresia
    command = "vvdecapp -b " + Filename + "vvc_Q" + str(Q) + ".266 -o " + Filename + "vvc_Q" + str(Q) + "_420p10le.yuv -t 0"
    subprocess.call(command,shell=True)
    # YUV 420
    command = "ffmpeg -y -f rawvideo -video_size " + str(width) + "x" + str(height) + " -pix_fmt yuv420p10le -i " + Filename + "vvc_Q" + str(Q) + "_420p10le.yuv -pix_fmt yuv420p " + Filename + "vvc_Q" + str(Q) + "_420.yuv"
    subprocess.call(command,shell=True)
    # YUV 420p10LE Delete
    command = "del " + Filename + "vvc_Q" + str(Q) + "_420p10le.yuv"
    subprocess.call(command,shell=True)
    # YUV 444
    command = "ffmpeg -y -f rawvideo -video_size " + str(width) + "x" + str(height) + " -pix_fmt yuv420p -i " + Filename + "vvc_Q" + str(Q) + "_420.yuv -pix_fmt yuv444p " + Filename + "vvc_Q" + str(Q) + "_444.yuv"
    subprocess.call(command,shell=True)
    # Y4M 444
    command = "ffmpeg -y -f rawvideo -video_size " + str(width) + "x" + str(height) + " -pix_fmt yuv444p -i " + Filename + "vvc_Q" + str(Q) + "_444.yuv " + Filename + "vvc_Q" + str(Q) + "_444.y4m"
    subprocess.call(command,shell=True)
    # PNG
    command = "ffmpeg -y -i " + Filename + "vvc_Q" + str(Q) + "_444.y4m " + Filename + "vvc_Q" + str(Q) + ".png"
    subprocess.call(command,shell=True)
    # PGM
    command = "ffmpeg -y -i " + Filename + "vvc_Q" + str(Q) + ".png " + Filename + "vvc_Q" + str(Q) + ".pgm"
    subprocess.call(command,shell=True)
    Casovac = CasovacEnd - CasovacStart
    Cas = time.strftime("%H:%M:%S", time.gmtime(Casovac))
    ttk.Label(main, text=Cas).grid(column=ColumnVysledky + 5, row=11 + RowShift)

# Kompresia a dekompresia Full Resolution Image Compression with Recurrent Neural Networks
def Compress_FRICwRNN():
    global Q
    Q = Quality_FRICwRNN
    if Q > 9:
        QGapFRICwRNN = ""
    else:
        QGapFRICwRNN = "0"
    # Cas na ustalenie a vycistenie CPU, GPU a RAM
    time.sleep(1)
    # FRICwRNN kompresia a dekompresia
    command = "C:\\ProgramData\\Anaconda3\\python.exe C:\\ProgramData\\Anaconda3\\cwp.py C:\\ProgramData\\Anaconda3\\envs\\FRICwRNN C:\\ProgramData\\Anaconda3\\envs\\FRICwRNN\\python.exe C:\\ProgramData\\Anaconda3\\envs\\FRICwRNN\\_GITHUB\\image_encoder\\encoder.py --input_image=" + Path + " --output_codes=" + Head + "/" + Filename +"FRICwRNN_Q" + str(Q) + ".npz --iteration=" + str(Q) + " --model=C:\\ProgramData\\Anaconda3\\envs\\FRICwRNN\\_GITHUB\\compression_residual_gru\\residual_gru.pb"
    CasovacStart = timer()
    subprocess.call(command,shell=True)
    CasovacEnd = timer()
    # Presunutie suboru
    shutil.move(Head + "/" + Filename + "FRICwRNN_Q" + str(Q) + ".npz", WorkDirPython + "/" + Filename + "FRICwRNN_Q" + str(Q) + ".npz")
    # FRICwRNN dekompresia    
    command = "C:\\ProgramData\\Anaconda3\\python.exe C:\\ProgramData\\Anaconda3\\cwp.py C:\\ProgramData\\Anaconda3\\envs\\FRICwRNN C:\\ProgramData\\Anaconda3\\envs\\FRICwRNN\\python.exe C:\\ProgramData\\Anaconda3\\envs\\FRICwRNN\\_GITHUB\\image_encoder\\decoder.py --input_codes=" + WorkDirPython + "/" + Filename + "FRICwRNN_Q" + str(Q) + ".npz --output_directory=" + WorkDirPython + " --model=C:\\ProgramData\\Anaconda3\\envs\\FRICwRNN\\_GITHUB\\compression_residual_gru\\residual_gru.pb"
    subprocess.call(command,shell=True)
    # Premenovanue suboru
    shutil.move(WorkDirPython + "/image_" + QGapFRICwRNN + str(Q) + ".png", WorkDirPython + "/" + Filename + "FRICwRNN_Q" + str(Q) + ".png")
    # Y4M 444
    command = "ffmpeg -y -i " + Filename + "FRICwRNN_Q" + str(Q) + ".png -pix_fmt yuv444p " + Filename + "FRICwRNN_Q" + str(Q) + "_444.y4m"
    subprocess.call(command,shell=True)
    # YUV 444
    command = "ffmpeg -y -i " + Filename + "FRICwRNN_Q" + str(Q) + ".png -pix_fmt yuv444p " + Filename + "FRICwRNN_Q" + str(Q) + "_444.yuv"
    subprocess.call(command,shell=True)
    # YUV 420
    command = "ffmpeg -y -i " + Filename + "FRICwRNN_Q" + str(Q) + ".png -pix_fmt yuv420p " + Filename + "FRICwRNN_Q" + str(Q) + "_420.yuv"
    subprocess.call(command,shell=True)
    # PGM
    command = "ffmpeg -y -i " + Filename + "FRICwRNN_Q" + str(Q) + ".png " + Filename + "FRICwRNN_Q" + str(Q) + ".pgm"
    subprocess.call(command,shell=True)
    Casovac = CasovacEnd - CasovacStart
    Cas = time.strftime("%H:%M:%S", time.gmtime(Casovac))
    ttk.Label(main, text=Cas).grid(column=ColumnVysledky + 6, row=11 + RowShift)

# Kompresia a dekompresia Context-adaptive Entropy Model for End-to-end Optimized Image Compression
def Compress_CAEMfE2EOIC():
    global Q
    Q = Quality_CAEMfE2EOIC
    # Cas na ustalenie a vycistenie CPU, GPU a RAM
    time.sleep(1)
    # CAEMfE2EOIC kompresia a dekompresia
    file = open("batch_CAEMfE2EOIC.bat", "w")
    command = "call activate CAEMfE2EOIC \n pushd C:\ProgramData\Anaconda3\envs\CAEMfE2EOIC\_GITHUB\CA_EntropyModel_Test_v2\ \n python C:\ProgramData\Anaconda3\envs\CAEMfE2EOIC\_GITHUB\CA_EntropyModel_Test_v2\encode.py --model_type 1 --input_path " + WorkDirPython + "/" + Filename + ".png --quality_level " + str(Q) + " \n python C:\ProgramData\Anaconda3\envs\CAEMfE2EOIC\_GITHUB\CA_EntropyModel_Test_v2\decode.py --compressed_file_path C:\ProgramData\Anaconda3\envs\CAEMfE2EOIC\_GITHUB\CA_EntropyModel_Test_v2\compressed_files\\1\\" + str(Q) + "\\" + Filename + ".cmp"                                         
    file.write(command)
    file.close()
    CasovacStart = timer()
    subprocess.call([r'D:\Temp\WorkDir\py\batch_CAEMfE2EOIC.bat'])
    CasovacEnd = timer()
    # Presunutie suboru
    shutil.move("C:/ProgramData/Anaconda3/envs/CAEMfE2EOIC/_GITHUB/CA_EntropyModel_Test_v2/compressed_files/1/" + str(Q) + "/" + Filename + ".cmp", WorkDirPython + "/" + Filename + "CAEMfE2EOIC_Q" + str(Q) + ".cmp")
    shutil.move("C:/ProgramData/Anaconda3/envs/CAEMfE2EOIC/_GITHUB/CA_EntropyModel_Test_v2/compressed_files/1/" + str(Q) + "/" + Filename + ".png", WorkDirPython + "/" + Filename + "CAEMfE2EOIC_Q" + str(Q) + ".png")
    # Y4M 444
    command = "ffmpeg -y -i " + Filename + "CAEMfE2EOIC_Q" + str(Q) + ".png -pix_fmt yuv444p " + Filename + "CAEMfE2EOIC_Q" + str(Q) + "_444.y4m"
    subprocess.call(command,shell=True)
    # YUV 444
    command = "ffmpeg -y -i " + Filename + "CAEMfE2EOIC_Q" + str(Q) + ".png -pix_fmt yuv444p " + Filename + "CAEMfE2EOIC_Q" + str(Q) + "_444.yuv"
    subprocess.call(command,shell=True)
    # YUV 420
    command = "ffmpeg -y -i " + Filename + "CAEMfE2EOIC_Q" + str(Q) + ".png -pix_fmt yuv420p " + Filename + "CAEMfE2EOIC_Q" + str(Q) + "_420.yuv"
    subprocess.call(command,shell=True)
    # PGM
    command = "ffmpeg -y -i " + Filename + "CAEMfE2EOIC_Q" + str(Q) + ".png " + Filename + "CAEMfE2EOIC_Q" + str(Q) + ".pgm"
    subprocess.call(command,shell=True)
    Casovac = (CasovacEnd - CasovacStart)*0.5
    Cas = time.strftime("%H:%M:%S", time.gmtime(Casovac))
    ttk.Label(main, text=Cas).grid(column=ColumnVysledky + 7, row=11 + RowShift)

# Kompresia a dekompresia High-Fidelity Generative Image Compression
def Compress_HiFiC():
    global Q, pngname
    Q = Quality_HiFiC
    # Cas na ustalenie a vycistenie CPU, GPU a RAM
    time.sleep(1)
    # HiFiC kompresia a dekompresia
    if Q == 1:
        model = "low"
    if Q == 2:
        model = "med"
    if Q == 3:
        model = "hi"
    file = open("batch_HiFiC.bat", "w")
    try:
        os.mkdir(WorkDirPython + "/data/")
    except:
        pass
    shutil.copy(WorkDirPython + "/" + Filename + ".png", WorkDirPython + "/data/" + Filename + ".png")
    command = "call activate HiFiC\n python C:\ProgramData\Anaconda3\envs\HiFiC\_GITHUB\compress.py -i " + WorkDirWindows + "/data" + " -ckpt C:\ProgramData\Anaconda3\envs\HiFiC\_GITHUB\models\hific_" + model + ".pt --save"
    file.write(command)
    file.close()
    CasovacStart = timer()
    subprocess.call([r'D:\Temp\WorkDir\py\batch_HiFiC.bat'])
    CasovacEnd = timer()
    # Presunutie suboru
    pngname = glob.glob(WorkDirPython + "/data/reconstructions/inc" + '_RECON*.png')
    #pngname = ''.join(pngname)
    pngname[0] = pngname[0].replace("\\", "/")
    shutil.move(pngname[0], WorkDirPython + "/" + Filename + "HiFiC_Q" + str(Q) + ".png")
    shutil.move(WorkDirPython + "/data/reconstructions/" + Filename + "_compressed.hfc", WorkDirPython + "/" + Filename + "HiFiC_Q" + str(Q) + ".hfc")
    # Y4M 444
    command = "ffmpeg -y -i " + Filename + "HiFiC_Q" + str(Q) + ".png -pix_fmt yuv444p " + Filename + "HiFiC_Q" + str(Q) + "_444.y4m"
    subprocess.call(command,shell=True)
    # YUV 444
    command = "ffmpeg -y -i " + Filename + "HiFiC_Q" + str(Q) + ".png -pix_fmt yuv444p " + Filename + "HiFiC_Q" + str(Q) + "_444.yuv"
    subprocess.call(command,shell=True)
    # YUV 420
    command = "ffmpeg -y -i " + Filename + "HiFiC_Q" + str(Q) + ".png -pix_fmt yuv420p " + Filename + "HiFiC_Q" + str(Q) + "_420.yuv"
    subprocess.call(command,shell=True)
    # PGM
    command = "ffmpeg -y -i " + Filename + "HiFiC_Q" + str(Q) + ".png " + Filename + "HiFiC_Q" + str(Q) + ".pgm"
    subprocess.call(command,shell=True)
    Casovac = (CasovacEnd - CasovacStart)*0.5
    Cas = time.strftime("%H:%M:%S", time.gmtime(Casovac))
    ttk.Label(main, text=Cas).grid(column=ColumnVysledky + 8, row=11 + RowShift)

# Kompresia a dekompresia End-to-End Optimized 360 Image Compression
def Compress_LIC360():
    global Q
    Q = Quality_LIC360
    # Cas na ustalenie a vycistenie CPU, GPU a RAM
    time.sleep(1)
    # LIC360 kompresia a dekompresia
    file = open("batch_LIC360.bat", "w")
    command = "call activate LIC360 \n pushd " + WorkDirWindows +"\ \n python C:\ProgramData\Anaconda3\envs\LIC360\_GITHUB\\test\lic360_demo.py --enc --img-list inc.png --code-list " + Filename + "LIC360_Q" + str(Q) + " --model-idx " + str(Q) + " --ssim \n python C:\ProgramData\Anaconda3\envs\LIC360\_GITHUB\\test\lic360_demo.py --dec --out-list " + Filename + "LIC360_Q" + str(Q) + ".png --code-list " + Filename + "LIC360_Q" + str(Q) + " --model-idx " + str(Q) +" --ssim"                                         
    file.write(command)
    file.close()
    CasovacStart = timer()
    subprocess.call([r'D:\Temp\WorkDir\py\batch_LIC360.bat'])
    CasovacEnd = timer()
    imgLIC360 = Image.open(WorkDirPython + "/" + Filename + "LIC360_Q" + str(Q) + ".png")
    imgLIC360 = imgLIC360.resize((width, height))
    imgLIC360 = imgLIC360.save(WorkDirPython + "/" + Filename + "LIC360_Q" + str(Q) + ".png")
    # Y4M 444
    command = "ffmpeg -y -i " + Filename + "LIC360_Q" + str(Q) + ".png -pix_fmt yuv444p " + Filename + "LIC360_Q" + str(Q) + "_444.y4m"
    subprocess.call(command,shell=True)
    # YUV 444
    command = "ffmpeg -y -i " + Filename + "LIC360_Q" + str(Q) + ".png -pix_fmt yuv444p " + Filename + "LIC360_Q" + str(Q) + "_444.yuv"
    subprocess.call(command,shell=True)
    # YUV 420
    command = "ffmpeg -y -i " + Filename + "LIC360_Q" + str(Q) + ".png -pix_fmt yuv420p " + Filename + "LIC360_Q" + str(Q) + "_420.yuv"
    subprocess.call(command,shell=True)
    # PGM
    command = "ffmpeg -y -i " + Filename + "LIC360_Q" + str(Q) + ".png " + Filename + "LIC360_Q" + str(Q) + ".pgm"
    subprocess.call(command,shell=True)
    Casovac = (CasovacEnd - CasovacStart)*0.5
    Cas = time.strftime("%H:%M:%S", time.gmtime(Casovac))
    ttk.Label(main, text=Cas).grid(column=ColumnVysledky + 9, row=11 + RowShift)



# Definicia funkcii vypoctu metrik
# Vypocet PSNR-HVS-M
def Calculate_PSNR_HVS_M():
    command = "VQMT " + Filename + "_444.yuv " + Filename + kodek + "_Q" + str(Q) + "_444.yuv " + str(width) + " " + str(height) + " 1 3 Score_" + kodek + "_Q" + str(Q) + " PSNRHVSM"
    subprocess.call(command,shell=True)

# Vypocet MS-SSIM
def Calculate_MS_SSIM():
    command = "VQMT " + Filename + "_444.yuv " + Filename + kodek + "_Q" + str(Q) + "_444.yuv " + str(width) + " " + str(height) + " 1 3 Score_" + kodek + "_Q" + str(Q) + " MSSSIM"
    subprocess.call(command,shell=True)

# Vypocet VIFp
def Calculate_VIFp():
    command = "VQMT " + Filename + "_444.yuv " + Filename + kodek + "_Q" + str(Q) + "_444.yuv " + str(width) + " " + str(height) + " 1 3 Score_" + kodek + "_Q" + str(Q) + " VIFP"
    subprocess.call(command,shell=True)

# Vypocet VMAF
def Calculate_VMAF():
    command = "vmaf -r " + Filename + "_444.y4m -d " + Filename + kodek + "_Q" + str(Q) + "_444.y4m -m path=vmaf_v0.6.1.json -o ScoreVMAF_" + kodek + "_Q" + str(Q) + ".txt --sub --threads 12"
    subprocess.call(command,shell=True)

# Vypocet WS-PSNR
def Calculate_WS_PSNR():
    command = "360tools_metric -o " + Filename + "_420.yuv -r " + Filename + kodek + "_Q" + str(Q) + "_420.yuv -w " + str(width) + " -h " + str(height) + " -n 1 -q 3 -f 1 -t 1 -x 1 -y 1 > ScoreWSPSNR_" + kodek + "_Q" + str(Q) + ".txt"
    subprocess.call(command,shell=True)

# Vypocet FSIMc
def Calculate_FSIMc():
    with open('Calculate_FSIMc.m', 'w') as file:
        file.write(" fileID = fopen('ScoreFSIMc_" + kodek + "_Q" + str(Q) + ".txt', 'w');\n imageRef = imread ('" + Filename + ".png');\n imageDis = imread ('" + Filename + kodek + "_Q" + str(Q) + ".png');\n [FSIM, FSIMc] = FeatureSIM(imageRef, imageDis);\n FSIMc\n fprintf(fileID,'%1.4f', FSIMc);\n fclose(fileID);\n ")
    eng = matlab.engine.start_matlab()
    eng.Calculate_FSIMc(nargout=0)
    eng.quit()

# Vypocet GMSD
def Calculate_GMSD():
    with open('Calculate_GMSD.m', 'w') as file:
        file.write(" fileID = fopen('ScoreGMSD_" + kodek + "_Q" + str(Q) + ".txt', 'w');\n Y1 = imread ('" + Filename + ".pgm');\n Y2 = imread ('" + Filename + kodek + "_Q" + str(Q) + ".pgm');\n [score, quality_map] = GMSD(Y1, Y2);\n score\n fprintf(fileID,'%1.4f', score);\n fclose(fileID);\n ")
    eng = matlab.engine.start_matlab()
    eng.Calculate_GMSD(nargout=0)
    eng.quit()


# Definicia funkcie vypoctu BPP
# Vypocet BPP
def Calculate_BPP():
    global BPP
    FilesizeRAW = width * height * 3 * 8
    FilesizeLIC360 = 1024 * 512 * 3 * 8
    CodecExtension = [".jpg",".jxl",".avif",".bin",".266",".npz",".cmp",".hfc",""]

    if kodek == "jpg":
        FilesizeCompressed = os.path.getsize(WorkDirWindows + "\\" + Filename + kodek + "_Q" + str(Q) + CodecExtension[0])
        BPP = (24*8*FilesizeCompressed)/FilesizeRAW
        ttk.Label(main, text="          " + str(BPP)[0:5]).grid(column=ColumnVysledky + 1, row=3 + RowShift)
    elif kodek == "jxl":
        FilesizeCompressed = os.path.getsize(WorkDirWindows + "\\" + Filename + kodek + "_Q" + str(Q) + CodecExtension[1])
        BPP = (24*8*FilesizeCompressed)/FilesizeRAW
        ttk.Label(main, text=str(BPP)[0:5]               ).grid(column=ColumnVysledky + 2, row=3 + RowShift)
    elif kodek == "avif":
        FilesizeCompressed = os.path.getsize(WorkDirWindows + "\\" + Filename + kodek + "_Q" + str(Q) + CodecExtension[2])
        BPP = (24*8*FilesizeCompressed)/FilesizeRAW
        ttk.Label(main, text=str(BPP)[0:5]               ).grid(column=ColumnVysledky + 3, row=3 + RowShift)
    elif kodek == "heic":
        FilesizeCompressed = os.path.getsize(WorkDirWindows + "\\" + Filename + kodek + "_Q" + str(Q) + CodecExtension[3])
        BPP = (24*8*FilesizeCompressed)/FilesizeRAW
        ttk.Label(main, text=str(BPP)[0:5]               ).grid(column=ColumnVysledky + 4, row=3 + RowShift)
    elif kodek == "vvc":
        FilesizeCompressed = os.path.getsize(WorkDirWindows + "\\" + Filename + kodek + "_Q" + str(Q) + CodecExtension[4])
        BPP = (24*8*FilesizeCompressed)/FilesizeRAW
        ttk.Label(main, text=str(BPP)[0:5]               ).grid(column=ColumnVysledky + 5, row=3 + RowShift)
    elif kodek == "FRICwRNN":
        FilesizeCompressed = os.path.getsize(WorkDirWindows + "\\" + Filename + kodek + "_Q" + str(Q) + CodecExtension[5])
        BPP = (24*8*FilesizeCompressed)/FilesizeRAW
        ttk.Label(main, text=str(BPP)[0:5]               ).grid(column=ColumnVysledky + 6, row=3 + RowShift)
    elif kodek == "CAEMfE2EOIC":
        FilesizeCompressed = os.path.getsize(WorkDirWindows + "\\" + Filename + kodek + "_Q" + str(Q) + CodecExtension[6])
        BPP = (24*8*FilesizeCompressed)/FilesizeRAW
        ttk.Label(main, text=str(BPP)[0:5]               ).grid(column=ColumnVysledky + 7, row=3 + RowShift)
    elif kodek == "HiFiC":
        FilesizeCompressed = os.path.getsize(WorkDirWindows + "\\" + Filename + kodek + "_Q" + str(Q) + CodecExtension[7])
        BPP = (24*8*FilesizeCompressed)/FilesizeRAW
        ttk.Label(main, text=str(BPP)[0:5]               ).grid(column=ColumnVysledky + 8, row=3 + RowShift)
    elif kodek == "LIC360":
        FilesizeCompressed = os.path.getsize(WorkDirWindows + "\\" + Filename + kodek + "_Q" + str(Q) + CodecExtension[8])
        BPP = (24*8*FilesizeCompressed)/FilesizeLIC360
        ttk.Label(main, text=str(BPP)[0:5]               ).grid(column=ColumnVysledky + 9, row=3 + RowShift)


#GUI start
main.mainloop()
