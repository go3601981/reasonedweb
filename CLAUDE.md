# CLAUDE.md — ReasonedWeb.com

> **Este archivo tiene que bastarse solo.** Abrir esta carpeta como raíz de VSCode significa
> **cero memorias heredadas y cero instrucciones de otros proyectos**. Aquí el aislamiento es
> DESEADO: este sitio no vende lo que venden los otros dos negocios de Carlos. Si algo hace
> falta de afuera, se LEE y se decide; jamás se hereda por costumbre.

## Qué es

Portafolio personal de Carlos Marruffo en **www.reasonedweb.com**.

⚠️ **EL PÚBLICO CAMBIÓ EL 2026-08-18 — orden de Carlos: «Shopify and Klaviyo goes again,
those don't pay what I need».** El sitio ya NO se dirige a agencias de diseño web ni a
Shopify/Klaviyo Partners. Se dirige a **agencias experienciales, constructores de stands
(exhibit builders) y equipos de brand experience**, y se vende como **creative technologist**:
experiencias de producto en tiempo real, AR y VR, construidas de punta a punta. Sitios,
software y decks pasan a ser **rango de apoyo**, no la oferta.
Todo lo que abajo hable de Shopify, Klaviyo o «storefronts» como público es HISTORIA del
papel, no copy vigente. La palabra «storefront» solo sobrevive donde nombra la pieza de
UdV, que se llama así.
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
     anuncio). ⚠️ **SUPERSEDIDO EL 2026-08-18 — el sitio ya NO es noindex entero.** Carlos
     decidió, sobre el riesgo puesto por escrito: se indexan **la home Y la página del caso
     LG** («tras una buena llamada lo primero que hace un productor es buscar tu nombre»).
     Todo lo demás sigue fuera, **incluido el embed `live/` de LG** — indexar la experiencia
     con marca LG sería peor que indexar el caso que la enmarca con sus deslindes. Detalle
     y puerta en § El pase del 2026-08-18.
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

- **Un scroll + páginas satélite.** Orden vigente desde el 2026-08-18:
  **01 LG · 02 Augmented reality (UDV Blue) · 03 How I work · 04 Reasoned redesigns ·
  05 Range · 06 The principal · 07 Contact.** Las DOS pruebas interactivas van primero y el
  método sube DELANTE de la obra web estática: antes había catorce piezas estáticas entre
  medias y para un comprador experiencial eso diluye. LG y cada rediseño tier-1 tienen **página
  propia**; el embed de LG (~25 MB) **JAMÁS carga en la home** — entra por su gate (§ Kit LG).
- **El aparato de nota al pie es la interacción-firma del sitio** (aceptado por Carlos). Las
  afirmaciones llevan marcador; el marcador abre el razonamiento escrito. **El compromiso que
  trae:** toda página de caso DEBE sus anotaciones — una página de caso sin anotar se lee rota.
- **Contacto: formulario + `hello@reasonedweb.com`.** ✅ MX verificado 2026-08-16; correo
  impreso en contacto y en los 7 pies — ⛔ **IMPRESO, JAMÁS ENLAZADO** (orden de Carlos,
  2026-08-17: «nadie usa esa forma de mandar emails»). Cero `mailto:` en todo el sitio; la
  dirección va en `.correo` con `user-select: all` para que un toque largo la copie entera.
  **TODA puerta de contacto lleva al formulario**: el CTA de la barra en las 7 páginas (las 6
  de caso lo ganaron el 17 — antes, desde un caso, no se llegaba al formulario sin bajar
  5.000 px), el de los 8 pies (`.pie-acciones`) y el del 404. **El formulario ENVÍA de verdad (2026-08-16): endpoint
  propio `site/api/contact.js` (función Vercel) → Resend**, clave SOLO en env vars de Vercel
  (`RESEND_API_KEY`; opcionales `CONTACT_TO`/`CONTACT_FROM`). Campos que Carlos exige del
  prospecto: nombre, work email, agencia, ROL, TELÉFONO (+ ships opcional y mensaje); honeypot
  `website`; reply-to = el email del visitante. **Degradación honesta verificada**: si la
  clave no está o Resend falla, el frontend LO DICE, NO borra lo escrito y da la dirección
  para copiarla — jamás un «enviado» falso. ⛔ Ya **no** abre un compositor mailto (2026-08-17);
  lo que no se negocia es que nunca finja un envío. ⛔ El endpoint es propio de este proyecto — jamás compartido con nada de
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
3. ⛔ **ANULADOS los puntos 3 y 4 el 2026-08-18** (set de comercio UdV y outreach a
   Shopify/Klaviyo Partners): «those don't pay what I need». Lo que ocupa su lugar es
   **subir una pieza de VR** — hoy es la única etiqueta del hero sin nada detrás — y luego
   outreach a agencias experienciales, constructores de stands y equipos de brand
   experience. La regla de fondo NO cambia: **ni un correo a un segmento antes de que exista
   la pieza que lo justifica**, porque cada prospecto abre una sola vez.

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

## § Pase de diseño del 2026-08-17 — decisiones que ya no se re-discuten

Ocho puntos aprobados por Carlos de una revisión pensada para el ojo de OTRO diseñador
(es el público: agencias, Shopify Partners, Klaviyo Partners). Lo que quedó fijado:

1. **EL APARATO VIVE EN EL MARGEN (≥72rem).** El defecto más visible del sitio era que en
   escritorio la columna derecha estaba vacía a lo largo de miles de píxeles en cada página
   de caso. La solución no fue rellenar: fue mover ahí lo que ya era el diferencial. La nota
   flota a la derecha, SIEMPRE visible, a la altura del bloque que hace la afirmación; el
   marcador `[n]` sigue vivo y la DESTACA. Tres estados y ninguno pierde el porqué: sin JS
   todas visibles al pie de sección · angosto plegadas · ancho al margen.
   ⛔ **Regla dura descubierta midiendo:** el margen es SOLO para secciones de texto. Un
   contenedor de rejilla nunca se solapa con un flotante — se empuja debajo —, así que una
   nota alta junto a una galería abría un hueco vertical de su mismo alto (la home creció
   1.200 px la primera vez). `apparatus.js` lo decide solo: `conMargen(caja)` niega el margen
   a cualquier caja que contenga `.cards`, `.mosaico`, `.case-lead` o `.persona`. Si mañana
   una sección gana una galería, deja de usar el margen sin que nadie lo recuerde.
