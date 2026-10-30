// Minimal v2 2D example: paper grid, a bouncing circle character, a counter. Draw with C.g (CanvasRenderingContext2D).
export default async function (C) {
  const g = C.g, W = 720, H = 1280;
  const bg = () => { g.setTransform(1, 0, 0, 1, 0, 0); g.fillStyle = '#F2EFE8'; g.fillRect(0, 0, W, H); g.strokeStyle = 'rgba(14,14,12,.06)'; for (let x = 0; x <= W; x += 60) { g.beginPath(); g.moveTo(x, 0); g.lineTo(x, H); g.stroke(); } };
  return [
    { from: 0, to: 4.5, run: (t) => { bg(); const y = 640 - Math.abs(Math.sin(t * 4)) * 120; g.beginPath(); g.arc(360, y, 90, 0, 6.29); g.fillStyle = '#E8501C'; g.fill(); g.lineWidth = 6; g.strokeStyle = '#0E0E0C'; g.stroke();
        g.font = '900 64px Archivo'; g.fillStyle = '#0E0E0C'; g.textAlign = 'center'; g.fillText(Math.round(t * 1e5).toLocaleString('en-US'), 360, 360); } },
    { from: 4.5, to: 1e9, run: () => { bg(); C.hud = false; } },
  ];
}
