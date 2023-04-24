# -*- coding: utf-8 -*-
"""
Created on Thu Sep 22 08:33:25 2022

@author: angelo.milfont
"""

import time
import extracao
import organizacao
import pandas as pd

#
# Processamento Completo
#

# Parâmetros
# Maquina Virtual
#EstaMaquina = "CL058"

# Diretório de Leitura
caminho_CSV = "C:/Users/angelo.milfont/Documents/Python Scripts/CSVs/"
caminho_xls = r"C:/Users/angelo.milfont/Documents/Python Scripts/excel/"
caminho_pickle = r"C:/Users/angelo.milfont/Documents/Python Scripts/pickles/"

# Diretórios de transição e Saída
#caminho_Temp = r"E:/Transicao_PAX_CL072/"
caminho_Temp = r"E:/Transicao_20230123_OUT/"
#caminho_Temp = r"E:/Filtragem/"
#caminho_Temp = r"E:/Grupo/"
caminho_OUT = r"E:/Novos_Projetos_Tributário/"

# Carrega CFOPs de interesse
CFOP_Compra = organizacao.lista_CFOP_Compra(caminho_CSV)
CFOP_Venda = organizacao.lista_CFOP_Venda(caminho_CSV)

# Carrega Lista de CNPJs e Caminhos
CNPJs = pd.read_excel(caminho_xls+"Lista_Empresas_CNPJ_AM_230123.xlsx")
# Clientes
Cliente_CNPJ= []
lista_01 = CNPJs["CNPJ"].tolist()
for j in range(len(lista_01)):
    #if(CNPJs.loc[j, "MV"] == EstaMaquina):      
    if (1 == 1):
        ncnpj = str(lista_01[j]).replace(".","")
        ncnpj = ncnpj.replace("/","")
        ncnpj = ncnpj.replace("-","")
        Cliente_CNPJ.append(ncnpj)
      
Status_list = []
print("Total de CNPJs listados: ", CNPJs.shape[0])

for i in range(0, 1): # CNPJs.shape[0]):   
    
    caminho_IN = CNPJs.loc[i, "Caminho"]
    caminho_IN = caminho_IN.replace("\\", "/")
    caminho_IN = caminho_IN + "/"
    
    #if(CNPJs.loc[i, "MV"] == EstaMaquina):      
    if (1==1):
        print("Caminho In ")
        print(caminho_IN)
        print("CNPJ ",Cliente_CNPJ )
        print("Iniciando...")

        # Fase 1 : lê diretório no File Server e
        #   extrai XMLs para diretório temporário Único
        st1 = time.time()
        print("Fase 1 - Extração iniciada.")
        #extracao.extrai_xml(caminho_IN, caminho_Temp)
        et1 = time.time()
        Status_list.append(["Extração ",caminho_IN, et1])
        print("Fase 1 - Extração levou : {:.2f}".format(et1-st1))
        print()
        
        # Fase 2 : Filtra diretório Temp até que só existam XMLs
        st2 = time.time()
        print("Fase 2 - Filtragem do diretório de transição iniciada.")
        # Abre zips mas não trasnfere XMLs
        limpo = False
        #while (not limpo):
        #    limpo = extracao.filtra_XML(caminho_Temp, caminho_Temp, limpo)
        #    print("Limpeza terminada ", limpo)
        et2 = time.time()
        print("Fase 2 - Filtragem levou : {:.2f}".format(et2-st2))
        print()
        
        # Fase 3 : Classifica e transfere XMLs corforme organização
        st3 = time.time()
        print("Fase 3 - Classificação e Transferência iniciada.")
        # transfere XMLs
        organizacao.separa(caminho_Temp, CFOP_Compra, CFOP_Venda, 
                           caminho_OUT, Cliente_CNPJ, "", "")
        et3 = time.time()
        Status_list.append(["Organização ",caminho_IN, et3])
        print("Fase 3 - Filtragem levou : {:.2f}".format(et3-st3))
        print()
        print("Fases 1 a 3 - tempo total : {:.2f}".format(et3-st1))
        
        # Fase 4 : Limpeza dos subdiretórios vazios e arquivos não utilizáveis
        st4 = time.time()
        print("Fase 4 - Remoção de arquivos sem uso do diretório transição iniciada.")
        #organizacao.limpeza(caminho_Temp)
        et4 = time.time()
        Status_list.append(["Limpeza ",caminho_Temp, et4])
        print("Fase 4 - Limpeza levou : {:.2f}".format(et4-st4))
        print()
        print("Fases 1 a 4 - tempo total : {:.2f}".format(et4-st1))

#df = pd.DataFrame(Status_list, columns = ["Fase","Caminho","Tempo"])
#df.to_pickle(caminho_pickle + "Processamento_Completo.pkl")