2. **FIGURAS DE EVIDENCIA — el caso que mide, enseña la medida.** Empezadas en UdV, que es
   la plantilla: el gráfico de unidades de las 270 instrucciones de color (237 celdas VACÍAS
   contra 33 LLENAS) y la paleta muestreada con procedencia y ratio medido de cada valor.
   ⛔ Dibujadas a mano en HTML/SVG, jamás capturas: nítidas a cualquier resolución, 0 KB de
   imagen, legibles por lector de pantalla, y **cada hexadecimal sale del CSS de la propia
   pieza** (`piece/index.html`), donde cada token viaja con el objeto del que se muestreó.
   `tools/evidencia.py` + `tools/evidencia_datos.py` VERIFICAN cada valor contra los fuentes
   declarados del caso antes de escribir: si un valor se mueve allá, la figura falla acá en
   vez de mentir. **COMPLETADO el 2026-08-17: los cinco casos tienen figura** (52 valores
   verificados). Una figura por caso, cada una de una FORMA distinta, porque cada caso prueba
   algo distinto — repetir la plantilla cinco veces demostraría plantilla, no rango:
   · **UdV** — el conteo (270 celdas: 237 vacías, 33 llenas) + la paleta muestreada.
   · **Smoothies** — las cinco parejas: el cartón como está fotografiado y ese MISMO matiz al
     peso que aguanta texto encima. El segundo valor se DERIVA del primero, no se elige al
     lado. Fuente: `piece/index.html`.
   · **Nanntu** — la paleta con RECIBOS: el dominante exacto de su logotipo (213 364 px), el
     cian de la firma de sus correos, el verde de Un Árbol Una Vida, el sillar de Arequipa, la
     teja. Cada ratio medido contra el fondo real. Es la mejor procedencia del portafolio.
   · **Woods & Co** — el LIBRO MAYOR: lo mirado → lo que salió de mirarlo (diez tiles clicados
     uno a uno, el Instagram vacío de 36 px, los dos bios apagados en el código, 30 de 31 logos
     ya transparentes, los campos de contacto a 1.04:1). La firma vende afirmaciones que
     resisten comprobación; el diagnóstico se hizo igual. Fuentes: la pieza Y la prosa del caso.
   · **LG** — la TUBERÍA CAD→web en cuatro etapas con la medida en cada extremo (STEP →
     FreeCAD por costuras reales, nunca por un plano → Blender, cada concha cerrada decimada
     entera → gltf-transform Draco+WebP). Fuentes: `LG-Demo/3D_assets/CONVERSION-LOG.md` y
     `context/09-STATUS.md`. **LG no tiene `piece/`: su pieza es el build de `live/`.**

   ⚠️ **DOS CIFRAS PUBLICADAS SE CORRIGIERON al construir estas figuras** — las dos salieron de
   ir a la fuente, que es exactamente para lo que sirve el mecanismo:
   1. **La puerta de LG decía «about 25 MB».** Los 25 MB eran el PRESUPUESTO de rendimiento
      (`06-ROADMAP-V2.md`, `11-COMPLETION-CHECKLIST.md`), no lo medido: `09-STATUS.md` cierra
      en «Package 22.8 → 19.6 MB» y `live/` mide 20 MB en disco (medido hoy). Ahora dice
      **19.6 MB**, y la figura repite la misma cifra — un número distinto en cada sitio de la
      misma página es peor que ninguno.
   2. **La home decía «146k triangles at 1.07 MB»** como si fuera el modelo entero. Esa cifra
      es del **M7 satélite ANTES de comprimir** (`CONVERSION-LOG.md`: ~1,07 MB · ~146k tris;
      después baja a 446 KB). En la home el bullet pasa a «3D built from LG's own STEP CAD
      files, published as Draco glTF» — cierto sin número; el número, CON su contexto, vive en
      la figura del caso. ⛔ Lección: una cifra correcta en un sitio se vuelve falsa al mudarla
      a otro sin su contexto.
   ⛔ **Vacío frente a lleno, no un gris frente a otro:** ningún tercer color puede estar a
   3:1 del grafito Y del papel a la vez (medido: imposible por aritmética de luminancia), así
   que la distinción la lleva la FORMA — que además dice lo que hay que decir. Los chips de
   la paleta llevan borde `--carton-borde` #6F746F (4.32:1 sobre papel) porque un chip claro
   no se delimita solo (WCAG 1.4.11).
3. **`text-wrap: balance`** en h1/h2/h3 y la tesis; `pretty` en párrafos, li y figcaption.
   Los títulos dejaban huérfanas («…the face does / not»).
4. **El máster ocupa su medida** (min(46rem,100%) en ≥72rem) y **el filete de la derivación
   pasa a ser del máster**: con la marca a 46rem un subrayado de 46ch quedaba corto y suelto.
5. **Range en cuatro columnas** (≥72rem): ocho verticales en tres columnas dejaban una fila
   huérfana de dos. La banda del corpus (`card--wide`) cierra la sección a todo el ancho.
6. **Anclas de sección en la nav** (Work · Redesigns · Range · Method · Principal), ocultas
   bajo 62rem — el CTA basta y la barra tiene que caber entera a 320 px.
7. ⚠️ **EL FORMULARIO PIDE MENOS — enmienda a la regla anterior.** Obligatorios: nombre,
   work email, agencia y mensaje. **ROL y TELÉFONO pasaron a OPCIONALES** (aprobado por
   Carlos el 2026-08-17; deroga «campos que Carlos exige» de § Arquitectura). Seis campos
   obligatorios para un primer hola cuestan respuestas. El teléfono se pide solo a quien
   prefiera que lo llamen. ⛔ `api/contact.js` exige la MISMA lista que `apparatus.js` — si
   se separan, el envío devuelve 400 y el frontend cae al mailto sin motivo.
8. **Detalle:** los bullets de LG hablan a un diseñador (el CAD lleva sus 146k triángulos a
   1,07 MB; «Installation and user manuals» dejó su sitio a la vista explosionada con seis
   hotspots verificados). El revelado de imágenes dispara ANTES de entrar en pantalla
   (`rootMargin` 12% positivo abajo): el defecto era el momento del disparo, no el peso —
   por eso NO se quitó `loading="lazy"`, que habría deshecho el trabajo de rendimiento.

**Medido después del pase**, con las herramientas del propio sitio: `auditar.py` sobre
`/`, UdV, LG y one-system a 320/768/1440 → **0 hallazgos, 0 no-medibles**, y a 1440 escanea
MÁS elementos que a 768 (las notas al margen), que es la prueba de que se están midiendo.
Cero desbordes horizontales. La home pasó de 8.136 a 8.393 px (+257, no +1.200) y UdV de
5.593 a 6.911 px — ese crecimiento son las dos figuras de evidencia, no huecos.

## § Revisión de copy del 2026-08-17 — la página se lee con ojos de comprador

⚠️⚠️ **SECCIÓN HISTÓRICA — sus puntos 1 y 2 quedaron SUPERSEDIDOS el 2026-08-18** por el
cambio de público (fuera Shopify y Klaviyo). Se conserva porque explica POR QUÉ se
escribieron aquellas frases, y ese razonamiento sigue siendo válido aunque el destinatario
haya cambiado. Los puntos 3 y 4 siguen vigentes.

