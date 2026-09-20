#!/usr/bin/env python3
"""
verificar_formulario.py — el formulario de contacto, medido EN SUS ESTADOS DE ERROR.

Por qué existe: ninguna puerta del sitio ve estos estados. auditar.py mide la
página en reposo, y en reposo el formulario no tiene un solo error pintado —
no existen hasta que alguien envía mal. Así se publicó durante semanas un aviso
que decía «the direct send didn't go through» cuando lo único que pasaba era
que el correo estaba mal escrito (2026-09-20).

VERDE EN VACÍO: publica su denominador (avisos disparados, campos marcados,
correos probados) y FALLA si contó cero. Un verde sin denominador tendría cara
de verificado.

Qué mide, por ancho:
  · La regex de correo del cliente y la del servidor son la MISMA cadena. Si
    se separan, el cliente acepta lo que el servidor rechaza y el visitante ve
    una caída que no ocurrió — el fallo original, exactamente.
  · Cada aviso de campo: contraste AA (4.5) contra el fondo REALMENTE pintado,
    texto ≥12px, y que lleva forma además de color (WCAG 1.4.1: quien no
    distingue el rojo tiene que ver igual que algo falla).
  · Cada campo marcado: aria-invalid="true" Y aria-describedby apuntando a SU
    aviso visible. El ojo y el lector de pantalla, o los dos o ninguno.
  · El borde del campo marcado: 3:1 contra el fondo pintado (WCAG 1.4.11).
  · El resumen al pie: contraste, forma, y que nombra tantos campos como
    avisos hay encendidos — un resumen que se desfase miente.
  · Que ningún aviso se sale de su columna, y que la página no desborda.
  · Coherencia de las reglas finas con la regex compartida: ningún correo
    puede ser bueno para una y malo para la otra.

Uso: python tools/verificar_formulario.py --base http://localhost:8899
     [--widths 320,768,1440]
"""
import argparse
import json
import pathlib
import re
import subprocess
import sys
import tempfile
import time
import urllib.request

import websocket

EDGE = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
PORT = 9344
RAIZ = pathlib.Path(__file__).resolve().parent.parent

# Correos que la puerta prueba en los DOS lados. Los de arriba tienen que
# pasar (son direcciones de agencia reales en forma), los de abajo caer.
BATERIA_BUENOS = [
    "carlos@agency.com",
    "c.marruffo+leads@sub.agency.co.uk",
    "hello@agency.io",
    "carlos_m@my-agency.com.pe",
    "a@b.co",
]
BATERIA_MALOS = [
    "safsdfasdf",          # el de la captura de Carlos, 2026-09-20
    "carlos.agency.com",
    "carlos@@agency.com",
    "@agency.com",
    "carlos@",
    "carlos@agency",
    "carlos@agency.c",
    "carlos@agency.",
    "carlos @agency.com",
    "",
]

