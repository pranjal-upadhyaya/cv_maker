from reportlab.pdfgen.canvas import Canvas
from reportlab.platypus import SimpleDocTemplate, Paragraph, Frame, PageTemplate, NextPageTemplate, NextFrameFlowable, PageBreak, FrameBreak, Spacer, Flowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter



page_width, page_height = letter
section_height = page_height / 3

frame1 = Frame(0, 2*section_height, page_width, section_height, 10, 10, 10, 10)
frame2 = Frame(0, section_height, page_width, section_height, 10, 10, 10, 10)
frame3 = Frame(0, 0, page_width, section_height, 10, 10, 10, 10)

class LineFlowable(Flowable):
    def __init__(self, x, y, width, height=1, color=colors.black, thickness=1):
        Flowable.__init__(self)
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.thickness = thickness
    
    def wrap(self, availWidth, availHeight):
        return self.width, self.height
    
    def draw(self):
        self.canv.setStrokeColor(self.color)
        self.canv.setLineWidth(self.thickness)
        # Draw line in the middle of the flowable's height
        self.canv.line(self.x, self.y, self.x + self.width, self.y)

def create_line(x, y, width, height=1, color=colors.black, thickness=1):
    """
    Create a horizontal line flowable
    
    Args:
        width: Line width in points (defaults to page width minus padding)
        height: Line height/space in points
        color: Line color
        thickness: Line thickness in points
    """
    
    return LineFlowable(x, y, width, height, color, thickness)

class SideBySideFlowable(Flowable):
    def __init__(self, left_content, right_content, left_width_ratio=0.5):
        Flowable.__init__(self)
        self.left_content = left_content
        self.right_content = right_content
        self.left_width_ratio = left_width_ratio
        self.right_width_ratio = 1 - left_width_ratio
        
    def wrap(self, availWidth, availHeight):
        # Calculate widths for each side
        left_width = availWidth * self.left_width_ratio
        right_width = availWidth * self.right_width_ratio
        
        # Wrap both contents
        left_w, left_h = self.left_content.wrap(left_width, availHeight)
        right_w, right_h = self.right_content.wrap(right_width, availHeight)
        
        # Store the calculated dimensions for use in draw()
        self.left_width = left_width
        self.left_h = left_h
        self.right_h = right_h
        
        # Return the total width and max height
        return availWidth, max(left_h, right_h)
    
    def draw(self):
        # Draw left content at bottom-left
        self.left_content.drawOn(self.canv, 0, 0)
        
        # Draw right content at bottom-right, aligned to same baseline
        self.right_content.drawOn(self.canv, self.left_width, 0)

def create_side_by_side_headers(left_text, right_text, left_style, right_style, left_width_ratio=0.5):
    """
    Create two headers side by side
    
    Args:
        left_text: Text for left header
        right_text: Text for right header
        left_style: Style for left header
        right_style: Style for right header
        left_width_ratio: Proportion of width for left header (0.0 to 1.0)
    """
    left_header = create_header(left_text, left_style)
    right_header = create_header(right_text, right_style)
    
    return SideBySideFlowable(left_header, right_header, left_width_ratio)

def create_hyperlink(url, display_text, color="blue", underline=True):
    """Create a hyperlink with custom styling"""
    if underline:
        return f'<a href="{url}" color="{color}" underline="1">{display_text}</a>'
    else:
        return f'<a href="{url}" color="{color}">{display_text}</a>'

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
    height_step = page_height / 18
    width_step = page_width / 12
    frame1 = create_frame("frame1", 0, 16*height_step, 12*width_step, 2 * height_step, left_padding=12, right_padding=12, top_padding=10, bottom_padding=10)
    frame2 = create_frame("frame2", 0, 0, 8*width_step, 16*height_step, left_padding=12, right_padding=12, top_padding=10, bottom_padding=10)
    frame3 = create_frame("frame3", 8 * width_step, 0, 4*width_step, 16 *height_step, left_padding=12, right_padding=12, top_padding=10, bottom_padding=10)
    def draw_background(canvas: Canvas, doc: SimpleDocTemplate):
        # Section 1 - Light Blue
        canvas.setFillColor(colors.darkslategrey)
        canvas.rect(0, 16*height_step, 12*width_step, 2 * height_step, fill=1, stroke=0)
        
        # Section 2 - Light Green
        canvas.setFillColor(colors.ghostwhite)
        canvas.rect(0, 0, 8*width_step, 16*height_step, fill=1, stroke=0)
        
        # Section 3 - Light Pink
        canvas.setFillColor(colors.lightgrey)
        canvas.rect(8 * width_step, 0, 4*width_step, 16 *height_step, fill=1, stroke=0)
    
    template = PageTemplate(frames=[frame1, frame2, frame3], onPage=draw_background)
    return template

