# CLAUDE.md — ReasonedWeb.com

> **Este archivo tiene que bastarse solo.** Abrir esta carpeta como raíz de VSCode significa
> **cero memorias heredadas y cero instrucciones de otros proyectos**. Aquí el aislamiento es
> DESEADO: este sitio no vende lo que venden los otros dos negocios de Carlos. Si algo hace
> falta de afuera, se LEE y se decide; jamás se hereda por costumbre.

## Qué es

Portafolio personal de Carlos Marruffo en **www.reasonedweb.com**. Único trabajo: que agencias
de diseño web, **Shopify Partners** y **Klaviyo Partners de EE. UU.** lo contraten como socio de
producción remoto, en retainer mensual.

⛔ **No se pide trabajo explícitamente.** Postura de **estudio de un solo integrante**, no de
candidato: las agencias subcontratan a estudios, no contratan freelancers desde un portafolio.
CTA: *"Check availability"* / *"Start a project"*. Jamás *"Hire me"* ni *"Open to work"*.

⭐ **El diferenciador es el dominio:** cada pieza viaja con su **razonamiento escrito**. La frase
de Carlos que define el estándar: *«no hacemos un solo cambio sin una explicación objetiva — un
porqué que haga nuestros productos defendibles frente a cualquier juez»*. Todo en **primera
persona**; el sitio es **solo inglés de EE. UU.**

## ⛔ LA FRONTERA — de una sola dirección

Este proyecto **LEE** de otras carpetas y **NUNCA les escribe**. Nada de allá depende de acá.

| Fuente (SOLO LECTURA) | Qué contiene |
|---|---|
| `../LG-Demo/` | Encargo LG Sound Suite: `context/*.md` (13 docs), `deliverables/`, `3D_assets/`, `LG-preview/` (build embebible) |
| `../CRM Web/apps/web/public/wemadeyoursite/borradores/` | Rediseños de negocios reales + `-notas.html` y `-marca.html` |
| `../CRM Web/wemadeyoursite/site/demos/` | ~28 piezas en inglés (negocios inventados) |
| `../CRM Web/apps/web/public/demos/` | ~46 piezas en español (mercado peruano) |

⛔⛔ **SOLO CRUZAN PÍXELES** — capturas y video, alojados en reasonedweb.com. Las URLs publicadas
(`tuweb.pe/wemadeyoursite/demos/*`, `tuweb.pe/demos/*`) son **referencia INTERNA de esta sesión**
para encontrar las piezas — ⛔ **jamás se enlazan desde el sitio publicado**: el sitio no menciona
tuweb.pe, wemadeyoursite ni ninguna otra marca que no sea Reasoned Web (orden de Carlos), y un
enlace es una mención. **Jamás se copia el HTML fuente**: traería marcado en español, gates
ajenos, precios ajenos y el lenguaje visual de la obra que este sitio debe ENMARCAR, no imitar.
Y una copia se vuelve un fork que se pudre.

## Lo que NO se hereda

| | |
|---|---|
| **Precios** | Ni el canon Perú (S/500 · S/50 · S/20) ni el de WeMadeYourSite ($995 · $96 · $29). Aquí se vende **tiempo y criterio** en retainer; los números de ReasonedWeb no existen todavía. El piso que Carlos nombró ($90k/año) fue ANTES de que LG entrara al mapa — el sitio no debe insinuar cifra alguna |
| **Voz y marca** | "Mejora continua", `wa.me`, el guion de WhatsApp, el deslinde de Google, las marcas WMYS y TuWeb.pe |
| **Aparato de QA** | `verificar.mjs`, `gate-*.mjs`, ledgers ajenos. Si hace falta un check, se escribe uno nuevo y mínimo |
| **Infra** | Supabase, CRM, motor V3, crons, migraciones |
| **Lenguaje visual** | ⛔ **El sitio no puede parecerse a las piezas que exhibe.** Un portafolio con la tipografía y el sustrato de su obra se lee como una pieza más, no como el marco |

## Lo que SÍ se hereda — método, no contenido

