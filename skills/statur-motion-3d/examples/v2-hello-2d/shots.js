// Minimal v2 2D example: plain paper, a bouncing circle character, one label. Draw with C.g (CanvasRenderingContext2D).
// Colors and fonts come from the brand tokens through C.brand (docs/BRAND-TOKENS.md), never from constants.
export default async function (C) {
  const g = C.g, W = 720, H = 1280, { paper, ink, accent } = C.brand.colors;
  const bg = () => { g.setTransform(1, 0, 0, 1, 0, 0); g.fillStyle = paper; g.fillRect(0, 0, W, H); };
  return [
    { from: 0, to: 4.5, run: (t) => { bg(); const y = 640 - Math.abs(Math.sin(t * 4)) * 120; g.beginPath(); g.arc(360, y, 90, 0, 6.29); g.fillStyle = accent; g.fill(); g.lineWidth = 6; g.strokeStyle = ink; g.stroke();
        g.font = `700 64px ${C.brand.fonts.display}`; g.fillStyle = ink; g.textAlign = 'center'; g.fillText('hello', 360, 360); } },
    { from: 4.5, to: 1e9, run: () => { bg(); C.hud = false; } },
  ];
}