Repaso final de la home leída como la leería el director de una agencia decidiendo si lo
contrata. Lo que cambió, y por qué, para que no se re-discuta:

1. ⚠️ **LA TESIS NOMBRA EL COMERCIO EN LA PRIMERA LÍNEA** (aprobado por Carlos, 17/08):
   «Sites **and storefronts**, immersive products, and software end to end…». El público
   elegido son agencias, **Shopify Partners** y **Klaviyo Partners**, y la palabra
   «storefront» no aparecía hasta el pie: un socio de Shopify escanea seis segundos y no
   encontraba motivo para seguir. Es cierto desde el encargo de Ulric de Varens. La `<meta
   name="description">` lleva la MISMA frase — si se separan, el unfurl contradice a la
   página. Enmienda las capacidades que Carlos fijó el 17 por la mañana: solo se AÑADE, el
   orden y el resto del listado se respetan.
2. ⚠️ **LA LÍNEA DE CONTACTO DECLARA LA OFERTA, NO LA CLIENTELA** (aprobado por Carlos,
   17/08). Decía «Web design agencies and Shopify and Klaviyo partners **hire me**…», que
   leído literal afirma una cartera de agencias que hoy no se puede nombrar: el único cliente
   nombrable en la página es Ulric de Varens. Ahora: *«The work I take on: embedded senior
   web design for agencies, Shopify Partners and Klaviyo Partners — the sites and storefronts
   you deliver, designed and built. Contract or full-time.»* Misma fuerza, y **aguanta que el
   director creativo pregunte «¿qué agencias?»** — que es exactamente la prueba que el resto
   del sitio se impone. «Partners» va en mayúscula: así se llaman los dos programas, y
   decirlo bien es señal de conocer el ecosistema al que se escribe. La palabra «hire» sigue
   permitida (punto 7 del pase de diseño); lo que se retira es la afirmación de clientela.
3. **El pie ya no dice «Personal portfolio».** Era la última línea que lee un director
   creativo y degradaba todo lo anterior — la página entera se vende como estudio. El aviso
   de no-indexación se mantiene (es orden de Carlos) sin el diminutivo: *«A private showcase,
   deliberately kept out of search results — no sitemap, noindex on every page. It reaches
   the people I send it to.»* Y así el aviso además TRABAJA: explica por qué un sitio que
   vende webs optimizadas para buscadores no tiene huella en ellos. En las 7 páginas.
4. **Errata corregida en la nota [7]**, la que se titula «The record, checkable»: una frase
   empezaba en minúscula. En esa nota concreta una errata cuesta más que en ninguna otra.

⛔ **LOS RECIBOS CADUCAN — SIGUEN SIN RE-SELLAR (al 2026-08-19).** El párrafo `.receipts`
sigue diciendo «272 measured elements» y es de antes de TODO lo de estos dos días. Hoy
`auditar.py` mide muchos más elementos y hay tres puertas nuevas. **Carlos tiene que decir
con qué regla se contaron los 272** para reformularlo en su misma forma; cambiar un número
publicado por otro con distinta definición es peor que dejarlo. Contexto original: El párrafo
`.receipts` («Lighthouse 100·100·100 desktop, 97 mobile · 0 AA contrast failures across 272
measured elements · 0 layout shift») está fechado el 2026-08-16 y es anterior a TODO lo de
esta tanda. Estado real medido el 17:
  · **«272 measured elements» ya no describe el sitio.** `auditar.py` sobre las 7 páginas a
    320/768/1440 da hoy **0 fallos sobre 1.320 elementos-ancho**. ⛔ No se reescribió el
    número: no se pudo reconstruir con qué regla se contaron los 272, y cambiar un número
    publicado por otro con distinta definición es peor que dejarlo. **Carlos dice la regla
    y se reformula en su misma forma.**
  · **«0 layout shift»**: el informe de Lighthouse que trajo Carlos daba CLS **0,246** —
    era la Switzer Semibold llegando tarde (sin precargar). Con la precarga puesta mide
    **0,000–0,020** en local. La afirmación vuelve a ser cierta EN CUANTO SE DESPLIEGUE.
  · **Los 100 de Lighthouse** se midieron antes del trabajo de imágenes, caché y fuentes.
    La nota [6] promete «re-measured after every change that could move it»: esa promesa es
    parte de lo que se vende, así que se re-mide contra la URL desplegada y se re-fecha.

**Lo que NO se toca** (queda dicho para que nadie lo «mejore»): «I build the work you sell»;
«You bring the work you've sold; I produce it — design and build — under your flag or mine»
con su nota [5] del white-label acordado por escrito; la nota [2] de LG, que convierte un
deslinde legal en argumento de venta («a portfolio that blurs that line deserves the distrust
it gets»); la nota [3] del material público con oferta de retirada permanente; y **el 97 de
móvil de la nota [6]** — publicar POR QUÉ es 97 en vez de redondear a 100 es lo que hace
creíbles los demás números.

## Reglas de operación vigentes (no re-aprender)

1. **Push**: las sesiones COMMITEAN (`-F archivo` + `--only -- rutas`) y, ⚠️ **desde el
   2026-09-03, también EMPUJAN** — Carlos abrió el permiso al pedir que el proyecto de decks
   pudiera publicar aquí sin pasar por él. El permiso vive en `~/.claude/settings.json`
   (`permissions.allow`: `Bash(git push:*)` y `Bash(ARRASTRE_OK=1 git push:*)`) y es GLOBAL,
   no por repositorio: una regla de Bash se define por comando, así que no se puede acotar a
   este repo. Para revocarlo, quitar esas dos entradas.
   **La puerta de arrastre sigue en pie y sigue siendo el control real**: `githooks/pre-push`
   nombra cada commit firmado por otra sesión y se niega a publicarlo sin `ARRASTRE_OK=1`. Un
   push de commits propios de la sesión pasa solo; adoptar los de otra sesión sigue siendo un
   acto explícito. Carlos, desde su shell, cuenta como `humano` y necesita `ARRASTRE_OK=1`
   para publicar commits `claude:*`: `$env:ARRASTRE_OK="1"; git push`.
   ⚠️ Lo anterior decía que el push no-interactivo fallaba con «Cannot prompt». Ya no: el
   credential manager tiene la credencial de github.com en caché (comprobado con
   `git credential fill`, y el fetch de este repo PRIVADO se autentica sin pedir nada), así
   que una sesión empuja sin consola interactiva. `gh` además está logueado como `go3601981`
   con scope `repo`, por si hiciera falta `gh auth setup-git`.
   Vercel auto-deploya cada push en <1 min.