def create_template_v2():
    width_step = page_width / 12
    frame1 = create_frame("frame1", 0, 0, 8*width_step, page_height, left_padding=12, right_padding=12, top_padding=10, bottom_padding=10)
    frame2 = create_frame("frame2", 8*width_step, 0, 4*width_step, page_height, left_padding=12, right_padding=12, top_padding=10, bottom_padding=10)
    def draw_background(canvas: Canvas, doc: SimpleDocTemplate):
        # Section 2 - Light Green
        canvas.setFillColor(colors.ghostwhite)
        canvas.rect(0, 0, 8*width_step, page_height, fill=1, stroke=0)
        
        # Section 3 - Light Pink
        canvas.setFillColor(colors.lightgrey)
        canvas.rect(8 * width_step, 0, 4*width_step, page_height, fill=1, stroke=0)

    template = PageTemplate(frames=[frame1, frame2], onPage=draw_background)
    return template
        
        

def create_styles():
    styles = getSampleStyleSheet()
    title_style = styles['Title']
    return title_style

def create_paragraph_styles(style_name: str):
    title_style = ParagraphStyle(
        name="Title",
        fontSize=30,
        fontName="Helvetica-Bold",
        textColor=colors.black,
        spaceAfter=10,
    )
    title_style_light = ParagraphStyle(
        name="TitleLight",
        fontSize=30,
        fontName="Helvetica-Bold",
        textColor=colors.white,
        spaceAfter=10,
    )
    header1_style = ParagraphStyle(
        name="Header1",
        fontSize=24,
        fontName="Helvetica-Bold",
        textColor=colors.black,
        spaceAfter=10,
    )
    header1_style_light = ParagraphStyle(
        name="Header1Light",
        fontSize=24,
        fontName="Helvetica-Bold",
        textColor=colors.white,
    )
    header2_style = ParagraphStyle(
        name="Header2",
        fontSize=20,
        fontName="Helvetica-Bold",
        textColor=colors.black,
    )
    header2_style_light = ParagraphStyle(
        name="Header2Light",
        fontSize=20,
        fontName="Helvetica-Bold",
        textColor=colors.white,
    )
    header3_style = ParagraphStyle(
        name="Header3",
        fontSize=16,
        fontName="Helvetica-Bold",
        textColor=colors.black,
    )
    header3_style_light = ParagraphStyle(
        name="Header3Light",
        fontSize=16,
        fontName="Helvetica-Bold",
        textColor=colors.white,
    )
    header4_style = ParagraphStyle(
        name="Header4",
        fontSize=12,
        fontName="Helvetica-Bold",
        textColor=colors.black,
    )
    header5_style = ParagraphStyle(
        name="Header5",
        fontSize=12,
        fontName="Helvetica-Bold",
        textColor=colors.dimgrey,
    )
    body_style = ParagraphStyle(
        name="Body",
        fontSize=10,
        fontName="Helvetica",
        textColor=colors.black,
    )
    body_style_bold = ParagraphStyle(
        name="BodyBold",
        fontSize=10,
        fontName="Helvetica-Bold",
        textColor=colors.black,
    )
    body_style_italic = ParagraphStyle(
        name="BodyItalic",
        fontSize=10,
        fontName="Helvetica-Oblique",
        textColor=colors.dimgrey,
    )
    body_dim = ParagraphStyle(
        name="BodyDim",
        fontSize=10,
        fontName="Helvetica",
        textColor=colors.dimgrey,
    )
    bullet_point_style = ParagraphStyle(
        name="BulletPointStyle",
        bulletFontSize=10,
        bulletFontName="Helvetica",
        bulletIndent=2,
        leftIndent=12,
        textColor=colors.black,
    )
    styles = {
        "title_style": title_style,
        "title_style_light": title_style_light,
        "header1_style": header1_style,
        "header1_style_light": header1_style_light,
        "header2_style": header2_style,
        "header2_style_light": header2_style_light,
        "header3_style": header3_style,
        "header3_style_light": header3_style_light,
        "header4_style": header4_style,
        "header5_style": header5_style,
        "body_style": body_style,
        "body_style_bold": body_style_bold,
        "body_style_italic": body_style_italic,
        "body_dim": body_dim,
        "bullet_point_style": bullet_point_style,
    }
    return styles[style_name]


