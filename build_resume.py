import os
import subprocess
import pymupdf

def build_resume(output_pdf_path, preview_png_path=None):
    html_content = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Aman Sharma - Resume</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;600;700&family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">
<style>
  @page {
    size: letter portrait;
    margin: 0;
  }
  * {
    box-sizing: border-box;
    margin: 0;
    padding: 0;
  }
  html, body {
    width: 8.5in;
    height: 11in;
    background-color: #ffffff;
    color: #171717;
    font-family: 'Plus Jakarta Sans', -apple-system, sans-serif;
    -webkit-print-color-adjust: exact;
    print-color-adjust: exact;
    overflow: hidden;
    font-size: 8.2pt;
    line-height: 1.32;
  }

  .page-container {
    padding: 0.38in 0.44in;
    height: 11in;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
  }

  /* Header - Rajat Sahu Signature Style */
  .resume-header {
    border-bottom: 2.5px solid #171717;
    padding-bottom: 11px;
    margin-bottom: 10px;
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
  }

  .header-left h1 {
    font-size: 22pt;
    font-weight: 800;
    text-transform: uppercase;
    letter-spacing: -0.5px;
    color: #171717;
    line-height: 1.05;
  }

  .header-left .subtitle {
    font-size: 8.5pt;
    font-weight: 700;
    color: #ef4444; /* Signature Rajat Red */
    text-transform: uppercase;
    letter-spacing: 0.8px;
    margin-top: 3px;
  }

  .header-left .college-tag {
    font-size: 7.2pt;
    color: #525252;
    margin-top: 2px;
    font-weight: 500;
  }

  .header-right {
    text-align: right;
    font-family: 'JetBrains Mono', monospace;
    font-size: 7pt;
    color: #525252;
    display: flex;
    flex-direction: column;
    gap: 2.5px;
  }

  .header-right a {
    color: #525252;
    text-decoration: none;
    transition: color 0.2s;
  }
  .header-right a:hover {
    color: #ef4444;
    text-decoration: underline;
  }

  .icon-red {
    color: #ef4444;
    margin-right: 4px;
    font-size: 7.5pt;
    width: 11px;
    display: inline-block;
    text-align: center;
  }

  /* Section Title - Rajat Monospace Style */
  .section-title {
    font-size: 8.2pt;
    font-weight: 700;
    font-family: 'JetBrains Mono', monospace;
    text-transform: uppercase;
    letter-spacing: 0.8px;
    color: #171717;
    border-bottom: 1.2px solid #d4d4d4;
    padding-bottom: 2.5px;
    margin-bottom: 6px;
    margin-top: 7px;
    display: flex;
    align-items: center;
    justify-content: space-between;
  }
  .section-title:first-of-type {
    margin-top: 0;
  }

  /* Content Text */
  .objective-text {
    font-size: 7.6pt;
    line-height: 1.38;
    color: #404040;
    text-align: justify;
  }
  .objective-text b {
    color: #171717;
  }

  /* Education Items */
  .edu-item {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    margin-bottom: 5px;
  }
  .edu-item:last-child {
    margin-bottom: 0;
  }
  .edu-title {
    font-size: 8pt;
    font-weight: 700;
    color: #171717;
  }
  .edu-sub {
    font-size: 7.2pt;
    color: #525252;
    font-weight: 500;
  }
  .edu-details {
    font-size: 6.8pt;
    color: #737373;
    font-family: 'JetBrains Mono', monospace;
  }
  .badge-pill {
    font-family: 'JetBrains Mono', monospace;
    font-size: 7pt;
    font-weight: 600;
    color: #262626;
    background-color: #f5f5f5;
    border: 1px solid #e5e5e5;
    padding: 1.5px 7px;
    border-radius: 4px;
    white-space: nowrap;
  }

  /* Skills Grid */
  .skills-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 3.5px 14px;
    font-size: 7.4pt;
  }
  .skill-row {
    display: flex;
    align-items: baseline;
  }
  .skill-label {
    font-weight: 700;
    color: #171717;
    white-space: nowrap;
    margin-right: 5px;
  }
  .skill-val {
    color: #404040;
  }

  /* Project Entries */
  .project-entry {
    margin-bottom: 6px;
  }
  .project-entry:last-child {
    margin-bottom: 0;
  }
  .proj-header {
    display: flex;
    justify-content: space-between;
    align-items: baseline;
    margin-bottom: 1.5px;
  }
  .proj-title {
    font-size: 8.2pt;
    font-weight: 700;
    color: #171717;
  }
  .proj-links {
    font-family: 'JetBrains Mono', monospace;
    font-size: 7pt;
    font-weight: 600;
  }
  .proj-links a {
    color: #ef4444; /* Rajat Red Accent */
    text-decoration: none;
    margin-left: 6px;
  }
  .proj-links a:hover {
    text-decoration: underline;
  }
  .proj-tech {
    font-family: 'JetBrains Mono', monospace;
    font-size: 6.7pt;
    color: #525252;
    margin-bottom: 2px;
  }
  .proj-bullets {
    list-style: none;
    padding-left: 0;
  }
  .proj-bullets li {
    position: relative;
    padding-left: 11px;
    font-size: 7.2pt;
    line-height: 1.32;
    color: #404040;
    margin-bottom: 1.5px;
    text-align: justify;
  }
  .proj-bullets li::before {
    content: '•';
    position: absolute;
    left: 2px;
    color: #ef4444; /* Signature red bullet */
    font-weight: bold;
    font-size: 9pt;
    line-height: 1;
  }
  .proj-bullets li b {
    color: #171717;
    font-weight: 600;
  }

  /* Work Experience */
  .exp-entry {
    margin-bottom: 5px;
  }
  .exp-header {
    display: flex;
    justify-content: space-between;
    align-items: baseline;
    margin-bottom: 1px;
  }
  .exp-title {
    font-size: 8.2pt;
    font-weight: 700;
    color: #171717;
  }
  .exp-company {
    color: #ef4444;
    font-weight: 600;
  }

  /* Certifications & Achievements */
  .cert-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 2.5px 12px;
    font-size: 7.2pt;
    color: #404040;
  }
  .cert-item {
    display: flex;
    align-items: baseline;
    gap: 4px;
  }
  .cert-item::before {
    content: '•';
    color: #ef4444;
    font-weight: bold;
    font-size: 8.5pt;
  }
  .cert-item b {
    color: #171717;
  }
  .cert-item span {
    color: #737373;
    font-family: 'JetBrains Mono', monospace;
    font-size: 6.6pt;
  }

  /* Bottom Stamp */
  .resume-footer {
    border-top: 1px solid #e5e5e5;
    padding-top: 4px;
    margin-top: 6px;
    display: flex;
    justify-content: space-between;
    font-family: 'JetBrains Mono', monospace;
    font-size: 6pt;
    color: #737373;
  }
