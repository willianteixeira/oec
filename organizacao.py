# -*- coding: utf-8 -*-
"""
Created on Fri Sep 16 12:25:25 2022

@author: angelo.milfont
"""

import csv

from os import listdir, chdir
import os
import shutil

from os.path import isfile, join
import pathlib 

import xml.etree.ElementTree as ET

def lista_Ano_Mes(caminho, nome):
    """
    """
    lista = []
    f = open(caminho + nome, 'r')
    reader = csv.reader(f)
    headers = next(reader, None)
    for row in reader:
        lista.append(row[0])
    
    print(lista)
    
    return lista

def lista_CFOP_Compra(caminho):
    """
    """
    lista = []
    f = open(caminho + "CFOP_Compra.csv", 'r')
    reader = csv.reader(f)
    headers = next(reader, None)
    for row in reader:
        lista.append(row[0])
    
    return lista

def lista_CFOP_Venda(caminho):
    """
    """
    lista = []
    f = open(caminho + "CFOP_Venda.csv", 'r')
    reader = csv.reader(f)
    headers = next(reader, None)
    for row in reader:
        lista.append(row[0])
    return lista

def lista_CSV(caminho, nome):
    """
    """
    lista = []
    f = open(caminho + nome, 'r')
    reader = csv.reader(f)
    headers = next(reader, None)
    for row in reader:
        lista.append([row[0], row[1]])
    return lista

def movimenta(entrada, caminho, cliente, tipo, subtipo, dtH, item, arq_csv):
    """
    """
    #print("Data hora Emissão ", dtH)
    if(tipo == "" and subtipo == ""):
        caminho_destino = caminho + cliente + "/" 
    elif (subtipo == ""):
        caminho_destino = caminho + cliente + "/" + tipo + "/" 
    else:    
        caminho_destino = caminho + cliente + "/" + tipo + "/" + subtipo + "/" 
    
    if(str(dtH)[0:4].isnumeric()):
        if(str(dtH)[4] == '_') or (str(dtH)[4] == '-'):
            data_dir = str(dtH)[0:4] +"_"+ str(dtH)[5:7] # versão 2022_XX...
        else:
            data_dir = str(dtH)[0:4] +"_"+ str(dtH)[4:6] # versão 2022XX...
            
        # Crio diretório com Ano_Mês
        pathlib.Path(caminho_destino + "/" + data_dir).mkdir(parents=True, exist_ok=True) 
        #print(caminho_destino + "/" + data_dir + "/")
        shutil.move(entrada+"/"+item, caminho_destino + "/" + data_dir + "/"+ item)
    
    else:
        print("Err - Dir/data não é válido.", entrada," - ", dtH, " removendo...")
        #print(entrada +"/"+ item)
        fields=[entrada ,item, dtH, entrada +"/"+ item, "Err - Dir/data não é válido"]
        with open(arq_csv, 'a') as f:
            writer = csv.writer(f)
            #print("Fields")
            #print(fields)
            writer.writerow(fields)
        #os.remove(entrada+"/"+item)
        #print(item)
        
    return

