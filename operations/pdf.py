import io
import base64
import textwrap
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.utils import ImageReader

class Pdf:
    def __init__(self, name: str):
        self.name = name
        
    def convertImg(self, base64_img: str):
        if "base64," in base64_img:
            base64_img = base64_img.split('base64,')[1]
        img_data = base64.b64decode(base64_img)
        return ImageReader(io.BytesIO(img_data))
    
    @staticmethod
    def convertText(pdf, x, y, text):
        safe_text = str(text)
        lines = textwrap.wrap(safe_text, width=92)
        leading = pdf._leading
        for line in lines:
            pdf.drawString(x, y, line)
            y -= leading
        return y
    
    def createPdf(self, img1, img2, img3, report):
        pdf_buffer = io.BytesIO()
        pdf = canvas.Canvas(pdf_buffer, pagesize=A4)
        page_width, page_height = A4
        img_reader1 = self.convertImg(img1)
        img_reader2 = self.convertImg(img2)
        img_reader3 = self.convertImg(img3)
        
        pdf.setFont("Helvetica-Bold", 16)
        pdf.drawString(50, page_height - 50, f"Relatório: {self.name}")
        pdf.drawImage(img_reader1, 5, page_height - 520, width=280, preserveAspectRatio=True, mask='auto')
        pdf.drawImage(img_reader2, 320, page_height - 520, width=280, preserveAspectRatio=True, mask='auto')
        pdf.drawImage(img_reader3, 5, page_height - 820, width=280, preserveAspectRatio=True, mask='auto')
        pdf.showPage()
        pdf.setFont("Helvetica-Bold", 16)
        pdf.drawString(50, page_height - 50, "Relatório Detalhado de Gastos: ")
        pdf.setFont("Helvetica", 12)
        self.convertText(pdf, 15, page_height - 80, report)
        pdf.save()
        pdf_buffer.seek(0)
        return pdf_buffer