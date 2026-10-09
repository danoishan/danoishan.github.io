import { evaluateScenario } from './engine.mjs';

const select = document.querySelector('#scenario');
const runButton = document.querySelector('#run-scenario');
const status = document.querySelector('#demo-status');
const description = document.querySelector('#scenario-description');
const summary = document.querySelector('#demo-summary');
const decisions = document.querySelector('#demo-decisions');
const input = document.querySelector('#demo-input');
const trace = document.querySelector('#demo-trace');
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
    const fixture = current(), result = evaluateScenario(fixture.input);
    decisions.textContent = JSON.stringify(result.decisions, null, 2);
    trace.textContent = JSON.stringify({ duplicates: result.duplicates, rejected: result.rejected, trace: result.trace }, null, 2);
    const counts = result.decisions.reduce((out, item) => { out[item.decision] = (out[item.decision] ?? 0) + 1; return out; }, {});
    summary.textContent = Object.entries(counts).map(([state, count]) => `${count} ${state}`).join(' · ') || 'No eligible search records were created.';
    summary.hidden = false;
    status.textContent = `${fixture.title}: evaluation complete. ${result.duplicates} duplicate events ignored; ${result.rejected.length} records rejected. No messages sent.`;
  } catch {
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
