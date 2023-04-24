# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import organizacao

# Lista de arquivos no diretório
from os import listdir, chdir

import os
import shutil

from os.path import isfile, join

# Cria Novos Diretórios
from pathlib import Path

import pathlib 

import os.path

import zipfile
#import py7zr
import rarfile

import shutil
import pathlib

import csv

from pyunpack import Archive

def le_Unzip(dir_in, dir_out, arq_csv):
    """

    """
    if(os.path.isdir(join(dir_in)) == True): # É diretório
        print(join(dir_in), " é diretório")
        list_dir = [f for f in listdir(dir_in)] 
        for item in list_dir:
            print(item)
            if isfile(join(dir_in, item)):
                #print(join(dir_in, item), " é arquivo")
                extension = os.path.splitext(item)[1]
                
                if (extension == '.rar'):
                  #print(join(dir_in,item), " é rar.")
                  #if(os.path.isdir(dir_out) == False): # Diretorio não existe, então cria diretório
                  #    #print("Criando dir...", dir_out)
                  #    pathlib.Path(dir_out).mkdir(parents=True, exist_ok=True) 
                  
                  try:
                      rf = rarfile.RarFile(join(dir_in,item))
                      rf.extractall(path = dir_out, members=None, pwd=None)
                      le_Unzip(join(dir_out, item), dir_out, arq_csv)
                  except:
                      print("Erro RAR", item)
                      fields=[join(dir_in,item),'rar']
                      with open(arq_csv, 'a') as f:
                          writer = csv.writer(f)
                          writer.writerow(fields)
                  #os.remove(join(dir_out,item))
              
                elif  (extension == '.zip'):
                    #print(join(dir_in, item), " é zip.")
                    #if(os.path.isdir(dir_out) == False): # Diretorio não existe, então cria diretório
                    #    #print("Criando dir...", dir_out)
                    #    pathlib.Path(dir_out).mkdir(parents=True, exist_ok=True) 
                    
                    try:
                      with zipfile.ZipFile(join(dir_in,item), mode="r") as archive:
                        #print(dir_out)
                        archive.extractall(dir_out)
                        le_Unzip(join(dir_out, item), dir_out, arq_csv)
                          # Funciona também
                          #Archive(join(dir_in,item)).extractall(dir_out)
                          #le_Unzip(join(dir_out, item), dir_out)
                          #os.remove(join(dir_out,item))
                    except zipfile.BadZipFile as error:
                      print("Bad Zip File")  
                      #print(error)
                      fields=[join(dir_in,item),'zip']
                      with open(arq_csv, 'a') as f:
                          writer = csv.writer(f)
                          writer.writerow(fields)
                 
                elif  (extension == '.7z'):
                  #print(join(dir_in, item), " é 7 Zip.")
                  #print("Copiando de : ", join(dir_out,item))
                  #print("  para: ", dir_out + "/"+ item)
                  
                  #if(os.path.isdir(dir_out) == False): # Diretorio não existe, então cria diretório
                  #    #print("Criando dir...", dir_out)
                  #    pathlib.Path(dir_out).mkdir(parents=True, exist_ok=True) 
                  
                  # Descompacta 7 Zip    
                  try:
                      Archive(join(dir_in,item)).extractall(dir_out)
                  except:
                      print("Bad 7.Zip File")  
                      fields=[join(dir_in,item),'7zip']
                      with open(arq_csv, 'a') as f:
                          writer = csv.writer(f)
                          writer.writerow(fields)
            
                elif  (extension == '.xml'):
                  #print(join(dir_in, item), " é xml.")
                  # Copia XML  
                  #print("Copiando XML")
                  #print(join(dir_in,item))
                  #print("para ")
                  #print(join(dir_out,item))
                  
                  shutil.copyfile(join(dir_in,item), join(dir_out,item))
                  
                      
                else:
                  print(join(dir_in, item), " - não considero porque não é zip nem rar, nem 7 Zip, nem xml.")
                                 
            else:
                #print("Não é um arquivo, então verificando... ", join(dir_in, item))
                #if(os.path.isdir(join(dir_in, item)) == True):
                #    print(join(dir_in, item), " é diretório")
                #    le_Unzip(join(dir_in, item), dir_out)
                #else:
                #    print("Verificar: ", join(dir_in, item))
                try:
                    le_Unzip(join(dir_in, item), dir_out, arq_csv)
                except:
                      print("ERRO de leitura")
                      
    else: # Dir_in é arquivo
        if isfile(dir_in):
            #print(join(dir_in, item), " é arquivo")
            extension = os.path.splitext(dir_in)[1]
            
            if (extension == '.rar'):
              #print(join(dir_in,item), " é rar.")
              rf = rarfile.RarFile(dir_in)
              
              #if(os.path.isdir(dir_out) == False): # Diretorio não existe, então cria diretório
              #    #print("Criando dir...", dir_out)
              #    pathlib.Path(dir_out).mkdir(parents=True, exist_ok=True) 
              try:
                  rf.extractall(path = dir_out, members=None, pwd=None)
              except:
                  print("Erro na leitura do arquivo rar.", dir_in)
                  fields=[dir_in,'rar']
                  with open(arq_csv, 'a') as f:
                      writer = csv.writer(f)
                      writer.writerow(fields)
    
              #le_Unzip(dir_in, dir_out)
              #os.remove(join(dir_out,item))
          
            elif  (extension == '.zip'):
                #print(join(dir_in, item), " é zip.")
                  
                #if(os.path.isdir(dir_out) == False): # Diretorio não existe, então cria diretório
                #    #print("Criando dir...", dir_out)
                #    pathlib.Path(dir_out).mkdir(parents=True, exist_ok=True) 
                try:
                  with zipfile.ZipFile(dir_in, mode="r") as archive:
                    #print(dir_out)
                    archive.extractall(dir_out)
                    #le_Unzip(dir_out, dir_out)
                      # Funciona também
                      #Archive(join(dir_in,item)).extractall(dir_out)
                      #le_Unzip(join(dir_out, item), dir_out)
                      #os.remove(join(dir_out,item))
                except zipfile.BadZipFile as error:
                  print("Bad Zip File ", dir_in)  
                  #print(error)
                  fields=[dir_in,'zip']
                  with open(arq_csv, 'a') as f:
                      writer = csv.writer(f)
                      writer.writerow(fields)
        
      
            elif  (extension == '.7z'):
              #print(join(dir_in, item), " é 7 Zip.")
              #print("Copiando de : ", join(dir_out,item))
              #print("  para: ", dir_out + "/"+ item)
              
              #if(os.path.isdir(dir_out) == False): # Diretorio não existe, então cria diretório
              #    #print("Criando dir...", dir_out)
              #    pathlib.Path(dir_out).mkdir(parents=True, exist_ok=True) 
              
              # Descompacta 7 Zip  
              try:
                  Archive(dir_in).extractall(dir_out)
                  
              except:
                  print("Erro na leitura do arquivo .7Zip. ", dir_in)
                  fields=[dir_in,'7zip']
                  with open(arq_csv, 'a') as f:
                      writer = csv.writer(f)
                      writer.writerow(fields)
        
              
            elif  (extension == '.xml'):
              #print(join(dir_in, item), " é xml.")
              # Copia XML  
              #print("Copiando XML")
              #print(join(dir_in,item))
              #print("para ")
              #print(join(dir_out,item))
              
              shutil.copyfile(dir_in, dir_out)
              
                  
            else:
              print(dir_in, " - não considero porque não é zip nem rar, nem 7 Zip, nem xml.")
                             
        else:
            #print("Não é um arquivo, então verificando... ", join(dir_in, item))
            #if(os.path.isdir(join(dir_in, item)) == True):
            #    print(join(dir_in, item), " é diretório")
            #    le_Unzip(join(dir_in, item), dir_out)
            #else:
            #    print("Verificar: ", join(dir_in, item))
            try:
                le_Unzip(dir_in, dir_out, arq_csv)
            except:
                  print("ERRO de leitura")

    return

