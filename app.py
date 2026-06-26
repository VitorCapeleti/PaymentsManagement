from flask import Flask, render_template, request, redirect, url_for, session, send_file
from werkzeug.utils import secure_filename
from datetime import datetime
from entities.archive import Archive
from operations.graph import Graph
from operations.pdf import Pdf

app = Flask(__name__)
app.secret_key = "XXX" 

@app.route('/', methods=['GET', 'POST'])
def index():
    message = ""
    graphBase64 = None
    current_df = None

    if request.method == 'POST':
        uploaded_file = request.files.get('archive')
        new_archive_name = request.form.get('archiveName')

        if uploaded_file and uploaded_file.filename != '':
            filename = secure_filename(uploaded_file.filename)
            uploaded_file.save(filename)
            session['current_archive'] = filename
            message = f"Arquivo '{filename}' carregado com sucesso!"
            
        elif new_archive_name:
            filename = new_archive_name if new_archive_name.endswith('.csv') else f"{new_archive_name}.csv"
            session['current_archive'] = filename
            message = f"Nova área de trabalho '{filename}' criada."

        if 'current_archive' not in session:
            message = "Por favor, envie um arquivo CSV ou crie um novo."
            return render_template('index.html', message=message, df=current_df, graphBase64=graphBase64)

        archive = Archive(name=session['current_archive'])
        try:
            archive.load_csv_file(session['current_archive'])
            current_df = archive.pandasData
        except FileNotFoundError:
            pass

        names = request.form.getlist('name')
        if names and names[0].strip() != "":
            data = {
                'Produto': names,
                'Valor': list(map(float, request.form.getlist('amount'))),
                'Data': request.form.getlist('date'),
                'Categoria': request.form.getlist('category')
            }
            archive.set_dados(data)
            archive.export_csv_file()
            current_df = archive.pandasData
            message = "Novo item salvo com sucesso!"
            
        if current_df is not None and not current_df.empty:
            graphType = request.form.get('graphType', 'barH')
            graph = Graph("Gastos Mensais", "Valor gasto", "Categoria")
            
            if graphType == 'barH':
                dataPayment = archive.pandasData.groupby("Categoria")["Valor"].sum()
                graphBase64 = graph.plotLineGraph(dataPayment)
            elif graphType == 'pie':
                dataPayment = archive.pandasData.groupby("Categoria")["Valor"].sum()
                graphBase64 = graph.plotPieGraph(dataPayment)
            elif graphType == 'line':
                dataPayment = archive.pandasData.set_index('Data').resample('D')["Valor"].sum()
                graphBase64 = graph.plotLinePointGraph(dataPayment)

        if 'HX-Request' in request.headers:
            return render_template('partials/workspace.html', message=message, df=current_df, graphBase64=graphBase64)

    return render_template('index.html', message=message, df=current_df, graphBase64=graphBase64)

@app.route('/delete/<int:row_index>', methods=['POST'])
def delete_row(row_index):
    """Deletes a specific row based on its Pandas Index"""
    if 'current_archive' not in session:
        return "Erro de sessão", 400
        
    archive = Archive(name=session['current_archive'])
    archive.load_csv_file(session['current_archive'])
    archive.delete_row(row_index)
    message = "Item removido com sucesso!"
    
    graphType = request.form.get('graphType', 'barH')
    graph = Graph("Gastos Mensais", "Valor gasto", "Categoria")
    dataPayment = archive.pandasData.groupby("Categoria")["Valor"].sum()
    if graphType == 'barH':
        graphBase64 = graph.plotLineGraph(dataPayment)
    elif graphType == 'pie':
        graphBase64 = graph.plotPieGraph(dataPayment)
    elif graphType == 'line':
        dataPayment = archive.pandasData.set_index('Data').resample('D')["Valor"].sum()
        graphBase64 = graph.plotLinePointGraph(dataPayment)
    return render_template('partials/workspace.html', message=message, df=archive.pandasData, graphBase64=graphBase64)

@app.route('/export',  methods=['POST'])
def export_file():
    """Allows the user to download the current working CSV"""
    if 'current_archive' not in session:
        return redirect(url_for('index'))
    file_path = session['current_archive']
    custom_name = request.form.get('export_name', 'exportado.csv').strip()
    if not custom_name.endswith('.csv'):
        custom_name += '.csv'
        
    return send_file(file_path, as_attachment=True, download_name=custom_name)

@app.route('/export/pdf', methods=['POST'])
def export_pdf():
    if 'current_archive' not in session:
        return redirect(url_for('index'))
    file_path = session['current_archive']
    archive = Archive(name = file_path)
    archive.load_csv_file(file_path)
    dataPayment = archive.pandasData.groupby("Categoria")["Valor"].sum()
    graph = Graph("Gastos Mensais", "Valor gasto", "Categoria")
    img1 = graph.plotLineGraph(dataPayment)
    img2 = graph.plotPieGraph(dataPayment)
    dataPayment2 = archive.pandasData.set_index('Data').resample('D')["Valor"].sum()
    img3 = graph.plotLinePointGraph(dataPayment2)
    now = datetime.now()
    name_pdf = f"Relatorio_{now.strftime('%B_%Y')}.pdf"
    pdf = Pdf(name_pdf)
    final_pdf = pdf.createPdf(img1, img2, img3)
    return send_file(final_pdf, as_attachment=True, download_name=name_pdf, mimetype='application/pdf')
    