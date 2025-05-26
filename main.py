from reportlab.pdfgen.canvas import Canvas
from reportlab.platypus import SimpleDocTemplate, Paragraph, Frame, PageTemplate, NextPageTemplate, NextFrameFlowable, PageBreak, FrameBreak, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter



page_width, page_height = letter
section_height = page_height / 3

frame1 = Frame(0, 2*section_height, page_width, section_height, 10, 10, 10, 10)
frame2 = Frame(0, section_height, page_width, section_height, 10, 10, 10, 10)
frame3 = Frame(0, 0, page_width, section_height, 10, 10, 10, 10)

def draw_background(canvas: Canvas, doc: SimpleDocTemplate):
    # Section 1 - Light Blue
    canvas.setFillColor(colors.lightblue)
    canvas.rect(0, 2*section_height, page_width, section_height, fill=1, stroke=0)
    
    # Section 2 - Light Green
    canvas.setFillColor(colors.lightgreen)
    canvas.rect(0, section_height, page_width, section_height, fill=1, stroke=0)
    
    # Section 3 - Light Pink
    canvas.setFillColor(colors.pink)
    canvas.rect(0, 0, page_width, section_height, fill=1, stroke=0)

def create_template(id, x, y, width, height, bg_color: colors.Color):
    frame = Frame(x, y, width, height, 10, 10, 10, 10)

    def draw_background(canvas: Canvas, doc: SimpleDocTemplate):
        canvas.setFillColor(bg_color)
        canvas.rect(x, y, width, height, fill=1, stroke=0)

    template = PageTemplate(id=id, frames=[frame], onPage=draw_background)
    return template

template = PageTemplate(frames=[frame1, frame2, frame3], onPage=draw_background)

def create_frame(id, x, y, width, height, top_padding=6, bottom_padding=6, left_padding=6, right_padding=6):
    frame = Frame(x, y, width, height, leftPadding=left_padding, bottomPadding=bottom_padding, rightPadding=right_padding, topPadding=top_padding)
    return frame

def create_template():
    height_step = page_height / 12
    width_step = page_width / 10
    frame1 = create_frame("frame1", 0, 10*height_step, 10*width_step, 2 * height_step, left_padding=10, right_padding=10, top_padding=30, bottom_padding=12)
    frame2 = create_frame("frame2", 0, 0, 8*width_step, 10*height_step, left_padding=10, right_padding=10, top_padding=10, bottom_padding=10)
    frame3 = create_frame("frame3", 8 * width_step, 0, 2*width_step, 10 *height_step, left_padding=2, right_padding=2, top_padding=10, bottom_padding=10)
    def draw_background(canvas: Canvas, doc: SimpleDocTemplate):
        # Section 1 - Light Blue
        canvas.setFillColor(colors.dimgrey)
        canvas.rect(0, 10*height_step, 10*width_step, 2 * height_step, fill=1, stroke=0)
        
        # Section 2 - Light Green
        canvas.setFillColor(colors.ghostwhite)
        canvas.rect(0, 0, 8*width_step, 10*height_step, fill=1, stroke=0)
        
        # Section 3 - Light Pink
        canvas.setFillColor(colors.lightgrey)
        canvas.rect(8 * width_step, 0, 2*width_step, 10 *height_step, fill=1, stroke=0)
    
    template = PageTemplate(frames=[frame1, frame2, frame3], onPage=draw_background)
    return template

def create_styles():
    styles = getSampleStyleSheet()
    title_style = styles['Title']
    return title_style

def create_paragraph_styles(style_name: str):
    title_style = ParagraphStyle(
        name="Title",
        fontSize=36,
        fontName="Helvetica-Bold",
        textColor=colors.black,
        spaceAfter=10,
    )
    header1_style = ParagraphStyle(
        name="Header1",
        fontSize=30,
        fontName="Helvetica-Bold",
        textColor=colors.black,
        spaceAfter=10,
    )
    header2_style = ParagraphStyle(
        name="Header2",
        fontSize=24,
        fontName="Helvetica-Bold",
        textColor=colors.black,
    )
    header3_style = ParagraphStyle(
        name="Header3",
        fontSize=18,
        fontName="Helvetica-Bold",
        textColor=colors.black,
    )
    body_style = ParagraphStyle(
        name="Body",
        fontSize=12,
        fontName="Helvetica",
        textColor=colors.black,
    )
    styles = {
        "title_style": title_style,
        "header1_style": header1_style,
        "header2_style": header2_style,
        "header3_style": header3_style,
        "body_style": body_style,
    }
    return styles[style_name]


def create_header(header_text: str, header_style: str):
    style = create_paragraph_styles(header_style)
    header = Paragraph(header_text, style=style)
    return header

def create_title():
    style = create_paragraph_styles("title_style")
    title = Paragraph("Pranjal Upadhyaya", style=style)
    return title

def create_pdf():
    doc = SimpleDocTemplate("output.pdf", pagesize=letter)
    template = create_template()
    doc.addPageTemplates([template])

    title = create_title()
    designation = create_header("Data Engineer", "header2_style")
    story = []

    # story.append(NextFrameFlowable(0))
    story.append(title)
    story.append(Spacer(1, 30, isGlue=True))
    story.append(designation)
    story.append(NextFrameFlowable(2))
    story.append(FrameBreak())
    story.append(Paragraph("Hello"))
    # story.append(FrameBreak())
    
    # story.append(NextPageTemplate("template2"))
    # story.append(Paragraph("Hello"))
    # story.append(FrameBreak())
    
    # story.append(NextFrameFlowable(2))
    story.append(Paragraph("Hello"))
    # story.append(FrameBreak())
    doc.build(story)


if __name__ == "__main__":
    create_pdf()
    
    
    