def limpa(limpa_in, dir_out):
    """
    """
        
    list_dir = [f for f in listdir(limpa_in)] 

    for item in list_dir:
        if isfile(join(limpa_in, item)):
            # print(join(dir_in, item), " é arquivo")
            extension = os.path.splitext(item)[1]
            if (extension == '.rar'):
              #print(join(limpa_in,item), " é rar.")
              rf = rarfile.RarFile(join(limpa_in,item))
              rf.extractall(path = dir_out, members=None, pwd=None)
              #os.remove(join(limpa_in,item))
       
            elif  (extension == '.zip'):
              #print(join(limpa_in, item), " é zip.")
              try:
                with zipfile.ZipFile(join(limpa_in,item), mode="r") as archive:
                  archive.extractall(dir_out)
                  #os.remove(join(limpa_in,item))
           
              except zipfile.BadZipFile as error:
                print(error)
                  
            else:
              print(join(limpa_in, item), " - Não considero porque não é zip nem rar, nem xml.")
              
        else:
            #print(join(limpa_in, item), " é diretório")
            limpa(join(limpa_in, item), dir_out)
            #shutil.rmtree(join(limpa_in,item))
            
    return


def limpa_zips(limpa_in):
    """
    """
        
    list_dir = [f for f in listdir(limpa_in)] 

    for item in list_dir:
        if isfile(join(limpa_in, item)):
            # print(join(dir_in, item), " é arquivo")
            extension = os.path.splitext(item)[1]
            if (extension == '.rar') or ((extension == '.zip')):
              os.remove(join(limpa_in,item))
       
            else:
              print(join(limpa_in, item), " não é zip nem rar.")
               
    return


