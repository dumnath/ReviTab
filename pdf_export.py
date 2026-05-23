from reportlab.lib.units import inch
from reportlab.lib.pagesizes import A4
from reportlab.platypus import BaseDocTemplate, Table, TableStyle, Spacer, Paragraph, Frame, PageTemplate
from reportlab.lib.styles import getSampleStyleSheet

def generate_pdf(filepath, texts, data, title, pdf_header, column_header, headers, insert_image_after) :
    style = getSampleStyleSheet()['Title']
    
    boxdata = [[texts['surname'], texts['form']],
        [texts['first_name'], texts['date']],
        ["", ""],
        [texts['mark'], ""]]
    if column_header and headers :
        data.insert(0, headers)
    story = []

    page_width, page_height = A4
    aW = page_width - 1 * inch
    if insert_image_after :
        aH = page_height - 3 * inch
    else :
        aH = page_height - 1.5 * inch

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

        story.append(Spacer(1, 0.25 * inch))

    col_width = aW / len(data[0])
    row_height = aH / len(data)
    if row_height < 17 :
        row_height = 17

    tblstyle = TableStyle([('GRID', (0, 0), (-1, -1), 0.5, 'black'),
                    ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
                    ('FONTSIZE', (0, 0), (-1, -1), 12),
                    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                    ('ALIGN', (0, 0), (-1, -1), 'CENTER')])
    story.append(Table(data, style=tblstyle, colWidths=col_width, rowHeights=row_height))
    frame = Frame(0, 0, A4[0], A4[1] - 0.3 * inch, id='normal')
    template = PageTemplate(id='normal', frames=frame)

    doc = BaseDocTemplate(filepath, pagesize=A4, topmargin=0.5 * inch, bottomMargin=0.5 * inch)
    doc.addPageTemplates([template])
    doc.build(story)
