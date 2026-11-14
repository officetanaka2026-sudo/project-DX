// 問い合わせフォーム送信（Vercel Functions + Resend）
// 環境変数: RESEND_API_KEY, CONTACT_TO（受信先）, CONTACT_FROM（送信元 例: 中小企業DX研究所 <form@chusho-dx.com>）
const esc = (s) => String(s || '').replace(/[&<>"]/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));

module.exports = async (req, res) => {
  if (req.method !== 'POST') return res.status(405).json({ ok: false });
  const b = typeof req.body === 'string' ? JSON.parse(req.body || '{}') : (req.body || {});
  if (b.website) return res.status(200).json({ ok: true }); // ボット対策（隠し項目）
  const name = (b.name || '').trim(), email = (b.email || '').trim(), body = (b.body || '').trim();
  if (!name || !body || !/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(email) || body.length > 5000) {
    return res.status(400).json({ ok: false, error: '入力内容をご確認ください。' });
  }
  const { RESEND_API_KEY, CONTACT_TO, CONTACT_FROM } = process.env;
  if (!RESEND_API_KEY || !CONTACT_TO || !CONTACT_FROM) return res.status(500).json({ ok: false, error: '送信設定が未完了です。' });
  const html = `<p><b>種類:</b> ${esc(b.type)}</p><p><b>会社名:</b> ${esc(b.company)}</p><p><b>お名前:</b> ${esc(name)}</p><p><b>連絡先:</b> ${esc(email)}</p><p><b>内容:</b><br>${esc(body).replace(/\n/g, '<br>')}</p>`;
  const r = await fetch('https://api.resend.com/emails', {
    method: 'POST',
    headers: { Authorization: `Bearer ${RESEND_API_KEY}`, 'Content-Type': 'application/json' },
    body: JSON.stringify({ from: CONTACT_FROM, to: CONTACT_TO.split(','), reply_to: email, subject: `【中小企業DX研究所】お問い合わせ：${name}様`, html }),
  });
  if (!r.ok) return res.status(502).json({ ok: false, error: '送信に失敗しました。時間をおいて再度お試しください。' });
  return res.status(200).json({ ok: true });
};
