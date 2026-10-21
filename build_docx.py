import os
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import parse_xml, OxmlElement
from docx.oxml.ns import nsdecls, qn
from docx.opc.constants import RELATIONSHIP_TYPE

def add_hyperlink(paragraph, url, text, color="EF4444", underline=True, bold=False, font_size=Pt(7.5), font_name="Calibri"):
    """Adds a clickable hyperlink to a paragraph in python-docx."""
    part = paragraph.part
    r_id = part.relate_to(url, RELATIONSHIP_TYPE.HYPERLINK, is_external=True)

    hyperlink = parse_xml(
        f'<w:hyperlink xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main" '
        f'r:id="{r_id}" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"/>'
    )
    new_run = parse_xml(f'<w:r xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"/>')
    new_run_text = parse_xml(f'<w:t xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">{text}</w:t>')
    new_run.append(new_run_text)

    rPr = parse_xml(f'<w:rPr xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"/>')
    
    if font_name:
        f_elem = parse_xml(f'<w:rFonts xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main" w:ascii="{font_name}" w:hAnsi="{font_name}"/>')
        rPr.append(f_elem)

    if font_size:
        sz_val = int(font_size.pt * 2)
        sz_elem = parse_xml(f'<w:sz xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main" w:val="{sz_val}"/>')
        rPr.append(sz_elem)

    if color:
        c = parse_xml(f'<w:color xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main" w:val="{color}"/>')
        rPr.append(c)

    if underline:
        u = parse_xml('<w:u xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main" w:val="single"/>')
        rPr.append(u)

    if bold:
        b = parse_xml('<w:b xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"/>')
        rPr.append(b)

    new_run.append(rPr)
    hyperlink.append(new_run)
    paragraph._p.append(hyperlink)

def set_cell_margins(cell, top=0, bottom=0, left=0, right=0):
    """Sets inner margins for a table cell in dxa (1 pt = 20 dxa)."""
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = parse_xml(
        f'<w:tcMar xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">'
        f'<w:top w:w="{top}" w:type="dxa"/>'
        f'<w:bottom w:w="{bottom}" w:type="dxa"/>'
        f'<w:left w:w="{left}" w:type="dxa"/>'
        f'<w:right w:w="{right}" w:type="dxa"/>'
        f'</w:tcMar>'
    )
    tcPr.append(tcMar)

def clear_table_borders(table):
    """Clears all borders on a table."""
    tblPr = table._tbl.tblPr
    tblBorders = parse_xml(
        '<w:tblBorders xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">'
        '<w:top w:val="none" w:sz="0" w:space="0" w:color="auto"/>'
        '<w:left w:val="none" w:sz="0" w:space="0" w:color="auto"/>'
        '<w:bottom w:val="none" w:sz="0" w:space="0" w:color="auto"/>'
        '<w:right w:val="none" w:sz="0" w:space="0" w:color="auto"/>'
        '<w:insideH w:val="none" w:sz="0" w:space="0" w:color="auto"/>'
        '<w:insideV w:val="none" w:sz="0" w:space="0" w:color="auto"/>'
        '</w:tblBorders>'
    )
    tblPr.append(tblBorders)

def add_section_header(doc, title_text):
    """Adds a modern section header with a bottom rule line."""
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(8)
    p.paragraph_format.space_after = Pt(3)
    p.paragraph_format.keep_with_next = True
    
    # Bottom border XML on the paragraph
    pPr = p._p.get_or_add_pPr()
    pBdr = parse_xml(
        '<w:pBdr xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">'
        '<w:bottom w:val="single" w:sz="8" w:space="3" w:color="D4D4D4"/>'
        '</w:pBdr>'
    )
    pPr.append(pBdr)

    run = p.add_run(title_text)
    run.font.name = "Calibri"
    run.font.size = Pt(9.5)
    run.font.bold = True
    run.font.color.rgb = RGBColor(0x17, 0x17, 0x17)
    return p

