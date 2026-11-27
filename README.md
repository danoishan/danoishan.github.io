# Danoishan Sinnathamby

[Live portfolio](https://danoishan.github.io/) · [Recruiter brief](https://danoishan.github.io/brief.html) · [Resume](https://danoishan.github.io/resume.html)

I lead technical project and program delivery across CRM, loyalty and customer data at Vigorate.

## Selected work

| Project | Delivery decision |
| --- | --- |
| [Enterprise delivery](https://danoishan.github.io/work/200m-messages.html) | How requirements, teams, testing and release decisions come together across customer communications programs |
| [Three-brand CRM cleanup](https://danoishan.github.io/work/contact-cleanup.html) | Which records could be removed, how each brand could validate the population and when an automated run should stop |
| [SAP cutover](https://danoishan.github.io/work/sap-cutover.html) | Which of 20+ journeys to pause and what IT had to confirm before the restart |
| [Billing communications](https://danoishan.github.io/work/billing-journey.html) | How to trace a rejected record, restore missing reports and detect when one of eight journeys goes quiet |
| [AI-assisted delivery review](https://danoishan.github.io/work/ai-delivery-workflows.html) | How I use AI and specialist review to surface requirements and QA questions |

[Run Waypoint](https://danoishan.github.io/lab/waypoint-demo.html) to test a fictional travel reminder against booking, identity and consent events. The [source and tests](lab/waypoint-demo/) run against 19 synthetic scenarios. [Delivery examples](artifacts/) show project decisions and a downloadable SAP cutover snapshot.

## Local development

Serve the static site with Python.

```sh
python3 -m http.server 8000
```

Open `http://localhost:8000`. Run the checks with Python 3 and Node.js 20 or newer.

```sh
python3 scripts/check_site.py
node --test lab/waypoint-demo/test.mjs
node lab/waypoint-demo/run.mjs --check
```

GitHub Pages publishes the site. See the [maintenance guide](MAINTENANCE.md) for resume generation, link checks and release verification.

## Reuse

The [license](LICENSE.md) covers original site code, generic templates and fictional Waypoint examples. Personal resume content, career case prose, portfolio imagery and third-party resources are excluded.