def processa_XML(caminho_in, CFOP_Compra, CFOP_Venda, caminho_OUT, Cliente_CNPJ, item, ncmProc, arq_csv):
    """
    
    Le XML e define onde será enviado na esrtutura de diretórios
    
    """
    leitura = False
    caminho_item = caminho_in + "/" + item
    #print("Tentando ler ", caminho_item)
    CFOP = ""
    try:
        tree = ET.parse(caminho_item) 
        leitura = True
    except:
        print("ERRO de Leitura do XML ", caminho_item," removendo...")
        fields=[caminho_item, "Erro de Leitura"]
        with open(arq_csv, 'a') as f:
            writer = csv.writer(f)
            writer.writerow(fields)
   
        #os.remove(caminho_item)
        
    if (leitura):
        CNPJ_Emi = "VAZIO"
        dhEmi = "DH VAZIO"
        root = tree.getroot() 
        prefix = "{http://www.portalfiscal.inf.br/nfe}"
        
        # Leitura das informações do XML
        # Identifica Data e Natureza da Operação
        for info in root.findall('.//{}ide'.format(prefix)):
            #dhEmi =info.find(prefix + "dhEmi")
            dhEmi =info.find(prefix + "dEmi")
            #natOp = info.find(prefix + "natOp").text
            if (dhEmi != None): # Não encontrei data hora emitente
                dhEmi = dhEmi.text
                #print("achei data ", dhEmi)
            else:
                dhEmi = "Erro DH Emitente"
        
        # Identifica CNPJ Emitente
        for info in root.findall('.//{}emit'.format(prefix)):
            CNPJ_Emi = info.find(prefix + "CNPJ")
            if (CNPJ_Emi != None): # Não encontrei emitente
                 CNPJ_Emi = CNPJ_Emi.text
            else:
                CNPJ_Emi = "Erro CNPJ Emitente"
                 
        # Identifica destinatário: CNPJ ou CPF
        destinatario = ""
        for info in root.findall('.//{}dest'.format(prefix)):
            CNPJ_Dest = info.find(prefix + "CNPJ")
            CPF_Dest = info.find(prefix + "CPF")
            #print(CNPJ_Dest, CPF_Dest)
            if (CNPJ_Dest != None): # Destinatário é CNPJ
                CNPJ_Dest = CNPJ_Dest.text
                destinatario = CNPJ_Dest
            elif (CPF_Dest != None):  # Destinatário é CPF
                 CPF_Dest = CPF_Dest.text
                 destinatario = CPF_Dest
            else: 
                print("ERRO: Não identificado o destinatário")
                destinatario = "Erro CNPJ/CPF Destinatário"
            
        # Identifica CFOP
        for info in root.findall('.//{}prod'.format(prefix)):
            CFOP = info.find(prefix + "CFOP")
            if (CFOP != None): # Achei CFOP
                CFOP = CFOP.text
            else: 
                print("ERRO: Não identificado o CFOP")
                CFOP = "Erro Não encontrado."
        
        Achei_NCM = False
        # Identifica NCM Procurado
        if (ncmProc != ""):  
            lista_NCM = []
            for info in root.findall('.//{}prod'.format(prefix)):
                NCM = info.find(prefix + "NCM")
                if (NCM != None): # Encontrei um NCM
                    NCM = NCM.text
                    lista_NCM.append(NCM)
                else:
                    NCM = "Não há NCM"
            if (ncmProc in lista_NCM) :
                Achei_NCM = True
                #print("XML contém NCM Procurado.", NCM)

        #
        # Ações baseadas na leitura das informações
        #
        if(not Achei_NCM): # FALSE
            if (CNPJ_Emi not in Cliente_CNPJ) and (destinatario not in Cliente_CNPJ):
                movimenta(caminho_in, caminho_OUT, "Outros", "", "", dhEmi, item, arq_csv)
            
            else:
                #print("- emitido por: ", CNPJ_Emi,  "- em:  ", dhEmi)
                if (destinatario in Cliente_CNPJ) and (CNPJ_Emi in Cliente_CNPJ):
                    # Transferência !
                    print("Transferência! Duplica XML e movimenta um para cada subdirs Entrada/Saída.")
                    # Movimenta para subDiretório de Outras Entradas do Destinatário
                    movimenta(caminho_in, caminho_OUT, destinatario, "", "", dhEmi, item, arq_csv)
                    #
                    #  Preciso acertar : movimenta move arquivo, preciso copiar antes de mover.
                    #
                    # Movimenta para subDiretório de Outras Saídas do Emitente
                    #movimenta(caminho_in, caminho_OUT, CNPJ_Emi, "Saída", "Outras_Saídas", dhEmi, item)
    
                elif (destinatario in Cliente_CNPJ):     # NFe de Entrada
                    if (CFOP in CFOP_Compra) or (CFOP in CFOP_Venda):     ##  NFe de Compra
                        #print("Compra", destinatario, "-", CFOP)
                        movimenta(caminho_in, caminho_OUT, destinatario, "", "", dhEmi, item, arq_csv)
                    
                    else:                           ## NFE de Outras Entradas
                        #print("Outras Entradas", CFOP)
                        movimenta(caminho_in, caminho_OUT, destinatario, "", "", dhEmi, item, arq_csv)
                    
                elif (CNPJ_Emi in Cliente_CNPJ):    # NFe de Saída
                    if (CFOP in CFOP_Compra) or (CFOP in CFOP_Venda):  ##  NFe de Venda
                        #print("Venda")
                        movimenta(caminho_in, caminho_OUT, CNPJ_Emi, "", "", dhEmi, item, arq_csv)
                    
                    else:                           ## NFE de Outras Saídas
                       #print("Outras Saídas")
                       movimenta(caminho_in, caminho_OUT, CNPJ_Emi, "", "", dhEmi, item, arq_csv)
           
                else:
                    print("ERRO - Entrada x Saída", caminho_in,caminho_OUT)
        else:   # Achei NCM Procurado
            #print("XML contém NCM Procurado")
            movimenta(caminho_in, caminho_OUT, CNPJ_Emi, "NCM", "NCM", dhEmi, item, arq_csv)
            if (destinatario in Cliente_CNPJ):     # NFe de Entrada
                if (CFOP in CFOP_Compra) or (CFOP in CFOP_Venda):     ##  NFe de Compra
                    #print("Compra", destinatario, "-", CFOP)
                    movimenta(caminho_in, caminho_OUT, destinatario, "", "", dhEmi, item, arq_csv)
                
                else:                           ## NFE de Outras Entradas
                    #print("Outras Entradas", CFOP)
                    movimenta(caminho_in, caminho_OUT, destinatario, "", "", dhEmi, item, arq_csv)
                
            elif (CNPJ_Emi in Cliente_CNPJ):    # NFe de Saída
                if (CFOP in CFOP_Compra) or (CFOP in CFOP_Venda):  ##  NFe de Venda
                    #print("Venda")
                    movimenta(caminho_in, caminho_OUT, CNPJ_Emi, "", "", dhEmi, item, arq_csv)
                
                else:                           ## NFE de Outras Saídas
                   #print("Outras Saídas")
                   movimenta(caminho_in, caminho_OUT, CNPJ_Emi, "", "", dhEmi, item, arq_csv)

    return

