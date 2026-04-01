// Injects a simple cute anime face into .auth-mascot elements
document.addEventListener('DOMContentLoaded', function () {
  const svgHTML = `
  <svg viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg"
       style="width:80px;height:80px;border-radius:50%;border:3px solid rgba(255,255,255,0.9);
              box-shadow:0 4px 16px rgba(0,0,0,0.12);background:linear-gradient(135deg,#fde8d0,#ffd5dc);">
    <!-- Hair -->
    <ellipse cx="50" cy="44" rx="32" ry="36" fill="#2c1810"/>
    <!-- Face -->
    <ellipse cx="50" cy="50" rx="24" ry="26" fill="#fde8d0"/>
    <!-- Bangs -->
    <path d="M26 36 Q28 18 50 16 Q72 18 74 36 Q66 26 50 24 Q34 26 26 36Z" fill="#2c1810"/>
    <!-- Eyes — big, friendly -->
    <ellipse cx="40" cy="50" rx="7" ry="8" fill="#fff"/>
    <ellipse cx="60" cy="50" rx="7" ry="8" fill="#fff"/>
    <ellipse cx="40" cy="51" rx="4.5" ry="5.5" fill="#4a80c0"/>
    <ellipse cx="60" cy="51" rx="4.5" ry="5.5" fill="#4a80c0"/>
    <ellipse cx="40" cy="51" rx="3" ry="4" fill="#1a2e50"/>
    <ellipse cx="60" cy="51" rx="3" ry="4" fill="#1a2e50"/>
    <ellipse cx="42" cy="48" rx="1.5" ry="2" fill="white"/>
    <ellipse cx="62" cy="48" rx="1.5" ry="2" fill="white"/>
    <!-- Blush -->
    <ellipse cx="30" cy="60" rx="6" ry="3.5" fill="rgba(255,130,130,0.38)"/>
    <ellipse cx="70" cy="60" rx="6" ry="3.5" fill="rgba(255,130,130,0.38)"/>
    <!-- Big happy smile -->
    <path d="M38 66 Q50 76 62 66" stroke="#c06060" stroke-width="2.2" fill="none" stroke-linecap="round"/>
    <!-- Kimono collar peek -->
    <path d="M26 76 Q50 70 74 76 L74 100 L26 100Z" fill="#e8607a"/>
    <path d="M40 76 Q50 72 60 76 L57 100 L43 100Z" fill="#f5f0e8"/>
    <!-- Hair ribbon -->
    <path d="M68 30 Q74 22 80 28 Q74 32 70 30 Q74 36 68 36 Q70 30 68 30Z" fill="#f4a0b8"/>
  </svg>`;

  document.querySelectorAll('.auth-mascot').forEach(el => {
    el.innerHTML = svgHTML;
  });
});
