import csv
arquivoEntrada = open('entrada.csv', 'a')
csvEntrada = csv.writer(arquivoEntrada, delimiter=';')
csvEntrada.writerow(['Spam1', 'Spam2', 'Spam3'])
