# CLAUDE.md — ReasonedWeb.com

> **Este archivo tiene que bastarse solo.** Abrir esta carpeta como raíz de VSCode significa
> **cero memorias heredadas y cero instrucciones de otros proyectos**. Aquí el aislamiento es
> DESEADO: este sitio no vende lo que venden los otros dos negocios de Carlos. Si algo hace
> falta de afuera, se LEE y se decide; jamás se hereda por costumbre.

## Qué es

Portafolio personal de Carlos Marruffo en **www.reasonedweb.com**. Único trabajo: que UNA
agencia de diseño web, **Shopify Partner** o **Klaviyo Partner de EE. UU.** lo tome como socio
de producción remoto **dedicado, con vocación de full-time**.
⛔ **Aclaración de Carlos (2026-08-16, refinada el 17): el copy JAMÁS lo pinta trabajando para
varias agencias a la vez — Y TAMPOCO lo dice explícito.** «One partner at a time» se probó y
Carlos la retiró: contar clientes en voz alta huele a necesidad. **La exclusividad es
IMPLÍCITA o no existe**: se carga en «Dedicated» (title), «Embedded, end to end» (§04),
«Check availability» (CTA — la disponibilidad insinúa el cupo), y la línea de la bio «the
shape of work I do best: one product, one team» (preferencia, no pitch). Vetados: «retainer»,
vocabulario freelance/consultor, contar clientes, «Hire me» / «Open to work».

⛔ **No se pide trabajo explícitamente.** Postura de **estudio de un solo integrante**, no de
candidato: las agencias subcontratan a estudios, no contratan freelancers desde un portafolio.
CTA canónico: *"Check availability"* (el antiguo *"Start a project"* se retiró — sonaba a
proyecto suelto). Jamás *"Hire me"* ni *"Open to work"*.

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

⛔⛔ **SOLO CRUZAN PÍXELES** — capturas y video, alojados en reasonedweb.com.
**Enmienda de Carlos (2026-08-16): también cruzan EXHIBICIONES VIVAS** — copias del HTML
de una pieza, SOLO vía `tools/exhibir.py` (sanitiza banners/precios/metadatos ajenos con
puerta de residuo cero e inyecta la etiqueta honesta de Reasoned Web al pie). Un exhibit
es una copia CONGELADA: no se mantiene — si la fuente cambia, se re-genera con la
herramienta. Los walkthroughs en video se probaron primero y Carlos los retiró el mismo
día («the videos were not a good idea») a favor de los exhibits; `tools/record.py` queda
por si vuelven a servir (p. ej. loops de hover en la galería). Las URLs publicadas
(`tuweb.pe/wemadeyoursite/demos/*`, `tuweb.pe/demos/*`) son **referencia INTERNA de esta sesión**
para encontrar las piezas — ⛔ **jamás se enlazan desde el sitio publicado**: el sitio no menciona
tuweb.pe, wemadeyoursite ni ninguna otra marca que no sea Reasoned Web (orden de Carlos), y un
enlace es una mención. **Jamás se copia el HTML fuente**: traería marcado en español, gates
ajenos, precios ajenos y el lenguaje visual de la obra que este sitio debe ENMARCAR, no imitar.
Y una copia se vuelve un fork que se pudre.

## Lo que NO se hereda

