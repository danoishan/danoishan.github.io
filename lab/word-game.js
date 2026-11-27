(() => {
  const answer = 'BRIEF';
  const form = document.getElementById('word-form');
  const field = document.getElementById('guess');
  const status = document.getElementById('game-status');
  const list = document.getElementById('guesses');
  const reset = document.getElementById('reset-game');
  let tries = 0;
  form.addEventListener('submit', (event) => {
    event.preventDefault();
    const guess = field.value.trim().toUpperCase();
    if (!/^[A-Z]{5}$/.test(guess) || tries >= 6 || field.disabled) return;
    tries += 1;
    const remaining = [...answer];
    const feedback = Array(5).fill('not in the word');
    [...guess].forEach((letter, i) => { if (letter === answer[i]) { feedback[i] = 'correct position'; remaining[i] = null; } });
    [...guess].forEach((letter, i) => { if (feedback[i] !== 'not in the word') return; const j = remaining.indexOf(letter); if (j !== -1) { feedback[i] = 'different position'; remaining[j] = null; } });
    const item = document.createElement('li');
    item.setAttribute('aria-label', [...guess].map((letter, i) => `${letter}: ${feedback[i]}`).join('; '));
    [...guess].forEach((letter, i) => {
      const tile = document.createElement('span');
      tile.className = 'word-tile ' + (feedback[i] === 'correct position' ? 'correct' : feedback[i] === 'different position' ? 'present' : 'absent');
      tile.setAttribute('aria-hidden', 'true');
      tile.textContent = letter;
      item.append(tile);
    });
    list.append(item);
    if (guess === answer) { status.textContent = `You got it in ${tries} ${tries === 1 ? 'try' : 'tries'}!`; field.disabled = true; }
    else if (tries === 6) { status.textContent = `Good game! The word was ${answer}.`; field.disabled = true; }
    else { status.textContent = `${6 - tries} ${6 - tries === 1 ? 'try' : 'tries'} left.`; field.value = ''; field.focus(); }
  });
  reset.addEventListener('click', () => { tries = 0; field.disabled = false; field.value = ''; list.replaceChildren(); status.textContent = 'New game ready.'; field.focus(); });
})();
