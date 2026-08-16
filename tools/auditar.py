#!/usr/bin/env python3
"""
auditar.py — auditoría medida del sitio: desborde, contraste AA y básicos a11y.

VERDE EN VACÍO: cada página publica su denominador (elementos de texto
escaneados, imágenes revisadas). Una página con 0 elementos escaneados FALLA:
un verde sin denominador tendría cara de auditado.

Qué mide, por página × ancho:
  · desborde horizontal (scrollWidth vs innerWidth) — falla si hay
  · contraste WCAG de cada nodo de texto visible contra el fondo REALMENTE
    pintado (ascendiendo ancestros hasta el primer fondo opaco); AA: 4.5
    normal, 3.0 grande (≥24px o ≥18.7px bold). Fondos con imagen se marcan
    como NO MEDIBLES y se listan — el denominador se publica.
  · básicos: img sin alt, botones/enlaces sin nombre accesible, saltos de
    encabezado, iframes sin title, lang en <html>.

Uso: python tools/auditar.py --base http://localhost:8000 --paths / work/x/ ...
     [--widths 320,768,1440] [--json out.json]
"""
import argparse
import json
import subprocess
import sys
import tempfile
import time
import urllib.request

import websocket

EDGE = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
PORT = 9343

JS_AUDIT = r"""
(() => {
  const out = { scanned: 0, imgs: 0, violations: [], unmeasured: 0,
                flags: [], overflow: 0 };
  const de = document.documentElement;
  if (de.scrollWidth > window.innerWidth)
    out.overflow = de.scrollWidth - window.innerWidth;

  function lum(r,g,b){
    const f = c => { c/=255; return c<=0.04045 ? c/12.92 : Math.pow((c+0.055)/1.055,2.4); };
    return 0.2126*f(r)+0.7152*f(g)+0.0722*f(b);
  }
  function parse(c){
    const m = c.match(/rgba?\(([\d.]+),\s*([\d.]+),\s*([\d.]+)(?:,\s*([\d.]+))?\)/);
    return m ? [ +m[1], +m[2], +m[3], m[4]===undefined?1:+m[4] ] : null;
  }
  function ratio(a,b){
    const l1 = lum(...a.slice(0,3)), l2 = lum(...b.slice(0,3));
    const [hi,lo] = l1>l2 ? [l1,l2] : [l2,l1];
    return (hi+0.05)/(lo+0.05);
  }
  function bgOf(el){
    let n = el;
    while (n && n !== document) {
      const cs = getComputedStyle(n);
      if (cs.backgroundImage !== 'none') return 'image';
      const c = parse(cs.backgroundColor);
      if (c && c[3] >= 0.99) return c;
      n = n.parentElement;
    }
    return [255,255,255,1];
  }
  const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT, {
    acceptNode: t => t.textContent.trim().length > 1 &&
      t.parentElement && !['SCRIPT','STYLE','NOSCRIPT','IFRAME'].includes(t.parentElement.tagName)
      ? NodeFilter.FILTER_ACCEPT : NodeFilter.FILTER_REJECT });
  const seen = new Set();
  while (walker.nextNode()) {
    const el = walker.currentNode.parentElement;
    if (seen.has(el)) continue; seen.add(el);
    const cs = getComputedStyle(el);
    if (cs.visibility === 'hidden' || cs.display === 'none') continue;
    const r = el.getBoundingClientRect();
    if (r.width === 0 || r.height === 0) continue;
    out.scanned++;
    const fg = parse(cs.color); if (!fg) continue;
    const bg = bgOf(el);
    if (bg === 'image') { out.unmeasured++; continue; }
    const size = parseFloat(cs.fontSize);
    const bold = parseInt(cs.fontWeight, 10) >= 700;
    const need = (size >= 24 || (size >= 18.66 && bold)) ? 3.0 : 4.5;
    const rr = ratio(fg, bg);
    if (rr < need) {
      const id = el.tagName.toLowerCase() +
        (el.className && typeof el.className === 'string' ? '.'+el.className.split(' ')[0] : '');
      out.violations.push({ el: id, ratio: Math.round(rr*100)/100, need,
        text: el.textContent.trim().slice(0,40) });
    }
  }
  document.querySelectorAll('img').forEach(i => { out.imgs++;
    if (!i.hasAttribute('alt')) out.flags.push('img sin alt: '+(i.src||'').split('/').pop()); });
  document.querySelectorAll('button, a').forEach(b => {
    const name = (b.textContent.trim() || b.getAttribute('aria-label') || '').trim();
    if (!name && !b.querySelector('img[alt]'))
      out.flags.push(b.tagName.toLowerCase()+' sin nombre accesible: '+(b.className||'?'));
  });
  document.querySelectorAll('iframe').forEach(f => {
    if (!f.getAttribute('title')) out.flags.push('iframe sin title: '+f.src); });
  let last = 0;
  document.querySelectorAll('h1,h2,h3,h4,h5,h6').forEach(h => {
    const n = +h.tagName[1];
    if (last && n > last + 1) out.flags.push('salto de encabezado: h'+last+' -> h'+n+' ('+h.textContent.trim().slice(0,30)+')');
    last = n;
  });
  if (!document.documentElement.getAttribute('lang')) out.flags.push('html sin lang');
  const dups = {};
  out.violations = out.violations.filter(v => {
    const k = v.el + '|' + v.ratio;
    dups[k] = (dups[k]||0)+1; return dups[k] === 1; });
  return out;
})()
"""


