from services.contact import Contact
from persistent.concat_save import RepoContact
from pathlib import Path
import os
import json
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter


FOLDER_EXPORT = Path("export")

def exportJSON(repo: RepoContact, path = ""):
    
    if path == "":
        r_path = FOLDER_EXPORT
    else: 
        r_path = Path(path)
    
    l = []
    for key  in repo.getIndex().getIndex():
        data = repo.loadByID(key)
        l.append(data.setJson())
    
    if r_path == FOLDER_EXPORT:
        if len(l) > 0:
            FOLDER_EXPORT.mkdir(parents=True, exist_ok=True)
            with open(FOLDER_EXPORT / "contactos.json", 'w', encoding='utf-8') as file:
                json.dump(l, file, ensure_ascii=False, indent=4)
    else:
        if len(l) > 0:
            with open(r_path / "contactos.json", 'w', encoding='utf-8') as file:
                json.dump(l, file, ensure_ascii=False, indent=4)
                
                
def exportPDF(repo: RepoContact, path = ""):
    if path == "":
        r_path = FOLDER_EXPORT
    else: 
        r_path = Path(path)
    
    file_path = str(r_path / "reporte_contactos.pdf")
    pdf = canvas.Canvas(file_path, pagesize=letter)
    l = []
    for key in repo.getIndex().getIndex():
        data = repo.loadByID(key)
        if data:
            l.append(data.setJson())
    
    if not l:
        raise Exception("Datos no encontrados")
    
    def draw_header(c):
        c.setFont("Helvetica-Bold", 14)
        c.drawString(50, 750, "REPORTE DE CONTACTOS")
        c.setFont("Helvetica-Bold", 10)
        c.drawString(50, 710, "ID")
        c.drawString(90, 710, "NOMBRE")
        c.drawString(220, 710, "TELÉFONO")
        c.drawString(310, 710, "CORREO")
        c.drawString(450, 710, "CIUDAD")
        c.setLineWidth(1)
        c.line(50, 700, 560, 700)
    draw_header(pdf)
    
    y = 670
    pdf.setFont("Helvetica", 9)
    
    for d in l:
        if y < 50:
            pdf.showPage()
            draw_header(pdf)
            y = 670
            pdf.setFont("Helvetica", 9)
        pdf.drawString(50, y, str(d.get("id", "")))
        pdf.drawString(90, y, str(d.get("name", "")))
        pdf.drawString(220, y, str(d.get("phone", "")))
        pdf.drawString(310, y, str(d.get("email", "")))
        pdf.drawString(450, y, str(d.get("city", "")))
        y -= 20
        
    pdf.save()