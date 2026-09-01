from pathlib import Path
import re
import html as html_lib

ROOT = Path('.')
SITE = 'https://danoishan.github.io'
BRANCH = 'portfolio-review-upgrades'


def read(path):
    return (ROOT / path).read_text(encoding='utf-8')


def write(path, text):
    p = ROOT / path
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text, encoding='utf-8')


def canonical_for(path):
    if path == 'index.html':
        return SITE + '/'
    if path.endswith('/index.html'):
        return SITE + '/' + path[:-10]
    return SITE + '/' + path


def enhance_common(path, desc):
    html = read(path)
    title_m = re.search(r'<title>(.*?)</title>', html, re.I | re.S)
    title = re.sub(r'\s+', ' ', title_m.group(1)).strip() if title_m else 'Danoishan Sinnathamby'
    canonical = canonical_for(path)
    desc_e = html_lib.escape(desc, quote=True)
    title_e = html_lib.escape(title, quote=True)
    canonical_e = html_lib.escape(canonical, quote=True)

    meta_desc = f'<meta name="description" content="{desc_e}">'
    if re.search(r'<meta\s+name=["\']description["\'][^>]*>', html, re.I):
        html = re.sub(r'<meta\s+name=["\']description["\'][^>]*>', meta_desc, html, count=1, flags=re.I)
    else:
        html = html.replace('</title>', '</title>' + meta_desc, 1)

    canonical_tag = f'<link rel="canonical" href="{canonical_e}">'
    if re.search(r'<link\s+rel=["\']canonical["\'][^>]*>', html, re.I):
        html = re.sub(r'<link\s+rel=["\']canonical["\'][^>]*>', canonical_tag, html, count=1, flags=re.I)
    else:
        html = html.replace('</title>', '</title>' + canonical_tag, 1)

    replacements = {
        'og:type': '<meta property="og:type" content="website">',
        'og:title': f'<meta property="og:title" content="{title_e}">',
        'og:description': f'<meta property="og:description" content="{desc_e}">',
        'og:url': f'<meta property="og:url" content="{canonical_e}">',
        'og:image': f'<meta property="og:image" content="{SITE}/social-card.png">',
    }
    for prop, tag in replacements.items():
        pat = rf'<meta\s+property=["\']{re.escape(prop)}["\'][^>]*>'
        if re.search(pat, html, re.I):
            html = re.sub(pat, tag, html, count=1, flags=re.I)
        else:
            html = html.replace('</head>', tag + '</head>', 1)

    twitter = {
        'twitter:card': '<meta name="twitter:card" content="summary_large_image">',
        'twitter:title': f'<meta name="twitter:title" content="{title_e}">',
        'twitter:description': f'<meta name="twitter:description" content="{desc_e}">',
        'twitter:image': f'<meta name="twitter:image" content="{SITE}/social-card.png">',
    }
    for name, tag in twitter.items():
        pat = rf'<meta\s+name=["\']{re.escape(name)}["\'][^>]*>'
        if re.search(pat, html, re.I):
            html = re.sub(pat, tag, html, count=1, flags=re.I)
        else:
            html = html.replace('</head>', tag + '</head>', 1)

    for link_tag, marker in [
        ('<link rel="icon" href="/favicon.svg" type="image/svg+xml">', 'rel="icon"'),
        ('<link rel="apple-touch-icon" href="/apple-touch-icon.png">', 'rel="apple-touch-icon"'),
    ]:
        if marker not in html:
            html = html.replace('</head>', link_tag + '</head>', 1)

    if '<a class="skip-link"' not in html:
        html = html.replace('<body>', '<body><a class="skip-link" href="#main-content">Skip to main content</a>', 1)
    if '<main id="main-content">' not in html:
        html = html.replace('<main>', '<main id="main-content">', 1)
    html = html.replace('<nav class="nav-links">', '<nav class="nav-links" aria-label="Primary navigation">')
    html = html.replace('href="Danoishan_Sinnathamby_Resume.pdf" download', 'href="Danoishan_Sinnathamby_Resume_2026.pdf" download="Danoishan_Sinnathamby_Resume.pdf"')
    html = html.replace('href="../Danoishan_Sinnathamby_Resume.pdf" download', 'href="../Danoishan_Sinnathamby_Resume_2026.pdf" download="Danoishan_Sinnathamby_Resume.pdf"')
    write(path, html)


