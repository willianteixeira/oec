# -*- coding: utf-8 -*-
"""
Created on Tue Jan 17 08:39:41 2023

@author: angelo.milfont
"""

import time
import pandas as pd
import numpy as np

# Lista de arquivos no diretório
import os
from os import listdir, chdir

import os.path
from os.path import isfile, join


def identifica(texto, tamanho):
    """
    """
    lista = []
    long_words = texto.split('/')
    
    for word in long_words:
        lista.append(word.split('\\'))
        
    lista.append(tamanho)

    return lista
    
def organiza_lista(lista):
    """
    """
    nova_lista = []
    for item in lista:
        #print("item ", item)
        cnpj = item[3][0]
        linha = item[4]
        tamanho = item[5]
        # Para cada linha
        tipo = linha[2]
        #detalhe = ""
        #competencia = linha[0]
        nome = linha[1]
        #data = competencia.split('_')
        ano = linha[0]
        mes = linha[1]
        
        #print("linha ", [cnpj, data, nome, tamanho])
        nova_lista.append([cnpj, ano, mes, tipo, nome, tamanho])

    return nova_lista

#
# Início
#

# Diretório de Leitura
caminho_CSV = "C:/Users/angelo.milfont/Documents/MexLab/CSVs/"
caminho_xls = r"C:/Users/angelo.milfont/Documents/MexLab/Excel_Entrada/"
caminho_pickle = r"C:/Users/angelo.milfont/Documents/MexLab/pickle/"


caminho_dir = r"E:/Novos_Projetos_Tributário/Ordem_Reduzida/"

#lista_CNPJs = ['03951550000265','03951550000346','03951550000427','03951550000508',
#               '03951550000699','03951550000770','03951550000850','03951550000931',
#               '03951550001075','03951550001156']
#lista_CNPJs = ['10748214000102']
#lista_CNPJs = ['58026568000161', '58026568000242']

#lista_CNPJs = ['02198937000149']

# Harus
#lista_CNPJs = ['07196444000193',
#               '07196444000274',
#               '07196444000355',
#               '07196444000436',
#               '07196444000517']

# RPB
#lista_CNPJs = ['24382462000189']

# Leoncio
#lista_CNPJs = ['13353586000110',
#               '13353586000381']

# NB Vilaqua
lista_CNPJs = ['05354945000125',
               '05354945000206',
               '05354945000397',
               '05354945000478',
               '05354945000559',
               '05354945000630',
               '05354945000710']

dir_in = caminho_dir

#list_dir = [f for f in listdir(dir_in)] 
#for item in list_dir:
#    print(item)
#lista_CNPJs = list_dir

for cnpj in lista_CNPJs:
    
    dir_in = caminho_dir + cnpj + '/'
    print("Diretorio ", dir_in)
    # assign folder path
    Folderpath = dir_in
    
    # assign size
    size = 0

    print(dir_in)

    arquivos = []
    # get info
    for path, dirs, files in os.walk(Folderpath):
        #print("Arquivo encontrados ", files)
        for f in files:
            fp = os.path.join(path, f)
            tamanho = os.path.getsize(fp)
            arquivos.append(identifica(fp, tamanho))
    
    #for item in arquivos:
    #    print(item)
    #    print()
    
    nova = []
    nova = organiza_lista(arquivos)
    df = pd.DataFrame(nova, columns = ['CNPJ','Ano','Mês','Tipo', 'Nome','Tamanho'])
    #print(df.columns)
    df.to_pickle(caminho_pickle + cnpj + "_XMLs_lidos_CNPJ.pkl")
    lin, col = df.shape
    print("Tamanho da df: ", lin, " x ", col)
    # Habilitar quando df tiver menos do que 1M de linhas
    #df.to_excel(caminho_xls + cnpj+ "_XMLs_lidos_CNPJ.xlsx")
    
    
    max_rows = 900_000
    dataframes = []
    while df.shape[0] > max_rows:
        top = df[:max_rows]
        dataframes.append(top)
        df = df[max_rows:]
    else:
        dataframes.append(df)
    
    i =0
    for _, frame in enumerate(dataframes):
        #frame.to_csv(str(_)+'.csv', index=False)
        frame.to_excel(caminho_xls + cnpj+ "_XMLs_lidos_CNPJ" + str(i) + ".xlsx")
        i += 1
        