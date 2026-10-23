// 광고 설정 구조 · 검증 · 공개용 변환 (Cloudflare Pages Functions 와 로컬 개발 서버가 같이 사용)
//
// 설정(JSON) 모양
// {
//   version: 12, updatedAt: "2026-10-23T01:02:03.000Z", updatedBy: "me@gmail.com",
//   enabled: true,                                   ← 전체 스위치 (끄면 모든 광고 숨김)
//   slots: [{ id, label, enabled }],                 ← 광고 자리(위치)별 스위치
//   ads:   [{ id, name, slot, link, images[], enabled, weight, start, end }]
// }

export const KV_KEY = 'ads_config';
export const HISTORY_KEY = 'ads_history';

const ID_RE = /^[a-z0-9][a-z0-9_-]{0,39}$/;
const DATE_RE = /^\d{4}-\d{2}-\d{2}$/;
const IMG_EXT_RE = /\.(jpe?g|png|webp|gif|avif)(\?.*)?$/i;
const MAX_ADS = 100;
const MAX_SLOTS = 40;
const MAX_IMAGES = 60;

export function emptyConfig() {
  return { version: 0, updatedAt: '', updatedBy: '', enabled: true, slots: [], ads: [] };
}

function isHttps(u) {
  try {
    const x = new URL(u);
    return x.protocol === 'https:' && !!x.hostname;
  } catch {
    return false;
  }
}

function validImage(s) {
  if (typeof s !== 'string' || s.length > 500 || !IMG_EXT_RE.test(s)) return false;
  if (s.startsWith('/')) return !s.startsWith('//') && !s.includes('..') && !/[\s"'<>\\]/.test(s);
  return isHttps(s) && !/[\s"'<>\\]/.test(s);
}

/** 관리자가 보낸 설정을 검사·정리한다. 반환: { ok, errors[], config } */
export function validateConfig(input) {
  const errors = [];
  if (!input || typeof input !== 'object') return { ok: false, errors: ['설정 형식이 올바르지 않습니다.'] };

  const slots = [];
  const slotIds = new Set();
  if (!Array.isArray(input.slots)) errors.push('slots 가 배열이 아닙니다.');
  else {
    if (input.slots.length > MAX_SLOTS) errors.push(`광고 자리는 최대 ${MAX_SLOTS}개입니다.`);
    for (const s of input.slots.slice(0, MAX_SLOTS)) {
      const id = String(s?.id ?? '');
      if (!ID_RE.test(id)) { errors.push(`광고 자리 ID "${id}" 는 영문 소문자·숫자·-·_ 로 40자 이하여야 합니다.`); continue; }
      if (slotIds.has(id)) { errors.push(`광고 자리 ID "${id}" 가 중복입니다.`); continue; }
      slotIds.add(id);
      slots.push({ id, label: String(s.label ?? id).trim().slice(0, 40) || id, enabled: s.enabled !== false });
    }
  }

  const ads = [];
  const adIds = new Set();
  if (!Array.isArray(input.ads)) errors.push('ads 가 배열이 아닙니다.');
  else {
    if (input.ads.length > MAX_ADS) errors.push(`광고는 최대 ${MAX_ADS}개입니다.`);
    for (const a of input.ads.slice(0, MAX_ADS)) {
      const id = String(a?.id ?? '');
      const label = `광고 "${String(a?.name || id).slice(0, 30)}"`;
      if (!ID_RE.test(id)) { errors.push(`${label}: ID 는 영문 소문자·숫자·-·_ 로 40자 이하여야 합니다.`); continue; }
      if (adIds.has(id)) { errors.push(`${label}: ID "${id}" 가 중복입니다.`); continue; }
      adIds.add(id);
      const name = String(a.name ?? '').trim().slice(0, 60);
      if (!name) errors.push(`${label}: 이름이 비어 있습니다.`);
      if (!slotIds.has(String(a.slot))) errors.push(`${label}: 존재하지 않는 광고 자리 "${a.slot}" 입니다.`);
      if (!isHttps(a.link) || String(a.link).length > 500) errors.push(`${label}: 링크는 https:// 로 시작하는 주소여야 합니다.`);
      const images = Array.isArray(a.images) ? a.images.map((x) => String(x).trim()).filter(Boolean) : [];
      if (!images.length) errors.push(`${label}: 이미지가 한 장도 없습니다.`);
      if (images.length > MAX_IMAGES) errors.push(`${label}: 이미지는 최대 ${MAX_IMAGES}장입니다.`);
      for (const im of images) if (!validImage(im)) errors.push(`${label}: 이미지 주소가 올바르지 않습니다 → ${im.slice(0, 60)}`);
      const weight = Number.isInteger(a.weight) ? a.weight : parseInt(a.weight, 10);
      const start = String(a.start || ''), end = String(a.end || '');
      if (start && !DATE_RE.test(start)) errors.push(`${label}: 시작일 형식은 YYYY-MM-DD 입니다.`);
      if (end && !DATE_RE.test(end)) errors.push(`${label}: 종료일 형식은 YYYY-MM-DD 입니다.`);
      if (start && end && DATE_RE.test(start) && DATE_RE.test(end) && end < start) errors.push(`${label}: 종료일이 시작일보다 빠릅니다.`);
      ads.push({
        id, name, slot: String(a.slot), link: String(a.link), images: images.slice(0, MAX_IMAGES),
        enabled: a.enabled !== false, weight: weight >= 1 && weight <= 100 ? weight : 1, start, end,
      });
    }
  }

  if (errors.length) return { ok: false, errors };
  return { ok: true, errors: [], config: { enabled: input.enabled !== false, slots, ads } };
}

/** 한국 시간 기준 오늘 날짜(YYYY-MM-DD) */
export function todayKST(nowMs = Date.now()) {
  return new Date(nowMs + 9 * 3600 * 1000).toISOString().slice(0, 10);
}

/** 방문자에게 내려줄 설정: 켜져 있고 기간이 맞는 광고만, 관리용 필드는 제외 */
export function publicView(config, nowMs = Date.now()) {
  const out = { v: config.version || 0, enabled: config.enabled !== false, ads: [] };
  if (!out.enabled) return out;
  const today = todayKST(nowMs);
  const on = new Set((config.slots || []).filter((s) => s.enabled !== false).map((s) => s.id));
  for (const a of config.ads || []) {
    if (a.enabled === false || !on.has(a.slot)) continue;
    if (a.start && today < a.start) continue;
    if (a.end && today > a.end) continue;
    out.ads.push({ id: a.id, slot: a.slot, link: a.link, images: a.images, weight: a.weight || 1 });
  }
  return out;
}

export async function loadConfig(env, request) {
  if (env.ADS_KV) {
    const raw = await env.ADS_KV.get(KV_KEY);
    if (raw) {
      try { return JSON.parse(raw); } catch { /* 아래 기본값 사용 */ }
    }
  }
  // 저장된 설정이 없으면 저장소의 기본 설정(ads-default.json)을 사용
  try {
    const res = await env.ASSETS.fetch(new URL('/ads-default.json', request.url));
    if (res.ok) return await res.json();
  } catch { /* 무시 */ }
  return emptyConfig();
}

export function json(body, status = 200, headers = {}) {
  return new Response(JSON.stringify(body), {
    status,
    headers: { 'content-type': 'application/json; charset=utf-8', ...headers },
  });
}