DESCRIPTIONS = {
    'index.html': 'Technical project and program delivery across enterprise CRM, customer data, lifecycle marketing and MarTech, with case studies on diagnosis, operating at scale, technical handoffs and adoption.',
    'resume.html': 'Resume for Danoishan Sinnathamby: technical project and program delivery across CRM, lifecycle marketing, customer data, MarTech, product-oriented delivery and integrated digital programs.',
    'artifacts/index.html': 'Reusable technical delivery templates from Danoishan Sinnathamby: decision records, technical handoff briefs, launch readiness and end-to-end validation.',
    'work/80-percent-drop.html': 'An anonymized CRM and customer-data diagnostic case: tracing an apparent 80% submission decline across web forms, Salesforce, consent, identity, attribution and reporting.',
    'work/200m-messages.html': 'How Danoishan structures high-volume lifecycle delivery across 20+ concurrent workstreams and 200M+ annual communications using explicit handoffs, release controls and post-launch ownership.',
    'work/billing-journey.html': 'An anonymized enterprise billing case about making file-driven lifecycle failures observable across source systems, imports, journey logic, monitoring and recovery ownership.',
    'work/125-campaigns.html': 'An earlier-career program leadership case covering an eight-person team, six provinces, 125+ targeted campaigns and a repeatable operating model for national execution.',
    'lab/waypoint.html': 'A fictional lifecycle architecture lab showing technical reasoning across identity, data authority, SDK vs REST vs warehouse, real-time vs batch, scale, failure modes and rollout.',
    'notes/index.html': 'Short technical and operating notes from Danoishan Sinnathamby on delivery systems, architecture, APIs, identity, launch readiness, testing and decision-making.',
    'notes/schedule-vs-dependencies.html': 'Why dates are not enough: a practical note on dependency mapping, ownership and the conditions that make a technical delivery schedule achievable.',
    'notes/go-no-go.html': 'A practical note on making go/no-go an evidence review rather than a late discovery meeting.',
    'notes/decision-log.html': 'How to write decision records that preserve the choice, rationale, owner, assumptions and conditions for revisiting it.',
    'notes/raid-behavior.html': 'Why RAID only matters when risks, assumptions, issues and dependencies change sequencing, scope, ownership or stakeholder decisions.',
    'notes/sdk-vs-rest.html': 'A technical note on choosing SDK vs REST based on where the behavior originates, data authority, latency and ownership.',
    'notes/events-vs-attributes.html': 'A technical note on modeling moments as events and durable state as attributes in customer-data and lifecycle systems.',
    'notes/system-boundary.html': 'A troubleshooting note on tracing evidence across browser, web app, API, CRM and marketing-platform system boundaries.',
    'notes/design-exit-before-message.html': 'A lifecycle design note on defining the business event that makes a triggered message irrelevant before building the message itself.',
    'notes/api-docs-before-implementation.html': 'A technical delivery note on reading identity, rate limits, errors and data contracts early enough to influence architecture.',
    'notes/synthetic-test-users.html': 'A QA note on reusable synthetic users for testing identity, consent, lifecycle state and end-to-end customer outcomes.',
    'notes/200-ok-not-outcome.html': 'A troubleshooting note on why a successful API response proves transport acceptance, not identity, eligibility, journey behavior or the customer outcome.',
}

for path, desc in DESCRIPTIONS.items():
    if (ROOT / path).exists():
        enhance_common(path, desc)

index = read('index.html')
if '90-second brief' not in index:
    index = index.replace('<a class="button primary" href="#work">Selected work ↓</a>', '<a class="button primary" href="#work">Selected work ↓</a><a class="button" href="brief.html">90-second brief →</a>', 1)

fit_strip = '''<section class="fit-strip"><div class="wrap fit-strip-inner reveal"><span class="label">Best fit</span><div class="fit-roles"><strong>Technical Project / Program Management</strong><strong>Technical Account / Solutions</strong><strong>CRM / Customer Technology</strong></div><div class="fit-breadth"><span>Product roadmaps & prioritization</span><span>Brand, campaign & go-to-market support</span><span>Lifecycle & customer journey planning</span></div></div></section>'''
pattern = re.compile(r'<section class="section"><div class="wrap"><div class="section-head reveal"><p class="label">Best fit</p>.*?</section>\s*<section class="section" id="work">', re.S)
if pattern.search(index):
    index = pattern.sub(fit_strip + '\n<section class="section" id="work">', index, count=1)