</style>
</head>
<body>
<div class="page-container">

  <div>
    <!-- RESUME HEADER (Rajat Sahu Signature Style) -->
    <header class="resume-header">
      <div class="header-left">
        <h1>AMAN SHARMA</h1>
        <div class="subtitle">B.Tech CSE Student &bull; Full-Stack Software Developer</div>
        <div class="college-tag">G.L. Bajaj Group of Institutions, Mathura &bull; AKTU University</div>
      </div>

      <div class="header-right">
        <p>
          <i class="fa-solid fa-phone icon-red"></i>
          <a href="tel:+919690683156">+91-9690683156</a>
        </p>
        <p>
          <i class="fa-brands fa-whatsapp icon-red"></i>
          <a href="https://wa.me/919690683156">WhatsApp: +91-9690683156</a>
        </p>
        <p>
          <i class="fa-solid fa-envelope icon-red"></i>
          <a href="mailto:codewithaman88@gmail.com">codewithaman88@gmail.com</a>
        </p>
        <p>
          <i class="fa-solid fa-globe icon-red"></i>
          <a href="https://codingwithaman1.github.io/PORTFOLIO/">codingwithaman1.github.io/PORTFOLIO</a>
        </p>
        <p>
          <i class="fa-brands fa-github icon-red"></i>
          <a href="https://github.com/CodingWithAman1">github.com/CodingWithAman1</a>
        </p>
        <p>
          <i class="fa-brands fa-linkedin icon-red"></i>
          <a href="https://linkedin.com/in/aman-sharma">linkedin.com/in/aman-sharma</a>
        </p>
        <p>
          <i class="fa-solid fa-location-dot icon-red"></i>
          Mathura &amp; Lucknow, Uttar Pradesh, India
        </p>
      </div>
    </header>

    <!-- PROFESSIONAL OBJECTIVE -->
    <section>
      <h2 class="section-title">Professional Objective</h2>
      <p class="objective-text">
        Proactive <b>B.Tech Computer Science Engineering student</b> at G.L. Bajaj Group of Institutions with hands-on expertise building production web platforms, transactional database architectures, and AI-integrated workflows. Proven track record deploying live, full-stack cloud applications (<b>CivicConnect</b>, <b>Inventra</b>) with automated triage, RESTful APIs, and responsive interfaces. Dedicated to engineering scalable, high-impact software solutions within innovative engineering teams.
      </p>
    </section>

    <!-- EDUCATION -->
    <section>
      <h2 class="section-title">Education</h2>
      
      <!-- B.Tech -->
      <div class="edu-item">
        <div>
          <div class="edu-title">Bachelor of Technology (B.Tech) in Computer Science &amp; Engineering</div>
          <div class="edu-sub">G.L. Bajaj Group of Institutions, Mathura (AKTU)</div>
          <div class="edu-details">Core Coursework: Operating Systems, DBMS, OOP, Data Structures &amp; Algorithms, Computer Networks</div>
        </div>
        <div style="text-align: right;">
          <span class="badge-pill">2022 &ndash; 2026</span>
          <div style="font-family: 'JetBrains Mono', monospace; font-size: 6.8pt; color: #ef4444; font-weight: 700; margin-top: 1.5px;">CGPA: 7.8 / 10</div>
        </div>
      </div>

      <!-- Intermediate -->
      <div class="edu-item">
        <div>
          <div class="edu-title">Intermediate (Class XII) &bull; Science (PCM)</div>
          <div class="edu-sub">Brightland School, Lucknow (CBSE)</div>
        </div>
        <div style="text-align: right;">
          <span class="badge-pill">2024</span>
          <div style="font-family: 'JetBrains Mono', monospace; font-size: 6.8pt; color: #525252; font-weight: 600; margin-top: 1.5px;">Score: 78%</div>
        </div>
      </div>

      <!-- High School -->
      <div class="edu-item">
        <div>
          <div class="edu-title">High School (Class X)</div>
          <div class="edu-sub">Brightland School, Lucknow (CBSE)</div>
        </div>
        <div style="text-align: right;">
          <span class="badge-pill">2022</span>
          <div style="font-family: 'JetBrains Mono', monospace; font-size: 6.8pt; color: #525252; font-weight: 600; margin-top: 1.5px;">Score: 82%</div>
        </div>
      </div>
    </section>

    <!-- TECHNICAL SKILLS -->
    <section>
      <h2 class="section-title">Technical Skills</h2>
      <div class="skills-grid">
        <div class="skill-row">
          <span class="skill-label">Programming Languages:</span>
          <span class="skill-val">Python, JavaScript (ES6+), SQL, C, HTML5, CSS3</span>
        </div>
        <div class="skill-row">
          <span class="skill-label">Frameworks &amp; Web:</span>
          <span class="skill-val">Flask 3.x, Jinja2, RESTful APIs, Chart.js, Bootstrap 5, Tailwind CSS</span>
        </div>
        <div class="skill-row">
          <span class="skill-label">Databases &amp; ORM:</span>
          <span class="skill-val">PostgreSQL, Neon DB, SQLite, SQLAlchemy 2.0 (Relational Schemas)</span>
        </div>
        <div class="skill-row">
          <span class="skill-label">Cloud, AI &amp; DevOps:</span>
          <span class="skill-val">Gemini Vision AI, Vercel Serverless, Render, Git, GitHub, Linux/Bash</span>
        </div>
      </div>
    </section>

    <!-- PROJECTS -->
    <section>
      <h2 class="section-title">Featured Projects</h2>

      <!-- Project 1: CivicConnect -->
      <div class="project-entry">
        <div class="proj-header">
          <span class="proj-title">CIVICCONNECT &mdash; AI Civic Action &amp; Grievance Platform</span>
          <span class="proj-links">
            <a href="https://civicconnectweb.onrender.com/"><i class="fa-solid fa-arrow-up-right-from-square"></i> Live Demo</a>
            <a href="https://github.com/CodingWithAman1/CivicConnect"><i class="fa-brands fa-github"></i> GitHub</a>
          </span>
        </div>
        <div class="proj-tech">Flask 3.x &bull; Google Gemini Vision AI &bull; PostgreSQL &bull; Leaflet GPS &bull; Cloudinary &bull; Bootstrap 5</div>
        <ul class="proj-bullets">
          <li><b>Architected full-lifecycle civic governance portal</b> with role-based routing across Citizens, NGOs, and Municipal Authorities.</li>
          <li><b>Integrated Google Gemini Multimodal Vision AI</b> to analyze uploaded complaint photos, auto-detect infrastructure defects (potholes, garbage, water leaks), and compute severity index.</li>
          <li><b>Engineered Haversine GPS proximity clustering (300m radius)</b> to merge duplicate citizen reports, preventing municipal backlog.</li>
          <li><b>Implemented photographic resolution audit engine</b> comparing before/after repair photos before authorizing ticket completion.</li>
        </ul>
      </div>

      <!-- Project 2: Inventra -->
      <div class="project-entry">
        <div class="proj-header">
          <span class="proj-title">INVENTRA &mdash; Smart Cloud Inventory &amp; Stock Analytics</span>
          <span class="proj-links">
            <a href="https://inventra-rho-lac.vercel.app/"><i class="fa-solid fa-arrow-up-right-from-square"></i> Live Demo</a>
            <a href="https://github.com/CodingWithAman1/Inventra"><i class="fa-brands fa-github"></i> GitHub</a>
          </span>
        </div>
        <div class="proj-tech">Flask &bull; SQLAlchemy 2.0 &bull; Neon PostgreSQL &bull; Chart.js &bull; Vercel Serverless WSGI</div>
        <ul class="proj-bullets">
          <li><b>Engineered production warehouse inventory system</b> with real-time stock monitoring, automated low-inventory reorder alerts, and supplier directories.</li>
          <li><b>Built ACID-compliant relational audit trails</b> recording immutable delta history for every inventory transaction (+/- adjustments).</li>
          <li><b>Designed interactive Chart.js dashboards</b> delivering warehouse asset valuation, monthly movement graphs, and dynamic CSV exports.</li>
          <li><b>Architected serverless WSGI microservice on Vercel</b> connected to Neon cloud PostgreSQL with connection pooling.</li>
        </ul>
      </div>

      <!-- Project 3: MyRail -->
      <div class="project-entry">
        <div class="proj-header">
          <span class="proj-title">MYRAIL &mdash; Real-Time Indian Railway PNR &amp; Live Train Tracking</span>
          <span class="proj-links">
            <a href="https://github.com/CodingWithAman1/myrail"><i class="fa-brands fa-github"></i> GitHub</a>
          </span>
        </div>
        <div class="proj-tech">JavaScript (ES6+) &bull; RapidAPI &bull; Railway REST APIs &bull; Asynchronous Fetch &bull; Bootstrap 5</div>
        <ul class="proj-bullets">
          <li><b>Engineered responsive railway tracker web application</b> providing real-time PNR status, live train status, and station autocomplete lookups.</li>
          <li><b>Implemented asynchronous API caching and error boundary layer</b> ensuring sub-second response times and high availability.</li>
        </ul>
      </div>

      <!-- Project 4: Amanzon -->
      <div class="project-entry">
        <div class="proj-header">
          <span class="proj-title">AMANZON &mdash; Responsive Full-Featured E-Commerce Storefront</span>
          <span class="proj-links">
            <a href="https://github.com/CodingWithAman1/amanzon"><i class="fa-brands fa-github"></i> GitHub</a>
          </span>
        </div>
        <div class="proj-tech">HTML5 &bull; CSS3 (Modern Flexbox &amp; Grid) &bull; JavaScript (ES6+) &bull; LocalStorage State Management</div>
        <ul class="proj-bullets">
          <li><b>Developed responsive multi-page e-commerce storefront</b> featuring dynamic product catalog filtering, interactive cart state, and modal checkout.</li>
          <li><b>Optimized cross-browser rendering pipeline</b> ensuring 100% responsive fidelity across desktop, tablet, and mobile breakpoints.</li>
        </ul>
      </div>
    </section>

    <!-- WORK EXPERIENCE -->
    <section>
      <h2 class="section-title">Work Experience</h2>
      <div class="exp-entry">
        <div class="exp-header">
          <div class="exp-title">Web Development Intern &mdash; <span class="exp-company">3 Skills India</span></div>
          <span class="badge-pill">July 2024 &ndash; Aug 2024 &bull; Remote</span>
        </div>
        <ul class="proj-bullets">
          <li>Modernized frontend web architectures with semantic HTML5, CSS3, and JavaScript, reducing mobile layout shifts.</li>
          <li>Collaborated with senior engineers on sprint velocity, code reviews, and cross-device accessibility optimizations.</li>
        </ul>
      </div>
    </section>

    <!-- CERTIFICATIONS & ACHIEVEMENTS -->
    <section>
      <h2 class="section-title">Certifications &amp; Achievements</h2>
      <div class="cert-grid">
        <div class="cert-item">
          <b>Python Programming</b> &mdash; <span>Reliance Foundation &amp; N.S.D.C. (90h intensive)</span>
        </div>
        <div class="cert-item">
          <b>Cisco CyberSecurity &amp; AI</b> &mdash; <span>AI &amp; Security Learn-a-Thon</span>
        </div>
        <div class="cert-item">
          <b>Smart India Hackathon (SIH) Internal</b> &mdash; <span>AI civic grievance dispatch prototype</span>
        </div>
        <div class="cert-item">
          <b>Algorithmic Problem Solving</b> &mdash; <span>150+ DSA problems solved (LeetCode &amp; HackerRank)</span>
        </div>
      </div>
    </section>
  </div>

  <!-- FOOTER STAMP -->
  <footer class="resume-footer">
    <div>Portfolio: codingwithaman1.github.io/PORTFOLIO &bull; GitHub: github.com/CodingWithAman1</div>
    <div>Contact: +91-9690683156 &bull; codewithaman88@gmail.com</div>
  </footer>