- **Verde en vacío:** todo bucle o recolección cuenta lo que verificó y **falla si contó cero**.
- **Verde en vacío PARCIAL:** todo auditor **publica su denominador** y nombra lo que no pudo medir.
- **Un cambio reportado no es un cambio aplicado.** Se comprueba contra el estado, no el resumen.
- **Toda puerta nueva debe verse fallar una vez**, con el diagnóstico correcto.
- **Ante un hallazgo raro, sospechar del instrumento primero.**
- **Contraste AA medido contra el fondo realmente pintado.** Cero emoji; iconografía dibujada.
- **Una declaración sin efecto es peor que una equivocada:** parece pensada, y nadie la vuelve a mirar.
- **El costo en API se declara** siempre: estimado antes, real después. "$0" también se dice.

## ✅ IDENTIDAD — DECIDIDA (2026-08-13, cuatro especímenes)

**El principio que gobierna todo lo visual: NINGÚN VALOR SE ELIGE DONDE UNO SE PUEDE DERIVAR.**
La identidad no ilustra el razonamiento — lo EJECUTA.

- **Máster:** el nombre compuesto **justificado**. `REASONED` arriba, `WEB` abajo, ambas líneas
  a la MISMA medida. El tracking de WEB no se elige: se deriva — `gap = (W₁ − W₂) / 2`,
  aplicado entre las tres letras (el letter-spacing de CSS deja espacio tras la última letra;
  se recorta con `margin-right` negativo igual al gap). Línea 1 lleva tracking 0.02em con el
  mismo recorte. **Canal vertical entre líneas = m = capHeight/3** — la regla que el glifo ya
  ejecuta (su canal es m en una marca de 3m); `canal = gap` se probó y Carlos lo rechazó
  (2026-08-14, «demasiado aire»). Con Switzer: gap = 1583u = 1.583em; canal = 235.7u. Al
  cambiar de fuente, los números se re-derivan (`brand/derive.py` → `tools/inline_brand.py`);
  **la regla es el logo, el render es su output actual**. Mitigación del cold-read (revisor
  adversarial: la W E B abierta «se lee como bug de kerning»): la home anota la fórmula bajo
  el máster — la confusión se convierte en tesis.
- **Tipografía: Switzer 700** (Fontshare, ITF Free Font License, $0, uso comercial permitido).
  CSS de origen: `https://api.fontshare.com/v2/css?f[]=switzer@700` (el woff2 se saca de ahí;
  para el set completo de pesos, el zip de fontshare.com). Elegida sobre General Sans (cálida
  de más para la tesis) y Geist (es la cara de Vercel y el público objetivo lo reconoce).
- **Glifo** (favicon, sellos): el máster a resolución mínima. Módulo `m`; medida = `5m`.
  Barra sólida de `5m × m` (= REASONED macizo) sobre **tres cuadrados** de `m × m` (= W·E·B
  contadas), separados por gaps de `m`; gap vertical `m`. En viewBox 100: barra
  `x20 y32 w60 h12`; cuadrados `y56`, `x = 20 / 44 / 68`, `12×12`. Cuatro rellenos, cero
  trazos — no puede romperse a 16 px. **La forma ES el nombre**: no se puede copiar sin copiar
  el nombre.
- **Lockup horizontal** (nav, firmas, junto al logo de LG): glifo + «Reasoned Web» en caja de
  título, Switzer, tracking −0.015em aprox (se afina óptico).
- **Paleta de trabajo de los especímenes** (provisional, NO canon del sitio): tinta `#16181C`,
  papel `#F3F4F3`, azul de anotación `#2C6ECB` (solo apparatus, jamás marca).
- ⛔ **Vetos tipográficos:** Newsreader y JetBrains Mono (caras de TuWeb.pe), Inter, Poppins,
  Montserrat, Space Grotesk, Satoshi (saturación slop), Geist (asociación Vercel). Nada
  compartido con las ~74 piezas exhibidas.
- ⛔ **El logotipo jamás lo dibuja un modelo de imagen.** Ya está medido en esta máquina: 3 de 4
  renders falsificaron letras de una marca real. Los másters se construyen como SVG computado.
