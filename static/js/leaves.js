function spawnLeaves(count) {
  const container = document.getElementById('leaves');
  if (!container) return;

  const colorClasses  = ['leaf-1','leaf-2','leaf-3','leaf-4','leaf-5','leaf-6','leaf-7','leaf-8'];
  const sizeClasses   = ['leaf-sm','leaf-sm','leaf-md','leaf-md','leaf-md','leaf-lg','leaf-xl'];
  const shapeClasses  = ['','leaf-round','leaf-maple','leaf-long','leaf-wide'];
  const driftClasses  = ['leaf-drift-a','leaf-drift-b','leaf-drift-c',''];

  const total = count || 28;

  for (let i = 0; i < total; i++) {
    const leaf = document.createElement('div');
    leaf.className = [
      'leaf',
      colorClasses[Math.floor(Math.random() * colorClasses.length)],
      sizeClasses[Math.floor(Math.random() * sizeClasses.length)],
      shapeClasses[Math.floor(Math.random() * shapeClasses.length)],
      driftClasses[Math.floor(Math.random() * driftClasses.length)],
    ].join(' ').trim();

    leaf.style.left            = (Math.random() * 105) + 'vw';
    leaf.style.animationDuration  = (8 + Math.random() * 14) + 's';
    leaf.style.animationDelay     = (Math.random() * 16) + 's';
    leaf.style.opacity            = (0.5 + Math.random() * 0.5).toString();

    container.appendChild(leaf);
  }
}
