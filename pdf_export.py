from reportlab.lib.units import inch
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Spacer, Paragraph
from reportlab.lib.styles import getSampleStyleSheet

def generate_pdf(filepath, texts, data, title, pdf_header, column_header, headers) :
    style = getSampleStyleSheet()['Title']
    
    boxdata = [[texts['surname'], texts['form']],
        [texts['first_name'], texts['date']],
        ["", ""],
        [texts['mark'], ""]]
    if column_header and headers :
        data.insert(0, headers)
    story = []

    page_width, page_height = A4
    aW, aH = page_width - 1 * inch, page_height - 2.5 * inch
        
    story.append(Paragraph(title, style))
    story.append(Spacer(1, 0.25 * inch))

    if pdf_header :
        col_width = aW / len(boxdata[0])
        row_height = 15
        aH -= row_height * len(boxdata)

        boxstyle = TableStyle([('BOX', (0, 0), (-1, -1), 0.5, 'black'),
                    ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
                    ('FONTSIZE', (0, 0), (-1, -1), 12)])
        story.append(Table(boxdata, style=boxstyle, colWidths=col_width, rowHeights=row_height))

        story.append(Spacer(1, 0.5 * inch))

    col_width = aW / len(data[0])
    row_height = aH / len(data)
    if row_height < 18 :
        row_height = 18

    tblstyle = TableStyle([('GRID', (0, 0), (-1, -1), 0.5, 'black'),
                    ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
                    ('FONTSIZE', (0, 0), (-1, -1), 12),
                    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                    ('ALIGN', (0, 0), (-1, -1), 'CENTER')])
    story.append(Table(data, style=tblstyle, colWidths=col_width, rowHeights=row_height))

    doc = SimpleDocTemplate(filepath, pagesize=A4, topmargin=0, bottomMargin=0)
    doc.build(story)