meta_repls = {
    '<div class="work-meta"><span>Flagship diagnostic case</span><span>Web → Salesforce → customer data</span><span>Audit → handoffs → roadmap → validation</span></div>': '<div class="work-meta"><span><b>ROLE</b> Delivery lead</span><span><b>SCOPE</b> Web → Salesforce → customer data</span><span><b>OUTCOME</b> Recovery roadmap + proven validation path</span></div>',
    '<div class="work-meta"><span>20+ concurrent workstreams</span><span>200M+ annual sends</span><span>Launch → adoption → optimization</span></div>': '<div class="work-meta"><span><b>ROLE</b> Program delivery lead</span><span><b>SCALE</b> 20+ workstreams / 200M+ sends</span><span><b>OUTCOME</b> −30% late scope / −20% UAT-to-launch</span></div>',
    '<div class="work-meta"><span>Anonymized enterprise billing</span><span>ERP / file → Marketing Cloud → journey</span><span>Incident → controls → operational adoption</span></div>': '<div class="work-meta"><span><b>ROLE</b> Cross-system delivery lead</span><span><b>SCOPE</b> ERP / file → Marketing Cloud → journey</span><span><b>OUTCOME</b> Observable exceptions + recovery ownership</span></div>',
    '<div class="work-meta"><span>8-person team / 6 provinces</span><span>125+ campaigns</span><span>Repeat → learn → scale</span></div>': '<div class="work-meta"><span><b>ROLE</b> Team / program lead</span><span><b>SCALE</b> 8 people / 6 provinces / 125+ campaigns</span><span><b>OUTCOME</b> +10% retention / +15% acquisition</span></div>',
}
for old, new in meta_repls.items():
    index = index.replace(old, new)
write('index.html', index)

brief = '''<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="theme-color" content="#f3f0e8"><title>90-Second Brief — Danoishan Sinnathamby</title><link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500&family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet"><link rel="stylesheet" href="styles.css"></head><body><a class="skip-link" href="#main-content">Skip to main content</a><header class="site-header"><div class="wrap nav"><a class="wordmark" href="index.html">Danoishan Sinnathamby <span>/ brief</span></a><nav class="nav-links" aria-label="Primary navigation"><a href="index.html#work">Work</a><a href="lab/waypoint.html">Lab</a><a href="notes/index.html">Notes</a><a href="resume.html">Resume</a><a href="index.html#about">About</a></nav><a class="nav-cta" href="mailto:danoishan@gmail.com">email ↗</a></div></header><main id="main-content"><section class="case-hero brief-hero"><div class="wrap reveal"><a class="back-link" href="index.html">← portfolio</a><p class="eyebrow">Recruiter brief · ~90 seconds</p><h1>The shortest useful version.</h1><p class="case-dek">I lead technical project and program delivery where enterprise customers, CRM / customer data, cross-functional teams and production risk meet.</p><div class="hero-actions"><a class="button primary" href="Danoishan_Sinnathamby_Resume_2026.pdf" download="Danoishan_Sinnathamby_Resume.pdf">Download resume ↓</a><a class="button" href="mailto:danoishan@gmail.com">Email ↗</a><a class="button" href="https://www.linkedin.com/in/danoishan/" target="_blank" rel="noreferrer">LinkedIn ↗</a></div></div></section><section class="proof"><div class="wrap proof-grid"><div class="proof-item reveal"><strong>20+</strong><span>concurrent enterprise CRM / MarTech workstreams per quarter</span></div><div class="proof-item reveal"><strong>200M+</strong><span>annual SMS/MMS and email sends supported</span></div><div class="proof-item reveal"><strong>30% / 20%</strong><span>fewer late-stage scope changes / shorter UAT-to-launch</span></div></div></section><section class="section"><div class="wrap brief-grid"><article class="brief-card reveal"><p class="label">What I do</p><h2>I turn ambiguity into a delivery path.</h2><p>Business outcome → technical discovery → recommendation + trade-off → cross-functional handoffs → QA/UAT → launch → client adoption → optimization.</p></article><article class="brief-card reveal"><p class="label">Where I fit</p><h2>Technical delivery at the customer / platform boundary.</h2><p>Technical Project / Program Management · Technical Account / Solutions · CRM / Customer Technology.</p></article><article class="brief-card reveal"><p class="label">What I know how to reason about</p><h2>Systems, not just schedules.</h2><p>Identity, data authority, consent, APIs, SQL-based validation, real-time vs batch, failure behavior, release readiness, monitoring and operating ownership.</p></article><article class="brief-card reveal"><p class="label">How I work with specialists</p><h2>Own the outcome without pretending to own every implementation detail.</h2><p>I own problem framing, requirements, dependencies, decisions, handoffs, validation, client communication and rollout. Engineering / platform specialists own production implementation where appropriate.</p></article></div></section><section class="section"><div class="wrap"><div class="section-head reveal"><p class="label">Four proofs</p><div><h2>Open the signal you care about.</h2><p>The longer portfolio exists only if you want the evidence behind the headline.</p></div></div><div class="notes-grid"><article class="note-card reveal"><small>DIAGNOSIS</small><h3><a href="work/80-percent-drop.html">The 80% Drop</a></h3><p>Trace an apparent CRM collapse across browser, forms, Salesforce, consent, identity and attribution.</p></article><article class="note-card reveal"><small>ENTERPRISE SCALE</small><h3><a href="work/200m-messages.html">Making 200 Million Messages Boring</a></h3><p>Operating model, launch judgment, handoffs, UAT and post-launch ownership at high volume.</p></article><article class="note-card reveal"><small>CROSS-SYSTEM DELIVERY</small><h3><a href="work/billing-journey.html">The Bill That Couldn’t Go Missing</a></h3><p>Source data, file processing, imports, exceptions, recovery and observability.</p></article><article class="note-card reveal"><small>ARCHITECTURE JUDGMENT</small><h3><a href="lab/waypoint.html">Waypoint Lab</a></h3><p>Identity vs authority, SDK / REST / warehouse, real-time vs batch, scale and failure modes.</p></article></div></div></section></main><footer class="wrap footer"><span>© <span data-year></span> Danoishan Sinnathamby</span><span><a href="index.html">Portfolio</a> · <a href="resume.html">Resume</a> · <a href="mailto:danoishan@gmail.com">Email</a></span></footer><script src="script.js"></script></body></html>'''
write('brief.html', brief)
enhance_common('brief.html', 'A 90-second recruiter brief for Danoishan Sinnathamby: technical project/program delivery, enterprise CRM/MarTech scale, architecture judgment and selected evidence.')