2. ⛔ **Posicionamiento (regla dura de Carlos, refinada 2026-08-17)**: JAMÁS pintarlo
   trabajando para varias agencias a la vez, y la exclusividad JAMÁS se dice explícita
   («One partner at a time» se retiró — contar clientes suena a necesidad). Implícita en:
   «Dedicated», «Embedded, end to end», «Check availability», «one product, one team».
   Vetados: «retainer», vocabulario freelance/consultor, «Open to work».
   CTA canónico: «Check availability».
   ⚠️ **La línea de contacto se REESCRIBIÓ el 2026-08-18.** Vigente: «The work I take on:
   embedded creative technology for experiential agencies, exhibit builders and
   brand-experience teams — the interactive you have sold, designed and built. Contract or
   full-time, US hours.» (clase `.contrato`). La versión de 2026-08-17 que nombraba Shopify
   y Klaviyo Partners y usaba «hire me» quedó SUPERSEDIDA con el cambio de público.
   Sigue vetado el «Hire me» como CTA o título, y «Open to work». CTA del hero: «Check
   availability».
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

## Aviso de no-indexación — REESCRITO EL 2026-08-18

Carlos pidió que el sitio DIGA que es personal y que no está hecho para buscadores. Esa
frase **pasó a ser falsa en la home y en LG** cuando se decidió indexarlas, así que hay
TRES versiones y cada una es cierta donde está:
- **home**: «The work behind this page — every case study and every live exhibit — is
  deliberately kept out of search results…»
- **casos no indexados**: «This page is deliberately kept out of search results…»
- **página de LG**: habla de los conceptos no solicitados, que son los que siguen a oscuras.

⛔ La lección: al cambiar la indexación hay que cambiar el aviso EN EL MISMO MOVIMIENTO. Una
página que afirma no estar indexada mientras se indexa se desmiente a sí misma, y es el tipo
de contradicción que este sitio existe para no cometer.

## Rendimiento — reglas fijadas tras el Lighthouse del 2026-08-17

- **Cada `img.shot` viaja en TRES anchos: `-720`, `-1080` y el completo** (1440, o 1600 en LG),
  y el descriptor `w` dice el ancho REAL del archivo (LG es 1600w, no 1440w). Sin el 1080, el
  móvil de Lighthouse (412 px × DPR 1.75 = 721 px) saltaba del 720 al 1440 completo — 329 KiB
  de más en la home. Al capturar una pieza nueva se generan los tres (PIL, LANCZOS, q80).
- **`sizes` dice el ancho REAL de la columna, no «50vw»**: dentro de `.wrap` (72rem − 2×3rem
  = 66rem) las 2 columnas miden 32rem, las 3 de Range 21rem, el lead de LG 38rem, la banda
  del corpus/catálogo 34–36rem; en móvil `90vw` (el padding es 5vw por lado). Verificado con
  Playwright a 412@1.75, 1350@1 y 1440@2: el navegador elige siempre el candidato justo.
- **Precarga de fuentes = TODOS los pesos que pinta el above-the-fold**: Semibold (600 —
  kicker, h3, label, botones) faltaba y era el culpable de CLS nombrado por Lighthouse.
- **Caché**: fuentes `max-age=31536000, immutable` (una fuente nueva = un archivo nuevo);
  imágenes 30 días (`2592000`) — no un año, porque las capturas se regeneran con el mismo
  nombre y un año de caché en el navegador del visitante sería un año de captura vieja.
- Lo que se dejó a propósito: `site.css` (4.5 KiB) sigue como hoja externa render-blocking
  (10 ms estimados). Inlinearla en 7 páginas es deuda de mantenimiento por 10 ms.

## § Móvil — el pase del 2026-08-17 (tarde)

- **MENÚ MÓVIL.** Bajo 62rem las anclas de sección eran `display:none`: en móvil el sitio no
  tenía navegación. Ahora viven tras un botón, con los MISMOS tres estados que el aparato de
  notas — sin JS apiladas y sin botón (un control muerto es peor que ninguno) · angosto
  plegadas · ≥62rem en línea. ⛔ **El panel es una fila más de la barra (`flex-basis: 100%`),
  no una capa flotante**: empuja el contenido, así no hay scroll que bloquear ni forma de
  dejar a nadie atrapado. El orden del DOM es el visual en los dos estados → el foco no salta.
  El icono se deriva de la retícula del glifo (m=12 en lienzo de 100; al abrir, las barras 1 y
  3 recorren los 24u = 2m exactos hasta el centro).
- **Ocho hallazgos medidos y cerrados** (`verificar_hallazgos.py`, una puerta por hallazgo:
  16 vistas, 204 interactivos, 588 pares, 914 nodos de texto, 60 marcadores, 12 campos →
  0 fallos). Los que dejan regla:
  · **El área de toque crece, el marcador no.** Los `[n]` medían 24×27,7 px. Un pseudo-elemento
    los lleva a 44×44 **solo bajo 62rem**: en escritorio un área invisible de 44 px le robaría
    el click a un enlace vecino. La puerta comprueba las dos caras — que el área responde a
    21 px del centro Y que ningún marcador roba el punto central de otro control.
  · **`min-height`, no `padding`, para el lockup** (medía 16,38 px de alto): el SVG escala con
    el viewport y un padding fijo se quedaba corto justo a 320.
  · **El corpus caía a UNA columna a 320** (`minmax(150px)` no entra dos veces en 288 px de
    contenido): 11.619 px de alto. Con 130 px caben dos → 5.396 px medidos. De 13,8 pantallas
    a 6,4.
  · Texto: nada por debajo de 12 px (los rótulos del libro mayor de Woods estaban a 11,52) y
    las **etiquetas honestas** a 0.85rem — eran el texto más pequeño de la página siendo el
    que la regla 1 declara no negociable.
- ⚠️ **El CTA medía 43,91 px de alto** — 0,09 bajo los 44 de diana táctil. No se ve a ojo; lo
  encontró la puerta. `padding-block` 0.55 → 0.6rem.
- **Lección del instrumento, dos veces en la misma tarde:** `elementFromPoint` solo ve el
  viewport (hay que desplazar el elemento antes de preguntar), y `scroll-behavior: smooth`
  hace ASÍNCRONO a `scrollIntoView` — sin `behavior: 'instant'` la sonda mide a mitad del
  desplazamiento y reporta un fallo que no existe.

## § EL PASE DEL 2026-08-18/19 — el giro a creative technologist

Lo que Carlos pidió y lo que quedó. **Esto manda sobre cualquier cosa anterior que lo
contradiga.**

### El posicionamiento
- **Tesis del hero:** *«I build the interactive that wins the room — real-time product
  experiences, AR and VR, built end to end for your agency. Sites, software and the decks that
  carry them come with it, and every piece ships with its reasoning written down.»*
  `<title>`, `description` y `og:*` llevan la MISMA frase: si se separan, el unfurl
  contradice a la página.