def create_resume_docx(output_path):
    doc = docx.Document()

    # 1. Page Setup (Letter, 0.45 in margins)
    section = doc.sections[0]
    section.page_width = Inches(8.5)
    section.page_height = Inches(11.0)
    section.top_margin = Inches(0.42)
    section.bottom_margin = Inches(0.42)
    section.left_margin = Inches(0.45)
    section.right_margin = Inches(0.45)

    # Base style
    style_normal = doc.styles['Normal']
    style_normal.font.name = 'Calibri'
    style_normal.font.size = Pt(8.5)
    style_normal.font.color.rgb = RGBColor(0x33, 0x33, 0x33)

    content_width = 7.6 # inches

    # ==========================================
    # HEADER (2-Column Table)
    # ==========================================
    header_table = doc.add_table(rows=1, cols=2)
    header_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    clear_table_borders(header_table)
    header_table.autofit = False

    col_left, col_right = header_table.columns[0], header_table.columns[1]
    col_left.width = Inches(4.5)
    col_right.width = Inches(3.1)

    cell_left = header_table.cell(0, 0)
    cell_right = header_table.cell(0, 1)
    set_cell_margins(cell_left, top=0, bottom=60, left=0, right=40)
    set_cell_margins(cell_right, top=0, bottom=60, left=40, right=0)
    cell_left.vertical_alignment = WD_ALIGN_VERTICAL.TOP
    cell_right.vertical_alignment = WD_ALIGN_VERTICAL.TOP

    # Left Cell: Name, Title, Institution
    p_name = cell_left.paragraphs[0]
    p_name.paragraph_format.space_before = Pt(0)
    p_name.paragraph_format.space_after = Pt(1)
    r_name = p_name.add_run("AMAN SHARMA")
    r_name.font.name = "Calibri"
    r_name.font.size = Pt(20)
    r_name.font.bold = True
    r_name.font.color.rgb = RGBColor(0x17, 0x17, 0x17)

    p_sub = cell_left.add_paragraph()
    p_sub.paragraph_format.space_before = Pt(0)
    p_sub.paragraph_format.space_after = Pt(2)
    r_sub = p_sub.add_run("B.TECH CSE STUDENT • FULL-STACK SOFTWARE DEVELOPER")
    r_sub.font.name = "Calibri"
    r_sub.font.size = Pt(8.5)
    r_sub.font.bold = True
    r_sub.font.color.rgb = RGBColor(0xEF, 0x44, 0x44) # Signature Red

    p_col = cell_left.add_paragraph()
    p_col.paragraph_format.space_before = Pt(0)
    p_col.paragraph_format.space_after = Pt(0)
    r_col = p_col.add_run("GL Bajaj Institute of Technology and Management, Greater Noida")
    r_col.font.name = "Calibri"
    r_col.font.size = Pt(8)
    r_col.font.color.rgb = RGBColor(0x52, 0x52, 0x52)

    # Right Cell: Contact Info & Links
    p_right = cell_right.paragraphs[0]
    p_right.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    p_right.paragraph_format.space_before = Pt(0)
    p_right.paragraph_format.space_after = Pt(0)
    p_right.paragraph_format.line_spacing = Pt(9.5)

    def add_contact_line(p, label, text, url=None):
        r_lbl = p.add_run(label + ": ")
        r_lbl.font.name = "Calibri"
        r_lbl.font.size = Pt(7.2)
        r_lbl.font.bold = True
        r_lbl.font.color.rgb = RGBColor(0x73, 0x73, 0x73)

        if url:
            add_hyperlink(p, url, text, color="EF4444", underline=False, font_size=Pt(7.2))
        else:
            r_txt = p.add_run(text)
            r_txt.font.name = "Calibri"
            r_txt.font.size = Pt(7.2)
            r_txt.font.color.rgb = RGBColor(0x26, 0x26, 0x26)

    # Line 1: Phone & WhatsApp
    add_contact_line(p_right, "Phone", "+91-9690683156", "tel:+919690683156")
    p_right.add_run("  •  ")
    add_contact_line(p_right, "WhatsApp", "+91-9690683156", "https://wa.me/919690683156")

    # Line 2: Email & Portfolio
    p_r2 = cell_right.add_paragraph()
    p_r2.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    p_r2.paragraph_format.space_before = Pt(1)
    p_r2.paragraph_format.space_after = Pt(0)
    p_r2.paragraph_format.line_spacing = Pt(9.5)
    add_contact_line(p_r2, "Email", "codewithaman88@gmail.com", "mailto:codewithaman88@gmail.com")
    p_r2.add_run("  •  ")
    add_contact_line(p_r2, "Portfolio", "codingwithaman1.github.io", "https://codingwithaman1.github.io/PORTFOLIO/")

    # Line 3: GitHub & LinkedIn & LeetCode
    p_r3 = cell_right.add_paragraph()
    p_r3.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    p_r3.paragraph_format.space_before = Pt(1)
    p_r3.paragraph_format.space_after = Pt(0)
    p_r3.paragraph_format.line_spacing = Pt(9.5)
    add_contact_line(p_r3, "GitHub", "CodingWithAman1", "https://github.com/CodingWithAman1")
    p_r3.add_run("  •  ")
    add_contact_line(p_r3, "LinkedIn", "aman-sharma-web", "https://www.linkedin.com/in/aman-sharma-web/")
    p_r3.add_run("  •  ")
    add_contact_line(p_r3, "LeetCode", "CodingWithAman1", "https://leetcode.com/u/CodingWithAman1/")

    # Line 4: Location
    p_r4 = cell_right.add_paragraph()
    p_r4.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    p_r4.paragraph_format.space_before = Pt(1)
    p_r4.paragraph_format.space_after = Pt(0)
    p_r4.paragraph_format.line_spacing = Pt(9.5)
    add_contact_line(p_r4, "Location", "Greater Noida & Lucknow, UP, India")

    # Bottom border line under header
    p_hdr_rule = doc.add_paragraph()
    p_hdr_rule.paragraph_format.space_before = Pt(3)
    p_hdr_rule.paragraph_format.space_after = Pt(3)
    pPr = p_hdr_rule._p.get_or_add_pPr()
    pBdr = parse_xml(
        '<w:pBdr xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">'
        '<w:bottom w:val="single" w:sz="16" w:space="1" w:color="171717"/>'
        '</w:pBdr>'
    )
    pPr.append(pBdr)

    # ==========================================
    # 1. PROFESSIONAL OBJECTIVE
    # ==========================================
    add_section_header(doc, "PROFESSIONAL OBJECTIVE")
    p_obj = doc.add_paragraph()
    p_obj.paragraph_format.space_before = Pt(2)
    p_obj.paragraph_format.space_after = Pt(4)
    p_obj.paragraph_format.line_spacing = Pt(10.5)
    p_obj.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY

    def add_formatted_text(p, text_runs):
        for text, bold, italic in text_runs:
            r = p.add_run(text)
            r.font.name = "Calibri"
            r.font.size = Pt(8.0)
            r.font.bold = bold
            r.font.italic = italic
            r.font.color.rgb = RGBColor(0x33, 0x33, 0x33)

    obj_runs = [
        ("Proactive ", False, False),
        ("B.Tech Computer Science Engineering student", True, False),
        (" at GL Bajaj Institute of Technology and Management, Greater Noida, with hands-on expertise building production web platforms, transactional database architectures, and AI-integrated workflows. Proven track record deploying live, full-stack cloud applications (", False, False),
        ("CivicConnect", True, False),
        (", ", False, False),
        ("Inventra", True, False),
        (", ", False, False),
        ("MyRail", True, False),
        (") with automated triage, RESTful APIs, and responsive interfaces. Dedicated to engineering scalable, high-impact software solutions within innovative engineering teams.", False, False),
    ]
    add_formatted_text(p_obj, obj_runs)

    # ==========================================
    # 2. EDUCATION
    # ==========================================
    add_section_header(doc, "EDUCATION")

    def add_edu_row(title, inst, details, years):
        tbl = doc.add_table(rows=1, cols=2)
        tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
        clear_table_borders(tbl)
        tbl.autofit = False
        tbl.columns[0].width = Inches(6.2)
        tbl.columns[1].width = Inches(1.4)
        c_left, c_right = tbl.cell(0, 0), tbl.cell(0, 1)
        set_cell_margins(c_left, top=10, bottom=20, left=0, right=0)
        set_cell_margins(c_right, top=10, bottom=20, left=0, right=0)

        p_l = c_left.paragraphs[0]
        p_l.paragraph_format.space_before = Pt(0)
        p_l.paragraph_format.space_after = Pt(1)
        p_l.paragraph_format.line_spacing = Pt(9.5)
        r_t = p_l.add_run(title)
        r_t.font.name = "Calibri"
        r_t.font.size = Pt(8.2)
        r_t.font.bold = True
        r_t.font.color.rgb = RGBColor(0x17, 0x17, 0x17)

        p_sub = c_left.add_paragraph()
        p_sub.paragraph_format.space_before = Pt(0)
        p_sub.paragraph_format.space_after = Pt(1)
        p_sub.paragraph_format.line_spacing = Pt(9.0)
        r_i = p_sub.add_run(inst)
        r_i.font.name = "Calibri"
        r_i.font.size = Pt(7.6)
        r_i.font.color.rgb = RGBColor(0x52, 0x52, 0x52)

        if details:
            p_det = c_left.add_paragraph()
            p_det.paragraph_format.space_before = Pt(0)
            p_det.paragraph_format.space_after = Pt(1)
            p_det.paragraph_format.line_spacing = Pt(8.5)
            r_d = p_det.add_run(details)
            r_d.font.name = "Consolas"
            r_d.font.size = Pt(6.8)
            r_d.font.color.rgb = RGBColor(0x73, 0x73, 0x73)

        p_r = c_right.paragraphs[0]
        p_r.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        p_r.paragraph_format.space_before = Pt(0)
        p_r.paragraph_format.space_after = Pt(0)
        r_y = p_r.add_run(f"[{years}]")
        r_y.font.name = "Consolas"
        r_y.font.size = Pt(7.4)
        r_y.font.bold = True
        r_y.font.color.rgb = RGBColor(0x17, 0x17, 0x17)

    add_edu_row(
        "Bachelor of Technology (B.Tech) in Computer Science & Engineering",
        "GL Bajaj Institute of Technology and Management, Greater Noida",
        "Core Coursework: Operating Systems, DBMS, OOP, Data Structures & Algorithms, Computer Networks",
        "2025 – 2029"
    )
    add_edu_row(
        "Intermediate (Class XII) • Science (PCM)",
        "Brightland School, Lucknow (CBSE)",
        "",
        "2024"
    )
    add_edu_row(
        "High School (Class X)",
        "Brightland School, Lucknow (CBSE)",
        "",
        "2022"
    )

    # ==========================================
    # 3. TECHNICAL SKILLS
    # ==========================================
    add_section_header(doc, "TECHNICAL SKILLS")

    skills_data = [
        ("Programming Languages", "Python, JavaScript (ES6+), SQL, C, HTML5, CSS3"),
        ("Frameworks & Web", "Flask 3.x, Jinja2, RESTful APIs, Chart.js, Bootstrap 5, Tailwind CSS"),
        ("Databases & ORM", "PostgreSQL, SQLite, SQLAlchemy 2.0 (Relational Schemas)"),
        ("Cloud, AI & DevOps", "Gemini Vision AI, Vercel Serverless, Render, Git, GitHub, Postman"),
    ]

    for label, val in skills_data:
        p_sk = doc.add_paragraph()
        p_sk.paragraph_format.space_before = Pt(1)
        p_sk.paragraph_format.space_after = Pt(1)
        p_sk.paragraph_format.line_spacing = Pt(9.5)
        
        r_bullet = p_sk.add_run("•  ")
        r_bullet.font.name = "Calibri"
        r_bullet.font.size = Pt(8.5)
        r_bullet.font.bold = True
        r_bullet.font.color.rgb = RGBColor(0xEF, 0x44, 0x44)

        r_lbl = p_sk.add_run(label + ": ")
        r_lbl.font.name = "Calibri"
        r_lbl.font.size = Pt(7.8)
        r_lbl.font.bold = True
        r_lbl.font.color.rgb = RGBColor(0x17, 0x17, 0x17)

        r_v = p_sk.add_run(val)
        r_v.font.name = "Calibri"
        r_v.font.size = Pt(7.8)
        r_v.font.color.rgb = RGBColor(0x40, 0x40, 0x40)

    # ==========================================
    # 4. FEATURED PROJECTS
    # ==========================================
    add_section_header(doc, "FEATURED PROJECTS")

    def add_project(title, subtitle, live_url, gh_url, tech_stack, bullets):
        tbl = doc.add_table(rows=1, cols=2)
        tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
        clear_table_borders(tbl)
        tbl.autofit = False
        tbl.columns[0].width = Inches(5.4)
        tbl.columns[1].width = Inches(2.2)

        c_left, c_right = tbl.cell(0, 0), tbl.cell(0, 1)
        set_cell_margins(c_left, top=40, bottom=0, left=0, right=0)
        set_cell_margins(c_right, top=40, bottom=0, left=0, right=0)

        p_t = c_left.paragraphs[0]
        p_t.paragraph_format.space_before = Pt(0)
        p_t.paragraph_format.space_after = Pt(0)
        r_name = p_t.add_run(title.upper())
        r_name.font.name = "Calibri"
        r_name.font.size = Pt(8.4)
        r_name.font.bold = True
        r_name.font.color.rgb = RGBColor(0x17, 0x17, 0x17)

        if subtitle:
            r_s = p_t.add_run(" — " + subtitle)
            r_s.font.name = "Calibri"
            r_s.font.size = Pt(8.0)
            r_s.font.bold = False
            r_s.font.color.rgb = RGBColor(0x40, 0x40, 0x40)

        p_links = c_right.paragraphs[0]
        p_links.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        p_links.paragraph_format.space_before = Pt(0)
        p_links.paragraph_format.space_after = Pt(0)

        has_prev = False
        if live_url:
            add_hyperlink(p_links, live_url, "↗ Live Demo", color="EF4444", underline=True, bold=True, font_size=Pt(7.2))
            has_prev = True
        if gh_url:
            if has_prev:
                r_sep = p_links.add_run("  |  ")
                r_sep.font.size = Pt(7.0)
                r_sep.font.color.rgb = RGBColor(0x99, 0x99, 0x99)
            add_hyperlink(p_links, gh_url, "GitHub ↗", color="EF4444", underline=True, bold=True, font_size=Pt(7.2))

        # Tech stack
        p_tech = doc.add_paragraph()
        p_tech.paragraph_format.space_before = Pt(0)
        p_tech.paragraph_format.space_after = Pt(2)
        r_tc = p_tech.add_run(tech_stack)
        r_tc.font.name = "Consolas"
        r_tc.font.size = Pt(6.8)
        r_tc.font.color.rgb = RGBColor(0x52, 0x52, 0x52)

        # Bullets
        for lead, body in bullets:
            p_b = doc.add_paragraph()
            p_b.paragraph_format.left_indent = Inches(0.16)
            p_b.paragraph_format.space_before = Pt(0)
            p_b.paragraph_format.space_after = Pt(1)
            p_b.paragraph_format.line_spacing = Pt(9.2)

            r_dot = p_b.add_run("•  ")
            r_dot.font.name = "Calibri"
            r_dot.font.size = Pt(8.0)
            r_dot.font.bold = True
            r_dot.font.color.rgb = RGBColor(0xEF, 0x44, 0x44)

            r_lead = p_b.add_run(lead + " ")
            r_lead.font.name = "Calibri"
            r_lead.font.size = Pt(7.6)
            r_lead.font.bold = True
            r_lead.font.color.rgb = RGBColor(0x17, 0x17, 0x17)

            r_body = p_b.add_run(body)
            r_body.font.name = "Calibri"
            r_body.font.size = Pt(7.6)
            r_body.font.color.rgb = RGBColor(0x40, 0x40, 0x40)

    # CivicConnect
    add_project(
        "CivicConnect",
        "AI Civic Action & Grievance Platform",
        "https://civicconnectweb.onrender.com/",
        "https://github.com/CodingWithAman1/CivicConnect",
        "Flask 3.x • Google Gemini Vision AI • PostgreSQL • Leaflet GPS • Cloudinary • Bootstrap 5",
        [
            ("Architected full-lifecycle civic governance portal", "with role-based routing across Citizens, NGOs, and Municipal Authorities."),
            ("Integrated Google Gemini Multimodal Vision AI", "to analyze uploaded complaint photos, auto-detect infrastructure defects (potholes, garbage, water leaks), and compute severity index."),
            ("Engineered Haversine GPS proximity clustering (300m radius)", "to merge duplicate citizen reports, preventing municipal backlog."),
            ("Implemented photographic resolution audit engine", "comparing before/after repair photos before authorizing ticket completion."),
        ]
    )

    # Inventra
    add_project(
        "Inventra",
        "Smart Cloud Inventory & Stock Analytics",
        "https://inventra-rho-lac.vercel.app/",
        "https://github.com/CodingWithAman1/Inventra",
        "Flask • SQLAlchemy 2.0 • PostgreSQL • Chart.js • Vercel Serverless WSGI",
        [
            ("Engineered production warehouse inventory system", "with real-time stock monitoring, automated low-inventory reorder alerts, and supplier directories."),
            ("Built ACID-compliant relational audit trails", "recording immutable delta history for every inventory transaction (+/- adjustments)."),
            ("Designed interactive Chart.js dashboards", "delivering warehouse asset valuation, monthly movement graphs, and dynamic CSV exports."),
            ("Architected serverless WSGI microservice on Vercel", "with PostgreSQL cloud database connection pooling."),
        ]
    )

    # MyRail
    add_project(
        "MyRail",
        "Real-Time Indian Railway PNR & Live Train Tracking",
        "https://myrailbase.netlify.app/",
        "https://github.com/CodingWithAman1/myrail",
        "JavaScript (ES6+) • RapidAPI • Railway REST APIs • Asynchronous Fetch • Bootstrap 5",
        [
            ("Engineered responsive railway tracker web application", "providing real-time PNR status, live train status, and station autocomplete lookups."),
            ("Implemented asynchronous API caching and error boundary layer", "ensuring sub-second response times and high availability."),
        ]
    )

    # Amanzon
    add_project(
        "Amanzon",
        "Responsive Full-Featured E-Commerce Storefront",
        None,
        "https://github.com/CodingWithAman1/amanzon",
        "HTML5 • CSS3 (Modern Flexbox & Grid) • JavaScript (ES6+) • LocalStorage State Management",
        [
            ("Developed responsive multi-page e-commerce storefront", "featuring dynamic product catalog filtering, interactive cart state, and modal checkout."),
            ("Optimized cross-browser rendering pipeline", "ensuring 100% responsive fidelity across desktop, tablet, and mobile breakpoints."),
        ]
    )

    # ==========================================
    # 5. WORK EXPERIENCE
    # ==========================================
    add_section_header(doc, "WORK EXPERIENCE")

    tbl_exp = doc.add_table(rows=1, cols=2)
    tbl_exp.alignment = WD_TABLE_ALIGNMENT.CENTER
    clear_table_borders(tbl_exp)
    tbl_exp.autofit = False
    tbl_exp.columns[0].width = Inches(5.4)
    tbl_exp.columns[1].width = Inches(2.2)

    c_el, c_er = tbl_exp.cell(0, 0), tbl_exp.cell(0, 1)
    set_cell_margins(c_el, top=20, bottom=0, left=0, right=0)
    set_cell_margins(c_er, top=20, bottom=0, left=0, right=0)

    p_et = c_el.paragraphs[0]
    p_et.paragraph_format.space_before = Pt(0)
    p_et.paragraph_format.space_after = Pt(1)
    r_et = p_et.add_run("Web Development Intern — ")
    r_et.font.name = "Calibri"
    r_et.font.size = Pt(8.2)
    r_et.font.bold = True
    r_et.font.color.rgb = RGBColor(0x17, 0x17, 0x17)
    r_ec = p_et.add_run("3 Skills India")
    r_ec.font.name = "Calibri"
    r_ec.font.size = Pt(8.2)
    r_ec.font.bold = True
    r_ec.font.color.rgb = RGBColor(0xEF, 0x44, 0x44)

    p_ey = c_er.paragraphs[0]
    p_ey.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    p_ey.paragraph_format.space_before = Pt(0)
    p_ey.paragraph_format.space_after = Pt(1)
    r_ey = p_ey.add_run("[July 2024 – Aug 2024 • Remote]")
    r_ey.font.name = "Consolas"
    r_ey.font.size = Pt(7.2)
    r_ey.font.bold = True
    r_ey.font.color.rgb = RGBColor(0x17, 0x17, 0x17)

    exp_bullets = [
        "Modernized frontend web architectures with semantic HTML5, CSS3, and JavaScript, reducing mobile layout shifts.",
        "Collaborated with senior engineers on sprint velocity, code reviews, and cross-device accessibility optimizations.",
    ]
    for b in exp_bullets:
        p_eb = doc.add_paragraph()
        p_eb.paragraph_format.left_indent = Inches(0.16)
        p_eb.paragraph_format.space_before = Pt(0)
        p_eb.paragraph_format.space_after = Pt(1)
        p_eb.paragraph_format.line_spacing = Pt(9.0)

        r_dot = p_eb.add_run("•  ")
        r_dot.font.name = "Calibri"
        r_dot.font.size = Pt(8.0)
        r_dot.font.bold = True
        r_dot.font.color.rgb = RGBColor(0xEF, 0x44, 0x44)

        r_txt = p_eb.add_run(b)
        r_txt.font.name = "Calibri"
        r_txt.font.size = Pt(7.6)
        r_txt.font.color.rgb = RGBColor(0x40, 0x40, 0x40)

    # ==========================================
    # 6. CERTIFICATIONS & ACHIEVEMENTS
    # ==========================================
    add_section_header(doc, "CERTIFICATIONS & ACHIEVEMENTS")

    certs = [
        ("LeetCode Problem Solving", "208+ Problems Solved (116 Easy, 84 Med, 8 Hard) • 50 Days Badge 2026"),
        ("Python-Flask Web Dev", "Diploma in Website Development • Alison (94% Score • ID: 49008662)"),
        ("IBM Python for AI & Dev", "Python for Data Science, AI & Development • Coursera"),
        ("IBM Web Dev Fundamentals", "Web Development Concepts & Tooling • SkillsBuild"),
        ("Oracle Dev Gym SQL", "Dual Bronze Trophies for SQL & 42 Quizzes • Oracle Corporation"),
        ("Introduction to HTML5", "University of Michigan • Coursera Certified"),
        ("Python Programming", "Reliance Foundation & N.S.D.C. (90h intensive curriculum)"),
        ("Cisco CyberSecurity & AI", "AI & Security Learn-a-Thon Certified"),
    ]

    tbl_cert = doc.add_table(rows=4, cols=2)
    tbl_cert.alignment = WD_TABLE_ALIGNMENT.CENTER
    clear_table_borders(tbl_cert)
    tbl_cert.autofit = False
    tbl_cert.columns[0].width = Inches(3.8)
    tbl_cert.columns[1].width = Inches(3.8)

    for idx, (title, desc) in enumerate(certs):
        row_i = idx // 2
        col_i = idx % 2
        cell = tbl_cert.cell(row_i, col_i)
        set_cell_margins(cell, top=10, bottom=15, left=0, right=20)

        p = cell.paragraphs[0]
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(0)
        p.paragraph_format.line_spacing = Pt(9.0)

        r_dot = p.add_run("• ")
        r_dot.font.name = "Calibri"
        r_dot.font.size = Pt(7.5)
        r_dot.font.bold = True
        r_dot.font.color.rgb = RGBColor(0xEF, 0x44, 0x44)

        r_t = p.add_run(title + " — ")
        r_t.font.name = "Calibri"
        r_t.font.size = Pt(7.3)
        r_t.font.bold = True
        r_t.font.color.rgb = RGBColor(0x17, 0x17, 0x17)

        r_d = p.add_run(desc)
        r_d.font.name = "Consolas"
        r_d.font.size = Pt(6.5)
        r_d.font.color.rgb = RGBColor(0x66, 0x66, 0x66)

    # ==========================================
    # FOOTER STAMP
    # ==========================================
    p_ftr_rule = doc.add_paragraph()
    p_ftr_rule.paragraph_format.space_before = Pt(6)
    p_ftr_rule.paragraph_format.space_after = Pt(2)
    pPr = p_ftr_rule._p.get_or_add_pPr()
    pBdr = parse_xml(
        '<w:pBdr xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">'
        '<w:bottom w:val="single" w:sz="6" w:space="1" w:color="E5E5E5"/>'
        '</w:pBdr>'
    )
    pPr.append(pBdr)

    tbl_ftr = doc.add_table(rows=1, cols=2)
    tbl_ftr.alignment = WD_TABLE_ALIGNMENT.CENTER
    clear_table_borders(tbl_ftr)
    tbl_ftr.autofit = False
    tbl_ftr.columns[0].width = Inches(4.5)
    tbl_ftr.columns[1].width = Inches(3.1)

    c_fl, c_fr = tbl_ftr.cell(0, 0), tbl_ftr.cell(0, 1)
    set_cell_margins(c_fl, top=0, bottom=0, left=0, right=0)
    set_cell_margins(c_fr, top=0, bottom=0, left=0, right=0)

    p_fl = c_fl.paragraphs[0]
    p_fl.paragraph_format.space_before = Pt(0)
    p_fl.paragraph_format.space_after = Pt(0)
    r_fl = p_fl.add_run("Portfolio: codingwithaman1.github.io/PORTFOLIO  •  GitHub: github.com/CodingWithAman1")
    r_fl.font.name = "Consolas"
    r_fl.font.size = Pt(6.0)
    r_fl.font.color.rgb = RGBColor(0x73, 0x73, 0x73)

    p_fr = c_fr.paragraphs[0]
    p_fr.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    p_fr.paragraph_format.space_before = Pt(0)
    p_fr.paragraph_format.space_after = Pt(0)
    r_fr = p_fr.add_run("Contact: +91-9690683156  •  codewithaman88@gmail.com")
    r_fr.font.name = "Consolas"
    r_fr.font.size = Pt(6.0)
    r_fr.font.color.rgb = RGBColor(0x73, 0x73, 0x73)

    # Save DOCX
    doc.save(output_path)
    print(f"DOCX resume successfully created at: {output_path}")

if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.abspath(__file__))
    assets_dir = os.path.join(script_dir, "assets")
    os.makedirs(assets_dir, exist_ok=True)
    out_file = os.path.join(assets_dir, "Aman-Sharma-Resume.docx")
    create_resume_docx(out_file)