visuals = {
    'work/80-percent-drop.html': '''<section class="case-visual visual-drop"><div class="wrap"><div class="visual-kicker"><span>SYSTEM TRACE</span><strong>The symptom appeared in reporting. The breakpoint lived upstream.</strong></div><div class="trace-track"><span>Browser</span><i>→</i><span>Website</span><i>→</i><span class="fault">Form boundary<b>BREAKPOINT</b></span><i>→</i><span>Salesforce</span><i>→</i><span>Consent / identity</span><i>→</i><span>Reporting</span></div></div></section>''',
    'work/200m-messages.html': '''<section class="case-visual visual-ops"><div class="wrap"><div class="visual-kicker"><span>OPERATING SYSTEM</span><strong>Standardize the controls, not every piece of work.</strong></div><div class="ops-flow"><div>Intake</div><div>Requirements</div><div>Data ready</div><div>Build</div><div>QA / UAT</div><div>Go / No-Go</div><div>Deploy</div><div>Optimize</div></div><div class="control-rail"><span>RAID</span><span>capacity</span><span>budget</span><span>change control</span><span>ownership</span><span>monitoring</span></div></div></section>''',
    'work/billing-journey.html': '''<section class="case-visual visual-billing"><div class="wrap"><div class="visual-kicker"><span>EXCEPTION PATH</span><strong>A reliable journey includes a visible way back when one row fails.</strong></div><div class="billing-flow"><div>Billing / ERP</div><i>→</i><div>File</div><i>→</i><div>Transfer</div><i>→</i><div class="fault">Import<b>FAILED ROW</b></div><i>→</i><div>Journey</div><i>→</i><div>Customer</div></div><div class="feedback-loop">↳ alert + failed-record detail → recovery owner → corrected resend → validation</div></div></section>''',
    'work/125-campaigns.html': '''<section class="case-visual visual-markets"><div class="wrap"><div class="visual-kicker"><span>PORTFOLIO RHYTHM</span><strong>One operating model. Six markets. Local execution.</strong></div><div class="market-row"><span>BC</span><span>AB</span><span>SK</span><span>MB</span><span>ON</span><span>QC</span></div><div class="market-rhythm"><b>Segment</b><i>→</i><b>Workback</b><i>→</i><b>Execute</b><i>→</i><b>Review</b><i>→</i><b>Improve next market</b></div></div></section>''',
}
for path, visual in visuals.items():
    h = read(path)
    if 'class="case-visual ' not in h:
        h = re.sub(r'(<section class="case-facts">.*?</section>)', r'\1' + visual, h, count=1, flags=re.S)
        write(path, h)

