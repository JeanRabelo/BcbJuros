import requests
import csv
from time import sleep
from pprint import pprint

def dataMascaraTraducao(dataMascara):
    dia = dataMascara[:dataMascara.find('/',1)]
    mes = dataMascara[3:5]
    if dia[0] == '0':
        dia = dia[1]
    if mes[0] == '0':
        mes = mes[1]

    ano = dataMascara[-4:]
    dataTraducao = dia + '/' + mes + '/' + ano + r'%2012:00:00%20AM'
    return str(dataTraducao)

def tentar(url, tentativas = 5):
    try:
        sleep(5)
        response = requests.get(url)
    except:
        if tentativas >=0:
            sleep(60 - 10 * tentativas)
            print('tentativas restantes = ' + tentativas)
            response = tentar(url, tentativas - 1)
        else:
            print('deu ruim')
    return response

# Config dicionario
dicionarioArquivo = open('dicionario.csv', 'r')
dicionarioCsv = csv.reader(dicionarioArquivo, delimiter=';')
next(dicionarioCsv)
dicionario = {rows[1]:rows[2] for rows in dicionarioCsv}
# pprint(dicionario)


# Config temporario
temporarioArquivo = open('temporario.csv', 'w', newline='')
temporarioCsv = csv.writer(temporarioArquivo, delimiter=';')
temporarioCsv.writerow(['tipoPessoa', 'modalidade', 'encargo', 'periodoInicial', 'temos', 'ignorar'])

# Config entrada
entradaArquivo = open('entrada.csv', 'r')
entradaCsv = csv.reader(entradaArquivo, delimiter=';')
next(entradaCsv)

for row in entradaCsv:
    tipoPessoa = {'value':dicionario[str(row[0])], 'label':str(row[0])}
    modalidade = {'value':dicionario[str(row[1])], 'label':str(row[1])}
    encargo = {'value':dicionario[str(row[2])], 'label':str(row[2])}
    periodoInicial = dataMascaraTraducao(row[3])
    periodoInicialMascara = row[3]
    temos = row[4]
    ignorar = row[5]

    if temos == 'FALSE' and ignorar == 'FALSE':
        urlCsv = r'https://www.bcb.gov.br/api/relatorio/pt-br/contaspub?path=conteudo/txcred/Reports/TaxasCredito-Consolidadas-porTaxasAnuais-Historico.rdl&nome=RelatorioHist%C3%B3rico%20Posterior%20a%2001/01/2012&parametros=tipoPessoa:' + tipoPessoa['value'] + r';modalidade:' + modalidade['value'] + r';periodoInicial:' + periodoInicial + r';&exportar=CSV&exibeparametros=false'
        response = tentar(urlCsv)
        conteudo = response.content.decode("utf-8", "ignore")
        conteudoCsv = csv.reader(conteudo.splitlines(),delimiter=',')
        path = r'C:\Users\jean_\Documents\GitHub\Upp_BcbJuros\csvs\\' + tipoPessoa['label'] + '-' + modalidade['label'] + '-' + encargo['label'] + '-' + periodoInicialMascara.replace('/','-') + r'.csv'
        arquivo = open(path,'w', newline='', encoding = 'utf-8')
        writer = csv.writer(arquivo)
        writer.writerows(conteudoCsv)
        arquivo.close()
        temporarioCsv.writerow([tipoPessoa['label'], modalidade['label'], encargo['label'], periodoInicialMascara, True, False])
    elif temos == 'TRUE':
        temporarioCsv.writerow([tipoPessoa['label'], modalidade['label'], encargo['label'], periodoInicialMascara, True, ignorar])
    else:
        temporarioCsv.writerow([tipoPessoa['label'], modalidade['label'], encargo['label'], periodoInicialMascara, temos, True])

    print('Baixado o ', end='')
    print([tipoPessoa['label'], modalidade['label'], encargo['label'], periodoInicialMascara])