- **Referencias (especímenes publicados, artifacts privados de Claude):**
  1. Marks round 1 — `https://claude.ai/code/artifact/77f3695d-8e40-49d2-a683-4db95f53391a`
  2. Marks round 2 — `https://claude.ai/code/artifact/b9107a25-bf21-4d4d-9729-9187e659d510`
  3. El replanteo (la identidad tipográfica) — `https://claude.ai/code/artifact/28d9cea9-15cb-49f8-ab42-cb980f5a8052`
  4. Prueba de tipografías con derivación en vivo — `https://claude.ai/code/artifact/12f5d90c-ec7a-4822-ba1a-97dd0cae1b74`
- **Camino licenciado (después, si el sitio lo gana):** Söhne o ABC Diatype (~$100–400 web).
  Cambiar la fuente = re-derivar y re-exportar; una tarde, no un rediseño.

## Reglas duras del contenido

1. ⛔ **ETIQUETADO HONESTO.** Tres clases visibles en cada pieza: **(a)** encargo real ·
   **(b)** *"Unsolicited concept. Not affiliated with, or commissioned by, [marca]"* ·
   **(c)** *"Speculative concept — fictional business"*. Si un director creativo caza UNA pieza
   especulativa sin etiquetar, asume que todo el portafolio es inventado — y razona bien.
2. ⛔ **JAMÁS SE PUBLICA LO FACTURADO.** La cifra del encargo LG está en sus archivos; no sale.
3. ⛔ **ATRIBUCIÓN EXACTA:** *"For LG Electronics Canada, with Next Latam"*.
4. ⛔ **LG ES PÚBLICO CON DISCLAIMER — decisión de Carlos, 2026-08-13** (advertido el riesgo:
   V2 se construyó at-risk antes del sign-off; decisión suya — no volver a vetarlo). Condiciones
   que la acompañan, no negociables:
   - **El kit de disclaimers va completo** (§ Kit LG, abajo): gate de entrada + bloque legal al
     pie + reglas de meta/OG. No se publica la página sin las tres piezas.
   - **La primera tarea del caso LG es leer `../LG-Demo/proposals/` y `deliverables/`** para
     fijar la variante de atribución (A o B del kit) según lo que el papel realmente diga.
   - ⚠️ Un disclaimer cura la CONFUSIÓN (marca, afiliación); **no licencia la PI** (modelos 3D
     derivados del CAD de LG, fotografía, tagline). Ese residuo se acepta por decisión, y se
     achica pidiendo el visto bueno por escrito EN PARALELO — el correo sale vía Next Latam
     después de lanzar, no bloquea nada.
   - ⛔ La ruta de LG **no va en `robots.txt`** por ningún motivo (una línea disallow es un
     anuncio). **Actualización 2026-08-15 (orden de Carlos): el SITIO ENTERO es noindex** —
     `X-Robots-Tag: noindex, nofollow` global en `site/vercel.json`, sin sitemap, y
     robots.txt SIN disallow (rastreable para que el noindex se vea; un disallow impediría
     des-indexar). La regla de no-anuncio se mantiene: nada señala la ruta LG en particular.
5. ⛔ **NADA DE DOCUMENTOS INTERNOS EN CRUDO** (correos con nombres, propuestas con cifras).
6. **El sitio es el verdadero caso de estudio.** AA medido, 320 px, sin bloat de framework.
   El caso LG se estructura de punta a punta: producto físico → research → concepto → idea →
   implementación → accesibilidad/estándares legales del país → tecnologías → resultado
   EMBEBIDO con sus disclaimers. Las notas de los rediseños US (UdV, Smoothies, Nanntu,
   Woods & Co) llevan la URL del sitio original si existe, el proceso entero y el porqué de
   cada decisión.