templates = {
    'decision-record.md': '''# Decision Record\n\n## Business outcome\nWhat must become true for the customer or operating team?\n\n## Decision required\nWhat specific choice are we making?\n\n## Constraints\n- Source of truth:\n- Identity:\n- Latency:\n- Scale:\n- Consent / compliance:\n- Timing / cost / operating effort:\n\n## Options considered\n1.\n2.\n3.\n\n## Recommendation\nState the path and why.\n\n## Trade-off accepted\nWhat do we lose, defer or make more complex?\n\n## Ownership\n- Decision owner:\n- Implementation owner:\n- Validation owner:\n\n## Revisit condition\nWhat new evidence would justify reopening the decision?\n''',
    'technical-handoff-brief.md': '''# Technical Handoff Brief\n\n## Customer / business behavior\nWhat should the user, customer or operating team experience?\n\n## Current evidence\nWhat is happening now? Include reproducible behavior, logs, counts or test evidence.\n\n## System boundary\nWhere does ownership or data move from one system/team to another?\n\n## Data contract\n- Source:\n- Identifier:\n- Event / attribute / file shape:\n- Timing / freshness:\n- Required fields:\n\n## Constraints\nLatency, scale, consent, environment access, dependencies and known limitations.\n\n## Acceptance criteria\n1.\n2.\n3.\n\n## Negative cases\nWhat must not happen? Include opt-out, duplicate, stale-data and failure scenarios.\n\n## Ownership\n- Implementation:\n- Decision:\n- QA / UAT:\n- Escalation:\n\n## Open decisions\nWhat is still genuinely unresolved?\n''',
    'launch-readiness-checklist.md': '''# Launch Readiness Checklist\n\n- [ ] Business objective and requirements accepted\n- [ ] Source data and identity behavior validated\n- [ ] Consent / suppression rules tested\n- [ ] Build and configuration complete\n- [ ] Positive and negative test cases passed\n- [ ] Client UAT / approval evidence captured\n- [ ] Release candidate / version frozen\n- [ ] Monitoring owner named\n- [ ] Rollback / stop path understood\n- [ ] Support and escalation path documented\n- [ ] Operational users briefed / enabled\n- [ ] Post-launch review point scheduled\n''',
    'end-to-end-validation-matrix.md': '''# End-to-End Validation Matrix\n\n| Layer | Question | Proof | Owner if it fails |\n|---|---|---|---|\n| Source | Did the business event become true? | Source record / event evidence | Source-system owner |\n| Transport / ingestion | Was the payload or file accepted? | Request, file or ingestion evidence | Integration / platform owner |\n| Identity | Did it attach to the intended customer? | Canonical ID / profile evidence | Identity owner |\n| Profile / data state | Are required fields/events present and current? | Profile / dataset validation | Data owner |\n| Eligibility | Does the customer qualify under business rules? | Segment / decision evidence | Journey / business-rule owner |\n| Orchestration | Did the workflow enter, branch and exit correctly? | Journey / automation evidence | Platform owner |\n| Customer outcome | Did the intended experience actually happen? | Rendered message / action / conversion | Delivery owner |\n| Exception path | If anything failed, did the right team know? | Alert / log / escalation evidence | Operations / support |\n''',
}
for name, content in templates.items():
    write('artifacts/templates/' + name, content)
write('artifacts/templates/technical-delivery-toolkit.md', '# Technical Delivery Toolkit\n\nFour reusable templates for decisions, technical handoffs, launch readiness and end-to-end validation.\n\n' + '\n---\n\n'.join(templates.values()))

art = read('artifacts/index.html')
if 'Download full toolkit' not in art:
    art = art.replace('<p class="case-dek">These are generic, reusable templates based on how I structure technical delivery. They contain no client data or proprietary implementation detail. The point is not the document itself. It is making the decision, ownership and proof explicit enough that another team can act on it.</p>', '<p class="case-dek">These are generic, reusable templates based on how I structure technical delivery. They contain no client data or proprietary implementation detail. The point is not the document itself. It is making the decision, ownership and proof explicit enough that another team can act on it.</p><div class="hero-actions"><a class="button primary" href="templates/technical-delivery-toolkit.md" download>Download full toolkit ↓</a><a class="button" href="https://github.com/danoishan/danoishan.github.io/tree/' + BRANCH + '/artifacts/templates" target="_blank" rel="noreferrer">View source on GitHub ↗</a></div>', 1)
controls = {
    'decision': ('decision-record.md', 'Decision Record'),
    'handoff': ('technical-handoff-brief.md', 'Technical Handoff Brief'),
    'launch': ('launch-readiness-checklist.md', 'Launch Readiness Checklist'),
    'validation': ('end-to-end-validation-matrix.md', 'End-to-End Validation Matrix'),
}
for sec_id, (filename, label) in controls.items():
    if f'data-copy-path="templates/{filename}"' in art:
        continue
    m = re.search(rf'(<section id="{sec_id}">)(.*?)(</section>)', art, re.S)
    if m:
        actions = f'<div class="artifact-actions"><button type="button" class="button copy-template" data-copy-path="templates/{filename}">Copy template</button><a class="button" href="templates/{filename}" download>Download Markdown ↓</a><a class="button" href="https://github.com/danoishan/danoishan.github.io/blob/{BRANCH}/artifacts/templates/{filename}" target="_blank" rel="noreferrer">GitHub source ↗</a></div>'
        replacement = m.group(1) + m.group(2) + actions + m.group(3)
        art = art[:m.start()] + replacement + art[m.end():]
