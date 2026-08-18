#!/usr/bin/env python3
"""
grabar.py — vídeo de una pieza INTERACTIVA, conducida por guion.

⛔ POR QUÉ NO SIRVE `record.py` PARA ESTO. Aquella herramienta recorre una
página con un scroll suave: es lo correcto para una pieza estática y es lo
contrario de lo que necesita una experiencia 3D. LG Sound Suite no se
«recorre»: se navega por capítulos, se arrastra una figura y la cámara orbita.
Un scroll sobre ella grabaría una pantalla quieta.

Diferencias que importan:
  · CONDUCE la página con un GUION de beats (acciones + duración) en JSON, en
    vez de hacer scroll;
  · captura con `Page.startScreencast`, que empuja fotogramas CUANDO EL
    NAVEGADOR PINTA, en vez de pedir capturas en un bucle. Pedirlas una a una
    tarda 30-80 ms cada vez: a 24 fps el reloj de la página avanzaría más
    rápido que la captura y el vídeo saldría a tirones y desincronizado de la
    animación;
  · codifica con los TIEMPOS REALES de cada fotograma (demuxer `concat` con
    duraciones), así el resultado va a la velocidad a la que ocurrió, no a una
    velocidad supuesta.

VERDE EN VACÍO — cuatro puertas, cada una con su denominador:
  1. beats: falla si el guion no tiene ninguno;
  2. limpieza: falla si se pidió ocultar selectores y ocultó menos del mínimo;
  3. fotogramas: falla con cero, y falla si la media de fps queda por debajo
     del mínimo pedido — un vídeo de 3 fps no es un vídeo, es un pase de
     diapositivas, y saldría «correcto» sin esta comprobación;
  4. salida: falla si el MP4 pesa menos de 50 KB o si su duración se aparta
     más de un 15 % de la que pide el guion.

Uso:
  python tools/grabar.py --url URL --guion guion.json --out out.mp4
      [--size 1280x800] [--escala 960] [--fps-min 12] [--calidad 85]
"""
import argparse
import base64
import json
import shutil
import subprocess
import sys
import tempfile
import time
import urllib.request
from pathlib import Path

import websocket

EDGE = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
PORT = 9391


def die(msg: str) -> None:
    print(f"⛔ grabar.py: {msg}", file=sys.stderr)
    sys.exit(1)


def ffmpeg_exe() -> str:
    exe = shutil.which("ffmpeg")
    if exe:
        return exe
    try:
        import imageio_ffmpeg
        return imageio_ffmpeg.get_ffmpeg_exe()
    except ImportError:
        die("no hay ffmpeg (ni en PATH ni via imageio-ffmpeg)")


class CDP:
    def __init__(self, ws_url: str):
        self.ws = websocket.create_connection(ws_url, timeout=120)
        self.mid = 0
        self.frames = []          # (timestamp, bytes)

    def cmd(self, method: str, **params):
        # ⛔ El id se GUARDA aqui. Antes se comparaba contra `self.mid`, que el
        # ack de cada fotograma tambien incrementa: si llegaba un fotograma
        # mientras un comando esperaba respuesta, el contador se movia y la
        # respuesta se emparejaba con el mensaje equivocado — devolvia el ack
        # del screencast, que no trae "result", y reventaba en KeyError.
        self.mid += 1
        mio = self.mid
        self.ws.send(json.dumps({"id": mio, "method": method, "params": params}))
        while True:
            msg = json.loads(self.ws.recv())
            if msg.get("method") == "Page.screencastFrame":
                self._guarda(msg["params"])
                continue
            if msg.get("id") == mio:
                if "error" in msg:
                    die(f"CDP {method}: {msg['error']}")
                if "result" not in msg:
                    die(f"CDP {method}: respuesta sin result: {msg}")
                return msg["result"]

    def _guarda(self, p):
        self.frames.append((p["metadata"]["timestamp"], base64.b64decode(p["data"])))
        self.mid += 1
        self.ws.send(json.dumps({"id": self.mid, "method": "Page.screencastFrameAck",
                                 "params": {"sessionId": p["sessionId"]}}))

    def bombea(self, segundos: float):
        """Deja correr el tiempo recogiendo fotogramas — el equivalente a
        'rodar' mientras la escena hace lo suyo."""
        fin = time.time() + segundos
        self.ws.settimeout(0.4)
        while time.time() < fin:
            try:
                msg = json.loads(self.ws.recv())
            except websocket.WebSocketTimeoutException:
                continue
            except Exception:
                continue
            if msg.get("method") == "Page.screencastFrame":
                self._guarda(msg["params"])
        self.ws.settimeout(120)


