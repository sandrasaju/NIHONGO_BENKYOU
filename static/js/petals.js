function spawnPetals(count) {
  const container = document.getElementById('sakura');
  if (!container) return;
  const items = ['🌸','🌺','🍃','🌿','✿','🌾','🎋'];
  for (let i = 0; i < (count || 14); i++) {
    const p = document.createElement('div');
    p.className = 'petal';
    p.textContent = items[Math.floor(Math.random() * items.length)];
    p.style.left = Math.random() * 100 + 'vw';
    p.style.animationDuration = (10 + Math.random() * 14) + 's';
    p.style.animationDelay = (Math.random() * 10) + 's';
    p.style.fontSize = (0.75 + Math.random() * 0.6) + 'rem';
    container.appendChild(p);
  }
}
