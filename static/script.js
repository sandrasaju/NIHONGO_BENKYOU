let answered = false;

async function loadQuestion() {
  answered = false;
  const res = await fetch('/api/question');
  const data = await res.json();

  if (data.done) {
    window.location.href = '/result';
    return;
  }

  document.getElementById('word').textContent = data.word;
  document.getElementById('reading').textContent = data.reading;
  document.getElementById('counter').textContent = `Question ${data.current} / ${data.total}`;
  document.getElementById('progress').style.width = `${(data.current - 1) / data.total * 100}%`;
  document.getElementById('feedback').textContent = '';
  document.getElementById('feedback').className = 'feedback';
  document.getElementById('next-btn').style.display = 'none';

  const optionsEl = document.getElementById('options');
  optionsEl.innerHTML = '';
  data.options.forEach(opt => {
    const btn = document.createElement('button');
    btn.className = 'option-btn';
    btn.textContent = opt;
    btn.onclick = () => submitAnswer(opt);
    optionsEl.appendChild(btn);
  });
}

async function submitAnswer(answer) {
  if (answered) return;
  answered = true;

  const res = await fetch('/api/answer', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ answer })
  });
  const data = await res.json();

  const feedback = document.getElementById('feedback');
  const buttons = document.querySelectorAll('.option-btn');

  buttons.forEach(btn => {
    btn.disabled = true;
    if (btn.textContent === data.correct_answer) btn.classList.add('correct');
    else if (btn.textContent === answer && !data.correct) btn.classList.add('wrong');
  });

  if (data.correct) {
    feedback.textContent = '✓ Correct!';
    feedback.className = 'feedback correct';
  } else {
    feedback.textContent = `✗ The answer was: ${data.correct_answer}`;
    feedback.className = 'feedback wrong';
  }

  document.getElementById('next-btn').style.display = 'inline-block';
}

function nextQuestion() {
  loadQuestion();
}