7. ⛔ **EL SITIO JAMÁS DICE "AI-assisted" NI NOMBRA EL MECANISMO** (decisión Carlos,
   2026-08-13: *«that will cheapen us»*). El corpus se presenta como lo que demuestra —
   capacidad de diseñar masivamente entre verticales con calidad sostenida — y el CÓMO no se
   cuenta, igual que ningún estudio lista sus herramientas. **El límite:** callar el mecanismo
   sí; AFIRMAR un proceso falso (p. ej. «drawn one by one») no. La regla 1 (etiquetado) sigue
   intacta: las piezas especulativas se marcan ficticias — eso es sobre el NEGOCIO retratado,
   no sobre la herramienta.

## § Kit LG — disclaimers listos (inglés; se ajustan solo si el papel obliga)

**Atribución — FIJADA EN VARIANTE B (2026-08-14, papel leído):** *"An interactive
demonstration developed with Next Latam for presentation to LG Electronics Canada."*
Evidencia: propuesta V2 con firma de LG EN BLANCO, checklist de sign-off sin marcar, V2
construida at-risk, status «paused in a clean state, waiting on LG». **Sube a Variante A**
(*"Developed for LG Electronics Canada, with Next Latam."*) solo con evidencia escrita de
aceptación posterior al 2026-07-15 (p. ej. en el correo real de Carlos, no en las carpetas).

**Gate de entrada** (visible ANTES de cargar la experiencia — cumple doble función: disclaimer
y aviso de peso de la carga ~25 MB):

> **Independent demonstration.** This interactive experience was [Variante A/B]. It is not an
> official LG property, and it is not affiliated with, sponsored by, or endorsed by LG
> Electronics. Product behavior shown here is a demonstration approximation — for official
> product information, visit lg.com.

**Bloque legal al pie de la página del caso:**

> LG, the LG logo, "Life's Good," and LG Sound Suite product names are trademarks of
> LG Electronics Inc., used here solely to identify the product this work depicts. This case
> study documents design and engineering work; it is not an offer of LG products and contains
> no official LG product information. 3D assets shown were derived from manufacturer CAD data
> in the course of this engagement. All design rationale and implementation described are the
> work of Reasoned Web [/ con la variante que corresponda].

**Reglas de meta/OG del caso LG:**
- `<title>`: "LG Sound Suite — Case Study · Reasoned Web" — jamás "LG Sound Suite" a secas.
- `og:image`: composición PROPIA con la marca Reasoned Web visible; jamás el logo de LG solo
  (una tarjeta que parece oficial de LG en un unfurl de WhatsApp es exactamente la confusión
  que el disclaimer existe para impedir).
- En el cuerpo del caso: afirmaciones sobre el PRODUCTO de LG solo las que respalda
  `../LG-Demo/context/10-PRODUCT-TRUTH.md`; cero métricas inventadas de resultados.

## El material, por peso

| Nivel | Pieza | Qué prueba |
|---|---|---|
| **0 — titular** | **LG Sound Suite** | Encargo real de marca global, punta a punta: CAD del cliente → 3D → audio binaural → build → manuales → accesibilidad → EN/FR-CA |
| **1 — razonamiento** | UdV USA · Smoothies · Nanntu · Woods & Co (+ Levain, Donahue si aportan) | Diagnóstico medido + rediseño + porqué escrito |
| **2 — rango** | ~12 curadas de las exemplars EN | "Ya resolví tu vertical" — selección manual de Carlos, presentación distinta (demos sin cliente), como CAPTURAS |
| **3 — corpus** | Las ~46 demos ES, DENTRO de un solo caso de sistema («one system, 46 verticals») | Diseño masivo entre verticales con calidad sostenida. ⛔ Jamás tiles individuales — la estructura repetida los delata como serie; como corpus, la repetición ES el argumento. ⛔ Sin nombrar AI (regla 7). El español se declara como RASGO: trabajo real para el mercado peruano, capacidad bilingüe — no un defecto que esconder |

⛔ **El volumen es pasivo:** 80 piezas volcadas se leen como generadas; 12 con razonamiento se
leen como senior. La curaduría es parte del trabajo de diseño.

## § Arquitectura del sitio — decisiones TOMADAS (2026-08-13)