JS = r"""
(async () => {
  const out = { avisos: [], campos: [], resumen: null, desborde: 0,
                correos: [], problemas: [] };
  const form = document.getElementById("form-contacto");
  if (!form) { out.problemas.push("no hay formulario en la pagina"); return out; }
  const st = form.querySelector(".form-status");
  const val = (n, v) => { const e = form.querySelector('[name="'+n+'"]'); if (e) e.value = v; };

  function lum(r,g,b){ const f=c=>{c/=255; return c<=0.04045?c/12.92:Math.pow((c+0.055)/1.055,2.4);};
    return 0.2126*f(r)+0.7152*f(g)+0.0722*f(b); }
  function parse(c){ const m=c.match(/rgba?\(([\d.]+),\s*([\d.]+),\s*([\d.]+)(?:,\s*([\d.]+))?\)/);
    return m?[+m[1],+m[2],+m[3],m[4]===undefined?1:+m[4]]:null; }
  function ratio(a,b){ const l1=lum(...a.slice(0,3)), l2=lum(...b.slice(0,3));
    const [hi,lo]=l1>l2?[l1,l2]:[l2,l1]; return Math.round(((hi+0.05)/(lo+0.05))*100)/100; }
  // el fondo REALMENTE pintado, subiendo hasta el primer opaco
  function bgOf(el){ let n=el;
    while(n && n!==document){ const cs=getComputedStyle(n);
      if (cs.backgroundImage !== 'none') return 'image';
      const c=parse(cs.backgroundColor); if (c && c[3]===1) return c; n=n.parentElement; }
    return [255,255,255]; }

  // 1. Disparar TODOS los errores a la vez: el peor caso visual.
  form.reset();
  val("phone", "sadfsf");   // el unico opcional que se valida, tambien tiene que saltar
  form.requestSubmit();
  await new Promise(r => setTimeout(r, 250));

  const de = document.documentElement;
  if (de.scrollWidth > window.innerWidth) out.desborde = de.scrollWidth - window.innerWidth;

  form.querySelectorAll('.campo-error:not([hidden])').forEach(a => {
    const cs = getComputedStyle(a);
    const fondo = bgOf(a);
    const campo = a.parentElement.querySelector('input, textarea');
    const columna = a.closest('label').getBoundingClientRect();
    const caja = a.getBoundingClientRect();
    out.avisos.push({
      id: a.id,
      texto: a.textContent.trim().slice(0, 80),
      px: Math.round(parseFloat(cs.fontSize) * 100) / 100,
      ratio: fondo === 'image' ? null : ratio(parse(cs.color), fondo),
      fondoImagen: fondo === 'image',
      tieneForma: !!a.querySelector('svg'),
      seSale: Math.round(Math.max(0, caja.right - columna.right, columna.left - caja.left)),
      campo: campo ? campo.name : null,
      ariaInvalid: campo ? campo.getAttribute('aria-invalid') : null,
      descrito: campo ? (campo.getAttribute('aria-describedby') || '').split(/\s+/).indexOf(a.id) >= 0 : false
    });
  });

  form.querySelectorAll('[aria-invalid="true"]').forEach(c => {
    const cs = getComputedStyle(c);
    const fondoSeccion = bgOf(c.parentElement);
    const aviso = document.getElementById('err-' + c.name);
    out.campos.push({
      name: c.name,
      bordeRatio: fondoSeccion === 'image' ? null : ratio(parse(cs.borderTopColor), fondoSeccion),
      textoRatio: ratio(parse(cs.color), parse(cs.backgroundColor)),
      avisoVisible: !!(aviso && !aviso.hidden)
    });
  });

  if (st) {
    const cs = getComputedStyle(st);
    const fondo = bgOf(st);
    out.resumen = {
      estado: st.dataset.estado || null,
      texto: st.textContent.trim(),
      px: Math.round(parseFloat(cs.fontSize) * 100) / 100,
      ratio: fondo === 'image' ? null : ratio(parse(cs.color), fondo),
      tieneForma: !!st.querySelector('svg')
    };
  }

  // 2. Las reglas finas contra la regex compartida: ningun correo puede ser
  //    bueno para una y malo para la otra.
  const REGEX = window.__REGEX_SERVIDOR;
  const campo = form.querySelector('[name="email"]');
  const aviso = document.getElementById('err-email');
  for (const dir of window.__CORREOS) {
    form.reset();
    ["name","company","message"].forEach(n => val(n, "x"));
    val("email", dir);
    campo.dispatchEvent(new Event("blur"));
    await new Promise(r => setTimeout(r, 30));
    out.correos.push({
      dir: dir,
      reglas: aviso.hidden ? "acepta" : "rechaza",
      regex: REGEX.test(dir) ? "acepta" : "rechaza",
      motivo: aviso.hidden ? null : aviso.textContent.trim().slice(0, 70)
    });
  }
  form.reset();
  return out;
})()
"""


def die(msg):
    print(f"⛔ verificar_formulario.py: {msg}", file=sys.stderr)
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

    def js(self, expr, espera=True):
        r = self.cmd("Runtime.evaluate", expression=expr, returnByValue=True,
                     awaitPromise=espera)
        return r.get("result", {}).get("value")