- **Línea de contacto:** *«The work I take on: embedded creative technology for experiential
  agencies, exhibit builders and brand-experience teams — the interactive you have sold,
  designed and built. Contract or full-time, US hours.»* «US hours» es nuevo y trabaja:
  desde Lima, quita la objeción antes de que la piensen.
- ⛔ **NO se puso «One embedded engagement at a time»**: es «One partner at a time» con otras
  palabras, y Carlos la retiró en su día porque contar clientes suena a necesidad. La
  exclusividad sigue siendo IMPLÍCITA.
- **Etiquetas escaneables en el hero** (`.capacidades`): Three.js/WebGL · Real-time 3D · AR ·
  VR · glTF/Draco · Binaural HRTF · CAD→web. Un productor mira diez segundos; la prosa no
  sobrevive a eso.
  ⚠️ **Fuera, por no tener pieza que las sostenga:** **WebXR** (todas sus apariciones están
  dentro de `node_modules/three`, ninguna en código propio de Carlos), **WebAR con motor**
  (8thwall quedó en `legacy/`, la AR viva es entrega nativa al visor del sistema) y **kiosk**
  (solo una línea sugerida en el manual de LG). Carlos lo confirmó.
  ⚠️ **VR es la única etiqueta sin pieza en el sitio.** Se publica porque Carlos lleva años
  haciendo AR/VR en Next Latam y pidió nombrarlo sin ocupar sitio. Se cierra en cuanto suba
  uno de sus vídeos (ver Pendientes).

### La demo de 48 horas, y su prueba
Bloque propio (`.oferta`) cerrando «How I work». ⛔ **El texto es de la sesión, no de Carlos**
— es una promesa pública y tiene que leerla antes de dar por buena.
La acompaña la única cifra que el papel sostiene: *«the five-chapter LG Sound Suite experience
went from first working build to feature-complete and walkable in **eight days**»* (15→23 de
junio de 2026, con sesiones fechadas los días 15, 16, 17, 18, 19, 21 y 23).
⛔ **NO dice «de concepto a build»**, que es lo que se pidió: en los documentos de LG **no
existe fecha de arranque**, y el tramo completo contiene una pausa declarada. La nota [5] lo
dice con esas palabras, incluido que no se inventa un kickoff para que el número luzca mejor.
⛔ **Del estado del proyecto LG no sale NADA publicado** (orden de Carlos, 2026-08-18: «with
LG we are still negotiating; try not to mention any of the status»).

### El correo, y todas las puertas al formulario
⛔ **La dirección se IMPRIME pero JAMÁS se enlaza** (orden de Carlos: «nadie usa esa forma de
mandar emails»). Cero `mailto:` en el sitio. Va en `.correo` con `user-select: all` — un toque
largo la copia entera. **Toda ruta de contacto lleva al formulario**: CTA en la barra de las 7
páginas, en los 8 pies y en el 404.
**La caída del formulario ya no abre un compositor**: si `/api/contact` falla, lo dice, NO
borra lo escrito y da la dirección. Lo que no se negocia sigue igual: jamás un «enviado» falso.

### El formulario entra en una pantalla
Reportado por Carlos con captura. Dos causas medidas: `label { display: grid }` convertía cada
`(optional)` en una FILA propia (tres campos opcionales = tres renglones de aire), y la oferta
de 48h ocupaba 194 px DENTRO de Contact. De **1.076 px a 739 px**, medido pulsando el CTA de
verdad. Entra completo con viewport ≥ 760 px — lo que deja una pantalla de 1440×900 con la
barra del navegador. Por debajo no entra y con siete campos no hay recorte razonable.

### El menú móvil
Bajo 62rem las anclas eran `display:none`: en móvil no había navegación. Ahora viven tras un
botón, con los MISMOS tres estados que el aparato de notas (sin JS apiladas y sin botón ·
angosto plegadas · ≥62rem en línea). ⛔ **El panel es una fila más de la barra
(`flex-basis: 100%`), no una capa flotante**: empuja el contenido, así no hay scroll que
bloquear ni forma de dejar a nadie atrapado. El icono se deriva de la retícula del glifo.

### El vídeo: se hizo, se publicó y SE QUITÓ
Se grabó un walkthrough de 76 s de LG Sound Suite y se montó en la home. **Carlos lo retiró al
día siguiente, y el argumento manda: «a muted video doesn't help at all when LG is all about
sound».** Un vídeo mudo de una pieza cuya tesis es el sonido espacial no la demuestra: la
CONTRADICE. Y el embudo correcto ya existía — la captura lleva al caso, el caso al gate, y el
gate PIDE AURICULARES.
⛔ **Esta es la SEGUNDA vez que un vídeo entra y sale del sitio.** Antes de proponer otro, que
el silencio no contradiga la pieza. `tools/grabar.py` y su guion quedan **en reserva**, sin
usar — igual que `record.py`.

### Los vídeos de VR/AR de Next Latam (conversación del 19, sin ejecutar)
Next Latam es empresa de Carlos y el trabajo creativo es suyo: **puede publicarlos**, y suben
como trabajo SUYO — el sitio sigue sin nombrar la empresa porque no le hace falta, no porque
haya problema. Lo único vivo: si en un vídeo aparece marca, producto o metraje de un cliente
final, ese permiso es del cliente.
Acordado: **dos, tres a lo sumo**, en la sección 02 ampliada a «Augmented and virtual
reality», **self-host, NO YouTube incrustado**.
⚠️ **El ancho de banda NO es el problema, medido**: la home entera son 0,25 MB por visita y la
página de LG 0,13 MB; el embed de LG son 20 MB y UDV Blue 21 MB. **Una sola persona que abre
la experiencia de LG consume más que cinco viendo tres vídeos enteros.** Con `preload="none"`
un vídeo no baja un byte hasta que le dan al play. Lo que YouTube sí cuesta: mete su marca en
la página, planta cookies donde hoy no hay ninguna, carga ~1 MB de scripts que se lleva el
recibo de «sin framework», y un canal público es indexable.
**Punto medio acordado: YouTube NO LISTADO como copia reenviable, y `<video>` propio en la
web.** Si algún día el tráfico crece, el paso es CDN/almacenamiento de objetos con la misma
etiqueta `<video>`, nunca un iframe de YouTube.

### Herramientas nuevas — CORRER ANTES DE CADA PUSH
| | |
|---|---|
| `tools/verificar_assets.py` | Todo lo que el HTML pide existe, pesa y **git lo sigue**. Nació porque 15 imágenes `-1080` estaban en disco y no en el repo: en local perfecto, en producción 404 |
| `tools/verificar_indexacion.py` | Cabecera y `<meta robots>` dicen lo mismo, y el sitemap coincide. Cabecera ausente = FALLA; meta ausente = se cuenta y se nombra |
| `tools/verificar_maqueta.py` | Nada con texto se sale de su columna, y **las notas al pie cuelgan del `.wrap`** |
| `tools/marca_png.py` | La marca en PNG con alfa para sobreimprimir en vídeo (`brand/png/`, no se despliega) |
| `tools/grabar.py` + guion | Vídeo de una pieza INTERACTIVA conducida por guion. **En reserva** |
`exhibir.py` creció: escanea TODO el árbol del exhibit (no solo el HTML), `--sub`, `--qr`,
`--assets` acepta ficheros sueltos, `--label-after`, e inyecta `noindex` si la pieza no lo trae.

