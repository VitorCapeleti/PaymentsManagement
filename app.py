from flask import Flask, render_template, request, url_for, redirect
import os
from entities.archive import Archive
from operations.graph import Graph
from datetime import datetime

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    message = ""
    if request.method == 'POST':
        if request.form.get('archive'):
            archiveName = request.form.get('archive')
            archive = Archive(name=archiveName)
            archive.load_csv_file(archiveName)
        else:
            archive = Archive(name=request.form.get('archiveName'))
        
        for item in range(len(request.form.getlist('name'))):
            data = {}
            if request.form.getlist('name')[item] == "" or request.form.getlist('amount')[item] == "" or request.form.getlist('date')[item] == "" or request.form.getlist('category')[item] == "":
                continue
            else:
                data['Produto'] = request.form.getlist('name')[item]
                data['Valor'] = float(request.form.getlist('amount')[item])
                data['Data'] = datetime.strptime(request.form.getlist('date')[item], "%Y-%m-%d")
                data['Categoria'] = request.form.getlist('category')[item]
                archive.set_dados(data)
        archive.export_csv_file()
        graph = Graph("Gastos Mensais", "Valor gasto", "Categoria")
        dataPayment = archive.pandasData.groupby("Categoria")["Valor"].sum()
        graphBase64 = graph.plotLineGraph(dataPayment)
        return render_template('index.html', message=message, graphBase64=graphBase64)
    return render_template('index.html', message=message, graphBase64=None)

