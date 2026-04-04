from entities.archive import Archive
from operations.graph import Graph
from datetime import datetime

print("\n Pressione 1 para adicionar os dados ou 2 paracarregar um arquivo existente \n")
while True:
    inputOpt = int(input("1 ou 2: "))
    if(inputOpt == 2):
        path = input("Digite o caminho do arquivo: ")
        archive1 = Archive(path)
        archive1.load_csv_file(path)
        break
    elif(inputOpt == 1):
        nameArchive = input("Digite o nome do arquivo: ")
        archive1 = Archive(nameArchive)
        break
    else:
        print("Opção inválida\n")
        
print("-" * 25)
print("\n 1 para adicionar os dados, 2 para sair\n")
print("-" * 25)
while True:
    data = {}
    option = int(input("Escolha opção 1 ou 2: "))
    if(option == 2):
        break
    elif(option == 1):
        data['Produto'] = input("Digite o nome do produto: ")
        data['Valor'] = float(input("Digite o valor gasto: "))
        data['Categoria'] = input("Digite a categoria: ")
        data['Data'] = datetime.strptime(input("Data (dd/mm/yyyy): "), "%d/%m/%Y")
        archive1.set_dados(data)
    else:
        print("Opção inválida\n")

print("Gostaria de exportar um arquivo CSV? 1 para sim 2 para não")
while True:
    inputOpt = int(input("1 ou 2: "))
    if(inputOpt == 1):
        archive1.export_csv_file()
        break
    elif(inputOpt == 2):
        break
    else:
        print("Opção inválida\n")
print(archive1.pandasData.head())
graph1 = Graph("Gastos Mensais", "Valor gasto", "Categoria")
dataPayment = archive1.pandasData.groupby("Categoria")["Valor"].sum()
print(graph1.plotLineGraph(dataPayment))