def separa(caminho, CFOP_Compra, CFOP_Venda, caminho_OUT, Cliente_CNPJ, item, ncm, arq_csv):
    """
    """
    i = 0
    caminho_item = caminho + item
    if (os.path.isdir(caminho_item) == True): # caminho_item É subdiretório
        #print("Procuro em ", caminho_item )
        list_dir = [f for f in listdir(caminho_item)] 
        for item in list_dir:
            #print(i, caminho_item, "-",item)
            extension = os.path.splitext(item)[1]
            if (extension == ".xml") or (extension == ".Xml"):
                #print("Achei XML")
                processa2_XML(caminho_item,CFOP_Compra, CFOP_Venda, caminho_OUT, Cliente_CNPJ, item, ncm, arq_csv)
            elif (os.path.isdir(join(caminho, item)) == True): # É subdiretório
                #print(join(caminho_item, item), " é diretório")
                separa(join(caminho_item, item), CFOP_Compra, CFOP_Venda, caminho_OUT, Cliente_CNPJ,"", ncm, arq_csv)
            else:
                print(i, " - ", item, " não é xml.")
            i+= 1
    else: # caminho_item não é subdiretório
        extension = os.path.splitext(caminho_item)[1]
        if (extension == ".xml"):
            #print("Achei XML")
            processa_XML(caminho_item,CFOP_Compra, CFOP_Venda, caminho_OUT, Cliente_CNPJ, item, ncm, arq_csv)
        else:
            print(i, " - ", item, " não é xml.")
        i+= 1

    return

