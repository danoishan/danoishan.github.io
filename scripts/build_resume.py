"""Reproduce the two-page portfolio resume. Requires ReportLab."""
from pathlib import Path
import os
from xml.sax.saxutils import escape
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, KeepTogether
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

ROOT=Path(__file__).resolve().parents[1]
DEST=ROOT/'Danoishan_Sinnathamby_Resume_2026.pdf'
FONT_DIR=Path(os.environ.get('RESUME_FONT_DIR','/usr/share/fonts/truetype/dejavu'))
pdfmetrics.registerFont(TTFont('ResumeSans',str(FONT_DIR/'DejaVuSans.ttf')))
pdfmetrics.registerFont(TTFont('ResumeSans-Bold',str(FONT_DIR/'DejaVuSans-Bold.ttf')))
pdfmetrics.registerFontFamily('ResumeSans',normal='ResumeSans',bold='ResumeSans-Bold')
INK=colors.HexColor('#171a1f');BLUE=colors.HexColor('#2457ff');MUTED=colors.HexColor('#555b64')
styles={
 'name':ParagraphStyle('name',fontName='ResumeSans-Bold',fontSize=23,leading=26,textColor=INK,spaceAfter=7),
 'contact':ParagraphStyle('contact',fontName='ResumeSans',fontSize=8.6,leading=12,textColor=MUTED,spaceAfter=12),
 'heading':ParagraphStyle('heading',fontName='ResumeSans-Bold',fontSize=11,leading=14,textColor=BLUE,spaceBefore=12,spaceAfter=7,keepWithNext=True),
 'role':ParagraphStyle('role',fontName='ResumeSans-Bold',fontSize=9.8,leading=13,textColor=INK,spaceAfter=3,keepWithNext=True),
 'meta':ParagraphStyle('meta',fontName='ResumeSans',fontSize=9,leading=12,textColor=MUTED,spaceAfter=7,keepWithNext=True),
 'body':ParagraphStyle('body',fontName='ResumeSans',fontSize=9.3,leading=12.2,textColor=INK,spaceAfter=6),
 'bullet':ParagraphStyle('bullet',fontName='ResumeSans',fontSize=9.3,leading=12.2,textColor=INK,leftIndent=11,firstLineIndent=-9,spaceAfter=5),
 'small':ParagraphStyle('small',fontName='ResumeSans',fontSize=8.8,leading=11.7,textColor=INK,spaceAfter=5),
}
story=[]
def p(text,kind='body'): return Paragraph(text,styles[kind])
def section(label):story.append(p(label,'heading'))
def role(title,company,dates,location):
 story.extend([p(title+' | '+company,'role'),p(location+' | '+dates,'meta')])
def bullets(items):
 for text in items:story.append(p('- '+text,'bullet'))