write('artifacts/index.html', art)

note_related = {
    'notes/schedule-vs-dependencies.html': [('Related case', '../work/200m-messages.html', 'Making 200 Million Messages Boring'), ('Related artifact', '../artifacts/index.html#decision', 'Decision Record')],
    'notes/go-no-go.html': [('Related case', '../work/200m-messages.html#launch', 'Launch readiness at scale'), ('Related artifact', '../artifacts/index.html#launch', 'Launch Readiness Checklist')],
    'notes/decision-log.html': [('Related case', '../work/200m-messages.html#controls', 'Delivery controls'), ('Related artifact', '../artifacts/index.html#decision', 'Decision Record')],
    'notes/raid-behavior.html': [('Related case', '../work/200m-messages.html#controls', 'RAID as an active tool'), ('Related artifact', '../artifacts/index.html#decision', 'Decision Record')],
    'notes/sdk-vs-rest.html': [('Related lab', '../lab/waypoint.html#ingestion', 'Waypoint ingestion choices'), ('Related case', '../work/80-percent-drop.html', 'The 80% Drop')],
    'notes/events-vs-attributes.html': [('Related lab', '../lab/waypoint.html#ingestion', 'Waypoint data model'), ('Related artifact', '../artifacts/index.html#handoff', 'Technical Handoff Brief')],
    'notes/system-boundary.html': [('Related case', '../work/80-percent-drop.html#breakpoint', 'The breakpoint'), ('Related artifact', '../artifacts/index.html#validation', 'End-to-End Validation Matrix')],
    'notes/design-exit-before-message.html': [('Related lab', '../lab/waypoint.html#journey', 'Abandoned-search journey'), ('Related artifact', '../artifacts/index.html#validation', 'End-to-End Validation Matrix')],
    'notes/api-docs-before-implementation.html': [('Related lab', '../lab/waypoint.html#throughput', 'Throughput constraints'), ('Related artifact', '../artifacts/index.html#handoff', 'Technical Handoff Brief')],
    'notes/synthetic-test-users.html': [('Related lab', '../lab/waypoint.html#test', 'Waypoint test plan'), ('Related artifact', '../artifacts/index.html#validation', 'End-to-End Validation Matrix')],
    'notes/200-ok-not-outcome.html': [('Related case', '../work/80-percent-drop.html#validation', 'End-to-end proof'), ('Related artifact', '../artifacts/index.html#validation', 'End-to-End Validation Matrix')],
}
for path, links in note_related.items():
    if not (ROOT / path).exists():
        continue
    h = read(path)
    if 'SEP 2026 ·' not in h:
        h = re.sub(r'<p class="eyebrow">(.*?)</p>', r'<p class="eyebrow">SEP 2026 · \1</p>', h, count=1, flags=re.S)
    if 'class="related-links"' not in h:
        cards = ''.join(f'<a href="{href}"><small>{kind}</small><strong>{label}</strong></a>' for kind, href, label in links)
        related = f'<section class="related-links"><p class="label">Keep going</p><div>{cards}</div></section>'
        h = h.replace('</article>', related + '</article>', 1)
    write(path, h)

notes_idx = read('notes/index.html')
for fn in ['schedule-vs-dependencies','go-no-go','decision-log','raid-behavior','200-ok-not-outcome','sdk-vs-rest','events-vs-attributes','system-boundary','design-exit-before-message']:
    needle = f'<h3><a href="{fn}.html">'
    dated = f'<small class="note-date">SEP 2026</small>{needle}'
    if needle in notes_idx and dated not in notes_idx:
        notes_idx = notes_idx.replace(needle, dated, 1)
write('notes/index.html', notes_idx)

