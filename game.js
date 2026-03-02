// game.js — Scout Jeopardy! Game Engine

let teams = [], currentTeam = 0, currentRound = 0, used = [], currentCell = null;

function resetUsed() {
  const numCols = ROUNDS[currentRound].cats.length;
  used = Array.from({ length: numCols }, () => Array(5).fill(false));
}

function startGame() {
  const names = [
    document.getElementById('t1').value.trim() || 'Team 1',
    document.getElementById('t2').value.trim() || 'Team 2',
    document.getElementById('t3').value.trim(),
  ].filter(Boolean);
  teams = names.map(n => ({ name: n, score: 0 }));
  document.getElementById('setup-screen').style.display = 'none';
  currentRound = 0;
  resetUsed();
  renderAll();
}

function renderAll() {
  renderLabel();
  renderScoreboard();
  renderBoard();
  updateTurn();
}

function renderLabel() {
  document.getElementById('round-label').textContent = ROUNDS[currentRound].label;
}

function renderScoreboard() {
  document.getElementById('scoreboard').innerHTML = teams.map((t, i) => `
    <div class="team-score ${i === currentTeam ? 'active-team' : ''}">
      <div class="team-name">${t.name}</div>
      <div class="team-points ${t.score < 0 ? 'negative' : ''}">${t.score}</div>
    </div>`).join('');
}

function updateTurn() {
  document.getElementById('turn-indicator').textContent =
    `🎯 ${teams[currentTeam].name}'s turn to pick`;
}

function renderBoard() {
  const R = ROUNDS[currentRound];
  const numCols = R.cats.length;
  const vals = [100, 200, 300, 400, 500].map(v => v * R.mult);
  const board = document.getElementById('board');
  board.innerHTML = '';
  board.style.setProperty('--cols', numCols);

  R.cats.forEach(c => {
    const h = document.createElement('div');
    h.className = 'category-header';
    h.textContent = `${c.emoji} ${c.name}`;
    board.appendChild(h);
  });

  for (let ri = 0; ri < 5; ri++) {
    for (let ci = 0; ci < numCols; ci++) {
      const cell = document.createElement('div');
      const isUsed = used[ci][ri];
      const isDD = R.qs[ci][ri].dd;
      cell.className = 'cell' + (isUsed ? ' used' : '') + (isDD ? ' daily-double' : '');
      cell.textContent = isUsed ? '' : `$${vals[ri]}`;
      if (!isUsed) cell.addEventListener('click', () => openQ(ci, ri));
      board.appendChild(cell);
    }
  }
}

function openQ(col, row) {
  currentCell = { col, row };
  if (ROUNDS[currentRound].qs[col][row].dd) {
    const s = document.getElementById('dd-splash');
    s.classList.add('open');
    setTimeout(() => { s.classList.remove('open'); showModal(col, row); }, 2200);
  } else {
    showModal(col, row);
  }
}

function showModal(col, row) {
  const R = ROUNDS[currentRound];
  const q = R.qs[col][row];
  const pts = [100, 200, 300, 400, 500][row] * R.mult;
  document.getElementById('modal-cat').textContent = `${R.cats[col].emoji} ${R.cats[col].name}`;
  document.getElementById('modal-pts').textContent = `$${pts}`;
  document.getElementById('modal-q').textContent = q.q;
  document.getElementById('modal-a').textContent = `✅ ${q.a}`;
  document.getElementById('modal-a').classList.remove('visible');
  document.getElementById('modal-btns').innerHTML =
    `<button class="btn btn-reveal" onclick="revealAnswer()">Reveal Answer</button>`;
  document.getElementById('modal-overlay').classList.add('open');
}

function revealAnswer() {
  document.getElementById('modal-a').classList.add('visible');
  const pts = [100, 200, 300, 400, 500][currentCell.row] * ROUNDS[currentRound].mult;
  document.getElementById('modal-btns').innerHTML =
    teams.map((t, i) =>
      `<button class="btn btn-correct" onclick="score(${i},${pts})">✓ ${t.name}</button>`
    ).join('') +
    `<button class="btn btn-wrong" onclick="score(-1,${pts})">✗ No one</button>`;
}

function score(teamIdx, pts) {
  if (teamIdx >= 0) teams[teamIdx].score += pts;
  used[currentCell.col][currentCell.row] = true;
  currentTeam = teamIdx >= 0 ? teamIdx : (currentTeam + 1) % teams.length;
  document.getElementById('modal-overlay').classList.remove('open');
  renderScoreboard();
  renderBoard();
  updateTurn();
  if (used.every(col => col.every(c => c))) {
    currentRound < ROUNDS.length - 1 ? showTransition() : showWin();
  }
}

function showTransition() {
  document.getElementById('rt-title').textContent = `Round ${currentRound + 1} Complete!`;
  const next = ROUNDS[currentRound + 1];
  document.getElementById('rt-next-name').textContent = `Up Next: ${next.label}`;
  const sorted = [...teams].sort((a, b) => b.score - a.score);
  document.getElementById('rt-scores').innerHTML = sorted.map((t, i) =>
    `<div class="rt-row">
      <span>${['🥇','🥈','🥉'][i] || ''} ${t.name}</span>
      <span class="rt-pts">$${t.score}</span>
    </div>`
  ).join('');
  document.getElementById('btn-next-round').onclick = startNext;
  document.getElementById('round-transition').classList.add('open');
}

function startNext() {
  currentRound++;
  resetUsed();
  document.getElementById('round-transition').classList.remove('open');
  renderAll();
}

function showWin() {
  const sorted = [...teams].sort((a, b) => b.score - a.score);
  document.getElementById('winner-name').textContent =
    sorted[0].score > 0 ? `🏆 ${sorted[0].name} Wins!` : 'Amazing game, Scouts!';
  document.getElementById('final-scores').innerHTML = sorted.map((t, i) =>
    `<div class="fs-row">
      <span>${['🥇','🥈','🥉'][i] || ''} ${t.name}</span>
      <span style="color:var(--gold);font-weight:800">$${t.score}</span>
    </div>`
  ).join('');
  document.getElementById('win-screen').classList.add('open');
}