- **Un scroll + páginas satélite.** Home en un solo scroll: hero → LG → rediseños razonados →
  galería de rango → cómo trabajo → contacto. LG y cada rediseño tier-1 tienen **página
  propia**; el embed de LG (~25 MB) **JAMÁS carga en la home** — entra por su gate (§ Kit LG).
- **El aparato de nota al pie es la interacción-firma del sitio** (aceptado por Carlos). Las
  afirmaciones llevan marcador; el marcador abre el razonamiento escrito. **El compromiso que
  trae:** toda página de caso DEBE sus anotaciones — una página de caso sin anotar se lee rota.
- **Contacto: formulario + `hello@reasonedweb.com`.** El Workspace lo crea Carlos (pendiente
  SUYO, no de la sesión). ⛔ El correo **no se imprime en ninguna página hasta verificar MX**
  (lección WMYS: se imprimió una dirección cuyo dominio no enrutaba correo). ⛔ El endpoint del
  formulario es **NUEVO y propio de este proyecto** — jamás compartido con nada de Perú
  (lección: el form US posteaba al endpoint peruano y horneaba `wa.me/51…`).
- **Stack: estático, autorado a mano.** HTML/CSS/JS vanilla, sin framework. Se introduce SOLO
  lo absolutamente necesario (orden de Carlos: contexto mínimo). El rendimiento del sitio es
  una pieza más de la vitrina — «100 Lighthouse, sin framework» es una frase que este público
  entiende. El build de LG se monta como ruta estática propia.
- **Primera persona en todo.** Y antes de publicar: revisión anti-contradicciones — cero
  menciones de wemadeyoursite, tuweb.pe o cualquier sitio que no sea Reasoned Web.

## § Secuencia de lanzamiento — decisión C (Carlos, 2026-08-13)

1. **Lanzar** cuando tier 0 (LG) + tier 1 (rediseños con notas) estén en pie.
2. Outreach **SOLO a agencias** de diseño.
3. Producir el **set de comercio UdV**: PDP con UN momento interactivo real de producto (la
   técnica LG a escala DTC), página de colección, cart drawer **display-only** (jamás acepta
   nada que parezca datos de pago), y 3 correos Klaviyo (welcome, abandoned cart,
   post-purchase). Etiqueta clase (b) en todo. Estimado: ~$0.10–0.40 de API en escenas.
4. **Recién entonces** outreach a Shopify Partners y Klaviyo Partners. ⛔ Ni un solo correo a
   ese segmento antes de que el set exista — cada prospecto abre una sola vez.

## ✅ Estado al 2026-08-14 — lo que EXISTE (dos rondas completas)

- **Identidad computada y commiteada**: `brand/` (derive.py, derivation.json, tres másters
  SVG, spec.html con re-derivación en vivo PASS/FAIL), favicons en rejilla entera, fuentes
  400–700 autoalojadas con licencia. Wireframes en `wireframes/`.
- **Sitio en pie bajo `site/`** (la raíz del deploy — lo interno JAMÁS viaja): home de un
  scroll con aparato de notas funcionando, folios 01–04, og propio renderizado del máster,
  404, y **cinco casos**: LG (placeholder por orden de Carlos: gate = bloque de disclaimer
  Variante B, sin embed), UdV, Smoothies, Woods & Co y Nanntu — los cuatro tier 1 con su
  razonamiento escrito completo y anotado.
- **Herramientas propias mínimas**: `tools/capture.py` (capturas CDP con limpieza verificada
  — solo cruzan píxeles, sin banners de otras marcas) y `tools/inline_brand.py` (másters
  inline idempotentes). Flujo al cambiar la marca: `brand/derive.py` → `tools/inline_brand.py`.
