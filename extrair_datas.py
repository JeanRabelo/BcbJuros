import requests
from bs4 import BeautifulSoup as BS
from pprint import pprint
import csv

def extrairListasDeValoresDePropriedades(dictResposta):
    entrada = {}
    for i in range(0,4):
        entrada[dictResposta['parametros'][i]['Name']] = []
        for validValue in dictResposta['parametros'][i]['ValidValues']:
            entrada[dictResposta['parametros'][i]['Name']].append(validValue['Value'])
    return entrada

def dataTraducaoMascara(periodoInicial):
    stringData = periodoInicial[:-12]
    dia = stringData[stringData.find('/',1)+1:stringData.find('/',2)]
    mes = stringData[:stringData.find('/',1)]
    ano = stringData[-4:]
    dataMascara = dia + '/' + mes + '/' + ano
    return dataMascara

arquivoEntrada = open('entrada.csv', 'a', newline='')
csvEntrada = csv.writer(arquivoEntrada, delimiter=';')

urlBcb = r'https://www.bcb.gov.br/api/relatorio/pt-br/contaspub?path=conteudo/txcred/Reports/TaxasCredito-Consolidadas-porTaxasAnuais-Historico.rdl&parametros=&exibeparametros=true'
resposta = requests.get(urlBcb)
dictResposta = resposta.json()
entrada = extrairListasDeValoresDePropriedades(dictResposta)

for tipoPessoa in entrada['tipoPessoa']:
    for modalidade in entrada['modalidade']:
        for encargo in entrada['encargo']:
            for periodoInicial in entrada['periodoInicial']:
                csvEntrada.writerow([tipoPessoa, modalidade, encargo, dataTraducaoMascara(periodoInicial), False, False])
