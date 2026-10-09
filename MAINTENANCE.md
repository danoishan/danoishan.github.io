# Portfolio maintenance

## Before publishing

Run the three checks in the root README. Review the changed pages in both themes, navigate using the keyboard and check a narrow viewport. Confirm the resume download and contact links. The automated link and contrast checks are focused checks, not an accessibility certification or a substitute for visual review.

The site fails open when JavaScript is unavailable. Core career content and recorded Waypoint results should remain reachable. Check the custom 404 page and preserve existing case and note URLs and section IDs when editing.

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