def limpeza(dir_in):
    """
    Remove subdiretórios vazios
    Remove arquivo sem uso (não XMLs)
    """
    mantenho = [".xml",".zip",".rar",".7zip"]
    if (os.path.isdir(dir_in) == True): # É subdiretório
        list_dir = [f for f in listdir(dir_in)] 
        if (len(list_dir) == 0): # Diretório Vazio => remove
            print(dir_in, " é um diretório vazio. Removendo...")
            os.rmdir(dir_in)
        else:
            i = 0
            for item in list_dir:
                if (os.path.isdir(join(dir_in, item)) == True): # É subdiretório
                    limpeza(join(dir_in, item))
                else:
                    extension = os.path.splitext(item)[1]
                    if (extension not in mantenho):
                        print(item, " - removo arquivo.")
                        os.remove(join(dir_in,item))
                    
                    i+= 1
    
    else:   # Não é subdiretório
        print("Não é Sub diretório")
        extension = os.path.splitext(dir_in)[1]
        if (extension not in mantenho):
            print(dir_in, " - Removo arquivo.")
            os.remove(dir_in,item)
        i+= 1
        
    return

def processa_XML_Transf(caminho_in, caminho_OUT, Cliente_CNPJ, item):
    """
    Procura XMLs de transferência nos arquivos já processados
        e faz cópia do XML de transferência no diretório de saída.
    
    """
    leitura = False
    caminho_item = caminho_in + "/" + item
    #print("Tentando ler ", caminho_item)
    CFOP = ""
    try:
        tree = ET.parse(caminho_item) 
        leitura = True
    except:
        print("ERRO de Leitura do XML", caminho_item
              )
        
    if (leitura):
        CNPJ_Emi = "VAZIO"
        dhEmi = "VAZIO"
        root = tree.getroot() 
        prefix = "{http://www.portalfiscal.inf.br/nfe}"
         
        # Leitura das informações do XML
        # Identifica Data e Natureza da Operação
        for info in root.findall('.//{}ide'.format(prefix)):
            dhEmi =info.find(prefix + "dhEmi")
            #natOp = info.find(prefix + "natOp").text
            if (dhEmi != None): # Não encontrei data hora emitente
                dhEmi = dhEmi.text
            else:
                dhEmi = "Erro DH Emitente"
        
        # Identifica CNPJ Emitente
        for info in root.findall('.//{}emit'.format(prefix)):
            CNPJ_Emi = info.find(prefix + "CNPJ")
            if (CNPJ_Emi != None): # Não encontrei emitente
                 CNPJ_Emi = CNPJ_Emi.text
            else:
                CNPJ_Emi = "Erro CNPJ Emitente"
                 
        # Identifica destinatário: CNPJ ou CPF
        destinatario = ""
        for info in root.findall('.//{}dest'.format(prefix)):
            CNPJ_Dest = info.find(prefix + "CNPJ")
            CPF_Dest = info.find(prefix + "CPF")
            #print(CNPJ_Dest, CPF_Dest)
            if (CNPJ_Dest != None): # Destinatário é CNPJ
                CNPJ_Dest = CNPJ_Dest.text
                destinatario = CNPJ_Dest
            elif (CPF_Dest != None):  # Destinatário é CPF
                 CPF_Dest = CPF_Dest.text
                 destinatario = CPF_Dest
            else: 
                print("ERRO: Não identificado o destinatário")
                destinatario = "Erro CNPJ/CPF Destinatário"
            
        # Identifica CFOP
        for info in root.findall('.//{}prod'.format(prefix)):
            CFOP = info.find(prefix + "CFOP")
            if (CFOP != None): # Achei CFOP
                CFOP = CFOP.text
            else: 
                print("ERRO: Não identificado o CFOP")
                CFOP = "Erro Não encontrado."
        
        #
        # Ações baseadas na leitura das informações
        #
        if (CNPJ_Emi not in Cliente_CNPJ) and (destinatario not in Cliente_CNPJ):
            print("Erro: CNPJ não pertence aos Emitentes nem Destinatários")
            #movimenta(caminho_in, caminho_OUT, "Outros", "", "", dhEmi, item)
        
        else:
            #print("- emitido por: ", CNPJ_Emi,  "- em:  ", dhEmi)
            if (destinatario in Cliente_CNPJ) and (CNPJ_Emi in Cliente_CNPJ):
                # Transferência !
                print("Transferência! Duplica XML e movimenta um para cada subdirs Entrada/Saída.")
                # Movimenta para subDiretório de Outras Entradas do Destinatário
                Transf_CNPJ = CNPJ_Emi #caminho_item[29:43]
                transf_out = caminho_OUT + Transf_CNPJ + "/Saída/Outras_Saídas/"
                print("Transf de : ", Transf_CNPJ, " para ", destinatario)
                print("Copiar de : ", join(caminho_in,item))
                print("Copiar para : ", join(transf_out, item))
                #shutil.copy(join(caminho_in,item) join(caminho_OUT,item) destinatario, "Entrada", "Outras_Entradas", dhEmi, item)
                #movimenta(caminho_in, caminho_OUT, CNPJ_Emi, "Saída", "Outras_Saídas", dhEmi, item)
                  
    return

