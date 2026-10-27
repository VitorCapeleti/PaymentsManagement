from flask import Flask, render_template, request, redirect, url_for, session, send_file
from werkzeug.utils import secure_filename
from datetime import datetime
import os
from dotenv import load_dotenv
load_dotenv()
from entities.archive import Archive
from entities.ai_model import AiModel
from operations.graph import Graph
from operations.pdf import Pdf

app = Flask(__name__)
app.secret_key = os.environ.get('APP_FLASK_SECRET_KEY')

def build_graph(df, graphType):
    """Builds the base64 graph for the current dataframe, or None when there is no data"""
    if df is None or df.empty:
        return None
    graph = Graph("Gastos Mensais", "Valor gasto", "Categoria")
    if graphType == 'pie':
        return graph.plotPieGraph(df.groupby("Categoria")["Valor"].sum())
    if graphType == 'line':
        return graph.plotLinePointGraph(df.set_index('Data').resample('D')["Valor"].sum())
    return graph.plotLineGraph(df.groupby("Categoria")["Valor"].sum())

def income_summary(df):
    """Income informed in the session minus the sum of the spending in the table"""
    income = session.get('income')
    total_spent = float(df['Valor'].sum()) if df is not None and not df.empty else 0.0
    balance = income - total_spent if income is not None else None
    return {'income': income, 'total_spent': total_spent, 'balance': balance}

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
            session.pop('income', None)
            message = f"Arquivo '{filename}' carregado com sucesso!"
            
        elif new_archive_name:
            filename = new_archive_name if new_archive_name.endswith('.csv') else f"{new_archive_name}.csv"
            session['current_archive'] = filename
            session.pop('income', None)
            message = f"Nova área de trabalho '{filename}' criada."

        if 'current_archive' not in session:
            message = "Por favor, envie um arquivo CSV ou crie um novo."
            return render_template('index.html', message=message, df=current_df, graphBase64=graphBase64, summary=income_summary(current_df))

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
            
        graphBase64 = build_graph(current_df, request.form.get('graphType', 'barH'))

        if 'HX-Request' in request.headers:
            return render_template('partials/workspace.html', message=message, df=current_df, graphBase64=graphBase64, summary=income_summary(current_df))

    return render_template('index.html', message=message, df=current_df, graphBase64=graphBase64, summary=income_summary(current_df))

@app.route('/delete/<int:row_index>', methods=['POST'])
def delete_row(row_index):
    """Deletes a specific row based on its Pandas Index"""
    if 'current_archive' not in session:
        return "Erro de sessão", 400
        
    archive = Archive(name=session['current_archive'])
    archive.load_csv_file(session['current_archive'])
    archive.delete_row(row_index)
    message = "Item removido com sucesso!"
    
    graphBase64 = build_graph(archive.pandasData, request.form.get('graphType', 'barH'))
    return render_template('partials/workspace.html', message=message, df=archive.pandasData, graphBase64=graphBase64, summary=income_summary(archive.pandasData))

@app.route('/income', methods=['POST'])
def set_income():
    """Saves the income informed by the user for the current session and recalculates the balance"""
    if 'current_archive' not in session:
        return "Erro de sessão", 400

    try:
        session['income'] = float(request.form.get('income', '').replace(',', '.'))
        message = "Renda atualizada com sucesso!"
    except ValueError:
        message = "Informe um valor de renda válido."

    archive = Archive(name=session['current_archive'])
    try:
        archive.load_csv_file(session['current_archive'])
    except FileNotFoundError:
        pass

    graphBase64 = build_graph(archive.pandasData, request.form.get('graphType', 'barH'))
    return render_template('partials/workspace.html', message=message, df=archive.pandasData, graphBase64=graphBase64, summary=income_summary(archive.pandasData))

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
    
    ai_chat = AiModel('phi4-mini')
    report = ai_chat.generate_report(archive.pandasData.to_markdown(index=False))
    
    dataPayment = archive.pandasData.groupby("Categoria")["Valor"].sum()
    graph = Graph("Gastos Mensais", "Valor gasto", "Categoria")
    img1 = graph.plotLineGraph(dataPayment)
    img2 = graph.plotPieGraph(dataPayment)
    dataPayment2 = archive.pandasData.set_index('Data').resample('D')["Valor"].sum()
    img3 = graph.plotLinePointGraph(dataPayment2)
    
    now = datetime.now()
    name_pdf = f"Relatorio_{now.strftime('%B_%Y')}.pdf"
    pdf = Pdf(name_pdf)
    final_pdf = pdf.createPdf(img1, img2, img3, report)
    return send_file(final_pdf, as_attachment=True, download_name=name_pdf, mimetype='application/pdf')
    