</div>
</body>
</html>
"""
    html_file = os.path.abspath("resume_source.html")
    with open(html_file, "w", encoding="utf-8") as f:
        f.write(html_content)

    edge_path = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
    abs_pdf = os.path.abspath(output_pdf_path)
    file_url = "file:///" + html_file.replace("\\", "/")

    cmd = [
        edge_path,
        "--headless",
        "--disable-gpu",
        "--no-pdf-header-footer",
        f"--print-to-pdf={abs_pdf}",
        file_url
    ]
    subprocess.run(cmd, capture_output=True, text=True, timeout=30)

    if not os.path.exists(abs_pdf):
        raise RuntimeError("PDF was not created!")

    pdf_doc = pymupdf.open(abs_pdf)
    total_pages = len(pdf_doc)

    if preview_png_path:
        page = pdf_doc[0]
        pix = page.get_pixmap(dpi=150)
        pix.save(preview_png_path)

    return total_pages

if __name__ == "__main__":
    out_pdf = "c:/Users/lenovo/Documents/antigravity/PORTFOLIO/assets/Aman-Sharma-Resume.pdf"
    preview_png = "c:/Users/lenovo/Documents/antigravity/PORTFOLIO/assets/resume_preview.png"
    pages = build_resume(out_pdf, preview_png)
    print(f"Built PDF successfully. Total pages: {pages}")
