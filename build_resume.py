import os
import sys
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT, TA_JUSTIFY
import pymupdf

def build_resume_pdf(output_path):
    # Single-page executive engineering resume
    doc = SimpleDocTemplate(
        output_path,
        pagesize=letter,
        leftMargin=30,
        rightMargin=30,
        topMargin=24,
        bottomMargin=24
    )

    PRIMARY = colors.HexColor("#0f2942")     # Deep navy
    SECONDARY = colors.HexColor("#1e40af")   # Strong royal blue
    TEXT_DARK = colors.HexColor("#1e293b")   # Slate 800
    TEXT_MUTED = colors.HexColor("#475569")  # Slate 600
    BORDER_COLOR = colors.HexColor("#94a3b8")# Slate 400
    LINK_COLOR = colors.HexColor("#2563eb")  # Vibrant blue

    styles = getSampleStyleSheet()

    name_style = ParagraphStyle(
        'Name',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=21,
        leading=23,
        textColor=PRIMARY,
        alignment=TA_CENTER
    )

    subtitle_style = ParagraphStyle(
        'Subtitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9.5,
        leading=11.5,
        textColor=SECONDARY,
        alignment=TA_CENTER,
        spaceBefore=2,
        spaceAfter=3
    )

    contact_style = ParagraphStyle(
        'Contact',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8,
        leading=10.5,
        textColor=TEXT_DARK,
        alignment=TA_CENTER
    )

    section_hdr_style = ParagraphStyle(
        'SecHeader',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9.5,
        leading=11.5,
        textColor=PRIMARY,
        spaceBefore=5,
        spaceAfter=1
    )

    body_style = ParagraphStyle(
        'Body',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8,
        leading=10.5,
        textColor=TEXT_DARK,
        alignment=TA_JUSTIFY
    )

    item_title_style = ParagraphStyle(
        'ItemTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8.5,
        leading=10.5,
        textColor=PRIMARY
    )

    item_meta_style = ParagraphStyle(
        'ItemMeta',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=7.8,
        leading=9.5,
        textColor=TEXT_MUTED
    )

    right_links_style = ParagraphStyle(
        'RightLinks',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8,
        leading=10,
        textColor=LINK_COLOR,
        alignment=TA_RIGHT
    )

    bullet_style = ParagraphStyle(
        'Bullet',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=7.8,
        leading=9.8,
        textColor=TEXT_DARK,
        leftIndent=11,
        firstLineIndent=-8,
        spaceAfter=1
    )

    skill_label_style = ParagraphStyle(
        'SkillLabel',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8,
        leading=10.2,
        textColor=PRIMARY
    )

    skill_val_style = ParagraphStyle(
        'SkillVal',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8,
        leading=10.2,
        textColor=TEXT_DARK
    )

    def section_block(title):
        return [
            Paragraph(title.upper(), section_hdr_style),
            HRFlowable(width="100%", thickness=0.8, color=BORDER_COLOR, spaceBefore=1, spaceAfter=3)
        ]

    story = []

    # 1. HEADER
    story.append(Paragraph("AMAN SHARMA", name_style))
    story.append(Paragraph("FULL-STACK DEVELOPER &bull; COMPUTER SCIENCE &amp; ENGINEERING", subtitle_style))
    
    contact_line = (
        "Lucknow / Greater Noida, UP &nbsp;|&nbsp; "
        "<a href='tel:+919690683156' color='#2563eb'><b>+91-9690683156</b></a> &nbsp;|&nbsp; "
        "<a href='https://wa.me/919690683156' color='#2563eb'><b>WhatsApp</b></a> &nbsp;|&nbsp; "
        "<a href='mailto:codewithaman88@gmail.com' color='#2563eb'><b>codewithaman88@gmail.com</b></a><br/>"
        "<a href='https://www.linkedin.com/in/aman-sharma-web/' color='#2563eb'><b>LinkedIn</b></a> &nbsp;|&nbsp; "
        "<a href='https://github.com/CodingWithAman1' color='#2563eb'><b>GitHub</b></a> &nbsp;|&nbsp; "
        "<a href='https://codingwithaman1.github.io/PORTFOLIO/' color='#2563eb'><b>Portfolio Website</b></a>"
    )
    story.append(Paragraph(contact_line, contact_style))
    story.append(Spacer(1, 2))
    story.append(HRFlowable(width="100%", thickness=1.2, color=PRIMARY, spaceBefore=2, spaceAfter=4))

    # 2. SUMMARY
    story.extend(section_block("Professional Summary"))
    summary = (
        "Forward-thinking Computer Science Engineering student and Full-Stack Developer with hands-on expertise "
        "engineering robust web architectures, relational database schemas, and AI-integrated applications. "
        "Proficient in Python (Flask 3.x), modern JavaScript, SQL (PostgreSQL, SQLite), and responsive frontend systems. "
        "Demonstrated track record delivering production platforms with cloud deployments (Vercel, Render), RESTful APIs, "
        "and Google Gemini multimodal AI vision pipelines. Passionate about writing scalable, clean code to solve real-world challenges."
    )
    story.append(Paragraph(summary, body_style))
    story.append(Spacer(1, 2))

    # 3. TECHNICAL SKILLS
    story.extend(section_block("Technical Skills"))
    skill_rows = [
        [
            Paragraph("Languages:", skill_label_style),
            Paragraph("Python, JavaScript (ES6+), SQL, C, HTML5, CSS3", skill_val_style)
        ],
        [
            Paragraph("Frameworks & Web:", skill_label_style),
            Paragraph("Flask 3.x, Jinja2, Bootstrap 5, Tailwind CSS, REST APIs, Chart.js, p5.js", skill_val_style)
        ],
        [
            Paragraph("Databases & ORM:", skill_label_style),
            Paragraph("PostgreSQL, SQLite, SQLAlchemy 2.0 (Relational modeling, migrations, transaction logging)", skill_val_style)
        ],
        [
            Paragraph("AI & Cloud DevOps:", skill_label_style),
            Paragraph("Google Gemini Multimodal Vision API, Vercel Serverless, Render, Git, GitHub, Linux / Bash", skill_val_style)
        ]
    ]
    st = Table(skill_rows, colWidths=[110, 442])
    st.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('TOPPADDING', (0,0), (-1,-1), 0.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 0.5),
        ('LEFTPADDING', (0,0), (-1,-1), 0),
        ('RIGHTPADDING', (0,0), (-1,-1), 0),
    ]))
    story.append(st)
    story.append(Spacer(1, 2))

    # 4. PROJECTS
    story.extend(section_block("Featured Projects"))

    def project_item(name, subtitle, tech, live_url, gh_url, bullets):
        links_parts = []
        if live_url:
            links_parts.append(f"<a href='{live_url}' color='#2563eb'>Live App</a>")
        if gh_url:
            links_parts.append(f"<a href='{gh_url}' color='#2563eb'>GitHub</a>")
        links_str = " | ".join(links_parts)

        tbl = Table([
            [
                Paragraph(f"<b>{name}</b> &mdash; {subtitle}", item_title_style),
                Paragraph(links_str, right_links_style)
            ]
        ], colWidths=[420, 132])
        tbl.setStyle(TableStyle([
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
            ('TOPPADDING', (0,0), (-1,-1), 0),
            ('BOTTOMPADDING', (0,0), (-1,-1), 0),
            ('LEFTPADDING', (0,0), (-1,-1), 0),
            ('RIGHTPADDING', (0,0), (-1,-1), 0),
        ]))
        story.append(tbl)
        story.append(Paragraph(f"<i>{tech}</i>", item_meta_style))
        story.append(Spacer(1, 1))
        for b in bullets:
            story.append(Paragraph(f"&bull; {b}", bullet_style))
        story.append(Spacer(1, 2))

    project_item(
        "CIVICCONNECT",
        "AI-Powered Civic Action & Grievance Platform",
        "Python, Flask, Google Gemini Multimodal Vision, SQLAlchemy, Leaflet GPS, Bootstrap 5",
        "https://civicconnectweb.onrender.com/",
        "https://github.com/CodingWithAman1/CivicConnect",
        [
            "Architected a comprehensive civic grievance resolution portal enabling multi-role workflows for Citizens, NGOs, and Municipal Authorities.",
            "Integrated Google Gemini Multimodal Vision AI to automatically analyze uploaded complaint imagery, categorize infrastructure defects, score severity, and auto-route tickets to transport/sanitation departments.",
            "Built GPS proximity clustering using Haversine algorithm (300m radius) to merge duplicate citizen complaints and prevent municipal backlog.",
            "Implemented real-time emergency broadcasts and visual resolution cross-verification comparing before-and-after repair photographs."
        ]
    )

    project_item(
        "INVENTRA",
        "Smart Cloud Inventory & Supply Chain Platform",
        "Python, Flask 3.x, PostgreSQL, SQLite, SQLAlchemy 2.0, Chart.js, Bootstrap 5, Vercel Serverless",
        "https://inventra-rho-lac.vercel.app/",
        "https://github.com/CodingWithAman1/Inventra",
        [
            "Designed and deployed a production inventory system featuring live stock monitoring, supplier directories, and automated reorder threshold alerts.",
            "Implemented relational schema with cascade protections and full audit trail logging for all inventory transactions (+/- adjustments).",
            "Built interactive Chart.js analytics dashboards visualizing warehouse valuation and dynamic CSV export pipelines for inventory/supplier data.",
            "Engineered zero-configuration serverless deployment on Vercel with path normalization middleware and fluid compute scalability."
        ]
    )

    project_item(
        "MYRAIL",
        "Real-Time Railway Utility & Travel Platform",
        "JavaScript (ES6+), RESTful Railway APIs, Asynchronous Fetch, HTML5, CSS3, Netlify",
        "https://myrailbase.netlify.app/",
        "https://github.com/CodingWithAman1/myRail",
        [
            "Engineered a responsive railway utility web app providing live train status tracking, station code search with autocomplete, and route schedules.",
            "Integrated third-party railway APIs with robust asynchronous error boundaries, dynamic caching, and mobile-optimized layouts."
        ]
    )

    project_item(
        "AMANZON",
        "Responsive E-Commerce Web Storefront",
        "HTML5, CSS3 (Flexbox & CSS Grid), JavaScript",
        None,
        "https://github.com/CodingWithAman1/AMANZON",
        [
            "Developed a responsive multi-page e-commerce storefront clone replicating Amazon's modern UI, navigation hierarchy, and product card layouts.",
            "Utilized CSS Flexbox and Grid architectures ensuring fluid responsiveness across desktop, tablet, and mobile breakpoints."
        ]
    )

    # 5. EXPERIENCE & CERTIFICATIONS
    story.extend(section_block("Experience & Certifications"))
    exp_table = Table([
        [
            Paragraph("<b>Web Development Intern</b> &mdash; <i>3 Skills India</i>", item_title_style),
            Paragraph("<b>2-Month Internship</b>", right_links_style)
        ]
    ], colWidths=[420, 132])
    exp_table.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 0),
        ('BOTTOMPADDING', (0,0), (-1,-1), 0),
        ('LEFTPADDING', (0,0), (-1,-1), 0),
        ('RIGHTPADDING', (0,0), (-1,-1), 0),
    ]))
    story.append(exp_table)
    story.append(Paragraph("&bull; Built responsive user interface components and modernized frontend styling using HTML5, CSS3, and JavaScript.", bullet_style))
    story.append(Paragraph("&bull; <b>Python Programming Certification</b> &mdash; 90-hour intensive skill curriculum under <i>Reliance Foundation &amp; N.S.D.C.</i>", bullet_style))
    story.append(Paragraph("&bull; <b>Upskilling Program for Python</b> (Upskill Campuses &amp; The IoT Academy) &nbsp;&bull;&nbsp; <b>Cisco CyberSecurity &amp; AI Learn-a-Thon</b>", bullet_style))
    story.append(Spacer(1, 2))

    # 6. EDUCATION
    story.extend(section_block("Education"))
    edu_rows = [
        [
            Paragraph("<b>B.Tech in Computer Science &amp; Engineering (CSE)</b> &mdash; <i>G.L. Bajaj Institute of Technology &amp; Management</i>, Greater Noida", body_style),
            Paragraph("<b>2025 &ndash; Ongoing</b>", right_links_style)
        ],
        [
            Paragraph("<b>Intermediate (Class XII)</b> &mdash; <i>Brightland School</i>, Lucknow, UP", body_style),
            Paragraph("<b>2024</b>", right_links_style)
        ],
        [
            Paragraph("<b>High School (Class X)</b> &mdash; <i>Brightland School</i>, Lucknow, UP", body_style),
            Paragraph("<b>2022</b>", right_links_style)
        ]
    ]
    et = Table(edu_rows, colWidths=[440, 112])
    et.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('TOPPADDING', (0,0), (-1,-1), 0.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 0.5),
        ('LEFTPADDING', (0,0), (-1,-1), 0),
        ('RIGHTPADDING', (0,0), (-1,-1), 0),
    ]))
    story.append(et)
    story.append(Spacer(1, 2))

    # 7. LANGUAGES
    story.extend(section_block("Languages"))
    story.append(Paragraph("<b>English</b> (Professional Working Proficiency) &nbsp;&bull;&nbsp; <b>Hindi</b> (Native / Bilingual)", body_style))

    doc.build(story)
    print(f"Generated PDF: {output_path}")

    # Inspect page count and preview
    doc_fitz = pymupdf.open(output_path)
    count = len(doc_fitz)
    print(f"Total pages: {count}")
    for i, page in enumerate(doc_fitz):
        pix = page.get_pixmap(dpi=150)
        img_path = output_path.replace(".pdf", f"_p{i+1}.png")
        pix.save(img_path)
        print(f"Preview image: {img_path}")
    doc_fitz.close()
    return count

if __name__ == '__main__':
    out = os.path.abspath(sys.argv[1]) if len(sys.argv) > 1 else 'resume_1page.pdf'
    build_resume_pdf(out)
