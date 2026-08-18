// /api/contact — el endpoint del formulario, propio de ESTE proyecto.
// Envía por Resend (https://resend.com) con la clave en variables de entorno
// de Vercel — la clave jamás toca el cliente. Si RESEND_API_KEY no está
// configurada, responde 503 y el frontend lo DICE sin borrar lo escrito (honesto:
// nada se pierde, nada se finge).
//
// Variables de entorno (Vercel → Settings → Environment Variables):
//   RESEND_API_KEY  — obligatoria (re_...)
//   CONTACT_TO      — opcional, default hello@reasonedweb.com
//   CONTACT_FROM    — opcional, default "Reasoned Web <hello@reasonedweb.com>"
//                     (requiere el dominio verificado en Resend)

const LIMITES = { name: 120, email: 200, company: 160, role: 120, phone: 60, ships: 200, message: 4000 };

function limpio(v, max) {
  return String(v || "").replace(/[\r\n\t]+/g, " ").trim().slice(0, max);
}

function esc(s) {
  return s.replace(/[&<>"']/g, c => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
}

module.exports = async (req, res) => {
  if (req.method !== "POST") {
    res.setHeader("Allow", "POST");
    return res.status(405).json({ ok: false, error: "method" });
  }

  const key = process.env.RESEND_API_KEY;
  if (!key) return res.status(503).json({ ok: false, error: "unconfigured" });

  const b = req.body || {};
  // honeypot: el campo "website" está oculto para humanos; si llega lleno, es un bot.
  if (b.website) return res.status(200).json({ ok: true });

  const d = {};
  for (const k of Object.keys(LIMITES)) d[k] = limpio(b[k], LIMITES[k]);

  // Obligatorios (2026-08-17): rol y teléfono pasaron a opcionales en el
  // formulario; el servidor tiene que exigir la MISMA lista o el envío
  // devolvería 400 y el frontend anunciaría un fallo sin motivo.
  const faltan = ["name", "email", "company", "message"].filter(k => !d[k]);
  if (faltan.length) return res.status(400).json({ ok: false, error: "missing", fields: faltan });
  if (!/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(d.email))
    return res.status(400).json({ ok: false, error: "email" });

  const to = process.env.CONTACT_TO || "hello@reasonedweb.com";
  const from = process.env.CONTACT_FROM || "Reasoned Web <hello@reasonedweb.com>";
  const fila = (k, v) => `<tr><td style="padding:4px 12px 4px 0;color:#555A61;white-space:nowrap">${k}</td><td style="padding:4px 0"><strong>${esc(v)}</strong></td></tr>`;

  const html =
    `<div style="font:15px/1.6 system-ui,sans-serif;color:#16181C">` +
    `<p style="margin:0 0 14px">Availability inquiry — reasonedweb.com</p>` +
    `<table style="border-collapse:collapse">` +
    fila("Name", d.name) + fila("Email", d.email) + fila("Agency / studio", d.company) +
    fila("Role", d.role) + fila("Phone", d.phone) +
    (d.ships ? fila("They ship", d.ships) : "") +
    `</table><hr style="border:0;border-top:1px solid #DCDEDC;margin:14px 0">` +
    `<p style="white-space:pre-wrap;margin:0">${esc(String(b.message || "").trim().slice(0, LIMITES.message))}</p></div>`;

  const r = await fetch("https://api.resend.com/emails", {
    method: "POST",
    headers: { Authorization: `Bearer ${key}`, "Content-Type": "application/json" },
    body: JSON.stringify({
      from,
      to: [to],
      reply_to: d.email,
      subject: `Availability inquiry — ${d.company} (${d.name})`,
      html,
    }),
  });

  if (!r.ok) {
    const detalle = await r.text().catch(() => "");
    console.error("resend fallo:", r.status, detalle.slice(0, 300));
    return res.status(502).json({ ok: false, error: "send" });
  }
  return res.status(200).json({ ok: true });
};