def regex_de_los_dos_lados():
    """La regex del cliente y la del servidor, sacadas del código fuente.

    Se comparan como CADENA: la lección del 2026-09-20 es que basta con que
    una de las dos cambie para que el visitante vea una caída inventada.
    """
    cli = (RAIZ / "site/assets/js/apparatus.js").read_text(encoding="utf-8")
    srv = (RAIZ / "site/api/contact.js").read_text(encoding="utf-8")
    m_cli = re.search(r"var CORREO = (/.+?/);", cli)
    m_srv = re.search(r"if \(!(/.+?/)\.test\(d\.email\)\)", srv)
    if not m_cli:
        die("no encuentro la regex de correo en apparatus.js (var CORREO = /…/;)")
    if not m_srv:
        die("no encuentro la regex de correo en api/contact.js (…test(d.email))")
    return m_cli.group(1), m_srv.group(1)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--base", required=True)
    ap.add_argument("--widths", default="320,768,1440")
    a = ap.parse_args()
    widths = [int(w) for w in a.widths.split(",")]

    problemas = []
    cli, srv = regex_de_los_dos_lados()
    print(f"regex del cliente : {cli}")
    print(f"regex del servidor: {srv}")
    if cli != srv:
        problemas.append("la regex de correo del cliente y la del servidor NO son la misma: "
                         f"{cli} vs {srv}")
        print("  ⛔ NO COINCIDEN")
    else:
        print("  coinciden — el cliente no puede dar por bueno lo que el servidor rechaza")
    print()

    correos = BATERIA_BUENOS + BATERIA_MALOS
    prof = tempfile.mkdtemp(prefix="form-")
    proc = subprocess.Popen([EDGE, f"--remote-debugging-port={PORT}",
        "--remote-allow-origins=*", f"--user-data-dir={prof}", "--headless=new",
        "--window-size=1440,900", "--mute-audio", "--hide-scrollbars", "about:blank"],
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    total_avisos = total_campos = total_correos = 0
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

        for w in widths:
            c.cmd("Emulation.setDeviceMetricsOverride", width=w, height=900,
                  deviceScaleFactor=1, mobile=(w < 700))
            c.cmd("Page.navigate", url=a.base.rstrip("/") + "/")
            time.sleep(2.2)
            c.js(f"window.__CORREOS = {json.dumps(correos)}; "
                 f"window.__REGEX_SERVIDOR = {srv};", espera=False)
            r = c.js(JS)
            if not r:
                die(f"@{w}: la sonda no devolvió nada")
            for p in r["problemas"]:
                problemas.append(f"@{w}: {p}")

            fallos_ancho = []
            if r["desborde"]:
                fallos_ancho.append(f"la página desborda {r['desborde']}px con los errores puestos")
            for av in r["avisos"]:
                q = f"aviso {av['id']}"
                if av["fondoImagen"]:
                    fallos_ancho.append(f"{q}: sobre imagen, NO MEDIBLE")
                elif av["ratio"] < 4.5:
                    fallos_ancho.append(f"{q}: contraste {av['ratio']} < 4.5")
                if av["px"] < 12:
                    fallos_ancho.append(f"{q}: texto a {av['px']}px, por debajo de 12")
                if not av["tieneForma"]:
                    fallos_ancho.append(f"{q}: solo color, sin forma (WCAG 1.4.1)")
                if av["seSale"]:
                    fallos_ancho.append(f"{q}: se sale {av['seSale']}px de su columna")
                if av["ariaInvalid"] != "true":
                    fallos_ancho.append(f"{q}: visible pero su campo no tiene aria-invalid")
                if not av["descrito"]:
                    fallos_ancho.append(f"{q}: su campo no lo referencia con aria-describedby")
            for cp in r["campos"]:
                if cp["bordeRatio"] is not None and cp["bordeRatio"] < 3:
                    fallos_ancho.append(f"campo {cp['name']}: borde a {cp['bordeRatio']} < 3 (1.4.11)")
                if cp["textoRatio"] < 4.5:
                    fallos_ancho.append(f"campo {cp['name']}: lo escrito a {cp['textoRatio']} < 4.5")
                if not cp["avisoVisible"]:
                    fallos_ancho.append(f"campo {cp['name']}: marcado en rojo sin aviso que lo explique")
            res = r["resumen"]
            if not res or res["estado"] != "error":
                fallos_ancho.append("el resumen al pie no quedó en estado de error")
            else:
                if res["ratio"] is not None and res["ratio"] < 4.5:
                    fallos_ancho.append(f"resumen: contraste {res['ratio']} < 4.5")
                if not res["tieneForma"]:
                    fallos_ancho.append("resumen: solo color, sin forma (WCAG 1.4.1)")
                if len(r["avisos"]) and "Not sent yet" not in res["texto"]:
                    fallos_ancho.append("resumen: no dice que no se envió")

            for co in r["correos"]:
                if co["reglas"] != co["regex"]:
                    fallos_ancho.append(
                        f"correo «{co['dir']}»: las reglas lo {co['reglas']}n y la regex lo "
                        f"{co['regex']}. Uno de los dos miente")
                if co["dir"] in BATERIA_BUENOS and co["reglas"] != "acepta":
                    fallos_ancho.append(f"correo legítimo «{co['dir']}» RECHAZADO: {co['motivo']}")
                if co["dir"] in BATERIA_MALOS and co["reglas"] != "rechaza":
                    fallos_ancho.append(f"correo inválido «{co['dir']}» ACEPTADO")
                if co["reglas"] == "rechaza" and not co["motivo"]:
                    fallos_ancho.append(f"correo «{co['dir']}» rechazado SIN motivo escrito")

            total_avisos += len(r["avisos"])
            total_campos += len(r["campos"])
            total_correos += len(r["correos"])
            estado = "OK" if not fallos_ancho else f"{len(fallos_ancho)} hallazgos"
            peor = min([av["ratio"] for av in r["avisos"] if av["ratio"] is not None] or [0])
            print(f"@{w:>4}: {estado} · {len(r['avisos'])} aviso(s) encendido(s) · "
                  f"{len(r['campos'])} campo(s) marcado(s) · {len(r['correos'])} correo(s) probado(s) "
                  f"· peor contraste {peor}")
            for f in fallos_ancho:
                print(f"    {f}")
            problemas += [f"@{w}: {f}" for f in fallos_ancho]
    finally:
        proc.kill()

    # VERDE EN VACÍO: sin denominador no hay verde.
    print()
    print(f"verificar_formulario.py: {total_avisos} aviso(s), {total_campos} campo(s) marcado(s) "
          f"y {total_correos} correo(s) medidos en {len(widths)} ancho(s)")
    if total_avisos == 0 or total_campos == 0 or total_correos == 0:
        die("CERO elementos medidos — verde en vacío. Los errores no se dispararon.")
    if problemas:
        print(f"⛔ {len(problemas)} hallazgo(s)")
        sys.exit(2)
    print("el formulario dice qué falla, dónde falla y por qué, y se mide al decirlo.")
    sys.exit(0)


if __name__ == "__main__":
    main()
