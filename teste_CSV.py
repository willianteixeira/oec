# -*- coding: utf-8 -*-
"""
Created on Thu Mar  9 18:32:09 2023

@author: angelo.milfont
"""

import csv   

caminho_CSV = "C:/Users/angelo.milfont/Documents/MexLab/CSVs/"
nome = "teste"

fields=['first','second','third']
with open(caminho_CSV+nome+".csv", 'a') as f:
    writer = csv.writer(f)
    writer.writerow(fields)