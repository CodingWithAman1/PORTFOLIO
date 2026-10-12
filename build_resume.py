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

def build_modern_resume(pdf_path, preview_png_path=None):
    # Total letter size: 612 x 792 pt
    # Margins: 16 pt left/right, 14 pt top/bottom => printable width = 580 pt, height = 764 pt
    doc = SimpleDocTemplate(
        pdf_path,
        pagesize=letter,
        leftMargin=16,
        rightMargin=16,
        topMargin=14,
        bottomMargin=14
    )

    # Modern Designer Color Palette
    C_HEADER_BG = colors.HexColor("#091428")    # Deep obsidian navy
    C_HEADER_CARD = colors.HexColor("#112240")  # Rich navy card
    C_ACCENT_BLUE = colors.HexColor("#2563eb")  # Royal blue
    C_ACCENT_CYAN = colors.HexColor("#0ea5e9")  # Bright cyan
    C_SIDEBAR_BG = colors.HexColor("#f8fafc")   # Crisp slate background
    C_BORDER_LIGHT = colors.HexColor("#e2e8f0") # Subtle divider border
    C_TEXT_MAIN = colors.HexColor("#0f172a")    # Deep slate
    C_TEXT_MUTED = colors.HexColor("#475569")   # Medium slate

    styles = getSampleStyleSheet()

    # --- Typography Styles ---
    h_badge = ParagraphStyle(
        'HBadge',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=15,
        leading=16,
        textColor=colors.white,
        alignment=TA_CENTER
    )

    h_name = ParagraphStyle(
        'HName',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=20,
        leading=21,
        textColor=colors.white
    )

    h_title = ParagraphStyle(
        'HTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8.5,
        leading=10,
        textColor=colors.HexColor("#38bdf8")
    )

    h_tagline = ParagraphStyle(
        'HTagline',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=7.2,
        leading=8.8,
        textColor=colors.HexColor("#94a3b8")
    )

    h_contact = ParagraphStyle(
        'HContact',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=7.2,
        leading=9.8,
        textColor=colors.HexColor("#cbd5e1"),
        alignment=TA_RIGHT
    )

    sb_sec_title = ParagraphStyle(
        'SBSecTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8.2,
        leading=9.5,
        textColor=C_HEADER_BG,
        spaceBefore=4,
        spaceAfter=2
    )

    sb_label = ParagraphStyle(
        'SBLabel',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=7.2,
        leading=8.6,
        textColor=C_ACCENT_BLUE
    )

    sb_body = ParagraphStyle(
        'SBBody',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=6.9,
        leading=8.5,
        textColor=C_TEXT_MAIN
    )

    sb_meta = ParagraphStyle(
        'SBMeta',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=6.5,
        leading=8.0,
        textColor=C_TEXT_MUTED
    )

    main_sec_title = ParagraphStyle(
        'MainSecTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8.8,
        leading=10.5,
        textColor=C_HEADER_BG,
        spaceBefore=4,
        spaceAfter=2
    )

    summary_text = ParagraphStyle(
        'SummaryText',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=7.3,
        leading=9.5,
        textColor=C_TEXT_MAIN,
        alignment=TA_JUSTIFY
    )

    proj_title = ParagraphStyle(
        'ProjTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8.2,
        leading=9.6,
        textColor=C_HEADER_BG
    )

    proj_tags = ParagraphStyle(
        'ProjTags',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=6.5,
        leading=7.8,
        textColor=C_ACCENT_BLUE
    )

    proj_links = ParagraphStyle(
        'ProjLinks',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=6.8,
        leading=8.4,
        textColor=C_ACCENT_CYAN,
        alignment=TA_RIGHT
    )

    bullet_style = ParagraphStyle(
        'BulletStyle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=6.8,
        leading=8.3,
        textColor=C_TEXT_MAIN,
        leftIndent=7,
        firstLineIndent=-7,
        alignment=TA_JUSTIFY
    )

    story = []

    # =========================================================================
    # 1. TOP HEADER BANNER (Obsidian Navy with Monogram Badge & Rich Contacts)
    # =========================================================================
    badge_table = Table([[Paragraph("AS", h_badge)]], colWidths=[36], rowHeights=[36])
    badge_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), C_HEADER_CARD),
        ('BOX', (0, 0), (-1, -1), 1.5, colors.HexColor("#38bdf8")),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 0),
        ('TOPPADDING', (0, 0), (-1, -1), 0),
        ('LEFTPADDING', (0, 0), (-1, -1), 0),
        ('RIGHTPADDING', (0, 0), (-1, -1), 0),
    ]))

    name_details = [
        Paragraph("AMAN SHARMA", h_name),
        Spacer(1, 1),
        Paragraph("FULL-STACK SOFTWARE ENGINEER &bull; AI &amp; CLOUD SYSTEMS", h_title),
        Spacer(1, 1),
        Paragraph("B.Tech CSE &bull; Specialized in Python (Flask), Neon PostgreSQL, RESTful APIs &amp; Gemini AI", h_tagline)
    ]

    hdr_left_combo = Table([[badge_table, name_details]], colWidths=[42, 274])
    hdr_left_combo.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('LEFTPADDING', (0, 0), (-1, -1), 0),
        ('RIGHTPADDING', (0, 0), (-1, -1), 0),
        ('TOPPADDING', (0, 0), (-1, -1), 0),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 0),
    ]))

    contact_html = (
        '<b>Phone:</b> <a href="tel:+919690683156" color="#38bdf8">+91-9690683156</a> &nbsp;|&nbsp; '
        '<b>WhatsApp:</b> <a href="https://wa.me/919690683156" color="#34d399"><b>+91-9690683156</b></a><br/>'
        '<b>Email:</b> <a href="mailto:codewithaman88@gmail.com" color="#38bdf8">codewithaman88@gmail.com</a> &nbsp;|&nbsp; '
        '<b>Location:</b> Mathura &amp; Lucknow, UP<br/>'
        '<b>Portfolio:</b> <a href="https://codingwithaman1.github.io/PORTFOLIO/" color="#38bdf8"><b>codingwithaman1.github.io/PORTFOLIO</b></a><br/>'
        '<b>GitHub:</b> <a href="https://github.com/CodingWithAman1" color="#38bdf8">github.com/CodingWithAman1</a> &nbsp;|&nbsp; '
        '<b>LinkedIn:</b> <a href="https://linkedin.com/in/aman-sharma" color="#38bdf8">linkedin.com/in/aman-sharma</a>'
    )
    hdr_right = [Paragraph(contact_html, h_contact)]

    header_table = Table([[hdr_left_combo, hdr_right]], colWidths=[320, 260])
    header_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), C_HEADER_BG),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('LEFTPADDING', (0, 0), (0, 0), 10),
        ('RIGHTPADDING', (-1, -1), (-1, -1), 10),
    ]))
    story.append(header_table)
    story.append(Spacer(1, 4))

    # =========================================================================
    # 2. BODY: TWO-COLUMN ARCHITECTURE
    # =========================================================================

    # ----------------- LEFT SIDEBAR -----------------
    sb = []

    def make_sb_header(title):
        return [
            Paragraph(f"<font color='#2563eb'>■</font> {title.upper()}", sb_sec_title),
            HRFlowable(width="100%", thickness=1, color=C_BORDER_LIGHT, spaceBefore=1, spaceAfter=3)
        ]

    # --- Technical Skills ---
    sb.extend(make_sb_header("Technical Skills"))

    skills = [
        ("Languages", "Python, JavaScript (ES6+), SQL, C, HTML5, CSS3"),
        ("Frameworks & Web", "Flask 3.x, Jinja2, REST APIs, Chart.js, Bootstrap 5, Tailwind"),
        ("Databases & ORM", "PostgreSQL, Neon DB, SQLite, SQLAlchemy 2.0 (Relational schema, Migrations)"),
        ("AI & Tools", "Google Gemini AI Vision, Git, GitHub, Linux, Bash, Postman"),
        ("Cloud & Hosting", "Vercel Serverless, Render, Cloudinary CDN, Neon Cloud DB")
    ]
    for cat, val in skills:
        sb.append(Paragraph(cat, sb_label))
        sb.append(Paragraph(val, sb_body))
        sb.append(Spacer(1, 2))

    # --- Core Competencies ---
    sb.extend(make_sb_header("Core Competencies"))
    competencies = [
        "Full-Stack Web Development",
        "Multimodal AI Vision Integration",
        "Relational Schema Design & ACID",
        "Serverless & Cloud Microservices",
        "Rapid Prototyping & Clean Code"
    ]
    for comp in competencies:
        sb.append(Paragraph(f"<font color='#2563eb'>&check;</font> {comp}", sb_body))
    sb.append(Spacer(1, 2))

    # --- Education ---
    sb.extend(make_sb_header("Education"))

    sb.append(Paragraph("B.Tech in Computer Science &amp; Engg.", sb_label))
    sb.append(Paragraph("G.L. Bajaj Group of Institutions, Mathura", sb_body))
    sb.append(Paragraph("AKTU &bull; 2022 &ndash; 2026 &bull; <b>CGPA: 7.8 / 10</b>", sb_meta))
    sb.append(Paragraph("<font color='#64748b'>Coursework: OS, DBMS, OOP, DSA, Networks</font>", sb_meta))
    sb.append(Spacer(1, 2.5))

    sb.append(Paragraph("Intermediate (Class XII) &bull; PCM", sb_label))
    sb.append(Paragraph("Brightland School, Lucknow (CBSE)", sb_body))
    sb.append(Paragraph("Scored: <b>78%</b> &bull; 2024", sb_meta))
    sb.append(Spacer(1, 2.5))

    sb.append(Paragraph("High School (Class X)", sb_label))
    sb.append(Paragraph("Brightland School, Lucknow (CBSE)", sb_body))
    sb.append(Paragraph("Scored: <b>82%</b> &bull; 2022", sb_meta))
    sb.append(Spacer(1, 2.5))

    # --- Certifications ---
    sb.extend(make_sb_header("Certifications"))
    certs = [
        ("Python Programming", "Reliance Foundation &amp; N.S.D.C. (90h)"),
        ("Cisco CyberSecurity &amp; AI", "AI &amp; Security Learn-a-Thon"),
        ("Upskilling Program for Python", "Upskill Campuses &amp; IoT Academy"),
        ("Problem Solving", "HackerRank Verified Certificate")
    ]
    for c_title, c_iss in certs:
        sb.append(Paragraph(f"&bull; <b>{c_title}</b>", sb_body))
        sb.append(Paragraph(f"&nbsp; {c_iss}", sb_meta))
        sb.append(Spacer(1, 1.5))

    # --- Languages ---
    sb.extend(make_sb_header("Languages"))
    sb.append(Paragraph("&bull; <b>English</b> &ndash; Professional Working", sb_body))
    sb.append(Paragraph("&bull; <b>Hindi</b> &ndash; Native / Bilingual", sb_body))
    sb.append(Spacer(1, 2))

    # --- Direct Project Links ---
    sb.extend(make_sb_header("Verified Links"))
    links_data = [
        ("Portfolio Website", "https://codingwithaman1.github.io/PORTFOLIO/", "#2563eb"),
        ("CivicConnect Live App", "https://civicconnectweb.onrender.com/", "#0d9488"),
        ("Inventra Live App", "https://inventra-rho-lac.vercel.app/", "#0ea5e9"),
        ("WhatsApp Direct Chat", "https://wa.me/919690683156", "#10b981"),
    ]
    for label, url, color_code in links_data:
        sb.append(Paragraph(f'<font color="{color_code}">&bull;</font> <a href="{url}" color="{color_code}"><b>{label} &rarr;</b></a>', sb_body))
        sb.append(Spacer(1, 1.5))


    # ----------------- MAIN COLUMN CONTENT -----------------
    main = []

    def make_main_header(title):
        return [
            Paragraph(f"<font color='#2563eb'>■</font> {title.upper()}", main_sec_title),
            HRFlowable(width="100%", thickness=1.2, color=C_ACCENT_BLUE, spaceBefore=1, spaceAfter=4)
        ]

    # --- Executive Summary ---
    main.extend(make_main_header("Executive Summary"))
    summary_html = (
        "Forward-thinking <b>Computer Science Engineer &amp; Full-Stack Developer</b> with demonstrated expertise "
        "engineering resilient web architectures, transactional database systems, and AI-assisted workflows. "
        "Proven track record deploying full-stack platforms to production (Render, Vercel) featuring multi-role authentication, "
        "multimodal vision intelligence (Google Gemini AI), and real-time analytics. Passionate about architecting scalable, "
        "high-performance, user-centric software."
    )
    summary_table = Table([[Paragraph(summary_html, summary_text)]], colWidths=[382])
    summary_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#f8fafc")),
        ('BOX', (0, 0), (-1, -1), 0.5, C_BORDER_LIGHT),
        ('LINEBEFORE', (0, 0), (0, -1), 2.5, C_ACCENT_BLUE),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (-1, -1), (-1, -1), 6),
    ]))
    main.append(summary_table)
    main.append(Spacer(1, 3))

    # --- Featured Projects ---
    main.extend(make_main_header("Featured Projects"))

    projects = [
        {
            "name": "CIVICCONNECT &mdash; AI Civic Action &amp; Grievance Platform",
            "tags": "Flask 3.x &bull; Google Gemini Vision AI &bull; PostgreSQL &bull; Leaflet GPS &bull; Cloudinary",
            "links": '<a href="https://civicconnectweb.onrender.com/" color="#2563eb"><b>[Live App]</b></a> &nbsp; <a href="https://github.com/CodingWithAman1/CivicConnect" color="#0f172a"><b>[GitHub]</b></a>',
            "bullets": [
                "<b>Architected full-lifecycle civic platform</b> with role-based routing across Citizens, NGOs, and Municipal Admins.",
                "<b>Automated triage pipeline using Gemini AI Vision</b> to scan uploaded photos, categorize municipal defects (potholes, garbage, leaks), and score priority.",
                "<b>Built Haversine GPS clustering (300m radius)</b> to merge duplicate citizen complaints and prevent municipal dispatch backlogs.",
                "<b>Implemented visual resolution audit verification</b> comparing before/after repair photos before marking tickets resolved."
            ]
        },
        {
            "name": "INVENTRA &mdash; Smart Cloud Inventory &amp; Stock Analytics",
            "tags": "Flask &bull; SQLAlchemy 2.0 &bull; Neon PostgreSQL &bull; Chart.js &bull; Vercel Serverless",
            "links": '<a href="https://inventra-rho-lac.vercel.app/" color="#2563eb"><b>[Live App]</b></a> &nbsp; <a href="https://github.com/CodingWithAman1/Inventra" color="#0f172a"><b>[GitHub]</b></a>',
            "bullets": [
                "<b>Engineered production warehouse inventory system</b> with real-time stock monitoring, supplier directories, and automated low-stock reorder alerts.",
                "<b>Implemented strict relational audit trails</b> recording all stock delta adjustments with database transaction guarantees.",
                "<b>Designed interactive Chart.js dashboards</b> delivering warehouse asset valuation, monthly movement graphs, and CSV data exports.",
                "<b>Optimized serverless WSGI deployment on Vercel</b> utilizing Neon cloud PostgreSQL with connection pooling."
            ]
        },
        {
            "name": "MYRAIL &mdash; Real-Time Indian Railway PNR &amp; Live Tracking",
            "tags": "JavaScript (ES6+) &bull; RapidAPI &bull; Railway REST APIs &bull; Asynchronous Fetch &bull; Bootstrap 5",
            "links": '<a href="https://github.com/CodingWithAman1/myrail" color="#0f172a"><b>[GitHub]</b></a>',
            "bullets": [
                "<b>Engineered responsive railway tracker</b> providing instant PNR status, live train running status, and station autocomplete lookups.",
                "<b>Built asynchronous client-side API caching layer</b> with robust error handling for API quotas and network timeouts."
            ]
        },
        {
            "name": "AMANZON &mdash; Responsive Full-Featured E-Commerce Storefront",
            "tags": "HTML5 &bull; CSS3 (Modern Flexbox &amp; Grid) &bull; JavaScript &bull; LocalStorage State",
            "links": '<a href="https://github.com/CodingWithAman1/amanzon" color="#0f172a"><b>[GitHub]</b></a>',
            "bullets": [
                "<b>Developed multi-page e-commerce storefront</b> featuring responsive product catalogues, dynamic cart state management, and modal checkout.",
                "<b>Ensured pixel-perfect cross-browser design</b> optimized across desktop, tablet, and mobile viewport breakpoints."
            ]
        }
    ]

    for p in projects:
        p_hdr_left = [
            Paragraph(p["name"], proj_title),
            Paragraph(f"<font color='#2563eb'>Tech:</font> {p['tags']}", proj_tags)
        ]
        p_hdr_right = [
            Paragraph(p["links"], proj_links)
        ]
        p_table = Table([[p_hdr_left, p_hdr_right]], colWidths=[296, 86])
        p_table.setStyle(TableStyle([
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('LEFTPADDING', (0, 0), (-1, -1), 0),
            ('RIGHTPADDING', (0, 0), (-1, -1), 0),
            ('TOPPADDING', (0, 0), (-1, -1), 0),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 1),
        ]))
        main.append(p_table)

        for b in p["bullets"]:
            main.append(Paragraph(f"&bull; {b}", bullet_style))
        main.append(Spacer(1, 2.5))

    # --- Experience ---
    main.extend(make_main_header("Work Experience"))

    exp_hdr_left = [
        Paragraph("<b>Web Development Intern</b> &mdash; <i>3 Skills India</i>", proj_title),
        Paragraph("<font color='#64748b'>Front-End Engineering &amp; Responsive Web Architecture</font>", proj_tags)
    ]
    exp_hdr_right = [
        Paragraph("<font color='#2563eb'><b>July 2024 &ndash; Aug 2024</b></font><br/><font color='#64748b'>Remote Internship</font>", proj_links)
    ]
    exp_table = Table([[exp_hdr_left, exp_hdr_right]], colWidths=[286, 96])
    exp_table.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('LEFTPADDING', (0, 0), (-1, -1), 0),
        ('RIGHTPADDING', (0, 0), (-1, -1), 0),
        ('TOPPADDING', (0, 0), (-1, -1), 0),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 1),
    ]))
    main.append(exp_table)
    main.append(Paragraph("&bull; Developed and modernized responsive web modules with clean semantic HTML5, CSS3, and JavaScript.", bullet_style))
    main.append(Paragraph("&bull; Optimized cross-device styling, reducing layout shifts and improving frontend performance across mobile viewports.", bullet_style))
    main.append(Paragraph("&bull; Participated in sprint reviews and UI/UX design refactoring under senior engineering mentorship.", bullet_style))
    main.append(Spacer(1, 2))

    # --- Key Achievements ---
    main.extend(make_main_header("Key Achievements &amp; Highlights"))
    main.append(Paragraph("&bull; <b>Production Cloud Deployments:</b> Architected, deployed, and maintain 4 live full-stack web platforms on Vercel and Render.", bullet_style))
    main.append(Paragraph("&bull; <b>Algorithmic Problem Solving:</b> Solved 150+ DSA and algorithmic problems across LeetCode &amp; HackerRank (Python &amp; C++).", bullet_style))
    main.append(Paragraph("&bull; <b>Smart India Hackathon (SIH) Internal:</b> Conceptualized and developed AI-assisted civic grievance routing prototype.", bullet_style))

    # =========================================================================
    # 3. COMBINE SIDEBAR AND MAIN BODY INTO A TWO-COLUMN CONTAINER TABLE
    # =========================================================================
    body_table = Table([[sb, main]], colWidths=[184, 396])
    body_table.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('BACKGROUND', (0, 0), (0, 0), C_SIDEBAR_BG),
        ('BOX', (0, 0), (0, 0), 0.5, C_BORDER_LIGHT),
        ('LEFTPADDING', (0, 0), (0, 0), 8),
        ('RIGHTPADDING', (0, 0), (0, 0), 8),
        ('TOPPADDING', (0, 0), (0, 0), 5),
        ('BOTTOMPADDING', (0, 0), (0, 0), 5),
        ('LEFTPADDING', (1, 0), (1, 0), 10),
        ('RIGHTPADDING', (1, 0), (1, 0), 2),
        ('TOPPADDING', (1, 0), (1, 0), 0),
        ('BOTTOMPADDING', (1, 0), (1, 0), 0),
    ]))
    story.append(body_table)

    doc.build(story)
    print(f"Built PDF at {pdf_path}")

    if preview_png_path:
        pdf_doc = pymupdf.open(pdf_path)
        print(f"Total pages generated: {len(pdf_doc)}")
        page = pdf_doc[0]
        pix = page.get_pixmap(dpi=150)
        pix.save(preview_png_path)
        print(f"Saved preview image to {preview_png_path}")
        return len(pdf_doc)

if __name__ == '__main__':
    out_pdf = "c:/Users/lenovo/Documents/antigravity/PORTFOLIO/assets/Aman-Sharma-Resume.pdf"
    preview_img = "c:/Users/lenovo/Documents/antigravity/PORTFOLIO/assets/preview.png"
    pages = build_modern_resume(out_pdf, preview_img)
    print("Execution complete. Pages:", pages)