def create_header(header_text: str, header_style: str):
    style = create_paragraph_styles(header_style)
    header = Paragraph(header_text, style=style)
    return header

def create_title(title_text: str, title_style: str):
    style = create_paragraph_styles(title_style)
    title = Paragraph(title_text, style=style)
    return title

def create_body(body_text: str):
    style = create_paragraph_styles("body_style")
    body = Paragraph(body_text, style=style)
    return body

def create_body_italic(body_text: str):
    style = create_paragraph_styles("body_style_italic")
    body = Paragraph(body_text, style=style)
    return body

def create_body_dim(body_text: str):
    style = create_paragraph_styles("body_dim")
    body = Paragraph(body_text, style=style)
    return body

def create_bullet_point(text: str):
    style = create_paragraph_styles("bullet_point_style")
    bullet_point = Paragraph(text = text, bulletText = "•", style=style)
    return bullet_point

def create_pdf():
    doc = SimpleDocTemplate("output.pdf", pagesize=letter)
    template = create_template()
    template_v2 = create_template_v2()
    doc.addPageTemplates([template, template_v2])

    title = create_title("Pranjal Upadhyaya", "title_style_light")
    designation = create_header("Data Engineer", "header2_style_light")
    story = []

    # story.append(NextFrameFlowable(0))
    story.append(title)
    story.append(Spacer(1, 24, isGlue=True))
    story.append(designation)
    story.append(NextFrameFlowable(1))
    story.append(FrameBreak())
    story.append(create_body("Experienced Data Engineer with a strong proficiency in Python and SQL, specializing in database management, data pipeline creation, and API development. Skilled at designing, constructing, and optimizing robust data processing systems to ensure efficient data flow and accessibility. Demonstrated expertise in building scalable ETL pipelines, managing complex SQL databases, and developing APIs to support seamless data integration across platforms. Adept at collaborating with cross-functional teams to deliver high-quality, reliable data solutions that drive business insights and operational efficiency"))
    story.append(Spacer(1, 24, isGlue=True))
    # story.append(FrameBreak())
    
    # story.append(NextPageTemplate("template2"))
    # story.append(Paragraph("Hello"))
    # story.append(FrameBreak())

    astuto_data_engineer_experience = [
        "Developed and maintained 100+ APIs, contributing extensively to API development initiatives.",
        "Managed and optimized API microservices architecture to ensure high performance and scalability.",
        "Designed, built, and maintained multiple scalable data pipelines using Dagster, ingesting and processing multiple terabytes of data on a daily basis.",
        "Worked extensively with PostgreSQL and ClickHouse databases, overseeing database maintenance and optimization.",
        "Utilized database systems for advanced data analysis to support business decision-making.",
        "Gained extensive hands-on experience with AWS, deploying and maintaining cloud resources to ensure secure, scalable, and reliable infrastructure.",
        "Led end-to-end development of high-volume data pipelines to ingest and transform AWS Cost and Usage Reports (CUR), analyzing and processing multi-terabyte datasets for storage in PostgreSQL and ClickHouse databases.",
        "Optimized database performance through partitioning, indexing, and distributed processing strategies to efficiently handle massive data loads.",
        "Designed and implemented fault-tolerant ETL workflows using Dagster, ensuring data integrity across a microservices architecture.",
        "Developed the entire API infrastructure for fetching multi-terabyte AWS CUR data stored in PostgreSQL and ClickHouse databases.",
        "Optimized large customer-facing APIs to achieve response times of less than 100 milliseconds by implementing advanced query optimization techniques and strategic indexing on frequently queried database columns.",
        "Led the end-to-end development of cloud cost calculation modules, overseeing both data pipeline and API development and maintenance, and managed a team of 4 developers to deliver robust, scalable solutions for accurate cloud cost analytics.",
        "Collaborated as part of a four-member team to optimize database systems, achieving a 75% reduction in database size through data migration, targeted data deletion, and API modifications for compatibility with the streamlined data structure.",
    ]

    oceanfrogs_data_engineer_experience = [
        "Created Selenium based web scrapers to extract data from various websites.",
        "Created and maintained python based data pipelines.",
        "Heavily involved in data cleaning and feature engineering.",
        "Frequently undertook DB migrations and optimizations to improve data quality and consistency.",
        "Created custom dashboards and data extraction tools for visualizing and analyzing data using Appsmith. These were used by the sales team to close deals.",
    ]

    thesis = create_hyperlink("http://dr.iiserpune.ac.in:8080/xmlui/handle/123456789/5547", "Improving the Radiometric Search of Stochastic Gravitational Wave Background with a Natural Set of Basis Functions", "blue")

    ms_researcher_experience = [
        "Performed Data Analysis of Stochastic Gravitational Wave Background.",
        "Solved complex mathematical problems and learned to use Python in solving problems pertaining to statistics.",
        "Learned advanced linear algebra and algebraic geometry during the MS project.",
        f"Thesis: {thesis}",
    ]

    socials = [
        create_hyperlink("mailto:rktpranjal@gmail.com", "rktpranjal@gmail.com", "blue"),
        create_hyperlink("https://www.linkedin.com/in/pranjal4107/", "www.linkedin.com/in/pranjal4107", "blue"),
        create_hyperlink("https://github.com/pranjal-upadhyaya", "github.com/pranjal-upadhyaya", "blue"),
    ]

    technical_skills = [
        "Python",
        "SQL",
        "Docker",
        "AWS",
        "Git",
        "CI/CD",
        "Data Pipelines",
        "ETL",
        "API Development",
    ]
    
    # story.append(NextFrameFlowable(2))
    story.append(create_header("Experience", "header3_style"))
    story.append(Spacer(1, 12, isGlue=True))
    story.append(create_line(x=0, y=0, width=384))
    story.append(Spacer(1, 12, isGlue=True))
    story.append(create_header("Data Engineer (April 2024-Present)", "header4_style"))
    story.append(Spacer(1, 6, isGlue=True))
    story.append(create_body_italic("Astuto.ai"))
    story.append(Spacer(1, 6, isGlue=True))
    story.append(create_body_dim("Fulltime | 1 year 2 months"))
    story.append(Spacer(1, 6, isGlue=True))
    for experience in astuto_data_engineer_experience:
        story.append(create_bullet_point(experience))
        story.append(Spacer(1, 6, isGlue=True))
    # story.append(create_side_by_side_headers("2024-Present", "Data Engineer, Astuto.ai", "header5_style", "header4_style", 0.3))
    # story.append(Spacer(1, 12, isGlue=True))
    # story.append(create_side_by_side_headers("2022-2024", "Data Engineer, Oceanfrogs", "header5_style", "header4_style", 0.3))
    # story.append(create_side_by_side_headers("astuto.ai", "Data Engineer", "header5_style", "header4_style"))
    # story.append(FrameBreak())
    
    story.append(NextFrameFlowable(2))
    story.append(FrameBreak())
    story.append(create_header("Personal Information", "header4_style"))
    story.append(Spacer(1, 6, isGlue=True))
    story.append(create_line(x=0, y=0, width=180))
    story.append(Spacer(1, 6, isGlue=True))
    story.append(create_header("Current Address", "body_style_bold"))
    story.append(Spacer(1, 6, isGlue=True))
    story.append(create_body("Bangalore, Karnataka, India"))
    story.append(Spacer(1, 6, isGlue=True))
    story.append(create_header("Permanent Address", "body_style_bold"))
    story.append(Spacer(1, 6, isGlue=True))
    story.append(create_body("Renukoot, Uttar Pradesh, India"))
    story.append(Spacer(1, 6, isGlue=True))
    story.append(create_header("Phone", "body_style_bold"))
    story.append(Spacer(1, 6, isGlue=True))
    story.append(create_body("+91 9763953468"))
    story.append(Spacer(1, 6, isGlue=True))
    story.append(create_header("Socials", "body_style_bold"))
    story.append(Spacer(1, 6, isGlue=True))
    for social in socials:
        story.append(create_body(social))
        story.append(Spacer(1, 6, isGlue=True))
    story.append(create_header("Experience", "body_style_bold"))
    story.append(Spacer(1, 6, isGlue=True))
    story.append(create_body("2 year 11 months"))
    story.append(Spacer(1, 12, isGlue=True))
    story.append(create_header("Technical Skills", "header4_style"))
    story.append(Spacer(1, 6, isGlue=True))
    story.append(create_line(x=0, y=0, width=180))
    story.append(Spacer(1, 6, isGlue=True))
    for skill in technical_skills:
        story.append(create_body(skill))
        story.append(Spacer(1, 6, isGlue=True))

    # Next Page

    story.append(NextPageTemplate(1))
    story.append(PageBreak())
    story.append(create_header("Experience", "header3_style"))
    story.append(Spacer(1, 12, isGlue=True))
    story.append(create_header("Data Engineer (July 2022-March 2024)", "header4_style"))
    story.append(Spacer(1, 6, isGlue=True))
    story.append(create_body_italic("Oceanfrogs"))
    story.append(Spacer(1, 6, isGlue=True))
    story.append(create_body_dim("Fulltime | 1 year 9 months"))
    story.append(Spacer(1, 6, isGlue=True))
    for experience in oceanfrogs_data_engineer_experience:
        story.append(create_bullet_point(experience))
        story.append(Spacer(1, 6, isGlue=True))
    story.append(Spacer(1, 6, isGlue=True))

    story.append(create_header("MS Researcher (May 2019-March 2020)", "header4_style"))
    story.append(Spacer(1, 6, isGlue=True))
    story.append(create_body_italic("Inter University Center for Astronomy and Astrophysics, Pune"))
    story.append(Spacer(1, 6, isGlue=True))
    story.append(create_body_dim("Fulltime | 1 year"))
    story.append(Spacer(1, 6, isGlue=True))
    for experience in ms_researcher_experience:
        story.append(create_bullet_point(experience))
        story.append(Spacer(1, 6, isGlue=True))
    story.append(Spacer(1, 6, isGlue=True))

    # Education
    story.append(create_header("Education", "header3_style"))
    story.append(Spacer(1, 12, isGlue=True))
    story.append(create_line(x=0, y=0, width=384))
    story.append(Spacer(1, 12, isGlue=True))
    story.append(create_header("Bachelor & Master of Science (BS-MS): Physics", "header4_style"))
    story.append(Spacer(1, 6, isGlue=True))
    story.append(create_body("Indian Institute of Science Education and Research, Pune"))
    story.append(Spacer(1, 6, isGlue=True))
    story.append(create_body_dim("2015-2020"))
    story.append(Spacer(1, 6, isGlue=True))
    story.append(create_header("Higher Secondary", "header4_style"))
    story.append(Spacer(1, 6, isGlue=True))
    story.append(create_body("Bhavan's K.D.K.V.M, Renukoot"))
    story.append(Spacer(1, 6, isGlue=True))
    story.append(create_body_dim("2013-2015"))
    story.append(Spacer(1, 6, isGlue=True))

    doc.build(story)


if __name__ == "__main__":
    create_pdf()
    
    
    