- **Revisión adversarial sin contexto ya pasada** (veredicto inicial «maybe, leaning no»;
  su defecto #1 —diferenciador sin pagar— quedó resuelto con los casos escritos).
- Etiquetas CONFIRMADAS por Carlos (2026-08-15): UdV fue encargo real — «Client engagement —
  Ulric de Varens USA» queda definitiva. Nanntu fue borrador REGALADO, no encargo — etiqueta
  definitiva «Design draft — gifted to Patricia Deza, not commissioned» (aplicada en su caso
  y en la tarjeta de la home; cierra la ambigüedad de "prepared for", que dejaba abierta la
  pregunta de si hubo comisión — regla 1).

## Primer encargo de la siguiente sesión

1. ~~Verificar el push~~ **RESUELTO 2026-08-15**: Carlos re-autenticó GCM desde su terminal
   y empujó la cola (5 commits + e77bb19). ⚠️ Vigente: las sesiones Claude LEEN de GitHub
   con el token guardado pero el PUSH sigue pidiendo prompt interactivo («Cannot prompt») —
   los pushes se siguen encolando para Carlos (`$env:ARRASTRE_OK="1"; git push`, la puerta
   de arrastre nombra los commits claude:* y la adopción es deliberada).
2. ~~Vercel~~ **EN PIE 2026-08-15**: proyecto `reasonedweb` (equipo ReasonedWeb, Hobby) ya
   existía conectado al repo — se corrigió **Root Directory a `site`** (deployaba la RAÍZ
   del repo: CLAUDE.md, brand/ y tools/ estuvieron públicos en reasonedweb.vercel.app;
   deployments viejos BORRADOS por Carlos). `site/vercel.json` mínimo con
   `trailingSlash: true` (las rutas relativas del embed rompen sin barra final).
   Verificado en vivo (33/33): rutas, 404 propio, redirect 308, 18 assets del embed,
   fuga cerrada (CLAUDE.md/brand/tools → 404). **PENDIENTE: DNS** — reasonedweb.com
   apunta al parking del registrador y www no existe; falta apuntar A/CNAME a Vercel y
   fijar www como primario.
3. ~~Montar el embed LG~~ **HECHO 2026-08-15** (`7ee32c4`): build en
   `site/work/lg-sound-suite/live/` (shell re-enmarcado a Reasoned Web: title/og propios,
   favicon del sitio — fuera `iso.svg`, que era el monograma LG, y el og-image de nextlatam);
   gate restaurado con línea de peso/auriculares y botón «Enter the demonstration» → `live/`.
   Verificado local: CDP renderiza start screen, 18 assets perezosos HEAD 200, log sin 404.
4. ~~Confirmaciones de una palabra~~ **RESUELTAS 2026-08-15**: UdV encargo real (etiqueta se
   mantiene); Nanntu borrador regalado (etiqueta definitiva aplicada, ver § Estado).
5. Lecciones de instrumento — no re-aprender: screenshots móviles con `--window-size`
   MIENTEN (mínimo de ventana ~400px) — usar `tools/capture.py` (métricas reales de
   dispositivo); hooks sh con CRLF no spawnean (`.gitattributes` ya fija LF); mensajes de
   commit SIEMPRE con `-F archivo` y `--only -- rutas`.

## Decisiones abiertas (esperan a Carlos)

1. ~~¿LG público o solo por enlace?~~ **RESUELTA 2026-08-13: público con disclaimer**.
   ~~¿Variante A o B?~~ **RESUELTA 2026-08-14: Variante B por el papel** (§ Kit LG).
2. ~~¿UdV commerce antes de lanzar?~~ **RESUELTA 2026-08-13: opción C — desacoplado**.
3. ~~¿Entran las demos de Perú?~~ **RESUELTA 2026-08-13: como CORPUS** — jamás tiles.
4. **Curaduría de Carlos pendiente**: las ~12 piezas de la galería de rango (tier 2) y el
   armado del caso-corpus (tier 3). Las secciones existen como comentario en la home.
5. Upgrade a fuente licenciada — después, si el sitio lo gana.
6. Google Workspace para `hello@reasonedweb.com` — MANUAL de Carlos; sin MX verificado el
   correo no se imprime y el formulario sigue en estado honesto (no envía y lo dice).
7. ~~Confirmación de clase de UdV y Nanntu~~ **RESUELTA 2026-08-15**: UdV encargo real,
   Nanntu borrador regalado (etiquetas definitivas aplicadas).