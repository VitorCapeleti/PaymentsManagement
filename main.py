from entities.archive import Archive
from operations.graph import Graph
import pandas as pd
from datetime import datetime

archive1 = Archive("Gastos Fevereiro")
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
        archive1.adicionar_dados(data)
    else:
        print("Opção inválida\n")
frameData = pd.DataFrame(archive1.data)
print(frameData.head())
graph1 = Graph("Gastos Mensais", "Valor gasto", "Categoria")
dataPayment = frameData.groupby("Categoria")["Valor"].sum()
print(graph1.plotLineGraph(dataPayment))
