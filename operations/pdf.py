import io
import base64
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
        
    
    def createPdf(self, img1, img2, img3):
        pdf_buffer = io.BytesIO()
        pdf = canvas.Canvas(pdf_buffer, pagesize=A4)
        page_width, page_height = A4
        img_reader1 = self.convertImg(img1)
        img_reader2 = self.convertImg(img2)
        img_reader3 = self.convertImg(img3)
        
        pdf.setFont("Helvetica-Bold", 16)
        pdf.drawString(50, page_height - 50, f"Relatório: {self.name}")
        pdf.drawImage(img_reader1, 50, page_height - 270, width=500, height=200, preserveAspectRatio=True, mask='auto')
        pdf.drawImage(img_reader2, 50, page_height - 500, width=500, height=200, preserveAspectRatio=True, mask='auto')
        pdf.drawImage(img_reader3, 50, page_height - 730, width=500, height=200, preserveAspectRatio=True, mask='auto')
        pdf.showPage()
        pdf.save()
        pdf_buffer.seek(0)
        return pdf_buffer