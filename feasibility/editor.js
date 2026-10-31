const board = document.querySelector('#board');
const status = document.querySelector('#status');
let shapes = [];
function draw() {
  board.replaceChildren();
  shapes.forEach((shape, index) => {
    const el = document.createElement('div');
    el.className = `shape ${shape.type}`;
    el.style.left = `${shape.x}%`; el.style.top = `${shape.y}%`; el.style.width = `${shape.width}%`; el.style.height = `${shape.height}%`;
    el.contentEditable = 'true'; el.setAttribute('aria-label', `Edit shape ${index + 1} label; drag its border to move`); el.textContent = shape.label;
    el.addEventListener('input', () => { shape.label = el.textContent; });
    el.addEventListener('pointerdown', event => {
      if (event.target !== el || (event.offsetX < el.clientWidth - 12 && event.offsetY < el.clientHeight - 12 && event.offsetX > 8 && event.offsetY > 8)) return;
      if (event.offsetX >= el.clientWidth - 12 && event.offsetY >= el.clientHeight - 12) return;
      event.preventDefault(); el.setPointerCapture(event.pointerId);
      const startX = event.clientX, startY = event.clientY, x = shape.x, y = shape.y;
      const move = e => { shape.x = Math.max(0, Math.min(100, x + (e.clientX - startX) / board.clientWidth * 100)); shape.y = Math.max(0, Math.min(100, y + (e.clientY - startY) / board.clientHeight * 100)); el.style.left = `${shape.x}%`; el.style.top = `${shape.y}%`; };
      const up = () => { el.removeEventListener('pointermove', move); el.removeEventListener('pointerup', up); };
      el.addEventListener('pointermove', move); el.addEventListener('pointerup', up);
    });
    new ResizeObserver(() => { shape.width = Math.min(100, el.offsetWidth / board.clientWidth * 100); shape.height = Math.min(100, el.offsetHeight / board.clientHeight * 100); }).observe(el);
    board.append(el);
  });
}
document.querySelector('#file').addEventListener('change', async e => { try { const value = JSON.parse(await e.target.files[0].text()); if (!Array.isArray(value.shapes) || value.shapes.some(s => !['rectangle','ellipse','diamond','arrow'].includes(s.type) || typeof s.label !== 'string' || !['x','y','width','height'].every(k => typeof s[k] === 'number' && Number.isFinite(s[k]) && s[k] >= 0 && s[k] <= 100))) throw Error('Invalid shape data'); shapes = value.shapes; draw(); status.textContent = `Loaded ${shapes.length} shapes. Drag a border, resize the corner, or edit a label.`; } catch (error) { status.textContent = `Could not load diagram: ${error.message}`; } });
document.querySelector('#save').addEventListener('click', () => { const url = URL.createObjectURL(new Blob([JSON.stringify({shapes}, null, 2)], {type:'application/json'})); const a = document.createElement('a'); a.href = url; a.download = 'edited-diagram.json'; a.click(); setTimeout(() => URL.revokeObjectURL(url), 1000); });