def extrai_xml(caminho_IN, caminho_OUT, csv_arq):
    """
    """
        
    if(os.path.isdir(caminho_OUT) == False): # Diretorio não existe, então cria diretório
        print("Criando dir...", caminho_OUT)
        pathlib.Path(caminho_OUT).mkdir(parents=True, exist_ok=True) 
    
    # Fase 0 -> Estou no diretorio com o nome do Grupo (empresa)
    list_dir = [f for f in listdir(caminho_IN)] 
    for item in list_dir:
        #novo_caminho_OUT = join(caminho_OUT,item)
        novo_caminho_OUT = caminho_OUT
        
        
        print("===============================")
        print("Transferindo de ", join(caminho_IN,item))
        print(" para ", novo_caminho_OUT)
        
        # Unzipa e move para out
        le_Unzip(join(caminho_IN,item), novo_caminho_OUT, csv_arq)
        
    return

def filtra_XML(caminho_IN, caminho_OUT, atual, arq_csv):
    """
    """
    if (os.path.isdir(caminho_IN) == True): # É subdiretório
        list_dir = [f for f in listdir(caminho_IN)] 
        if (len(list_dir) == 0): # Diretório Vazio 
            print(caminho_IN, " é um diretório vazio.")
            # Termina processamento
            atual = True
        else:
            i = 0
            for item in list_dir:
                print(join(caminho_IN, item))
                if (os.path.isdir(join(caminho_IN, item)) == True): # É subdiretório
                    atual = filtra_XML(join(caminho_IN, item), caminho_IN, atual, arq_csv) 
                else:
                    extension = os.path.splitext(item)[1]
                    descomp = True
                    if (extension == '.rar'):
                      try:
                          rf = rarfile.RarFile(join(caminho_IN,item))
                          rf.extractall(path = caminho_OUT, members=None, pwd=None)
                          le_Unzip(join(caminho_OUT, item), caminho_OUT, arq_csv)
                      except:
                          print("Erro RAR", item)
                          descomp = False
                          fields=[join(caminho_IN,item),'rar']
                          with open(arq_csv, 'a') as f:
                              writer = csv.writer(f)
                              writer.writerow(fields)
            
                      if (descomp):
                          # Se descompactado então não preciso mais do arquivo compactado, então apago
                          # Se erro de descompactação, então apago
                          os.remove(join(caminho_IN,item))
      
                    elif  (extension == '.zip'):
                        descomp = True
                        try:
                          with zipfile.ZipFile(join(caminho_IN,item), mode="r") as archive:
                            archive.extractall(caminho_OUT)
                            le_Unzip(join(caminho_OUT, item), caminho_OUT, arq_csv)
                             
                        except zipfile.BadZipFile as error:
                          print("Bad Zip File")  
                          print(error)
                          descomp = False
                          fields=[join(caminho_IN,item),'rar']
                          with open(arq_csv, 'a') as f:
                              writer = csv.writer(f)
                              writer.writerow(fields)
                        
                        if (descomp): 
                            # Se descompactado então não preciso mais do arquivo compactado, então apago
                            # Se erro de descompactação, então apago
                            os.remove(join(caminho_IN,item))
        
                    elif  (extension == '.7z'):
                      descomp = True 
                      try:
                          Archive(join(caminho_IN,item)).extractall(caminho_OUT)
                          le_Unzip(join(caminho_OUT, item), caminho_OUT, arq_csv)
                      except:
                          print("Erro de descompactação do 7zip: ",item) 
                          descomp = False
                          fields=[join(caminho_IN,item),'rar']
                          with open(arq_csv, 'a') as f:
                              writer = csv.writer(f)
                              writer.writerow(fields)
          
                      if(descomp):
                          # Se descompactado então não preciso mais do arquivo compactado, então apago
                          # Se erro de descompactação, então apago
                          os.remove(join(caminho_IN,item))
                         
                    else:
                      print(join(caminho_IN, item), " - não é arquivo compactado, então não considero para descompactação.")
                                        
                    i+= 1
    
    else:   # Não é subdiretório
        print(caminho_IN, " não é Sub diretório")
                
    return atual