| | |
|---|---|
| **Precios** | Ni el canon Perú (S/500 · S/50 · S/20) ni el de WeMadeYourSite ($995 · $96 · $29). Aquí se vende **dedicación exclusiva** (one partner at a time); los números de ReasonedWeb no existen todavía. El piso que Carlos nombró ($90k/año) fue ANTES de que LG entrara al mapa — el sitio no debe insinuar cifra alguna |
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
- **Sello de notas (gráfico secundario, 2026-08-16):** la marca B del specimen 01 («footnote
  apparatus»: regla horizontal + asterisco de 3 ejes a 60° debajo) — Carlos la recordaba como
  «comilla» y pidió usarla; el specimen 03 ya la conservaba «as apparatus». Se coloca como
  CIERRE del cuerpo: en la home antes de Contact, en cada caso al final del wrap (en LG antes
  del bloque legal). Clase `.sello-notas`, color --muted, decorativa (aria-hidden). Coordenadas
  exactas del specimen: línea y30 x22–78 sw3.2; ejes sw5.4 a 60°.
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
3. ⛔ **ATRIBUCIÓN — SUPERSEDIDA (orden Carlos 2026-08-17: «It was developed by me alone.
   I don't want no mentions of NextLatam anywhere»)**: el sitio NO menciona Next Latam en
   NINGUNA parte — ni casos, ni gate, ni bio, ni metas, ni el crédito final DENTRO del build
   LG (parchado en chunks `-p2`). Atribución vigente en todo el kit: *"developed for a
   presentation to LG Electronics Canada"*; el bloque legal cierra *"…are the work of
   Reasoned Web."* El patrón nextlatam está en los PROHIBIDOS de `tools/exhibir.py`. Las
   variantes A/B de abajo quedan como historia del papel, no como copy.
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
- **Contacto: formulario + `hello@reasonedweb.com`.** ✅ MX verificado 2026-08-16; correo
  impreso en contacto y en los 7 pies. **El formulario ENVÍA de verdad (2026-08-16): endpoint
  propio `site/api/contact.js` (función Vercel) → Resend**, clave SOLO en env vars de Vercel
  (`RESEND_API_KEY`; opcionales `CONTACT_TO`/`CONTACT_FROM`). Campos que Carlos exige del
  prospecto: nombre, work email, agencia, ROL, TELÉFONO (+ ships opcional y mensaje); honeypot
  `website`; reply-to = el email del visitante. **Degradación honesta verificada**: si la
  clave no está o Resend falla, el frontend cae al compositor mailto Y LO DICE — jamás un
  «enviado» falso. ⛔ El endpoint es propio de este proyecto — jamás compartido con nada de
  Perú (lección: el form US posteaba al endpoint peruano y horneaba `wa.me/51…`).
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

## ✅ Estado al 2026-08-16 — EL SITIO ESTÁ EN VIVO Y COMPLETO

**www.reasonedweb.com en producción** (Vercel, proyecto `reasonedweb`, raíz `site/`, DNS ok,
apex 308→www, **noindex total deliberado** — X-Robots-Tag; el único descuento SEO de
Lighthouse es ese y es intencional). Los CUATRO tiers de la carta están en pie:

- **Tier 0**: caso LG con el embed VIVO tras su gate (`live/`; chunks parchados `-p1` — los
  PiP CAM 1-4 renderizaban frame por medio; el fix de fondo sigue PENDIENTE en el fuente de
  LG-Demo, mismo toggle d5).
- **Tier 1**: UdV, Smoothies, Woods & Co y Nanntu — casos anotados + **exhibits vivos
  sanitizados** en iframes (`piece/`), generados SOLO con `tools/exhibir.py`.
- **Catálogo UdV 2026** (33 láminas): exhibit en `work/ulric-de-varens/deck/`, fuente
  canónica `Desktop/Claude/UDV-deck/` — se REGENERA, jamás se edita. Tarjeta propia en home.
- **Tier 2**: 8 exhibits en `site/range/` (orden de Carlos; Maison Corbiere/parfum retirado
  el 2026-08-17): oyster-house, gym, auto-body, hvac, jewelry, law-firm, med-spa, tree-care.
- **Tier 3**: corpus `work/one-system/` — muro de 46 capturas limpias, jamás tiles enlazados.
- **Home completa**: hero con derivación y tesis con las capacidades que Carlos fijó el 17
  («sites, immersive products, and software end to end; brand systems, and the decks and
  presentations that win the room» — su «WOW» dicho en el registro del sitio) · LG ·
  redesigns + catálogo · Range + banda corpus ·
  How I work («Embedded, end to end» + recibos medidos [6]) · **The principal** (retrato
  monocromo de `CRM Web/cv_photos/`, bio del CV maestro en `AI Job Search/` — SIN mencionar
  AI, regla 7) · Contact («Check availability», hello@ impreso con MX verificado, formulario
  que ENVÍA en producción vía `/api/contact` + Resend — probado real, campos: nombre, work
  email, agencia, ROL, TELÉFONO; detalles e interino en § Arquitectura y Pendientes 0).
  Sello de notas (marca B) cierra home y casos.
- **Calidad medida en vivo**: Lighthouse desktop 100/100/100, móvil 97/100/100, CLS 0;
  auditoría propia 272 elementos × 3 anchos, cero violaciones AA, cero desbordes.
- Identidad computada en `brand/`; herramientas en `tools/` (capture, inline_brand, exhibir,
  record en reserva, auditar). Etiquetas confirmadas: UdV encargo real; Nanntu regalado.

## Reglas de operación vigentes (no re-aprender)

1. **Push**: las sesiones COMMITEAN (`-F archivo` + `--only -- rutas`); el push es de Carlos:
   `$env:ARRASTRE_OK="1"; git push` (la puerta de arrastre nombra los commits claude:* —
   adopción deliberada). El push no-interactivo de las sesiones sigue fallando («Cannot
   prompt»); el fetch sí funciona. Vercel auto-deploya cada push en <1 min.
2. ⛔ **Posicionamiento (regla dura de Carlos, refinada 2026-08-17)**: JAMÁS pintarlo
   trabajando para varias agencias a la vez, y la exclusividad JAMÁS se dice explícita
   («One partner at a time» se retiró — contar clientes suena a necesidad). Implícita en:
   «Dedicated», «Embedded, end to end», «Check availability», «one product, one team».
   Vetados: «retainer», vocabulario freelance/consultor, «Hire me» / «Open to work».
   CTA canónico: «Check availability».
3. ⛔ **Pestañas**: enlaces a exhibits (live/, piece/, deck/, range/*) y externos SIEMPRE
   `target="_blank" rel="noopener"`; navegación interna en la misma pestaña.
4. **Exhibits**: solo vía `tools/exhibir.py` (puerta de residuo cero, 11 patrones, etiqueta
   honesta al pie). Si la fuente cambia, se regenera; el exhibit no se toca a mano. El cache
   del embed LG es immutable: cambiar un chunk = renombrarlo y actualizar sus referencias
   cruzadas (import graph completo).
5. **Instrumento**: capturas móviles con `--window-size` MIENTEN — usar `tools/capture.py`;
   auditar con `tools/auditar.py` (publica denominador, falla en cero); tras cambios de
   pantalla, re-correr auditoría; hooks sh con CRLF no spawnean (.gitattributes fija LF).
   Y la lección del 15: ante un reporte visual del usuario, sus capturas valen más que un
   burst lento en headless — el instrumento se sospecha primero.

## Pendientes (cortos)

0. **Resend — FUNCIONANDO EN INTERINO (2026-08-16)**: `RESEND_API_KEY` puesta en Vercel por
   CLI (la sesión quedó logueada como `hello-40633109`, team `reasoned-web` — el CLI de esta
   máquina PUEDE tocar Vercel: env vars, redeploy, logs). Envío real probado: 200 {"ok":true},
   entregado a hello@. **Interino**: `CONTACT_FROM=onboarding@resend.dev` porque el dominio
   NO está verificado en Resend (403 comprobado). **FALTA de Carlos**: resend.com/domains →
   añadir `reasonedweb.com` → poner los registros DNS en GoDaddy → verificar; entonces
   ELIMINAR `CONTACT_FROM` (`npx vercel env rm CONTACT_FROM production` + redeploy) y el
   correo sale como «Reasoned Web <hello@reasonedweb.com>». ⚠️ La API key quedó pegada en la
   conversación del 16 — rotarla en Resend cuando todo esté verificado es un clic. Nota:
   `trailingSlash` redirige /api/contact con 308 — los navegadores lo siguen conservando el
   POST (probado); curl necesita -L.
1. **LinkedIn**: ESPERA — perfil desactualizado, no enlazar hasta que Carlos lo renueve.
2. **Cita de Next Latam** (testimonio): pedir permiso ESCRITO antes de publicar nada.
3. **Fix upstream del PiP LG** en el fuente de LG-Demo (proyecto aparte; una línea, toggle d5).
4. **OG por caso** (cada unfurl con su propia pieza en vez del wordmark genérico) — mejora.
5. Fuente licenciada (Söhne / ABC Diatype) — después, si el sitio lo gana.
6. **Outreach**: movimiento de Carlos. Secuencia de la carta: primero agencias; el set de
   commerce UdV antes de tocar Shopify/Klaviyo Partners.