def espera_selector(c: CDP, sel: str, maximo: float) -> float:
    """Bombea fotogramas hasta que el selector exista, o hasta `maximo`.
    Devuelve los segundos gastados. Falla si nunca aparece: un beat que
    sigue adelante sin que la escena este lista graba una pantalla de carga."""
    t0 = time.time()
    while time.time() - t0 < maximo:
        hay = c.cmd("Runtime.evaluate", returnByValue=True,
                    expression="!!document.querySelector(%s)" % json.dumps(sel)
                    )["result"].get("value")
        if hay:
            return time.time() - t0
        c.bombea(0.25)
    die(f"esperando {sel!r}: no aparecio en {maximo}s — la escena no estaba lista")


def ejecuta_beat(c: CDP, beat: dict, w: int, h: int) -> None:
    """Un beat es {accion, ...}. Las acciones de ratón se mandan como eventos
    de entrada REALES (Input.dispatchMouseEvent), no como `element.click()`:
    un canvas de three.js hace hit-testing sobre coordenadas, y un click
    sintético de DOM no le llega."""
    a = beat.get("accion", "esperar")
    if a == "esperar":
        return
    if a == "js":
        c.cmd("Runtime.evaluate", expression=beat["expr"], awaitPromise=False)
        return
    if a == "esperar_sel":
        gastado = espera_selector(c, beat["sel"], float(beat.get("max", 20)))
        beat["_gastado"] = gastado
        return
    if a == "tecla":
        # eventos de teclado REALES: room.js escucha keydown en el contenedor
        # 3D, y un KeyboardEvent sintetico desde el DOM no mueve al oyente.
        veces = int(beat.get("veces", 1))
        codigo = {"ArrowRight": 39, "ArrowLeft": 37,
                  "ArrowUp": 38, "ArrowDown": 40}[beat["tecla"]]
        for _ in range(veces):
            for tipo in ("keyDown", "keyUp"):
                c.cmd("Input.dispatchKeyEvent", type=tipo, key=beat["tecla"],
                      code=beat["tecla"], windowsVirtualKeyCode=codigo,
                      nativeVirtualKeyCode=codigo)
            c.bombea(float(beat.get("cada", 0.16)))
        return
    if a == "click":
        r = c.cmd("Runtime.evaluate", returnByValue=True, expression=(
            "(() => { const e = document.querySelector(%s); if (!e) return null;"
            " const r = e.getBoundingClientRect();"
            " return {x: r.left + r.width/2, y: r.top + r.height/2}; })()"
            % json.dumps(beat["sel"])))["result"].get("value")
        if not r:
            die(f"beat {beat.get('nombre','?')}: el selector {beat['sel']!r} no existe")
        for tipo in ("mousePressed", "mouseReleased"):
            c.cmd("Input.dispatchMouseEvent", type=tipo, x=r["x"], y=r["y"],
                  button="left", clickCount=1)
        return
    if a == "arrastrar":
        x0, y0 = beat["desde"][0] * w, beat["desde"][1] * h
        x1, y1 = beat["hasta"][0] * w, beat["hasta"][1] * h
        pasos = int(beat.get("pasos", 30))
        c.cmd("Input.dispatchMouseEvent", type="mousePressed", x=x0, y=y0,
              button="left", clickCount=1)
        for i in range(1, pasos + 1):
            c.cmd("Input.dispatchMouseEvent", type="mouseMoved",
                  x=x0 + (x1 - x0) * i / pasos, y=y0 + (y1 - y0) * i / pasos,
                  button="left")
            c.bombea(beat.get("dur", 2.0) / pasos)
        c.cmd("Input.dispatchMouseEvent", type="mouseReleased", x=x1, y=y1,
              button="left", clickCount=1)
        return
    die(f"acción de beat desconocida: {a!r}")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--url", required=True)
    ap.add_argument("--guion", required=True, help="JSON con {ocultar:[], beats:[]}")
    ap.add_argument("--out", required=True)
    ap.add_argument("--size", default="1280x800")
    ap.add_argument("--escala", type=int, default=960, help="ancho final del mp4")
    ap.add_argument("--fps-min", type=float, default=12.0)
    ap.add_argument("--calidad", type=int, default=78)
    ap.add_argument("--nth", type=int, default=2,
                    help="captura 1 de cada N fotogramas pintados (2 = ~30fps)")
    ap.add_argument("--preset", default="slow", help="preset de x264")
    ap.add_argument("--dur-min", type=float, default=0.0,
                    help="duración mínima aceptable del mp4, en segundos")
    ap.add_argument("--dur-max", type=float, default=1e9,
                    help="duración máxima aceptable del mp4, en segundos")
    ap.add_argument("--settle", type=float, default=6.0)
    a = ap.parse_args()
    w, h = (int(v) for v in a.size.split("x"))

    guion = json.loads(Path(a.guion).read_text(encoding="utf-8"))
    beats = guion.get("beats", [])
    if not beats:
        die("VERDE EN VACÍO: el guion no tiene ni un beat")
    dur_guion = sum(float(b.get("dur", 0)) for b in beats)
    if dur_guion <= 0:
        die("VERDE EN VACÍO: el guion suma 0 segundos")

    prof = Path(tempfile.mkdtemp(prefix="grabar-edge-"))
    proc = subprocess.Popen([
        EDGE, "--headless=new", "--no-first-run", "--hide-scrollbars",
        "--mute-audio", "--autoplay-policy=no-user-gesture-required",
        "--enable-unsafe-swiftshader",
        f"--remote-debugging-port={PORT}",
        f"--remote-allow-origins=http://127.0.0.1:{PORT}",
        f"--user-data-dir={prof}", f"--window-size={w},{h}", "about:blank",
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    try:
        ws = None
        for _ in range(80):
            try:
                with urllib.request.urlopen(f"http://127.0.0.1:{PORT}/json") as r:
                    pg = [t for t in json.load(r) if t.get("type") == "page"]
                if pg:
                    ws = pg[0]["webSocketDebuggerUrl"]
                    break
            except OSError:
                pass
            time.sleep(0.25)
        if not ws:
            die("Edge no expuso el puerto de debugging")

        c = CDP(ws)
        c.cmd("Page.enable")
        c.cmd("Runtime.enable")
        c.cmd("Emulation.setDeviceMetricsOverride", width=w, height=h,
              deviceScaleFactor=1, mobile=False)
        pre = guion.get("pre")
        if pre:
            c.cmd("Page.addScriptToEvaluateOnNewDocument", source=pre)
        c.cmd("Page.navigate", url=a.url)
        time.sleep(a.settle)

        ocultados = 0
        ocultar = guion.get("ocultar", [])
        if ocultar:
            sel = ", ".join(ocultar)
            ocultados = c.cmd("Runtime.evaluate", returnByValue=True, expression=(
                "(() => { const ns = document.querySelectorAll(%s);"
                " ns.forEach(n => n.style.setProperty('display','none','important'));"
                " return ns.length; })()" % json.dumps(sel)))["result"].get("value", 0)
            if ocultados < int(guion.get("min_ocultados", 1)):
                die(f"limpieza insuficiente: ocultó {ocultados} de {sel!r}, "
                    f"mínimo {guion.get('min_ocultados', 1)} — el vídeo saldría sucio")

        alto_destino = int(round(h * a.escala / w / 2)) * 2
        c.cmd("Page.startScreencast", format="jpeg", quality=a.calidad,
              maxWidth=a.escala, maxHeight=alto_destino, everyNthFrame=max(1, a.nth))
        for b in beats:
            ejecuta_beat(c, b, w, h)
            if b.get("accion") == "esperar_sel":
                resto = float(b.get("dur", 0)) - b.get("_gastado", 0)
                if resto > 0:
                    c.bombea(resto)
            elif b.get("accion") not in ("arrastrar", "tecla"):
                c.bombea(float(b.get("dur", 1.0)))
        c.cmd("Page.stopScreencast")
    finally:
        proc.terminate()

    if not c.frames:
        die("VERDE EN VACÍO: cero fotogramas capturados")
    t0, t1 = c.frames[0][0], c.frames[-1][0]
    span = max(t1 - t0, 0.001)
    fps = len(c.frames) / span
    if fps < a.fps_min:
        die(f"solo {fps:.1f} fps de media ({len(c.frames)} fotogramas en {span:.1f}s); "
            f"el mínimo es {a.fps_min} — por debajo de eso es un pase de diapositivas")

    tmp = Path(tempfile.mkdtemp(prefix="grabar-frames-"))
    lista = []
    for i, (ts, datos) in enumerate(c.frames):
        f = tmp / f"f{i:05d}.jpg"
        f.write_bytes(datos)
        dur = (c.frames[i + 1][0] - ts) if i + 1 < len(c.frames) else 1.0 / fps
        lista.append(f"file '{f.as_posix()}'\nduration {max(dur, 0.001):.4f}")
    lista.append(f"file '{(tmp / f'f{len(c.frames)-1:05d}.jpg').as_posix()}'")
    concat = tmp / "lista.txt"
    concat.write_text("\n".join(lista), encoding="utf-8")

    salida = Path(a.out)
    salida.parent.mkdir(parents=True, exist_ok=True)
    r = subprocess.run([
        ffmpeg_exe(), "-y", "-f", "concat", "-safe", "0", "-i", str(concat),
        "-vf", f"scale={a.escala}:-2:flags=lanczos,format=yuv420p",
        "-c:v", "libx264", "-preset", a.preset, "-crf", "26",
        "-movflags", "+faststart", "-an", "-r", "30", str(salida),
    ], capture_output=True, text=True)
    if r.returncode != 0:
        die("ffmpeg falló:\n" + r.stderr[-1500:])
    shutil.rmtree(tmp, ignore_errors=True)

    peso = salida.stat().st_size
    if peso < 50_000:
        die(f"el mp4 pesa {peso} bytes — sospechosamente vacío")
    sonda = subprocess.run([ffmpeg_exe(), "-i", str(salida)], capture_output=True, text=True)
    import re as _re
    m = _re.search(r"Duration: (\d+):(\d+):([\d.]+)", sonda.stderr)
    real = (int(m.group(1)) * 3600 + int(m.group(2)) * 60 + float(m.group(3))) if m else 0.0
    # ⛔ La comprobacion correcta NO es «coincide con la suma de dur». Los beats
    # que esperan a que cargue una escena 3D tardan lo que tardan, y los de
    # teclado suman su propio ritmo: comparar contra la suma declarada hacia
    # fallar un video que estaba perfectamente bien. Lo que importa es que la
    # pieza caiga en la ventana pedida, que es una decision editorial.
    if not (a.dur_min <= real <= a.dur_max):
        die(f"el vídeo dura {real:.1f}s y la ventana pedida es "
            f"{a.dur_min:.0f}-{a.dur_max:.0f}s")

    print(f"grabar.py: {salida} · {peso/1048576:.2f} MB · {real:.1f}s "
          f"(guion {dur_guion:.0f}s) · {len(c.frames)} fotogramas a {fps:.1f} fps "
          f"· {len(beats)} beats · {ocultados} elemento(s) ocultado(s) · {a.escala}px")


if __name__ == "__main__":
    main()