def le_Unzip_apaga(dir_in, dir_out, status):
    """
    Descompacto e apago Zip, RAR, 7Zip

    """
    status = True
    i = 0
    if(dir_in[0] != "G"): # Não permito apagar no Servidor de arquivos
        #print("Caminho de Entrada não está no servidor de arquivos ", dir_in[0])
        if(os.path.isdir(join(dir_in)) == True): # É diretório
            print(join(dir_in), " é diretório")
            list_dir = [f for f in listdir(dir_in)] 
            if (len(list_dir)==0): # diretório vazio
               shutil.rmtree(dir_in)
            else:
                for item in list_dir:   
                    if isfile(join(dir_in, item)):
                        print(join(dir_in, item), " é arquivo")
                        extension = os.path.splitext(item)[1]
                        
                        if (extension == '.rar'):
                          print(join(dir_in,item), " é rar.")
                          rf = rarfile.RarFile(join(dir_in,item))
                          rf.extractall(path = dir_out, members=None, pwd=None)
                          os.remove(join(dir_in,item))
                          status = False
                          
                        elif  (extension == '.zip'):
                            print(join(dir_in, item), " é zip.")
                            status = False
                        
                            try:
                              with zipfile.ZipFile(join(dir_in,item), mode="r") as archive:
                                #print(dir_out)
                                archive.extractall(dir_out)
                                os.remove(join(dir_in,item))
                            except zipfile.BadZipFile as error:
                              print(error)
                             
                        elif  (extension == '.7z'):
                          print(join(dir_in, item), " é 7 Zip.")
                          status = False
                          # Descompacta 7 Zip    
                          Archive(join(dir_in,item)).extractall(dir_out)
                          os.remove(join(dir_in,item))  
                              
                        else:
                            #print(join(dir_in, item), " - não considero")
                            i += 1
                                         
                    else:
                        print("Não é um arquivo, então verificando... ", join(dir_in, item))
                        try:
                            status = le_Unzip_apaga(join(dir_in, item), dir_out, status)
                        except:
                            print("error")
                            
        else:  # Não é diretório
            print(join(dir_in), " nâo é diretório")
            if isfile(dir_in):
                print(dir_in, " é arquivo")
                extension = os.path.splitext(dir_in)[1]
                
                if (extension == '.rar'):
                  print(dir_in, " é rar.")
                  rf = rarfile.RarFile(dir_in)
                  rf.extractall(path = dir_out, members=None, pwd=None)
                  os.remove(dir_in)
                  status = False
                  
                elif  (extension == '.zip'):
                    print(dir_in, " é zip.")
                    status = False
                
                    try:
                      with zipfile.ZipFile(dir_in, mode="r") as archive:
                        #print(dir_out)
                        archive.extractall(dir_out)
                        os.remove(dir_in)
                    except zipfile.BadZipFile as error:
                      print(error)
                     
                elif  (extension == '.7z'):
                  print(dir_in, " é 7 Zip.")
                  status = False
                  # Descompacta 7 Zip    
                  Archive(dir_in).extractall(dir_out)
                  os.remove(dir_in)  
                      
                else:
                    #print(join(dir_in, item), " - não considero")
                    i += 1
                                 
            else:
                print("Não é um arquivo, então verificando... ", dir_in)
                        
    else:
        print("Cammhinho de entrada inválido no servidor de arquivos", dir_in[0])

    return status

def Valida_Transf_XML(caminho_IN, caminho_OUT, Cliente_CNPJ):
    """
    """
    if (os.path.isdir(caminho_IN) == True): # É subdiretório
        list_dir = [f for f in listdir(caminho_IN)] 
        if (len(caminho_IN) == 0): # Diretório Vazio 
            print(caminho_IN, " é um diretório vazio.")
        else:
            #print(caminho_IN)
            for item in list_dir:
                print(join(caminho_IN, item))
                if (os.path.isdir(join(caminho_IN, item)) == True): # É subdiretório
                    Valida_Transf_XML(join(caminho_IN, item), caminho_OUT ,Cliente_CNPJ) 
                else:
                    extension = os.path.splitext(item)[1]
                    if (extension == '.xml'):
                        #copia
                        organizacao.processa_XML_Transf(caminho_IN, caminho_OUT, Cliente_CNPJ, item)
                      
    else:   # Não é subdiretório
        #print(caminho_IN, " não é Sub diretório")
        extension = os.path.splitext(caminho_IN)[1]
        if (extension == '.xml'):
            #copia
            organizacao.processa_XML_Transf(caminho_IN, caminho_OUT, Cliente_CNPJ, "")
                
    return 

        