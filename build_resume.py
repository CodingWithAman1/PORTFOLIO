import os
import subprocess
import pymupdf

def build_futuristic_resume(output_pdf_path, preview_png_path=None):
    html_content = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Aman Sharma - Futuristic Resume</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;700&family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Space+Grotesk:wght@500;700;800&display=swap" rel="stylesheet">
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
    background-color: #030712;
    color: #cbd5e1;
    font-family: 'Plus Jakarta Sans', -apple-system, sans-serif;
    -webkit-print-color-adjust: exact;
    print-color-adjust: exact;
    overflow: hidden;
    position: relative;
    font-size: 8.2pt;
    line-height: 1.25;
  }

  /* Cyber Grid Background */
  body::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0; bottom: 0;
    background-image: 
      linear-gradient(to right, rgba(56, 189, 248, 0.03) 1px, transparent 1px),
      linear-gradient(to bottom, rgba(56, 189, 248, 0.03) 1px, transparent 1px);
    background-size: 20px 20px;
    pointer-events: none;
    z-index: 0;
  }

  .container {
    position: relative;
    z-index: 1;
    padding: 0.28in 0.32in;
    height: 11in;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
  }

  /* Telemetry Bar */
  .hud-bar {
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-bottom: 1px solid rgba(56, 189, 248, 0.2);
    padding-bottom: 5px;
    margin-bottom: 8px;
    font-family: 'JetBrains Mono', monospace;
    font-size: 6.2pt;
    color: #64748b;
    letter-spacing: 0.5px;
  }
  .hud-badge {
    display: inline-flex;
    align-items: center;
    gap: 4px;
    background: rgba(16, 185, 129, 0.1);
    color: #34d399;
    border: 1px solid rgba(16, 185, 129, 0.3);
    padding: 1.5px 6px;
    border-radius: 999px;
    font-weight: 600;
  }
  .hud-dot {
    width: 5px;
    height: 5px;
    border-radius: 50%;
    background: #10b981;
    box-shadow: 0 0 6px #10b981;
  }

  /* Header Section */
  .header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    background: linear-gradient(135deg, rgba(15, 23, 42, 0.9) 0%, rgba(10, 15, 29, 0.95) 100%);
    border: 1px solid rgba(56, 189, 248, 0.25);
    border-radius: 8px;
    padding: 10px 14px;
    box-shadow: 0 4px 20px -2px rgba(0, 0, 0, 0.5);
    margin-bottom: 9px;
  }
  .header-left {
    display: flex;
    align-items: center;
    gap: 12px;
  }
  .avatar-card {
    width: 46px;
    height: 46px;
    border-radius: 8px;
    background: linear-gradient(135deg, #0284c7 0%, #4f46e5 100%);
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    font-family: 'Space Grotesk', sans-serif;
    font-weight: 800;
    font-size: 15pt;
    color: #ffffff;
    box-shadow: 0 0 16px rgba(14, 165, 233, 0.45);
    border: 1px solid rgba(255, 255, 255, 0.3);
    flex-shrink: 0;
  }
  .avatar-card span {
    font-size: 4.8pt;
    font-family: 'JetBrains Mono', monospace;
    opacity: 0.85;
    margin-top: -2px;
    letter-spacing: 0.5px;
  }
  .name-block h1 {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 18pt;
    font-weight: 700;
    color: #ffffff;
    letter-spacing: -0.3px;
    line-height: 1.05;
    background: linear-gradient(90deg, #ffffff 0%, #38bdf8 65%, #818cf8 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
  }
  .name-block .role {
    font-family: 'JetBrains Mono', monospace;
    font-size: 7.2pt;
    font-weight: 700;
    color: #38bdf8;
    letter-spacing: 0.5px;
    margin-top: 2px;
  }
  .name-block .tagline {
    font-size: 6.8pt;
    color: #94a3b8;
    margin-top: 1px;
  }

  .header-right {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 4px 10px;
    font-size: 6.8pt;
    font-family: 'JetBrains Mono', monospace;
  }
  .contact-item {
    display: flex;
    align-items: center;
    gap: 6px;
    color: #94a3b8;
  }
  .contact-item a {
    color: #38bdf8;
    text-decoration: none;
    font-weight: 500;
  }
  .contact-item.wa a {
    color: #34d399;
    font-weight: 700;
  }
  .icon-svg {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    flex-shrink: 0;
  }

  /* Metrics Ribbon */
  .metrics-ribbon {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 7px;
    margin-bottom: 9px;
  }
  .metric-card {
    background: rgba(15, 23, 42, 0.6);
    border: 1px solid rgba(255, 255, 255, 0.07);
    border-radius: 6px;
    padding: 5px 8px;
    display: flex;
    align-items: center;
    gap: 7px;
  }
  .metric-num {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 11pt;
    font-weight: 700;
    color: #38bdf8;
    line-height: 1;
  }
  .metric-label {
    font-size: 5.8pt;
    font-family: 'JetBrains Mono', monospace;
    color: #94a3b8;
    line-height: 1.15;
    text-transform: uppercase;
    letter-spacing: 0.3px;
  }

  /* Main Grid */
  .main-grid {
    display: grid;
    grid-template-columns: 2.35in 1fr;
    gap: 10px;
    flex: 1;
  }

  /* Section Styles */
  .section-title {
    font-family: 'JetBrains Mono', monospace;
    font-size: 7.4pt;
    font-weight: 700;
    color: #ffffff;
    text-transform: uppercase;
    letter-spacing: 0.6px;
    display: flex;
    align-items: center;
    gap: 5px;
    margin-bottom: 5px;
  }
  .section-title::before {
    content: '//';
    color: #0284c7;
    font-weight: 800;
  }
  .section-title::after {
    content: '';
    flex: 1;
    height: 1px;
    background: linear-gradient(90deg, rgba(56, 189, 248, 0.3) 0%, transparent 100%);
    margin-left: 4px;
  }

  /* Left Column Cards */
  .side-card {
    background: rgba(15, 23, 42, 0.55);
    border: 1px solid rgba(255, 255, 255, 0.06);
    border-radius: 6px;
    padding: 6px 8px;
    margin-bottom: 7px;
  }
  .skill-group {
    margin-bottom: 4px;
  }
  .skill-group:last-child {
    margin-bottom: 0;
  }
  .skill-cat {
    font-family: 'JetBrains Mono', monospace;
    font-size: 6.2pt;
    font-weight: 700;
    color: #38bdf8;
    text-transform: uppercase;
    letter-spacing: 0.3px;
    margin-bottom: 2px;
  }
  .skill-tags {
    display: flex;
    flex-wrap: wrap;
    gap: 3px;
  }
  .tag {
    background: rgba(30, 41, 59, 0.8);
    border: 1px solid rgba(56, 189, 248, 0.2);
    color: #e2e8f0;
    font-size: 5.9pt;
    padding: 1px 4.5px;
    border-radius: 3px;
    font-family: 'JetBrains Mono', monospace;
  }
  .tag.hot {
    background: rgba(14, 165, 233, 0.15);
    border-color: rgba(56, 189, 248, 0.5);
    color: #38bdf8;
    font-weight: 600;
  }

  /* Education Item */
  .edu-item {
    margin-bottom: 5px;
    padding-left: 6px;
    border-left: 2px solid rgba(56, 189, 248, 0.3);
  }
  .edu-item:last-child {
    margin-bottom: 0;
  }
  .edu-deg {
    font-size: 6.8pt;
    font-weight: 700;
    color: #f1f5f9;
  }
  .edu-inst {
    font-size: 6.2pt;
    color: #94a3b8;
  }
  .edu-meta {
    font-family: 'JetBrains Mono', monospace;
    font-size: 5.8pt;
    color: #38bdf8;
  }

  /* Certifications */
  .cert-item {
    display: flex;
    align-items: baseline;
    gap: 4px;
    font-size: 6.2pt;
    margin-bottom: 3px;
    color: #cbd5e1;
  }
  .cert-item::before {
    content: '›';
    color: #34d399;
    font-size: 8pt;
    font-weight: 700;
  }
  .cert-meta {
    color: #64748b;
    font-size: 5.6pt;
    font-family: 'JetBrains Mono', monospace;
  }

  /* Cyber Launchpad Links */
  .launchpad-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 4px;
  }
  .launch-link {
    display: flex;
    align-items: center;
    justify-content: space-between;
    background: rgba(30, 41, 59, 0.6);
    border: 1px solid rgba(56, 189, 248, 0.25);
    border-radius: 4px;
    padding: 3px 5px;
    font-family: 'JetBrains Mono', monospace;
    font-size: 5.8pt;
    color: #38bdf8;
    text-decoration: none;
    font-weight: 600;
  }
  .launch-link.green {
    border-color: rgba(16, 185, 129, 0.3);
    color: #34d399;
    background: rgba(16, 185, 129, 0.08);
  }
  .launch-link span {
    font-size: 7pt;
  }

  /* Right Column (Cyberdeck) */
  .summary-card {
    background: linear-gradient(135deg, rgba(15, 23, 42, 0.7) 0%, rgba(30, 41, 59, 0.4) 100%);
    border: 1px solid rgba(56, 189, 248, 0.25);
    border-left: 3px solid #0284c7;
    border-radius: 6px;
    padding: 5px 8px;
    margin-bottom: 7px;
    font-size: 6.8pt;
    line-height: 1.35;
    color: #cbd5e1;
  }
  .summary-card b {
    color: #f8fafc;
  }

  /* Project Cards */
  .project-card {
    background: rgba(15, 23, 42, 0.6);
    border: 1px solid rgba(255, 255, 255, 0.07);
    border-radius: 6px;
    padding: 5px 8px;
    margin-bottom: 5.5px;
    position: relative;
  }
  .project-header {
    display: flex;
    justify-content: space-between;
    align-items: baseline;
    margin-bottom: 2px;
  }
  .proj-title-wrap {
    display: flex;
    align-items: center;
    gap: 6px;
  }
  .proj-title {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 8.2pt;
    font-weight: 700;
    color: #ffffff;
    letter-spacing: -0.2px;
  }
  .proj-badge {
    background: rgba(56, 189, 248, 0.12);
    border: 1px solid rgba(56, 189, 248, 0.35);
    color: #38bdf8;
    font-family: 'JetBrains Mono', monospace;
    font-size: 5.2pt;
    font-weight: 700;
    padding: 1px 4px;
    border-radius: 3px;
    text-transform: uppercase;
  }
  .proj-actions {
    display: flex;
    gap: 5px;
    font-family: 'JetBrains Mono', monospace;
    font-size: 6.2pt;
  }
  .btn-live {
    background: rgba(14, 165, 233, 0.18);
    border: 1px solid #0284c7;
    color: #38bdf8;
    text-decoration: none;
    padding: 1.5px 6px;
    border-radius: 3px;
    font-weight: 700;
  }
  .btn-code {
    background: rgba(255, 255, 255, 0.04);
    border: 1px solid rgba(255, 255, 255, 0.15);
    color: #94a3b8;
    text-decoration: none;
    padding: 1.5px 5px;
    border-radius: 3px;
    font-weight: 600;
  }
  .proj-tech {
    font-family: 'JetBrains Mono', monospace;
    font-size: 5.8pt;
    color: #818cf8;
    margin-bottom: 2.5px;
  }
  .bullet-list {
    list-style: none;
  }
  .bullet-list li {
    position: relative;
    padding-left: 9px;
    font-size: 6.5pt;
    line-height: 1.3;
    color: #94a3b8;
    margin-bottom: 1.5px;
  }
  .bullet-list li::before {
    content: '▹';
    position: absolute;
    left: 0;
    color: #38bdf8;
    font-size: 7.5pt;
  }
  .bullet-list li b {
    color: #e2e8f0;
    font-weight: 600;
  }

  /* Experience Card */
  .exp-card {
    background: rgba(15, 23, 42, 0.6);
    border: 1px solid rgba(255, 255, 255, 0.07);
    border-radius: 6px;
    padding: 5px 8px;
    margin-bottom: 5.5px;
  }
  .exp-header {
    display: flex;
    justify-content: space-between;
    align-items: baseline;
    margin-bottom: 2px;
  }
  .exp-role {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 7.8pt;
    font-weight: 700;
    color: #ffffff;
  }
  .exp-comp {
    color: #38bdf8;
    font-weight: 600;
  }
  .exp-date {
    font-family: 'JetBrains Mono', monospace;
    font-size: 6pt;
    color: #34d399;
  }

  /* Milestones */
  .milestones-card {
    background: rgba(15, 23, 42, 0.6);
    border: 1px solid rgba(255, 255, 255, 0.07);
    border-radius: 6px;
    padding: 4px 8px;
  }

  /* Footer Tech Stamp */
  .tech-footer {
    border-top: 1px solid rgba(255, 255, 255, 0.06);
    padding-top: 3px;
    display: flex;
    justify-content: space-between;
    font-family: 'JetBrains Mono', monospace;
    font-size: 5.5pt;
    color: #475569;
    letter-spacing: 0.5px;
  }
</style>
</head>
<body>
<div class="container">

  <!-- TOP TELEMETRY BAR -->
  <div class="hud-bar">
    <div>SYS_ID: AMAN-SHARMA // ARCH: FULL-STACK-AI // NODE: 27.4924° N, 77.6737° E (IN)</div>
    <div class="hud-badge"><span class="hud-dot"></span> OPEN FOR SOFTWARE ENGINEERING ROLES</div>
    <div>COMPILED: 2026.10 // VER: 4.2-FUTURISTIC</div>
  </div>

  <!-- HERO HEADER -->
  <header class="header">
    <div class="header-left">
      <div class="avatar-card">
        AS
        <span>DEV-01</span>
      </div>
      <div class="name-block">
        <h1>AMAN SHARMA</h1>
        <div class="role">&lt;FULL_STACK_SOFTWARE_ENGINEER :: AI_&amp;_CLOUD_SYSTEMS /&gt;</div>
        <div class="tagline">B.Tech CSE &bull; Specialized in Python (Flask), Neon PostgreSQL, RESTful APIs &amp; Gemini AI Vision</div>
      </div>
    </div>
    <div class="header-right">
      <div class="contact-item">
        <span class="icon-svg">
          <svg width="10" height="10" viewBox="0 0 24 24" fill="none" stroke="#38bdf8" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z"></path></svg>
        </span>
        <a href="tel:+919690683156">+91-9690683156</a>
      </div>
      <div class="contact-item wa">
        <span class="icon-svg">
          <svg width="10" height="10" viewBox="0 0 24 24" fill="none" stroke="#34d399" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 11.5a8.38 8.38 0 0 1-.9 3.8 8.5 8.5 0 0 1-7.6 4.7 8.38 8.38 0 0 1-3.8-.9L3 21l1.9-5.7a8.38 8.38 0 0 1-.9-3.8 8.5 8.5 0 0 1 4.7-7.6 8.38 8.38 0 0 1 3.8-.9h.5a8.48 8.48 0 0 1 8 8v.5z"></path></svg>
        </span>
        <a href="https://wa.me/919690683156">WhatsApp Direct</a>
      </div>
      <div class="contact-item">
        <span class="icon-svg">
          <svg width="10" height="10" viewBox="0 0 24 24" fill="none" stroke="#38bdf8" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"></path><polyline points="22,6 12,13 2,6"></polyline></svg>
        </span>
        <a href="mailto:codewithaman88@gmail.com">codewithaman88@gmail.com</a>
      </div>
      <div class="contact-item">
        <span class="icon-svg">
          <svg width="10" height="10" viewBox="0 0 24 24" fill="none" stroke="#38bdf8" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"></circle><line x1="2" y1="12" x2="22" y2="12"></line><path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"></path></svg>
        </span>
        <a href="https://codingwithaman1.github.io/PORTFOLIO/">codingwithaman1.github.io</a>
      </div>
      <div class="contact-item">
        <span class="icon-svg">
          <svg width="10" height="10" viewBox="0 0 24 24" fill="none" stroke="#38bdf8" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M9 19c-5 1.5-5-2.5-7-3m14 6v-3.87a3.37 3.37 0 0 0-.94-2.61c3.14-.35 6.44-1.54 6.44-7A5.44 5.44 0 0 0 20 4.77 5.07 5.07 0 0 0 19.91 1S18.73.65 16 2.48a13.38 13.38 0 0 0-7 0C6.27.65 5.09 1 5.09 1A5.07 5.07 0 0 0 5 4.77a5.44 5.44 0 0 0-1.5 3.78c0 5.42 3.3 6.61 6.44 7A3.37 3.37 0 0 0 9 18.13V22"></path></svg>
        </span>
        <a href="https://github.com/CodingWithAman1">gh/CodingWithAman1</a>
      </div>
      <div class="contact-item">
        <span class="icon-svg">
          <svg width="10" height="10" viewBox="0 0 24 24" fill="none" stroke="#38bdf8" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M16 8a6 6 0 0 1 6 6v7h-4v-7a2 2 0 0 0-2-2 2 2 0 0 0-2 2v7h-4v-7a6 6 0 0 1 6-6z"></path><rect x="2" y="9" width="4" height="12"></rect><circle cx="4" cy="4" r="2"></circle></svg>
        </span>
        <a href="https://linkedin.com/in/aman-sharma">in/aman-sharma</a>
      </div>
    </div>
  </header>

  <!-- METRICS HUD RIBBON -->
  <div class="metrics-ribbon">
    <div class="metric-card">
      <div class="metric-num">04+</div>
      <div class="metric-label">Live Production<br/>Cloud Platforms</div>
    </div>
    <div class="metric-card">
      <div class="metric-num">150+</div>
      <div class="metric-label">Algorithmic<br/>Problems Solved</div>
    </div>
    <div class="metric-card">
      <div class="metric-num">7.8</div>
      <div class="metric-label">B.Tech CGPA<br/>AKTU University</div>
    </div>
    <div class="metric-card">
      <div class="metric-num">90h</div>
      <div class="metric-label">Reliance &amp; NSDC<br/>Python Certified</div>
    </div>
  </div>

  <!-- MAIN TWO-COLUMN CYBER GRID -->
  <div class="main-grid">

    <!-- LEFT COLUMN: SYSTEM DATA -->
    <div class="left-col">

      <!-- SKILL MATRIX -->
      <div class="section-title">Tech Matrix</div>
      <div class="side-card">
        <div class="skill-group">
          <div class="skill-cat">Core Languages</div>
          <div class="skill-tags">
            <span class="tag hot">Python</span>
            <span class="tag hot">JavaScript (ES6+)</span>
            <span class="tag">SQL</span>
            <span class="tag">C</span>
            <span class="tag">HTML5 / CSS3</span>
          </div>
        </div>
        <div class="skill-group" style="margin-top: 3px;">
          <div class="skill-cat">Backend &amp; Frameworks</div>
          <div class="skill-tags">
            <span class="tag hot">Flask 3.x</span>
            <span class="tag">RESTful APIs</span>
            <span class="tag">Jinja2</span>
            <span class="tag">Chart.js</span>
            <span class="tag">Tailwind CSS</span>
            <span class="tag">Bootstrap 5</span>
          </div>
        </div>
        <div class="skill-group" style="margin-top: 3px;">
          <div class="skill-cat">Databases &amp; ORM</div>
          <div class="skill-tags">
            <span class="tag hot">PostgreSQL</span>
            <span class="tag hot">Neon Cloud DB</span>
            <span class="tag">SQLAlchemy 2.0</span>
            <span class="tag">SQLite</span>
          </div>
        </div>
        <div class="skill-group" style="margin-top: 3px;">
          <div class="skill-cat">AI, Cloud &amp; DevOps</div>
          <div class="skill-tags">
            <span class="tag hot">Gemini Vision AI</span>
            <span class="tag">Vercel Serverless</span>
            <span class="tag">Render Cloud</span>
            <span class="tag">Git / GitHub</span>
            <span class="tag">Linux / Bash</span>
            <span class="tag">Postman</span>
          </div>
        </div>
      </div>

      <!-- CORE COMPETENCIES -->
      <div class="section-title">Competencies</div>
      <div class="side-card">
        <div style="font-size: 6.3pt; line-height: 1.4; color: #cbd5e1;">
          <div><span style="color:#38bdf8;">⚡</span> Full-Stack Web Architecture</div>
          <div><span style="color:#38bdf8;">⚡</span> Multimodal AI Vision Integration</div>
          <div><span style="color:#38bdf8;">⚡</span> Relational Schema &amp; ACID Logging</div>
          <div><span style="color:#38bdf8;">⚡</span> Serverless Microservice Design</div>
          <div><span style="color:#38bdf8;">⚡</span> High-Performance Responsive UX</div>
        </div>
      </div>

      <!-- ACADEMIC TIMELINE -->
      <div class="section-title">Education</div>
      <div class="side-card">
        <div class="edu-item">
          <div class="edu-deg">B.Tech in Computer Science &amp; Engg</div>
          <div class="edu-inst">G.L. Bajaj Group of Institutions, Mathura</div>
          <div class="edu-meta">AKTU &bull; 2022 &ndash; 2026 &bull; CGPA: 7.8 / 10</div>
          <div style="font-size: 5.5pt; color: #64748b; font-family: 'JetBrains Mono', monospace;">Coursework: OS, DBMS, OOP, DSA, Networks</div>
        </div>
        <div class="edu-item" style="margin-top: 3.5px;">
          <div class="edu-deg">Intermediate (Class XII) &bull; PCM</div>
          <div class="edu-inst">Brightland School, Lucknow (CBSE)</div>
          <div class="edu-meta">Score: 78% &bull; 2024</div>
        </div>
        <div class="edu-item" style="margin-top: 3.5px;">
          <div class="edu-deg">High School (Class X)</div>
          <div class="edu-inst">Brightland School, Lucknow (CBSE)</div>
          <div class="edu-meta">Score: 82% &bull; 2022</div>
        </div>
      </div>

      <!-- CERTIFICATIONS -->
      <div class="section-title">Credentials</div>
      <div class="side-card">
        <div class="cert-item">
          <div><b>Python Programming</b> &bull; <span class="cert-meta">Reliance &amp; NSDC (90h)</span></div>
        </div>
        <div class="cert-item">
          <div><b>Cisco CyberSecurity &amp; AI</b> &bull; <span class="cert-meta">Learn-a-Thon</span></div>
        </div>
        <div class="cert-item">
          <div><b>Upskilling in Python</b> &bull; <span class="cert-meta">IoT Academy</span></div>
        </div>
        <div class="cert-item">
          <div><b>Problem Solving</b> &bull; <span class="cert-meta">HackerRank Verified</span></div>
        </div>
      </div>

      <!-- LAUNCHPAD VERIFIED LINKS -->
      <div class="section-title">Live Launchpad</div>
      <div class="launchpad-grid">
        <a href="https://codingwithaman1.github.io/PORTFOLIO/" class="launch-link">
          PORTFOLIO <span>↗</span>
        </a>
        <a href="https://civicconnectweb.onrender.com/" class="launch-link">
          CIVICCONNECT <span>↗</span>
        </a>
        <a href="https://inventra-rho-lac.vercel.app/" class="launch-link">
          INVENTRA <span>↗</span>
        </a>
        <a href="https://wa.me/919690683156" class="launch-link green">
          WHATSAPP <span>↗</span>
        </a>
      </div>

    </div>

    <!-- RIGHT COLUMN: MAIN CYBERDECK -->
    <div class="right-col">

      <!-- EXECUTIVE MANIFEST -->
      <div class="section-title">System Manifest // Summary</div>
      <div class="summary-card">
        Forward-thinking <b>Computer Science Engineer &amp; Full-Stack Developer</b> specializing in resilient backend architectures, transactional database systems, and AI-integrated workflows. Proven track record deploying <b>production applications to Render and Vercel</b> featuring multi-tenant authorization, <b>Google Gemini Multimodal Vision AI pipelines</b>, real-time telemetry, and serverless compute. Dedicated to high-velocity development and scalable, user-centric systems.
      </div>

      <!-- FEATURED PRODUCTION PROJECTS -->
      <div class="section-title">Production Deployments &amp; Projects</div>

      <!-- PROJECT 1: CIVICCONNECT -->
      <div class="project-card">
        <div class="project-header">
          <div class="proj-title-wrap">
            <span class="proj-title">CIVICCONNECT</span>
            <span class="proj-badge">AI VISION &bull; GOVTECH</span>
          </div>
          <div class="proj-actions">
            <a href="https://civicconnectweb.onrender.com/" class="btn-live">⚡ LIVE APP ↗</a>
            <a href="https://github.com/CodingWithAman1/CivicConnect" class="btn-code">CODE ↗</a>
          </div>
        </div>
        <div class="proj-tech">Flask 3.x &bull; Google Gemini Multimodal Vision AI &bull; PostgreSQL &bull; Leaflet GPS &bull; Cloudinary</div>
        <ul class="bullet-list">
          <li><b>Architected full-lifecycle civic governance platform</b> supporting automated role-based triage workflows across Citizens, NGOs, and Municipal Authorities.</li>
          <li><b>Integrated Gemini Vision Multimodal AI</b> to analyze uploaded defect imagery, auto-detect infrastructure failures (potholes, garbage, water leaks), and compute severity.</li>
          <li><b>Engineered Haversine geospatial proximity clustering (300m radius)</b> to merge duplicate reports, reducing municipal processing backlog by 40%.</li>
          <li><b>Implemented photographic resolution audit engine</b> comparing before/after repair imagery before authorizing ticket resolution.</li>
        </ul>
      </div>

      <!-- PROJECT 2: INVENTRA -->
      <div class="project-card">
        <div class="project-header">
          <div class="proj-title-wrap">
            <span class="proj-title">INVENTRA</span>
            <span class="proj-badge">CLOUD ERP &bull; SERVERLESS</span>
          </div>
          <div class="proj-actions">
            <a href="https://inventra-rho-lac.vercel.app/" class="btn-live">⚡ LIVE APP ↗</a>
            <a href="https://github.com/CodingWithAman1/Inventra" class="btn-code">CODE ↗</a>
          </div>
        </div>
        <div class="proj-tech">Flask &bull; SQLAlchemy 2.0 &bull; Neon PostgreSQL &bull; Chart.js &bull; Vercel Serverless WSGI</div>
        <ul class="bullet-list">
          <li><b>Engineered production warehouse inventory system</b> with real-time stock monitoring, automated low-inventory reorder alerts, and supplier directories.</li>
          <li><b>Built ACID-compliant relational audit ledger</b> recording immutable delta history for every inventory adjustment with database transaction safety.</li>
          <li><b>Designed Chart.js analytics engine</b> visualizing warehouse asset valuation, monthly stock deltas, and automated CSV export pipelines.</li>
          <li><b>Architected zero-configuration serverless deployment on Vercel</b> with Neon cloud PostgreSQL connection pooling.</li>
        </ul>
      </div>

      <!-- PROJECT 3: MYRAIL -->
      <div class="project-card">
        <div class="project-header">
          <div class="proj-title-wrap">
            <span class="proj-title">MYRAIL</span>
            <span class="proj-badge">HIGH-CONCURRENCY API</span>
          </div>
          <div class="proj-actions">
            <a href="https://github.com/CodingWithAman1/myrail" class="btn-code">CODE ↗</a>
          </div>
        </div>
        <div class="proj-tech">JavaScript (ES6+) &bull; RapidAPI &bull; Railway REST APIs &bull; Asynchronous Fetch &bull; Bootstrap 5</div>
        <ul class="bullet-list">
          <li><b>Engineered live railway utility web application</b> delivering real-time PNR confirmation status, live train tracking, and station autocomplete lookups.</li>
          <li><b>Implemented asynchronous API caching and error boundary layer</b> ensuring sub-second responses and resilience against external rate limits.</li>
        </ul>
      </div>

      <!-- PROJECT 4: AMANZON -->
      <div class="project-card">
        <div class="project-header">
          <div class="proj-title-wrap">
            <span class="proj-title">AMANZON</span>
            <span class="proj-badge">E-COMMERCE UI</span>
          </div>
          <div class="proj-actions">
            <a href="https://github.com/CodingWithAman1/amanzon" class="btn-code">CODE ↗</a>
          </div>
        </div>
        <div class="proj-tech">HTML5 &bull; CSS3 (Modern Flexbox &amp; Grid) &bull; JavaScript (ES6+) &bull; LocalStorage State Engine</div>
        <ul class="bullet-list">
          <li><b>Developed responsive multi-page e-commerce storefront</b> featuring dynamic product catalog filtering, interactive cart state, and modal checkout.</li>
          <li><b>Optimized cross-browser rendering pipeline</b> ensuring 100% responsive fidelity across mobile, tablet, and desktop viewports.</li>
        </ul>
      </div>

      <!-- PROFESSIONAL EXPERIENCE -->
      <div class="section-title">Work Experience</div>
      <div class="exp-card">
        <div class="exp-header">
          <div>
            <span class="exp-role">Web Development Intern</span> &mdash; 
            <span class="exp-comp">3 Skills India</span>
          </div>
          <div class="exp-date">July 2024 &ndash; Aug 2024 // Remote</div>
        </div>
        <ul class="bullet-list">
          <li>Modernized frontend web architectures with semantic HTML5, CSS3, and JavaScript, reducing mobile layout shifts.</li>
          <li>Collaborated with senior engineers on sprint velocity, code reviews, and cross-browser accessibility standards.</li>
        </ul>
      </div>

      <!-- ENGINEERING HIGHLIGHTS -->
      <div class="section-title">Engineering Highlights &amp; Honors</div>
      <div class="milestones-card">
        <ul class="bullet-list">
          <li><b>Cloud Deployments:</b> Architected and maintain 4 live full-stack applications with 99.9% uptime across Vercel and Render.</li>
          <li><b>Competitive Problem Solving:</b> Solved 150+ Data Structures &amp; Algorithms challenges across LeetCode &amp; HackerRank.</li>
          <li><b>Smart India Hackathon (SIH) Internal:</b> Conceptualized and prototyped AI-driven civic issue dispatch engine.</li>
        </ul>
      </div>

    </div>

  </div>

  <!-- TECH FOOTER STAMP -->
  <footer class="tech-footer">
    <div>PORTFOLIO: CODINGWITHAMAN1.GITHUB.IO/PORTFOLIO // REPO: GITHUB.COM/CODINGWITHAMAN1</div>
    <div>CONTACT: +91-9690683156 (CALL / WHATSAPP) // CODEWITHAMAN88@GMAIL.COM</div>
  </footer>

</div>
</body>
</html>
"""
    html_file = os.path.abspath("futuristic_resume.html")
    with open(html_file, "w", encoding="utf-8") as f:
        f.write(html_content)

    print(f"Written HTML to {html_file}")

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
    print(f"Rendering PDF with Edge headless: {' '.join(cmd)}")
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
    print("Edge process return code:", result.returncode)

    if not os.path.exists(abs_pdf):
        raise RuntimeError("PDF was not created!")

    pdf_doc = pymupdf.open(abs_pdf)
    total_pages = len(pdf_doc)
    print(f"Total pages generated: {total_pages}")

    if preview_png_path:
        page = pdf_doc[0]
        pix = page.get_pixmap(dpi=150)
        pix.save(preview_png_path)
        print(f"Saved preview image to {preview_png_path}")

    return total_pages

if __name__ == "__main__":
    out_pdf = "c:/Users/lenovo/Documents/antigravity/PORTFOLIO/assets/Aman-Sharma-Resume.pdf"
    preview_png = "c:/Users/lenovo/Documents/antigravity/PORTFOLIO/assets/preview_futuristic.png"
    pages = build_futuristic_resume(out_pdf, preview_png)
    print(f"Execution complete. Total Pages: {pages}")
