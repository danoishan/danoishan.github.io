import { evaluateScenario } from './engine.mjs';

const select = document.querySelector('#scenario');
const runButton = document.querySelector('#run-scenario');
const status = document.querySelector('#demo-status');
const description = document.querySelector('#scenario-description');
const summary = document.querySelector('#demo-summary');
const decisions = document.querySelector('#demo-decisions');
const input = document.querySelector('#demo-input');
const trace = document.querySelector('#demo-trace');
const explanations = {
  eligible_abandoned_search: 'Eligible. The delay has passed, the search is still fresh, and the customer has email consent and no matching booking.',
  unresolved_identity: 'Suppressed. The search could not be tied to an identified customer.',
  matched_booking: 'Suppressed. The customer already booked from this search.',
  stale_search: 'Expired. The search is more than 24 hours old.',
  no_email_consent: 'Suppressed. The customer has no current email consent.',
  delay_not_elapsed: 'Waiting. The two-hour reminder delay has yet to pass.',
};
let fixtures = [];
const current = () => fixtures.find(item => item.id === select.value);
function showInput() {
  const fixture = current();
  description.textContent = fixture.description;
  input.textContent = JSON.stringify(fixture.input, null, 2);
  summary.hidden = true;
  decisions.textContent = 'Run this scenario to evaluate the policy.';
  trace.textContent = '';
  status.textContent = 'Scenario ready. Evaluation time: ' + fixture.input.now;
}
runButton.addEventListener('click', () => {
  try {
    const fixture = current();
    const result = evaluateScenario(fixture.input);
    decisions.textContent = JSON.stringify(result.decisions, null, 2);
    trace.textContent = JSON.stringify({ duplicates: result.duplicates, rejected: result.rejected, trace: result.trace }, null, 2);
    summary.replaceChildren();
    for (const item of result.decisions) {
      const explanation = document.createElement('p');
      const label = result.decisions.length > 1 ? `${item.customerId} / ${item.searchId}. ` : '';
      explanation.textContent = label + explanations[item.reason];
      summary.append(explanation);
    }
    if (!result.decisions.length) summary.textContent = 'There was no valid search to evaluate.';
    summary.hidden = false;
    status.textContent = `${fixture.title}: evaluation complete. ${result.duplicates} duplicate events ignored; ${result.rejected.length} records rejected. No messages sent.`;
  } catch {
    summary.hidden = true;
    status.textContent = 'This scenario could not be evaluated. The source and recorded results are available below.';
  }
});
select.addEventListener('change', showInput);
try {
  const response = await fetch(new URL('./fixtures.json', import.meta.url));
  if (!response.ok) throw new Error('Fixtures unavailable');
  fixtures = await response.json();
  if (!Array.isArray(fixtures) || !fixtures.length) throw new Error('No scenarios');
  select.replaceChildren(...fixtures.map(fixture => {
    const option = document.createElement('option');
    option.value = fixture.id; option.textContent = fixture.title; return option;
  }));
  select.disabled = false; runButton.disabled = false;
  showInput();
} catch {
  status.textContent = 'The exercise could not load. Open the recorded results or source below.';
}