### ⛔ Lecciones que costaron tiempo — no re-aprender
1. **Un QR es un residuo ilegible.** El exhibit de UDV publicó un `qr-target.json` y un
   `qr.png` que mandaban a `eureka.pe` — dominio PROHIBIDO — porque la puerta de `exhibir.py`
   solo escaneaba el HTML. Ahora escanea todo el árbol, y `--qr` regenera el PNG.
2. **Escanear un binario comprimido como texto da falsos positivos GARANTIZADOS.** `$96` y
   `$29` aparecen en el ruido de cualquier `.glb`. En binarios se buscan solo los patrones de
   MARCA, y sobre las cadenas imprimibles largas, como haría `strings`.
3. **`elementFromPoint` solo ve el viewport**, y **`scroll-behavior: smooth` hace ASÍNCRONO a
   `scrollIntoView`**: sin `behavior:'instant'` la sonda mide a mitad del desplazamiento y
   reporta fallos que no existen.
4. ⛔⛔ **LOS PARCHES LARGOS VAN POR FICHERO, NUNCA POR HEREDOC DE BASH.** Cuatro veces esta
   sesión el heredoc se comió un escape (`\n`, `\'`) y dejó un `.py` sin compilar. Se escribe
   el script con la herramienta de ficheros y se ejecuta.
5. **Medir «no se sale» no es medir «está donde toca».** La nota [5] flotaba DENTRO del
   recuadro de la oferta y ninguna puerta lo vio: el texto estaba dentro de su columna.
6. **Lo que se despliega es lo commiteado, no lo que hay en la carpeta.**

## § EL PASE DE CONVERSIÓN DEL 2026-09-06 — la home deja de hablarle a un ingeniero

Carlos: «the site is not helping me convert. My target are people looking to build decks
for interactive experiences and for beauty and wellness, they are not technical, but there
is plenty of technical jargon». Pidió auditoría de copy **y de estructura** («organize my
work differently if you like»). **Esto manda sobre lo que lo contradiga arriba.**

### Lo que se midió antes de tocar nada
`scratchpad/auditar_copy.py` (no vive en el repo; se rehace si hace falta) sobre los 78
bloques de texto visible de la home: **52 apariciones de jerga** en cuatro familias,
**grado Flesch–Kincaid 10.9** (el copy que convierte vive en 7–8) y **10 frases de más de
30 palabras**. Después del pase: **26 apariciones — y casi todas dentro de las notas al
pie**, grado **9.8**, y las 5 frases largas que quedan están TODAS en notas. Las páginas de
caso ya estaban limpias (2–4 apariciones); el problema estaba concentrado en la home.