story.append(p('Danoishan Sinnathamby','name'))
story.append(p('Toronto, Ontario, Canada | 647-467-6986 | <link href="mailto:danoishan@gmail.com">danoishan@gmail.com</link><br/><link href="https://www.linkedin.com/in/danoishan/">linkedin.com/in/danoishan</link> | <link href="https://danoishan.github.io/">danoishan.github.io</link>','contact'))
section('Professional Summary')
story.append(p('Technical project and program delivery professional with 7+ years across CRM, lifecycle marketing, customer success and digital operations. Senior Account Manager at Vigorate since 2021, focused on enterprise CRM, customer data and MarTech. Lead discovery, scope, requirements, dependencies, specialist handoffs, QA/UAT, launch decisions and client adoption, with ownership of budgets, resourcing, risks and executive communication.'))
section('Core Competencies')
story.append(p('Technical project / program delivery | Scope, budget and capacity | Requirements and acceptance criteria | RAID, dependencies and change control | CRM and lifecycle journeys | Customer data, identity and consent | QA/UAT and release governance | Client enablement and operating handoffs','small'))
section('Professional Experience')
role('Senior Account Manager (Technical Project &amp; Program Delivery, CRM &amp; MarTech)','Vigorate','September 2021 to Present','Toronto, Ontario')
bullets([
 'Lead enterprise CRM, lifecycle marketing, customer data and MarTech delivery, translating commercial priorities into scope, workback schedules, technical requirements, QA plans, launch decisions and post-launch improvements.',
 'Manage <b>20+ concurrent client workstreams each quarter</b> across Salesforce Marketing Cloud, Marketing Cloud Next, Salesforce Data 360, Braze and connected data environments, balancing production releases with roadmap and optimization work.',
 'Lead customer engagement delivery across email, SMS/MMS, push and in-app, including programs supporting <b>200M+ annual email, SMS/MMS and push sends</b>. Coordinate audience logic, consent, eligibility, data validation, QA, readiness and reporting.',
 'Introduced structured intake, prioritization, RAID, change control and release practices associated with reported program improvements of <b>30% fewer late-stage scope changes</b> and <b>20% shorter UAT-to-launch cycles</b>.',
 'Own scoping, effort estimates, budgets, burn, SOW support, resource allocation and change planning; improved monthly forecast accuracy to <b>within 5% of actual delivery effort</b> through capacity planning and weekly burn reviews.',
 'Coordinate client, strategy, design, architecture, engineering, data, QA and operations teams. Clarify requirements, sequence dependencies, resolve trade-offs and preserve acceptance evidence across specialist handoffs.',
 'Guide improvements across consent capture, attribution, CRM field mappings, SQL-based audience validation, APIs and connected Salesforce environments. Specialists own production implementation.',
 'Stay involved after release through briefings, release documentation, training and handoff support; use customer feedback, support issues, adoption signals and platform analytics to prioritize optimization.',
 'Provide executive reporting that connects progress, budget, risks, dependencies, customer impact and decisions required.'
])
story.append(PageBreak())
section('Professional Experience, continued')
role('Digital Operations Manager','EnsembleIQ','January 2021 to September 2021','Toronto, Ontario')
bullets([
 'Led integrated digital programs across paid social, Google Ads, sponsored content, lifecycle email and web for retail, CPG and B2B media clients.',
 'Managed <b>30+ multi-channel campaign launches annually</b> from briefing through reporting, aligning audience strategy, creative, media pacing, tracking, landing pages, timelines and stakeholder expectations.',
 'Improved budget-to-click efficiency by a reported <b>5 to 8%</b> through audience refinement, A/B testing, budget pacing and channel-level monitoring.',
 'Built repeatable planning and performance reporting processes that <b>reduced reporting turnaround by 25%</b>, giving advertisers clearer visibility into pacing and optimization.',
 'Partnered with sales, editorial, media, creative and web teams to translate advertiser needs into executable programs while protecting quality and deadlines.'
])
role('Customer Success Manager','101 Mobility','July 2019 to December 2020','North York, Ontario')
bullets([
 'Managed CRM operations, customer analytics, service performance reporting and client-delivery processes supporting acquisition, retention and local growth.',
 'Consolidated referral, lead, service, revenue and customer data into reporting frameworks that <b>reduced manual analysis by 30%</b> and helped leaders identify underperforming channels.',
 'Analyzed customer trends, pull-through rates, job values, service patterns and market data to prioritize marketing, pricing and operational improvements.'
])
role('Project Team Lead, Marketing &amp; Events','Jobs Canada Fair','August 2018 to July 2019','Toronto, Ontario / national')
bullets([
 'Led an <b>eight-person cross-functional team across six provinces</b>, coordinating email, digital campaigns, partner communication, event logistics and on-site activation.',
 'Owned strategy and execution for <b>125+ targeted email campaigns</b>. The wider program contributed to reported increases of <b>10% in customer retention and 15% in new customer acquisition</b>.',
 'Managed simultaneous regional launches and time-sensitive dependencies; centralized planning and campaign tracking improved visibility and handoffs.'
])
section('Tools &amp; Platforms')
story.append(p('<b>Delivery:</b> Wrike, Jira, Asana, Confluence, Microsoft Project, Miro, Figma, Microsoft Office.<br/><b>CRM / data:</b> Salesforce Marketing Cloud, Marketing Cloud Next, Salesforce Data 360, Braze, Journey Builder, email, SMS/MMS, push, in-app, HTML email, SQL-based validation, REST APIs and integrations.<br/><b>Analytics / AI:</b> Google Analytics 4, Looker Studio, Excel; Claude and Claude Code for research, requirements, acceptance criteria, QA scenarios and documentation.','small'))
section('Credentials &amp; Education')
story.append(p('<b>Salesforce, earned 2025:</b> Administrator; Marketing Cloud Account Engagement Specialist; Marketing Cloud Email Specialist; AI Associate (retired February 2026).<br/><b>Braze, 2026:</b> Certified Practitioner; Certified AI Fundamentals.<br/><b>Project / product:</b> Professional Scrum Master I, Scrum.org (2026); BrainStation Product Management Certificate (2022); PMP Exam Preparation (2026, training).<br/><b>Education:</b> Sheridan College, Diploma, Marketing Management (2015).','small'))
story.append(p('Career measures are reported work-history results; program outcomes reflect cross-functional delivery. <link href="https://danoishan.github.io/work/measurement-notes.html">Measurement context and evidence limits</link>.','small'))

def footer(canvas,doc):
 canvas.saveState();canvas.setStrokeColor(colors.HexColor('#d9dce0'));canvas.line(42,31,570,31)
 canvas.setFont('ResumeSans',8);canvas.setFillColor(MUTED)
 canvas.drawString(42,20,'Danoishan Sinnathamby | Technical Delivery | October 2026')
 canvas.drawRightString(570,20,str(doc.page));canvas.restoreState()

doc=SimpleDocTemplate(str(DEST),pagesize=letter,rightMargin=42,leftMargin=42,topMargin=36,bottomMargin=42,title='Danoishan Sinnathamby - Technical Project and Program Delivery',author='Danoishan Sinnathamby',subject='CRM and MarTech delivery resume')
doc.build(story,onFirstPage=footer,onLaterPages=footer)
print(DEST)