def die(msg):
    print(f"⛔ auditar.py: {msg}", file=sys.stderr)
    sys.exit(1)


class CDP:
    def __init__(self, ws_url):
        self.ws = websocket.create_connection(ws_url, timeout=90)
        self.mid = 0

    def cmd(self, method, **params):
        self.mid += 1
        self.ws.send(json.dumps({"id": self.mid, "method": method, "params": params}))
        while True:
            m = json.loads(self.ws.recv())
            if m.get("id") == self.mid:
                if "error" in m:
                    die(f"CDP {method}: {m['error']}")
                return m.get("result", {})

    def js(self, expr):
        r = self.cmd("Runtime.evaluate", expression=expr, returnByValue=True)
        return r.get("result", {}).get("value")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--base", required=True)
    ap.add_argument("--paths", nargs="+", required=True)
    ap.add_argument("--widths", default="320,768,1440")
    ap.add_argument("--json", default=None)
    a = ap.parse_args()
    widths = [int(w) for w in a.widths.split(",")]

    prof = tempfile.mkdtemp(prefix="audit-")
    proc = subprocess.Popen([EDGE, f"--remote-debugging-port={PORT}",
        "--remote-allow-origins=*", f"--user-data-dir={prof}", "--headless=new",
        "--window-size=1440,900", "--mute-audio", "--hide-scrollbars", "about:blank"],
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    informe = {}
    problemas = 0
    try:
        ws_url = None
        for _ in range(50):
            try:
                tabs = json.loads(urllib.request.urlopen(
                    f"http://127.0.0.1:{PORT}/json", timeout=2).read())
                pages = [t for t in tabs if t.get("type") == "page"]
                if pages:
                    ws_url = pages[0]["webSocketDebuggerUrl"]
                    break
            except Exception:
                pass
            time.sleep(0.3)
        if not ws_url:
            die("Edge no expuso pestaña CDP")
        c = CDP(ws_url)
        c.cmd("Page.enable")
        c.cmd("Runtime.enable")

        for path in a.paths:
            url = a.base.rstrip("/") + "/" + path.lstrip("/")
            informe[path] = {}
            for w in widths:
                c.cmd("Emulation.setDeviceMetricsOverride", width=w,
                      height=900, deviceScaleFactor=1, mobile=(w < 700))
                c.cmd("Page.navigate", url=url)
                time.sleep(2.5)
                r = c.js(JS_AUDIT)
                if not r or r.get("scanned", 0) == 0:
                    die(f"{path} @{w}: CERO elementos escaneados — verde en vacío")
                informe[path][w] = r
                n_bad = (1 if r["overflow"] else 0) + len(r["violations"]) + len(r["flags"])
                problemas += n_bad
                estado = "OK" if n_bad == 0 else f"{n_bad} hallazgos"
                print(f"{path} @{w:>4}: {estado} · escaneados {r['scanned']} "
                      f"· no-medibles {r['unmeasured']} · imgs {r['imgs']}"
                      + (f" · DESBORDE {r['overflow']}px" if r["overflow"] else ""))
                for v in r["violations"][:6]:
                    print(f"    contraste {v['ratio']} < {v['need']}: <{v['el']}> «{v['text']}»")
                for f in r["flags"][:6]:
                    print(f"    {f}")
    finally:
        proc.kill()
    if a.json:
        with open(a.json, "w", encoding="utf-8") as f:
            json.dump(informe, f, indent=1)
    print(f"\nTOTAL hallazgos: {problemas}")
    sys.exit(0 if problemas == 0 else 2)


if __name__ == "__main__":
    main()