### El hallazgo que manda: es un estudio de belleza que no dice «belleza»
**8 de las 12 piezas destacadas** de la home son fragancia, cosmética, belleza o bienestar
(Sauvage, las cuatro de Ulric de Varens, Smoothies, L'Oréal, Woods & Co) — 10 de 14 si se
cuentan FLUENCE e Iron Island en Range. Las palabras «beauty» y «wellness» aparecían
**dos veces**, las dos dentro del título de una pieza o de un `alt`. Nunca como
posicionamiento. No hacía falta obra nueva: hacía falta nombrar la que ya había.

### Lo que cambió
- **Tesis nueva** (y `title`, `description` y `og:*` con ella, por la regla de siempre):
  *«I build the pitch that wins the work: interactive decks and live demos for beauty,
  wellness and experience brands. Every piece arrives finished, with the reasoning behind
  each decision written down.»*
- **Las etiquetas del hero dejan de ser de ingeniería.** Fuera Three.js/WebGL, glTF/Draco,
  Binaural HRTF, CAD→web. Dentro: Interactive decks · 3D product demos · Augmented reality ·
  Beauty & wellness · Live events & booths · English & Spanish. Lo técnico NO se borró: vive
  en las páginas de caso y en la bio, que es donde lo busca quien sabe leerlo.
- **La derivación del logo BAJA** debajo de la tesis y las etiquetas. Sigue en la página —
  es la mejor prueba de cómo se piensa aquí — pero ya no es la primera pared que ve un
  comprador de belleza. El filete sigue siendo del máster.
- **Orden nuevo, ocho secciones (⚠️ NUEVE desde el 2026-09-19: entró 03 · Film — ver § Film en la home):** 01 Pitch decks · 02 Live experiences (Sauvage + UDV Blue
  AR) · 03 A full production (LG) · 04 How it works · 05 Brand and web work · 06 More range ·
  07 Who you would work with · 08 Start.
  ⛔ **LG deja el primer puesto.** Sigue siendo la credencial más fuerte, pero es un caso de
  audio de electrónica de consumo y era la primera impresión para quien viene por fragancia.
- ⛔ **«Reasoned redesigns» desaparece como titular.** Dejó de describir su contenido el día
  que los decks se archivaron ahí dentro. Ahora es «Brand and web work / Four brands, rebuilt
  from the evidence» — y son cuatro negocios de verdad (UdV, Smoothies, Woods & Co, Nanntu).
- **Los recibos suben a lenguaje de comprador y los números BAJAN a la nota [4]**: arriba
  queda «loads fast on a phone, works for screen readers and holds together at any size — and
  every one of those claims was measured, not assumed». Lighthouse, AA, 272, 320 px y
  «no framework» siguen enteros, a un clic, donde los busca un evaluador técnico.
- ⛔ **La oferta de 48 h ya no dice «not a deck».** Decía *«you get something running in a
  browser on your own phone — not a deck, not a mockup»*: a quien venía a encargar un deck,
  la propia página le decía que su encargo era el artefacto menor. Ahora: «a working piece,
  not a flat mockup».
- **Menú en lengua de visitante:** Decks · Experiences · How it works · Brand work · About.
  «AR», «Range» y «Principal» eran nombres internos.
- **Línea de contacto:** *«interactive decks and demos for beauty, wellness and experience
  brands — and for the agencies that pitch them»*.

### Lo que NO se tocó (y por qué, para que nadie lo «mejore»)
Las **etiquetas honestas** de cada pieza — a un marketero de marca, que vive rodeado de
revisión legal, le leen como integridad; son activo, no lastre. El **aparato de notas**. La
nota de los **ocho días** y su negativa a inventar un kickoff. **Todos los deslindes de LG**.
Y *«You bring the work you've sold; I produce it — design and build — under your flag or
mine»*, que sigue siendo la frase más clara del sitio.

### Lo que esto SUPERSEDE
1. ⛔ **«Sitios, software y decks pasan a ser rango de apoyo, no la oferta» (2026-08-18) ya
   no rige: el DECK es la oferta.** Es lo que Carlos pidió vender.
2. El público añade **marcas de belleza y bienestar** a las agencias experienciales.
3. La tesis del 2026-08-18 («I build the interactive that wins the room…») queda como
   historia del papel.

### ⚠️ Lo que sigue abierto
**Quién firma el cheque: ¿la marca de belleza o la agencia que la presenta?** Se preguntó y
no se respondió, así que el copy vigente **nombra a las dos** («…and for the agencies that
pitch them»). Funciona, pero cuesta filo: si Carlos elige marca, la página debería decir
«for your launch» y abrir con L'Oréal y UdV; si elige agencia, vuelve «for your agency» y
manda la promesa white-label. **Es una decisión de una palabra que nadie debe tomar por él.**
Pendiente menor del mismo pase: el aviso del pie sigue diciendo «noindex» en las 8 páginas —
jerga para este comprador, pero es copy con decisión fechada y no se tocó sin orden.

Auditoría completa, con las cifras y los antes/después:
`https://claude.ai/code/artifact/27a9e8b1-3bc9-4929-8651-942043d2a853`

## § FILM EN LA HOME — 2026-09-19 (hecho desde la sesión de Decks, a pedido de Carlos)

Carlos: «with the video link, could you find a good place on reasonedweb.com and embed it there? I have
no examples of AI generated video on that personal portfolio». El enlace era el YouTube del film del
refrigerador LG French Door (`https://www.youtube.com/watch?v=gNsuCu1quCc`, canal de hello@reasonedweb.com).

**Dónde quedó:** sección nueva **03 · Film** («A launch film, made without a shoot») entre Live experiences
y LG Sound Suite. Las secciones pasan a ser NUEVE (LG 04 · How it works 05 · Brand and web work 06 · More
range 07 · Who 08 · Start 09); ancla «Film» en el menú y etiqueta «Product films» en el hero. Sin nota al
pie propia, así que la numeración [1]–[8] de las notas NO se movió.

**Dos choques con reglas vigentes, resueltos a favor de la regla (Carlos puede derogar cualquiera):**
1. **Regla 7 (jamás nombrar AI ni el mecanismo).** El copy no dice AI: dice lo que es cierto y le importa
   al comprador — sin cámara, sin estudio, sin mandar una muestra; cada pieza cotejada con las fotos del
   fabricante; planos que una cámara no puede hacer; medido, no a ojo. No afirma ningún proceso falso.
   Si Carlos quiere la palabra «AI» en el sitio, es decisión suya y deroga la regla 7.
2. **«`<video>` propio, jamás un iframe de YouTube» (acuerdo del 2026-08-19).** Se alojó en el sitio:
   `site/assets/video/lg-french-door-film.mp4` (1080p, CRF 24, 26 MB, faststart). El póster es un ENLACE
   al mp4 con `img` en los tres anchos de siempre; sin JS el navegador abre el archivo, con JS
   `apparatus.js` lo cambia por un `<video>` en su mismo hueco (medido: 614×346 antes y después, sin salto
   de maqueta), con subtítulos en inglés puestos (la locución es en español) y el foco en el reproductor.
   **Hasta el click no se pide un byte de vídeo** (0 peticiones de mp4/vtt al cargar la home). El sitio NO
   enlaza a YouTube: su descripción allá nombra las herramientas, y un enlace es una mención.

**Etiqueta honesta (clase b):** «Unsolicited concept, made for a pitch. Not affiliated with, or commissioned
by, LG Electronics.» ⚠️ Queda junto al caso LG Sound Suite, que es otra cosa (demostración para LG Canada):
las dos etiquetas lo distinguen. Del estado de la negociación con LG sigue sin salir nada.

**Cifras del copy, con su unidad:** «30 pixels off its center» y «within four» son las dos a 1080p (la
primera toma y la final). En LinkedIn/YouTube Carlos publicó «43 px», que es la misma medida en el cuadro
clave de 2752 px: no mezclarlas en un mismo texto.

**Menú:** seis anclas pedían 973 px de barra y un iPad apaisado da 928: entre 62 y 68rem se aprieta el aire
(pide 901). Medido a 1024 px: una sola fila, 27 px de hueco antes del CTA. Por encima de 68rem no cambia nada.

**Puertas corridas antes del push:** `verificar_assets` (33 documentos, 426 referencias, todo en git) ·
`verificar_indexacion` (2 indexables, sitemap coincide) · `verificar_maqueta` (9 secciones, 512 elementos
con texto dentro de su columna) · `auditar` a 320/768/1440 (172/172/182 elementos, 0 hallazgos AA).
⚠️ En Git Bash de Windows hay que exportar `MSYS_NO_PATHCONV=1` o `--paths /` se convierte en
`C:/Program Files/Git/` y las puertas dan VERDE EN VACÍO (escanearon 4 elementos de una URL inválida).
⚠️ `git fetch/push` fallaba con «repository not found»: el gestor de credenciales estaba usando la cuenta
`cmarruffo1982`. Sin tocar la configuración global, funciona con un helper de un solo uso:
`git -c credential.helper= -c credential.helper='!f() { echo username=go3601981; echo "password=$(gh auth token -u go3601981)"; }; f' push`.

**Fuente del film:** `C:\Developer\Videos\lg-gm57spm-hero\out\master-1920x1080.mp4` (proyecto de Decks). Si el
máster cambia, se re-codifica con el mismo nombre (caché de 30 días, como las imágenes). El copy de la
sección lo escribió la sesión: **Carlos tiene que leerlo.**

## § EL FORMULARIO DICE QUÉ FALLA — 2026-09-20

Carlos reportó dos veces «the contact form is not working», con captura. **No estaba roto:
el correo escrito era `sadf` / `safsdfasdf`.** El servidor lo rechazaba con 400 y
`apparatus.js` trataba cualquier respuesta no-ok como caída de red, así que el visitante
leía «the direct send didn't go through — try again in a moment»: **falso, y además
inútil** (esperar no arregla un correo mal tecleado). Su segundo mensaje fijó el encargo:
el aviso ni era claro ni destacaba.

**Lo que rige a partir de ahora:**
1. ⛔ **Un 400 NO es una caída.** El endpoint devuelve el motivo en el cuerpo y el cuerpo se
   lee SIEMPRE. La caída honesta («nothing you wrote was lost…») queda SOLO para lo que de
   verdad falló del lado del servidor: 503 sin clave, 502 de Resend, red muerta. Esa parte
   no se tocó y sigue sin borrar nada de lo escrito.
2. **El aviso nace en el campo, no al pie.** Cada campo validado lleva su `<span
   class="campo-error" id="err-<name>">` y su `aria-describedby`. El resumen al pie
   (`.form-status[data-estado="error"]`) nombra los rótulos VISIBLES de lo que falla —
   «agency or studio», nunca «company», que no está escrito en ninguna parte de la página.
3. ⛔ **El estado visual cuelga de `aria-invalid`, no de una clase paralela.** El CSS es
   `input[aria-invalid="true"]`. Así no existe un estado donde el ojo vea el error y el
   lector de pantalla no. El borde se dobla con `inset box-shadow`, **jamás con
   `border-width`**: engordar el borde movería la caja 1px y el formulario bailaría entero
   al aparecer el primer error.
4. **Un motivo por causa, no «invalid».** El correo tiene ocho: sin @, dos @, nada antes,
   nada después, dominio sin punto, TLD de una letra, acaba en punto, con espacio. Un aviso
   que no dice qué arreglar obliga a adivinar, y quien adivina se va.
5. **Cuándo se revisa importa tanto como el qué.** Al salir de un campo, solo si escribió
   algo (pasar de largo por un campo vacío no merece regaño) · después del primer intento de
   envío, siempre · mientras teclea, SOLO para borrar una marca ya puesta: nunca se estrena
   un error a mitad de palabra, porque «carlos@» está mal y a la vez va camino de estar bien.
6. ⛔ **EL TELÉFONO AVISA, NO BLOQUEA** (orden de Carlos el mismo día, derogando lo que la
   sesión había decidido: «un teléfono mal escrito, al no ser obligatorio, no debería
   bloquear el envío»). Tiene razón: **un campo opcional que frena el envío ha dejado de ser
   opcional**, y perder un prospecto por un teléfono es el peor negocio posible. Cómo queda:
   con menos de 7 dígitos avisa **al salir del campo** —a quien se comió un dígito le
   sirve— y el texto dice lo que va a pasar igualmente («I'll email you instead»); **enviar
   no estrena marca roja** en él (una marca roja que no frena nada es una contradicción), y
   el resumen al pie no lo nombra jamás. `BLOQUEAN` (los 4 de `api/contact.js`) es la lista
   que decide si el formulario sale, y el teléfono está fuera A PROPÓSITO.
7. ⛔ **La regex de correo de `apparatus.js` y la de `api/contact.js` son la MISMA cadena**,
   y hay una puerta que lo comprueba. Si se separan, el cliente da por bueno lo que el
   servidor rechaza — que es el fallo original, exactamente.
8. **`--error: #A4160D`** — medido, no elegido: 7.06:1 sobre el papel y 7.78:1 sobre el
   blanco del campo, más fuerte que `--note-strong` (5.89:1), porque un error tiene que
   pesar más que una anotación. El acierto **no lleva color nuevo**: tinta y barra de tinta.
   ⛔ Ningún estado se comunica solo con color (WCAG 1.4.1): todos llevan icono dibujado
   —disco sólido con la marca calada, que a 16px no se deshace como un trazo fino—, y los
   `maxlength` del HTML repiten los límites del servidor, porque un recorte silencioso es
   una mentira educada.

**`tools/verificar_formulario.py` — CORRER ANTES DE CADA PUSH que toque el formulario.**
Existe porque **ninguna puerta del sitio veía estos estados**: `auditar.py` mide la página en
reposo, y en reposo el formulario no tiene un solo error pintado. Dispara los cinco errores y
mide contraste contra el fondo realmente pintado, tamaño ≥12px, forma además de color,
`aria-invalid` + `aria-describedby` coherentes, borde a 3:1 (1.4.11), que ningún aviso se sale
de su columna, una batería de 15 correos contra los dos lados, y **que un teléfono mal escrito
llega igualmente al servidor** (con `fetch` interceptado: la puerta no manda un correo de verdad
cada vez que alguien la corre). Publica denominador y falla en cero. **Vista fallar seis veces**
(regex separada · aviso sin icono · color sin contraste · campo pintado sin `aria-invalid` ·
teléfono que vuelve a bloquear · teléfono que deja de avisar), cada una con su diagnóstico, y el
fuente restaurado y comprobado byte a byte.

⚠️ **Medido y NO arreglado, por estar fuera del encargo:** la sección Contact mide hoy **855
px** limpia a 1440 (con los dos errores del caso de Carlos, 990; con los cinco, 1002). La
referencia de **739 px** del 2026-08-18 —la que hacía que el formulario entrara en una
pantalla— **ya no se cumplía ANTES de este cambio**: la sección creció con el copy nuevo del
pase de conversión del 06/09. Decisión de Carlos si se recupera.
⚠️ **Sin JS el formulario sigue sin enviar** (no tiene `action`, y `novalidate` apaga la
validación nativa). Es anterior a hoy y no se tocó.

## Pendientes (cortos)
0-bis. ⛔ **ANULADO el 2026-08-18: la prueba Shopify y todo el outreach a Shopify/Klaviyo
  Partners.** Orden de Carlos: «those don't pay what I need». El set de comercio UdV del
  punto 3 de la secuencia de lanzamiento decae con ello. El outreach vigente es a agencias
  experienciales, constructores de stands y equipos de brand experience.

0-ter. ⭐ **LO QUE ESPERA A CARLOS, por orden de urgencia:**
  1. **Leer el texto de la oferta de 48 horas** antes de darlo por bueno — lo escribió la
     sesión, es una promesa pública y sus términos reales pueden ser otros.
  2. **Elegir eslogan de firma** entre las seis variantes de `brand/firma-correo.html`
     (A–F; la sesión recomienda C «Working builds, not mockups», B de segunda). Al elegir,
     ese fichero vuelve a contener UNA sola firma.
  3. **Mandar los vídeos de VR/AR** con, por cada uno: qué era, para quién, si el cliente se
     puede nombrar, y el PORQUÉ técnico que lo hace defendible.
  4. **Verificar `reasonedweb.com` en Resend** (sigue el interino `onboarding@resend.dev`).

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
1. ~~LinkedIn~~ ✅ **Enlazado 2026-08-17 por orden de Carlos** (crumb del retrato + pie de las 7 páginas del sitio): `https://www.linkedin.com/in/carlos-marruffo-vegas-a8689231/`.
2. **Cita de Next Latam** (testimonio): pedir permiso ESCRITO antes de publicar nada.
3. **Fix upstream del PiP LG** en el fuente de LG-Demo (proyecto aparte; una línea, toggle d5).
4. **OG por caso** (cada unfurl con su propia pieza en vez del wordmark genérico) — mejora.
5. Fuente licenciada (Söhne / ABC Diatype) — después, si el sitio lo gana.
6. **Outreach**: movimiento de Carlos. Secuencia vigente desde el 2026-08-18: agencias
   experienciales, constructores de stands y equipos de brand experience — y **una pieza de
   VR en el sitio antes de prometer VR en un correo**.