js = read('script.js')
js = re.sub(r'document\.querySelectorAll\(\'a\[href\$="Danoishan_Sinnathamby_Resume\.pdf"\]\'\).*?\n\}\);\n\n', '', js, flags=re.S)
js = re.sub(r'const bestFitLabel=.*?\n\}\n\nconst header=', 'const header=', js, flags=re.S)
if 'copy-template' not in js:
    js += '''\n\ndocument.querySelectorAll('.copy-template').forEach((button)=>{\n  button.addEventListener('click',async()=>{\n    const path=button.dataset.copyPath;\n    if(!path)return;\n    const original=button.textContent;\n    try{\n      const response=await fetch(path);\n      if(!response.ok)throw new Error('Template unavailable');\n      const text=await response.text();\n      await navigator.clipboard.writeText(text);\n      button.textContent='Copied ✓';\n    }catch{\n      button.textContent='Open Markdown to copy';\n    }\n    window.setTimeout(()=>{button.textContent=original;},1800);\n  });\n});\n'''
write('script.js', js)

css = read('styles.css')
append_css = r'''

/* review branch: recruiter speed, accessibility and richer proof */
.skip-link{position:fixed;left:12px;top:10px;z-index:200;transform:translateY(-160%);background:var(--ink);color:var(--paper);padding:10px 12px;font-family:var(--mono);font-size:11px;border:1px solid var(--ink)}
.skip-link:focus{transform:none}
a:focus-visible,button:focus-visible{outline:3px solid var(--accent);outline-offset:3px}
.work-meta b{display:block;font-size:9px;letter-spacing:.08em;color:var(--ink);margin-bottom:2px}
.fit-strip{border-bottom:1px solid var(--line);padding:22px 0}
.fit-strip-inner{display:grid;grid-template-columns:120px 1.4fr 1fr;gap:24px;align-items:center}
.fit-roles,.fit-breadth{display:flex;gap:16px;flex-wrap:wrap}
.fit-roles strong{font-size:13px}
.fit-breadth{font-family:var(--mono);font-size:9px;color:var(--muted)}
.case-visual{border-bottom:1px solid var(--line);padding:34px 0;background:var(--paper-2)}
.visual-kicker{display:flex;align-items:baseline;justify-content:space-between;gap:24px;margin-bottom:20px}
.visual-kicker span{font-family:var(--mono);font-size:9px;color:var(--accent);letter-spacing:.09em}
.visual-kicker strong{font-size:15px;letter-spacing:-.02em;text-align:right}
.trace-track,.billing-flow{display:flex;align-items:center;gap:8px;overflow-x:auto;padding-bottom:4px;font-family:var(--mono);font-size:10px}
.trace-track>span,.billing-flow>div{border:1px solid var(--ink);padding:12px 14px;background:var(--paper);white-space:nowrap;position:relative}
.trace-track i,.billing-flow i,.market-rhythm i{font-style:normal;color:var(--muted)}
.trace-track .fault,.billing-flow .fault{border-color:#d35232;background:#ffe6dd;color:#35150f}
.trace-track .fault b,.billing-flow .fault b{display:block;font-size:8px;color:#b33b23;margin-top:3px;letter-spacing:.08em}
.ops-flow{display:grid;grid-template-columns:repeat(8,1fr);border-top:1px solid var(--ink);border-left:1px solid var(--line)}
.ops-flow div{padding:14px 10px;border-right:1px solid var(--line);border-bottom:1px solid var(--line);font-family:var(--mono);font-size:9px;text-align:center;background:var(--paper)}
.control-rail{display:flex;justify-content:space-between;gap:8px;flex-wrap:wrap;border:1px solid var(--accent);border-top:0;padding:10px 12px;font-family:var(--mono);font-size:9px;color:var(--accent)}
.feedback-loop{margin-top:14px;border-left:3px solid var(--accent);padding:10px 14px;font-family:var(--mono);font-size:10px;color:var(--accent)}
.market-row{display:grid;grid-template-columns:repeat(6,1fr);gap:8px}
.market-row span{display:grid;place-items:center;aspect-ratio:2/1;border:1px solid var(--ink);font-family:var(--mono);font-weight:500;background:var(--paper)}
.market-rhythm{display:flex;align-items:center;justify-content:center;gap:12px;flex-wrap:wrap;margin-top:16px;font-family:var(--mono);font-size:10px;color:var(--muted)}
.market-rhythm b{color:var(--ink)}
.artifact-actions{display:flex;gap:8px;flex-wrap:wrap;margin:18px 0 0}
.copy-template{font-family:var(--sans);cursor:pointer;background:transparent;color:var(--ink)}
.note-date{display:block;font-family:var(--mono);font-size:9px;color:var(--accent);margin-top:26px;margin-bottom:-6px}
.related-links{border-top:1px solid var(--ink);padding-top:20px;margin-top:56px!important}
.related-links>div{display:grid;grid-template-columns:repeat(2,1fr);gap:12px;margin-top:14px}
.related-links a{border:1px solid var(--line);padding:14px;display:grid;gap:5px}
.related-links a:hover{border-color:var(--accent)}
.related-links small{font-family:var(--mono);font-size:9px;color:var(--accent);text-transform:uppercase}
.related-links strong{font-size:13px}
.brief-grid{display:grid;grid-template-columns:repeat(2,1fr);gap:16px}
.brief-card{border-top:2px solid var(--ink);padding-top:18px}
.brief-card h2{font-size:30px;line-height:1.05;letter-spacing:-.04em;margin:12px 0}
.brief-card p:last-child{color:var(--muted)}
:root[data-theme="dark"] .trace-track .fault,:root[data-theme="dark"] .billing-flow .fault{background:#3a201c;color:#f1d6d0;border-color:#d46e58}
:root[data-theme="dark"] .copy-template{color:var(--ink)}
@media(max-width:900px){
  .nav{height:auto;min-height:64px;flex-wrap:wrap;padding:10px 0;gap:10px 14px}
  .nav-links{display:flex!important;order:3;width:100%;overflow-x:auto;white-space:nowrap;gap:18px;padding:2px 0 8px;scrollbar-width:thin}
  .fit-strip-inner{grid-template-columns:1fr;gap:10px}
  .ops-flow{grid-template-columns:repeat(4,1fr)}
  .market-row{grid-template-columns:repeat(3,1fr)}
  .brief-grid{grid-template-columns:1fr}
}
@media(max-width:620px){
  .visual-kicker{display:block}.visual-kicker strong{display:block;text-align:left;margin-top:6px}
  .ops-flow{grid-template-columns:repeat(2,1fr)}
  .related-links>div{grid-template-columns:1fr}
}
'''
if 'review branch: recruiter speed' not in css:
    css += append_css