def processa2_XML(caminho_in, CFOP_Compra, CFOP_Venda, caminho_OUT, Cliente_CNPJ, item, ncmProc, arq_csv):
    """
    
    Le XML e define onde será enviado na esrtutura de diretórios
    
    """
    leitura = False
    caminho_item = caminho_in + "/" + item
    #print("Tentando ler ", caminho_item)
    CFOP = ""
    try:
        tree = ET.parse(caminho_item) 
        leitura = True
    except:
        print("ERRO de Leitura do XML ", caminho_item," removendo...")
        fields=[caminho_item, "Erro de Leitura"]
        with open(arq_csv, 'a') as f:
            writer = csv.writer(f)
            writer.writerow(fields)
   
        #os.remove(caminho_item)
        
    if (leitura):
        CNPJ_Emi = "VAZIO"
        dhEmi0 = "DH VAZIO"
        dhEmi1 = "DH VAZIO"
        
        root = tree.getroot() 
        
        prefix0 = "{http://www.portalfiscal.inf.br/nfe}"
        prefix = prefix0
        # Leitura das informações do XML
        # Identifica Data e Natureza da Operação
        for info in root.findall('.//{}ide'.format(prefix)):
            dhEmi =info.find(prefix + "dhEmi")
            #dhEmi =info.find(prefix + "dEmi")
            #natOp = info.find(prefix + "natOp").text
            if (dhEmi != None): # Não encontrei data hora emitente
                dhEmi0 = dhEmi.text
                #print("achei data ", dhEmi)
            else:
                dhEmi0 = "Erro DH Emitente"
        
        prefix1 = ""
        prefix = prefix1
        # Leitura das informações do XML
        # Identifica Data e Natureza da Operação
        for info in root.findall('.//{}ide'.format(prefix)):
            #dhEmi =info.find(prefix + "dhEmi")
            dhEmi =info.find(prefix + "dEmi")
            #natOp = info.find(prefix + "natOp").text
            if (dhEmi != None): # Não encontrei data hora emitente
                dhEmi1 = dhEmi.text
                #print("achei data ", dhEmi)
            else:
                dhEmi1 = "Erro DH Emitente"
        
        if (dhEmi0 == "DH VAZIO"):
            prefix = prefix1
            dhEmi = dhEmi1
        else:
            prefix = prefix0
            dhEmi = dhEmi0
            
        # Identifica CNPJ Emitente
        for info in root.findall('.//{}emit'.format(prefix)):
            CNPJ_Emi = info.find(prefix + "CNPJ")
            if (CNPJ_Emi != None): # Não encontrei emitente
                 CNPJ_Emi = CNPJ_Emi.text
            else:
                CNPJ_Emi = "Erro CNPJ Emitente"
                 
        # Identifica destinatário: CNPJ ou CPF
        destinatario = ""
        for info in root.findall('.//{}dest'.format(prefix)):
            CNPJ_Dest = info.find(prefix + "CNPJ")
            CPF_Dest = info.find(prefix + "CPF")
            #print(CNPJ_Dest, CPF_Dest)
            if (CNPJ_Dest != None): # Destinatário é CNPJ
                CNPJ_Dest = CNPJ_Dest.text
                destinatario = CNPJ_Dest
            elif (CPF_Dest != None):  # Destinatário é CPF
                 CPF_Dest = CPF_Dest.text
                 destinatario = CPF_Dest
            else: 
                #print("ERRO: Não identificado o destinatário")
                destinatario = "Erro CNPJ/CPF Destinatário"
            
        # Identifica CFOP
        for info in root.findall('.//{}prod'.format(prefix)):
            CFOP = info.find(prefix + "CFOP")
            if (CFOP != None): # Achei CFOP
                CFOP = CFOP.text
            else: 
                print("ERRO: Não identificado o CFOP")
                CFOP = "Erro Não encontrado."
        
        Achei_NCM = False
        # Identifica NCM Procurado
        if (ncmProc != ""):  
            lista_NCM = []
            for info in root.findall('.//{}prod'.format(prefix)):
                NCM = info.find(prefix + "NCM")
                if (NCM != None): # Encontrei um NCM
                    NCM = NCM.text
                    lista_NCM.append(NCM)
                else:
                    NCM = "Não há NCM"
            if (ncmProc in lista_NCM) :
                Achei_NCM = True
                #print("XML contém NCM Procurado.", NCM)

        #
        # Ações baseadas na leitura das informações
        #
        if(not Achei_NCM): # FALSE
            if (CNPJ_Emi not in Cliente_CNPJ) and (destinatario not in Cliente_CNPJ):
                movimenta2(caminho_in, caminho_OUT, "Outros", "", "", dhEmi, item, arq_csv)
            
            else:
                #print("- emitido por: ", CNPJ_Emi,  "- em:  ", dhEmi)
                if (destinatario in Cliente_CNPJ) and (CNPJ_Emi in Cliente_CNPJ):
                    # Transferência !
                    print("Transferência! Duplica XML e movimenta um para cada subdirs Entrada/Saída.")
                    # Movimenta para subDiretório de Outras Entradas do Destinatário
                    movimenta2(caminho_in, caminho_OUT, destinatario, "Entrada", "", dhEmi, item, arq_csv)
                    #
                    #  Preciso acertar : movimenta move arquivo, preciso copiar antes de mover.
                    #
                    # Movimenta para subDiretório de Outras Saídas do Emitente
                    #movimenta2(caminho_in, caminho_OUT, CNPJ_Emi, "Saída", "Outras_Saídas", dhEmi, item)
    
                elif (destinatario in Cliente_CNPJ):     # NFe de Entrada
                    if (CFOP in CFOP_Compra) or (CFOP in CFOP_Venda):     ##  NFe de Compra
                        #print("Compra", destinatario, "-", CFOP)
                        movimenta2(caminho_in, caminho_OUT, destinatario, "Entrada", "", dhEmi, item, arq_csv)
                    
                    else:                           ## NFE de Outras Entradas
                        #print("Outras Entradas", CFOP)
                        movimenta2(caminho_in, caminho_OUT, destinatario, "Entrada", "", dhEmi, item, arq_csv)
                    
                elif (CNPJ_Emi in Cliente_CNPJ):    # NFe de Saída
                    if (CFOP in CFOP_Compra) or (CFOP in CFOP_Venda):  ##  NFe de Venda
                        #print("Venda")
                        movimenta2(caminho_in, caminho_OUT, CNPJ_Emi, "Saída", "", dhEmi, item, arq_csv)
                    
                    else:                           ## NFE de Outras Saídas
                       #print("Outras Saídas")
                       movimenta2(caminho_in, caminho_OUT, CNPJ_Emi, "Saída", "", dhEmi, item, arq_csv)
           
                else:
                    print("ERRO - Entrada x Saída", caminho_in,caminho_OUT)
        else:   # Achei NCM Procurado
            #print("XML contém NCM Procurado")
            movimenta2(caminho_in, caminho_OUT, CNPJ_Emi, "NCM", "NCM", dhEmi, item, arq_csv)
            if (destinatario in Cliente_CNPJ):     # NFe de Entrada
                if (CFOP in CFOP_Compra) or (CFOP in CFOP_Venda):     ##  NFe de Compra
                    #print("Compra", destinatario, "-", CFOP)
                    movimenta2(caminho_in, caminho_OUT, destinatario, "Entrada", "", dhEmi, item, arq_csv)
                
                else:                           ## NFE de Outras Entradas
                    #print("Outras Entradas", CFOP)
                    movimenta2(caminho_in, caminho_OUT, destinatario, "Entrada", "", dhEmi, item, arq_csv)
                
            elif (CNPJ_Emi in Cliente_CNPJ):    # NFe de Saída
                if (CFOP in CFOP_Compra) or (CFOP in CFOP_Venda):  ##  NFe de Venda
                    #print("Venda")
                    movimenta2(caminho_in, caminho_OUT, CNPJ_Emi, "Saída", "", dhEmi, item, arq_csv)
                
                else:                           ## NFE de Outras Saídas
                   #print("Outras Saídas")
                   movimenta2(caminho_in, caminho_OUT, CNPJ_Emi, "Saída", "", dhEmi, item, arq_csv)
        
    return

