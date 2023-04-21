# -*- coding: utf-8 -*-
"""
Created on Thu Mar  9 17:47:46 2023

@author: angelo.milfont
"""

import time
import extracao
import organizacao
import pandas as pd

#
# Início
#

# Seleciona fases
# Fase 1: Extração
# Fase 2: Filtragem
# Fase 3: Transferência
# Fase 4: Remoção
fase = 1


#
#
#

Status_list = []
# Diretório de Leitura
caminho_CSV = "C:/Users/angelo.milfont/Documents/MexLab/CSVs/"
caminho_xls = r"C:/Users/angelo.milfont/Documents/MexLab/Excel_Entrada/"
caminho_pickle = r"C:/Users/angelo.milfont/Documents/MexLab/pickle/"

# Diretórios de transição e Saída


caminho_Temp = r"E:/Transicao/"
caminho_OUT = r"E:/Novos_Projetos_Tributário/Ordem_Reduzida/"

# Carrega Lista de CNPJs e Caminhos
CNPJs = pd.read_excel(caminho_xls+"CLIENTES PARA ORGANIZAR E PROCESSAR_230410.xlsx")

# Clientes
Cliente_CNPJ= []
lista_01 = CNPJs["CNPJ"].tolist()
for j in range(len(lista_01)):
    ncnpj = str(lista_01[j]).replace(".","")
    ncnpj = ncnpj.replace("/","")
    ncnpj = ncnpj.replace("-","")
    Cliente_CNPJ.append(ncnpj)
      
Status_list = []
print("Total de CNPJs listados: ", CNPJs.shape[0])
print(Cliente_CNPJ)

for i in range(7): # CNPJs.shape[0]):   
    
    caminho_IN = CNPJs.loc[i, "Caminho"]
    caminho_IN = caminho_IN.replace("\\", "/")
    caminho_IN = caminho_IN + "/"
    print()
    print("Caminho procurado: ",caminho_IN)
    print()
    print("CNPJ Procurado: ",Cliente_CNPJ[i])
    print()
    arq01_csv = caminho_CSV + str(Cliente_CNPJ[i])+"_arq_compactados_não_processados.csv"
    arq02_csv = caminho_CSV + str(Cliente_CNPJ[i])+"_arq_XMLs_não_processados.csv"
    print("Relatório de Arquivos com problema em ", arq01_csv)
    
print("==================================================================")
print("    Fase ", fase)
st1 = time.time()
if(fase == 1):
    print("Extração de arquivos XML do Servidor de Clientes.")
    print("Fase 1 - Extração iniciada.")
    extracao.extrai_xml(caminho_IN, caminho_Temp, arq01_csv)
    et1 = time.time()
    Status_list.append(["Extração ",caminho_IN, et1])
    print("Fase 1 - Extração levou : {:.2f}".format(et1-st1))
    print()
    
elif(fase == 2):
    print("Filtragem de arquivos XML do diretório de Transferência.")
    # Fase 2 : Filtra diretório Temp até que só existam XMLs
    st2 = time.time()
    # Abre zips mas não transfere XMLs
    limpo = False
    while (not limpo):
        limpo = extracao.filtra_XML(caminho_Temp, caminho_Temp, limpo, arq01_csv)
        print("Limpeza terminada ", limpo)
    et2 = time.time()
    print("Fase 2 - Filtragem levou : {:.2f}".format(et2-st2))
    print()
    
elif(fase == 3):
    print("Transferência de arquivos XML para diretório organizado.")
    # Fase 3 : Classifica e transfere XMLs corforme organização
    st3 = time.time()
    print("Fase 3 - Classificação e Transferência iniciada.")
    # transfere XMLs
    organizacao.separa(caminho_Temp, "","", caminho_OUT, Cliente_CNPJ, "", "",arq02_csv)
    et3 = time.time()
    Status_list.append(["Organização ",caminho_IN, et3])
    print("Fase 3 - Filtragem levou : {:.2f}".format(et3-st3))
    print()
    print("Fases 1 a 3 - tempo total : {:.2f}".format(et3-st1))
    

else:
    print("Remoção de arquivos sem uso do diretório de Transferência.")
    # Fase 4 : Limpeza dos subdiretórios vazios e arquivos não utilizáveis
    st4 = time.time()
    print("Fase 4 - Remoção de arquivos sem uso do diretório transição iniciada.")
    organizacao.limpeza(caminho_Temp)
    et4 = time.time()
    Status_list.append(["Limpeza ",caminho_Temp, et4])
    print("Fase 4 - Limpeza levou : {:.2f}".format(et4-st4))
    print()
    print("Fases 1 a 4 - tempo total : {:.2f}".format(et4-st1))
    
print("==================================================================")