write('styles.css', css)

write('favicon.svg', '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><rect width="64" height="64" rx="10" fill="#2457ff"/><text x="32" y="39" text-anchor="middle" font-family="Arial, sans-serif" font-size="24" font-weight="700" fill="#f3f0e8">DS</text></svg>''')

from PIL import Image, ImageDraw, ImageFont

def font(path, size):
    try: return ImageFont.truetype(path, size)
    except: return ImageFont.load_default()

img = Image.new('RGB', (1200, 630), '#f3f0e8')
d = ImageDraw.Draw(img)
blue = '#2457ff'; ink = '#171a1f'; muted = '#686c73'
d.rectangle([70,70,90,560], fill=blue)
f_bold = font('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 58)
f_body = font('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 28)
f_mono = font('/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf', 18)
d.text((130,105), 'Danoishan Sinnathamby', font=f_bold, fill=ink)
d.text((132,188), 'Technical Project & Program Delivery', font=f_body, fill=blue)
d.text((132,246), 'CRM · Customer Data · MarTech · Technical Solutions', font=f_body, fill=muted)
d.line([132,330,1080,330], fill='#c9c5bb', width=2)
d.text((132,370), '20+ concurrent workstreams  ·  200M+ annual communications', font=f_body, fill=ink)
d.text((132,430), 'Business outcome → recommendation → trade-off → proof', font=f_body, fill=ink)
d.text((132,520), 'danoishan.github.io', font=f_mono, fill=muted)
img.save('social-card.png', optimize=True)

icon = Image.new('RGB', (180,180), blue)
di = ImageDraw.Draw(icon)
fi = font('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 66)
bbox = di.textbbox((0,0),'DS',font=fi)
di.text(((180-(bbox[2]-bbox[0]))/2,(180-(bbox[3]-bbox[1]))/2-4),'DS',font=fi,fill='#f3f0e8')
icon.save('apple-touch-icon.png', optimize=True)

for path, desc in DESCRIPTIONS.items():
    if (ROOT / path).exists():
        enhance_common(path, desc)
enhance_common('brief.html', 'A 90-second recruiter brief for Danoishan Sinnathamby: technical project/program delivery, enterprise CRM/MarTech scale, architecture judgment and selected evidence.')

sitemap = read('sitemap.xml')
brief_url = f'  <url><loc>{SITE}/brief.html</loc><lastmod>2026-09-01</lastmod><priority>0.9</priority></url>\n'
if f'{SITE}/brief.html' not in sitemap:
    sitemap = sitemap.replace(f'  <url><loc>{SITE}/resume.html', brief_url + f'  <url><loc>{SITE}/resume.html', 1)
write('sitemap.xml', sitemap)

for cleanup in ['scripts/apply_portfolio_review.py', '.github/workflows/apply-review-upgrades.yml', '.review-trigger']:
    p = ROOT / cleanup
    if p.exists():
        p.unlink()
