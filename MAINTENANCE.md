# Portfolio maintenance

## Before publishing

Run the three checks in the root README. Review both themes at 320, 390, 768, 1280 and 1440 px. Check that pages fit the viewport, keyboard focus stays visible, and the Work, About and case links land below the header. Confirm the résumé download and contact links. The automated link and contrast checks supplement the browser review.

The site fails open when JavaScript is unavailable. Core career content and recorded Waypoint results should remain reachable. Check the custom 404 page and preserve existing case and note URLs and section IDs when editing.

The PDF uses `resume.html` and its print styles as its source. Install Python Playwright and its Chromium browser, then run `python3 scripts/build_resume.py`. Use `--browser-executable` to select an installed Chromium instead. Render both pages after any edit. The second page should start with the complete EnsembleIQ role, and the contact and portfolio links should be active.

## Content and evidence

- Keep the official role title separate from the delivery function.
- Label real program patterns, anonymized composites, recommendations and fictional exercises.
- Before adding a percentage, record its definition, period, numerator / denominator, baseline and data source. Get approval for any client-derived public evidence.
- Describe shared results as team / program results. State personal ownership separately.
- Record the credential's earned date and retirement status. Training is not the same as certification. Do not imply a credential is active without verifying its record.
- Replace a fictional example with client evidence only when it can be published and accurately attributed.

## Waypoint

Change the policy deliberately. Update independent fixture expectations, run the tests, regenerate `results.json` with `run.mjs --write`, then run `--check`. Keep browser and Node execution on the same engine. Never add vendor credentials or real customer identifiers to browser code or fixtures.

## Deployment and recovery

The existing GitHub Pages process publishes the site. The quality workflow validates pull requests and main-branch changes with read-only repository permissions. Inspect both runs after a release. To recover a bad site update, revert its commit; avoid rewriting branch history.

For a new HTML page, include title, description, canonical and social metadata, direct base / override CSS links, skip link, semantic main and consistent navigation. Add its canonical URL to both sitemaps. Exclude redirects, the 404 page and verification files from the sitemap.

The homepage, flagship and requirements case have separate 1200 × 630 share images. When updating them, verify each live URL and its image with LinkedIn Post Inspector.
