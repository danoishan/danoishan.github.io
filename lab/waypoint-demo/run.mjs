import { readFile, writeFile } from 'node:fs/promises';
import { evaluateScenario } from './engine.mjs';
const fixtures = JSON.parse(await readFile(new URL('./fixtures.json', import.meta.url), 'utf8'));
const results = fixtures.map(({ id, title, input }) => ({ id, title, ...evaluateScenario(input) }));
if (process.argv.includes('--write')) {
  await writeFile(new URL('./results.json', import.meta.url), JSON.stringify(results, null, 2) + '\n');
} else if (process.argv.includes('--check')) {
  const recorded = JSON.parse(await readFile(new URL('./results.json', import.meta.url), 'utf8'));
  if (JSON.stringify(recorded) !== JSON.stringify(results)) throw new Error('Published results differ from the current engine. Run node lab/waypoint-demo/run.mjs --write.');
}
console.log(JSON.stringify({ scenarios: results.length, eligible: results.reduce((n, r) => n + r.decisions.filter(d => d.decision === 'eligible').length, 0), results }, null, 2));
