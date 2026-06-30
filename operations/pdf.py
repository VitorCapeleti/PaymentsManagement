import io
import base64
import re
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.utils import ImageReader
from reportlab.lib import colors
from reportlab.platypus import Paragraph, Frame, Spacer
from reportlab.lib.styles import getSampleStyleSheet

class Pdf:
    def __init__(self, name: str):
        self.name = name
        
    def convertImg(self, base64_img: str):
        if "base64," in base64_img:
            base64_img = base64_img.split('base64,')[1]
        img_data = base64.b64decode(base64_img)
        return ImageReader(io.BytesIO(img_data))
    
    def createPdf(self, img1, img2, img3, report):
        pdf_buffer = io.BytesIO()
        pdf = canvas.Canvas(pdf_buffer, pagesize=A4)
        page_width, page_height = A4
        img_reader1 = self.convertImg(img1)
        img_reader2 = self.convertImg(img2)
        img_reader3 = self.convertImg(img3)
        pdf.setFillColor(colors.HexColor("#671580"))
        pdf.rect(0, page_height - 60, page_width, 60, fill=1, stroke=0)
        
        pdf.setFillColor(colors.white)
        pdf.setFont("Helvetica-Bold", 18)
        pdf.drawString(30, page_height - 38, f"Dashboard Financeiro: {self.name}")
        
        pdf.setFillColor(colors.black)
        pdf.setStrokeColor(colors.HexColor("#e5e7eb"))
        
        pdf.rect(20, page_height - 380, 270, 300)  
        pdf.rect(305, page_height - 380, 270, 300) 
        pdf.rect(20, page_height - 700, 555, 300)  
        
        pdf.drawImage(img_reader1, 25, page_height - 370, width=260, height=280, preserveAspectRatio=True, mask='auto')
        pdf.drawImage(img_reader2, 310, page_height - 370, width=260, height=280, preserveAspectRatio=True, mask='auto')
        pdf.drawImage(img_reader3, 25, page_height - 690, width=545, height=280, preserveAspectRatio=True, mask='auto')
        
        pdf.showPage() 
        clean_text = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', report)
        clean_text = clean_text.replace('### ', '').replace('## ', '').replace('# ', '')
        styles = getSampleStyleSheet()
        style = styles["Normal"]
        style.fontSize = 11
        style.leading = 16 
        story = []
        raw_paragraphs = clean_text.split('\n')
        
        for p_text in raw_paragraphs:
            p_text = p_text.strip()
            if p_text:
                story.append(Paragraph(p_text, style))
                story.append(Spacer(1, 12))
        margin = 30
        frame_width = page_width - (2 * margin)
        frame_height = page_height - 120 
        max_pages = 50 
        current_page = 0
        
        while len(story) > 0 and current_page < max_pages:
            current_page += 1
            
            pdf.setFillColor(colors.HexColor("#671580"))
            pdf.rect(0, page_height - 60, page_width, 60, fill=1, stroke=0)
            pdf.setFillColor(colors.white)
            pdf.setFont("Helvetica-Bold", 18)
            pdf.drawString(30, page_height - 38, "Relatório Detalhado da IA")
            pdf.setFillColor(colors.black)
            
            f = Frame(margin, margin, frame_width, frame_height, showBoundary=0)
            f.addFromList(story, pdf)
            
            if len(story) > 0:
                pdf.showPage()
                
        pdf.save()
        pdf_buffer.seek(0)
        return pdf_buffer