def movimenta2(entrada, caminho, cliente, tipo, subtipo, dtH, item, arq_csv):
    """
    """
    #print("Data hora Emissão ", dtH)
    #if(tipo == "" and subtipo == ""):
    #    caminho_destino = caminho + cliente + "/" 
    #elif (subtipo == ""):
    #    caminho_destino = caminho + cliente + "/" + tipo + "/" 
    #else:    
    #    caminho_destino = caminho + cliente + "/" + tipo + "/" + subtipo + "/" 
    caminho_destino = caminho + cliente + "/"
    
    if(str(dtH)[0:4].isnumeric()):
        if(str(dtH)[4] == '_') or (str(dtH)[4] == '-'):
            data_dir = str(dtH)[0:4] +"_"+ str(dtH)[5:7] # versão 2022_XX...
            ano_dir = str(dtH)[0:4]
            mes_dir = str(dtH)[5:7]
        else:
            data_dir = str(dtH)[0:4] +"_"+ str(dtH)[4:6] # versão 2022XX...
            ano_dir = str(dtH)[0:4]
            mes_dir = str(dtH)[4:6]
    
        # Crio diretório com Ano_Mês e TIPO
        pathlib.Path(caminho_destino + "/" + ano_dir + "/" + mes_dir + "/" + tipo).mkdir(parents=True, exist_ok=True) 
        #print(caminho_destino + "/" + data_dir + "/")
        shutil.move(entrada + "/" + item, caminho_destino + "/" + ano_dir + "/" + mes_dir + "/" + tipo + "/" + item)
    
    else:
        print("Err - Dir/data não é válido.", entrada," - ", dtH, " removendo...")
        #print(entrada +"/"+ item)
        fields=[entrada ,item, dtH, entrada +"/"+ item, "Err - Dir/data não é válido"]
        with open(arq_csv, 'a') as f:
            writer = csv.writer(f)
            #print("Fields")
            #print(fields)
            writer.writerow(fields)
        #os.remove(entrada+"/"+item)
        #print(item)
        
    return


