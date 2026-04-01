(function () {

  // ── Sakura flower SVG — 5 rounded petals, gradient, stamens ──
  function makeSakura(size) {
    var s = size;
    return '<svg viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">'
      + '<defs>'
      + '<radialGradient id="pg" cx="50%" cy="50%" r="55%">'
      + '<stop offset="0%" stop-color="#f9a8c0"/>'
      + '<stop offset="60%" stop-color="#f472a0"/>'
      + '<stop offset="100%" stop-color="#e8608a"/>'
      + '</radialGradient>'
      + '<radialGradient id="pg2" cx="50%" cy="50%" r="50%">'
      + '<stop offset="0%" stop-color="#ffd0e0"/>'
      + '<stop offset="100%" stop-color="#f472a0"/>'
      + '</radialGradient>'
      + '</defs>'
      // 5 petals rotated 72° apart — each petal is an ellipse
      + [0,72,144,216,288].map(function(a){
          return '<ellipse cx="50" cy="22" rx="14" ry="20" fill="url(#pg2)" opacity="0.92" transform="rotate('+a+',50,50)"/>';
        }).join('')
      // Petal highlight overlay
      + [0,72,144,216,288].map(function(a){
          return '<ellipse cx="50" cy="20" rx="7" ry="10" fill="rgba(255,240,248,0.35)" transform="rotate('+a+',50,50)"/>';
        }).join('')
      // Center circle
      + '<circle cx="50" cy="50" r="10" fill="#e8507a"/>'
      + '<circle cx="50" cy="50" r="7" fill="#f06090"/>'
      // Stamens — small lines radiating from center
      + [0,45,90,135,180,225,270,315].map(function(a){
          var rad = a * Math.PI / 180;
          var x2 = 50 + Math.cos(rad) * 12;
          var y2 = 50 + Math.sin(rad) * 12;
          return '<line x1="50" y1="50" x2="'+x2+'" y2="'+y2+'" stroke="#c03060" stroke-width="0.8" stroke-linecap="round"/>'
               + '<circle cx="'+x2+'" cy="'+y2+'" r="1.2" fill="#d04070"/>';
        }).join('')
      + '</svg>';
  }

  // ── Autumn leaf SVGs ──
  var LEAF_SVGS = [
    // Narrow elongated
    '<svg viewBox="0 0 40 80" xmlns="http://www.w3.org/2000/svg"><path d="M20 4 Q30 20 28 50 Q20 68 20 76 Q20 68 12 50 Q10 20 20 4Z" fill="#e85d04" stroke="#2c0a00" stroke-width="1.5"/><line x1="20" y1="8" x2="20" y2="72" stroke="#2c0a00" stroke-width="1"/><line x1="20" y1="25" x2="14" y2="35" stroke="#2c0a00" stroke-width="0.8"/><line x1="20" y1="25" x2="26" y2="35" stroke="#2c0a00" stroke-width="0.8"/><line x1="20" y1="40" x2="14" y2="50" stroke="#2c0a00" stroke-width="0.8"/><line x1="20" y1="40" x2="26" y2="50" stroke="#2c0a00" stroke-width="0.8"/><path d="M20 72 Q19 77 17 80" stroke="#2c0a00" stroke-width="1.2" fill="none"/></svg>',
    // Maple star
    '<svg viewBox="0 0 60 65" xmlns="http://www.w3.org/2000/svg"><path d="M30 2 L36 14 L48 8 L40 20 L56 22 L44 28 L52 40 L38 34 L34 50 L30 58 L26 50 L22 34 L8 40 L16 28 L4 22 L20 20 L12 8 L24 14 Z" fill="#e85d04" stroke="#2c0a00" stroke-width="1.5"/><line x1="30" y1="10" x2="30" y2="56" stroke="#2c0a00" stroke-width="1"/><line x1="30" y1="28" x2="18" y2="36" stroke="#2c0a00" stroke-width="0.8"/><line x1="30" y1="28" x2="42" y2="36" stroke="#2c0a00" stroke-width="0.8"/><path d="M30 56 Q28 61 26 65" stroke="#2c0a00" stroke-width="1.2" fill="none"/></svg>',
    // Birch oval
    '<svg viewBox="0 0 50 70" xmlns="http://www.w3.org/2000/svg"><path d="M25 5 Q38 8 42 25 Q44 40 38 55 Q32 65 25 68 Q18 65 12 55 Q6 40 8 25 Q12 8 25 5Z" fill="#f48c06" stroke="#2c0a00" stroke-width="1.5"/><line x1="25" y1="8" x2="25" y2="65" stroke="#2c0a00" stroke-width="1"/><line x1="25" y1="22" x2="14" y2="30" stroke="#2c0a00" stroke-width="0.8"/><line x1="25" y1="22" x2="36" y2="30" stroke="#2c0a00" stroke-width="0.8"/><line x1="25" y1="38" x2="14" y2="46" stroke="#2c0a00" stroke-width="0.8"/><line x1="25" y1="38" x2="36" y2="46" stroke="#2c0a00" stroke-width="0.8"/><path d="M25 65 Q24 70 22 74" stroke="#2c0a00" stroke-width="1.2" fill="none"/></svg>',
    // Oak lobed
    '<svg viewBox="0 0 65 70" xmlns="http://www.w3.org/2000/svg"><path d="M32 4 Q40 4 44 10 Q50 8 52 14 Q58 14 58 22 Q62 26 58 32 Q60 38 54 40 Q52 48 44 48 Q40 56 32 60 Q24 56 20 48 Q12 48 10 40 Q4 38 6 32 Q2 26 6 22 Q6 14 12 14 Q14 8 20 10 Q24 4 32 4Z" fill="#dc2f02" stroke="#2c0a00" stroke-width="1.5"/><line x1="32" y1="8" x2="32" y2="58" stroke="#2c0a00" stroke-width="1"/><line x1="32" y1="24" x2="18" y2="32" stroke="#2c0a00" stroke-width="0.8"/><line x1="32" y1="24" x2="46" y2="32" stroke="#2c0a00" stroke-width="0.8"/><path d="M32 58 Q30 63 28 68" stroke="#2c0a00" stroke-width="1.2" fill="none"/></svg>',
    // Round serrated
    '<svg viewBox="0 0 55 65" xmlns="http://www.w3.org/2000/svg"><path d="M27 5 Q38 4 44 12 Q50 20 50 32 Q50 44 42 52 Q34 60 27 62 Q20 60 12 52 Q4 44 4 32 Q4 20 10 12 Q16 4 27 5Z" fill="#faa307" stroke="#2c0a00" stroke-width="1.5"/><line x1="27" y1="8" x2="27" y2="60" stroke="#2c0a00" stroke-width="1"/><line x1="27" y1="22" x2="14" y2="32" stroke="#2c0a00" stroke-width="0.8"/><line x1="27" y1="22" x2="40" y2="32" stroke="#2c0a00" stroke-width="0.8"/><line x1="27" y1="38" x2="16" y2="46" stroke="#2c0a00" stroke-width="0.8"/><line x1="27" y1="38" x2="38" y2="46" stroke="#2c0a00" stroke-width="0.8"/><path d="M27 60 Q26 65 24 68" stroke="#2c0a00" stroke-width="1.2" fill="none"/></svg>',
    // Large maple
    '<svg viewBox="0 0 70 75" xmlns="http://www.w3.org/2000/svg"><path d="M35 3 L42 16 L56 10 L48 24 L64 26 L52 34 L60 48 L44 42 L40 58 L35 68 L30 58 L26 42 L10 48 L18 34 L6 26 L22 24 L14 10 L28 16 Z" fill="#e85d04" stroke="#2c0a00" stroke-width="1.8"/><line x1="35" y1="12" x2="35" y2="64" stroke="#2c0a00" stroke-width="1.2"/><line x1="35" y1="30" x2="20" y2="40" stroke="#2c0a00" stroke-width="0.9"/><line x1="35" y1="30" x2="50" y2="40" stroke="#2c0a00" stroke-width="0.9"/><path d="M35 64 Q33 70 30 74" stroke="#2c0a00" stroke-width="1.4" fill="none"/></svg>',
  ];

  // ── Snowflake SVG ──
  function makeSnowflakeSVG(size) {
    var cx = size / 2, r = size * 0.44;
    var svg = '<svg viewBox="0 0 '+size+' '+size+'" xmlns="http://www.w3.org/2000/svg"><g transform="translate('+cx+','+cx+')">';
    [0,60,120,180,240,300].forEach(function(a) {
      svg += '<g transform="rotate('+a+')">'
        + '<line x1="0" y1="0" x2="0" y2="-'+r+'" stroke="rgba(210,230,255,0.92)" stroke-width="'+(size*0.07)+'" stroke-linecap="round"/>'
        + '<line x1="0" y1="-'+(r*0.58)+'" x2="-'+(r*0.24)+'" y2="-'+(r*0.40)+'" stroke="rgba(210,230,255,0.88)" stroke-width="'+(size*0.055)+'" stroke-linecap="round"/>'
        + '<line x1="0" y1="-'+(r*0.58)+'" x2="'+(r*0.24)+'" y2="-'+(r*0.40)+'" stroke="rgba(210,230,255,0.88)" stroke-width="'+(size*0.055)+'" stroke-linecap="round"/>'
        + '<line x1="0" y1="-'+(r*0.32)+'" x2="-'+(r*0.15)+'" y2="-'+(r*0.20)+'" stroke="rgba(225,240,255,0.82)" stroke-width="'+(size*0.045)+'" stroke-linecap="round"/>'
        + '<line x1="0" y1="-'+(r*0.32)+'" x2="'+(r*0.15)+'" y2="-'+(r*0.20)+'" stroke="rgba(225,240,255,0.82)" stroke-width="'+(size*0.045)+'" stroke-linecap="round"/>'
        + '</g>';
    });
    svg += '<circle cx="0" cy="0" r="'+(size*0.09)+'" fill="rgba(240,248,255,0.98)"/>'
      + '</g></svg>';
    return svg;
  }

  var SNOW_SIZES = [12, 16, 20, 10, 24, 14, 18];
  var DRIFTS = ['', 'drift-a', 'drift-b'];

  var LIGHT = [
    // Sakura flowers
    {type:'sakura', size:18, count:5},
    {type:'sakura', size:14, count:5},
    {type:'sakura', size:22, count:4},
    {type:'sakura', size:16, count:4},
    // Autumn leaves
    {type:'leaf', idx:0, count:3},
    {type:'leaf', idx:1, count:3},
    {type:'leaf', idx:2, count:3},
    {type:'leaf', idx:3, count:2},
    {type:'leaf', idx:4, count:3},
    {type:'leaf', idx:5, count:2},
  ];

  var DARK = [{type:'snow', count:42}];

  function build(container, types) {
    container.innerHTML = '';
    var isDark = document.documentElement.getAttribute('data-theme') === 'dark';

    types.forEach(function(t) {
      for (var i = 0; i < t.count; i++) {
        var el = document.createElement('div');
        var drift = DRIFTS[Math.floor(Math.random() * DRIFTS.length)];

        if (t.type === 'sakura') {
          el.className = ('particle sakura-svg ' + drift).trim();
          el.style.width  = t.size + 'px';
          el.style.height = t.size + 'px';
          el.innerHTML = makeSakura(t.size);

        } else if (t.type === 'leaf') {
          var sz = 18 + Math.floor(Math.random() * 16);
          el.className = ('particle leaf-svg ' + drift).trim();
          el.style.width  = sz + 'px';
          el.style.height = sz + 'px';
          el.innerHTML = LEAF_SVGS[t.idx];
          el.querySelector('svg').style.cssText = 'width:100%;height:100%;display:block;';

        } else { // snow
          var ssz = SNOW_SIZES[Math.floor(Math.random() * SNOW_SIZES.length)];
          el.className = ('particle snow-svg ' + drift).trim();
          el.style.width  = ssz + 'px';
          el.style.height = ssz + 'px';
          el.innerHTML = makeSnowflakeSVG(ssz);
        }

        el.style.left = (Math.random() * 105) + 'vw';
        // Light mode faster: 4–9s, dark mode: 7–14s
        var minDur = isDark ? 7  : 4;
        var rngDur = isDark ? 7  : 5;
        el.style.animationDuration = (minDur + Math.random() * rngDur) + 's';
        el.style.animationDelay    = (Math.random() * 10) + 's';
        el.style.opacity           = (0.65 + Math.random() * 0.35).toString();
        container.appendChild(el);
      }
    });
  }

  function refresh() {
    var c = document.getElementById('particles');
    if (!c) return;
    var dark = document.documentElement.getAttribute('data-theme') === 'dark';
    build(c, dark ? DARK : LIGHT);
  }

  document.addEventListener('DOMContentLoaded', refresh);
  window.refreshParticles = refresh;
})();
