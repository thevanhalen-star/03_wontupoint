// 광고 관리 기능 자동 점검:  node tools/test_ads.mjs
import { webcrypto } from 'node:crypto';
import fs from 'node:fs';
import { validateConfig, publicView, todayKST } from '../functions/_lib/ads.js';
import { verifyAccess } from '../functions/_lib/access.js';
import * as mw from '../functions/api/admin/_middleware.js';
import * as adminAds from '../functions/api/admin/ads.js';
import * as publicAds from '../functions/api/ads.js';

const def = JSON.parse(fs.readFileSync(new URL('../ads-default.json', import.meta.url), 'utf8'));
let pass = 0, fail = 0;
const ok = (c, m) => { c ? pass++ : (fail++, console.log('  ✗ ' + m)); if (c) console.log('  ✓ ' + m); };

// ---------- 1. 검증
console.log('[검증]');
ok(validateConfig(def).ok, '기본 설정(현재 광고 4개)은 검증을 통과한다');
const bad = (mut) => { const c = JSON.parse(JSON.stringify(def)); mut(c); return validateConfig(c); };
ok(!bad((c) => { c.ads[0].link = 'http://x.com'; }).ok, 'http:// 링크는 거부');
ok(!bad((c) => { c.ads[0].link = 'javascript:alert(1)'; }).ok, 'javascript: 링크는 거부');
ok(!bad((c) => { c.ads[0].images = ['/ad_image/../secret.jpg']; }).ok, '상위 경로(..) 이미지는 거부');
ok(!bad((c) => { c.ads[0].images = ['//evil.com/a.jpg']; }).ok, '// 로 시작하는 이미지는 거부');
ok(!bad((c) => { c.ads[0].images = ['/a.jpg" onerror="x']; }).ok, '따옴표가 든 이미지 주소는 거부');
ok(!bad((c) => { c.ads[0].slot = 'nope'; }).ok, '없는 광고 자리는 거부');
ok(!bad((c) => { c.ads[1].id = c.ads[0].id; }).ok, '중복 ID 는 거부');
ok(!bad((c) => { c.ads[0].start = '2026-12-31'; c.ads[0].end = '2026-01-01'; }).ok, '종료일이 시작일보다 빠르면 거부');
ok(!bad((c) => { c.ads[0].images = []; }).ok, '이미지가 없으면 거부');

// ---------- 2. 공개용 변환
console.log('[공개용 변환]');
const now = Date.parse('2026-10-23T03:00:00Z');
let pv = publicView({ ...def, version: 3 }, now);
ok(pv.enabled && pv.ads.length === 4, '모두 켜져 있으면 광고 4개');
ok(!JSON.stringify(pv).includes('name'), '관리용 정보(이름 등)는 노출되지 않는다');
ok(publicView({ ...def, enabled: false }, now).ads.length === 0, '전체 스위치를 끄면 0개');
{ const c = JSON.parse(JSON.stringify(def)); c.ads[0].enabled = false; ok(publicView(c, now).ads.length === 3, '광고 하나를 끄면 3개'); }
{ const c = JSON.parse(JSON.stringify(def)); c.slots[1].enabled = false; ok(publicView(c, now).ads.length === 3, '자리 하나를 끄면 그 자리 광고가 빠진다'); }
{ const c = JSON.parse(JSON.stringify(def)); c.ads[0].start = '2026-11-01'; ok(publicView(c, now).ads.length === 3, '시작일 전 광고는 숨김'); c.ads[0].start = ''; c.ads[0].end = '2026-10-01'; ok(publicView(c, now).ads.length === 3, '종료일 지난 광고는 숨김'); }
ok(todayKST(Date.parse('2026-10-23T16:00:00Z')) === '2026-10-24', '한국 시간 날짜 계산(UTC 16시 = 다음날 01시)');

// ---------- 2-2. 이미지마다 링크 (이미지 100장 · 링크 100개)
console.log('[이미지별 링크]');
{
  const big = JSON.parse(JSON.stringify(def));
  big.ads = [{ id: 'many', name: '100개 묶음', slot: 'detail-top', link: '', enabled: true, weight: 1, start: '', end: '',
    images: Array.from({ length: 100 }, (_, i) => ({ src: `/ad_image/009/${String(i + 1).padStart(3, '0')}.jpg`, link: `https://shop.example.com/item/${i + 1}` })) }];
  const v = validateConfig(big);
  ok(v.ok && v.config.ads[0].images.length === 100, '이미지 100장 + 각각 다른 링크 100개를 광고 하나로 저장할 수 있다');
  const pv2 = publicView(v.config, now);
  ok(pv2.ads[0].images.length === 100 && pv2.ads[0].images[41].link === 'https://shop.example.com/item/42', '방문자용 데이터에 이미지와 링크가 짝지어 내려간다');
  const mix = JSON.parse(JSON.stringify(def)); mix.ads[0].images = ['/ad_image/001/001.jpg', { src: '/ad_image/001/002.jpg', link: 'https://other.example.com/x' }];
  const pm = publicView(mix, now).ads.find((a) => a.id === 'ad-1');
  ok(pm.images[0].link === mix.ads[0].link && pm.images[1].link === 'https://other.example.com/x', '링크가 없는 이미지는 광고의 기본 링크를 쓰고, 있는 이미지는 자기 링크를 쓴다');
  const noLink = JSON.parse(JSON.stringify(def)); noLink.ads[0].link = ''; noLink.ads[0].images = ['/ad_image/001/001.jpg'];
  ok(!validateConfig(noLink).ok, '기본 링크도 이미지 링크도 없으면 거부');
  const badLink = JSON.parse(JSON.stringify(def)); badLink.ads[0].images = [{ src: '/ad_image/001/001.jpg', link: 'javascript:alert(1)' }];
  ok(!validateConfig(badLink).ok, '이미지별 링크도 https 만 허용');
  const tooMany = JSON.parse(JSON.stringify(def)); tooMany.ads[0].images = Array.from({ length: 301 }, (_, i) => `/a/${i}.jpg`);
  ok(!validateConfig(tooMany).ok, '이미지는 광고당 300장까지');
}

// ---------- 3. Access JWT 검증
console.log('[로그인(Access) 검증]');
const { publicKey, privateKey } = await webcrypto.subtle.generateKey({ name: 'RSASSA-PKCS1-v1_5', modulusLength: 2048, publicExponent: new Uint8Array([1, 0, 1]), hash: 'SHA-256' }, true, ['sign', 'verify']);
const jwk = { ...(await webcrypto.subtle.exportKey('jwk', publicKey)), kid: 'k1', alg: 'RS256', use: 'sig' };
const TEAM = 'me.cloudflareaccess.com', AUD = 'aud123';
const b64 = (o) => Buffer.from(typeof o === 'string' ? o : JSON.stringify(o)).toString('base64url');
async function token(over = {}, kid = 'k1') {
  const h = b64({ alg: 'RS256', kid }), p = b64({ aud: [AUD], iss: `https://${TEAM}`, email: 'me@gmail.com', exp: Math.floor(Date.now() / 1000) + 600, ...over });
  const sig = Buffer.from(await webcrypto.subtle.sign('RSASSA-PKCS1-v1_5', privateKey, new TextEncoder().encode(`${h}.${p}`))).toString('base64url');
  return `${h}.${p}.${sig}`;
}
const realFetch = globalThis.fetch;
globalThis.fetch = async (u) => String(u).includes('/cdn-cgi/access/certs') ? new Response(JSON.stringify({ keys: [jwk] })) : realFetch(u);
const env0 = { ACCESS_TEAM_DOMAIN: TEAM, ACCESS_AUD: AUD };
const req = (t, extra = {}) => new Request('https://wontupoint.com/api/admin/ads', { headers: t ? { 'Cf-Access-Jwt-Assertion': t, ...extra } : extra });
ok((await verifyAccess(req(await token()), env0)).ok, '올바른 토큰은 통과');
ok(!(await verifyAccess(req(null), env0)).ok, '토큰이 없으면 거부');
ok(!(await verifyAccess(req(await token({ aud: ['other'] })), env0)).ok, '다른 앱(aud)의 토큰은 거부');
ok(!(await verifyAccess(req(await token({ exp: 1 })), env0)).ok, '만료된 토큰은 거부');
ok(!(await verifyAccess(req(await token({ iss: 'https://evil.com' })), env0)).ok, '발급자가 다르면 거부');
ok(!(await verifyAccess(req((await token()).replace(/.$/, 'A')), env0)).ok, '서명이 변조되면 거부');
ok(!(await verifyAccess(req(await token({}, 'zzz')), env0)).ok, '모르는 키(kid)는 거부');
ok((await verifyAccess(req(await token()), {})).status === 503, '인증 설정이 없으면 관리자 API 를 열지 않는다(503)');
ok(!(await verifyAccess(new Request('https://wontupoint.com/x'), { DEV_ACCESS_BYPASS: '1' })).ok, 'DEV 우회는 localhost 에서만 인정');

// ---------- 4. 관리자 API 흐름
console.log('[관리자 API]');
const store = {};
const env = { ...env0, ADS_KV: { get: async (k) => store[k] ?? null, put: async (k, v) => { store[k] = v; } },
  ASSETS: { fetch: async () => new Response(JSON.stringify(def)) } };
async function call(method, body, { t, origin = 'https://wontupoint.com', hdr = true } = {}) {
  const headers = { 'Cf-Access-Jwt-Assertion': t ?? (await token()) };
  if (method !== 'GET') { if (origin) headers.Origin = origin; if (hdr) headers['X-Wontu-Admin'] = '1'; headers['Content-Type'] = 'application/json'; }
  const request = new Request('https://wontupoint.com/api/admin/ads', { method, headers, body: body ? JSON.stringify(body) : undefined });
  const handler = method === 'PUT' ? adminAds.onRequestPut : adminAds.onRequestGet;
  const ctx = { request, env, data: {}, next: async () => handler({ request, env, data: ctx.data }) };
  const res = await mw.onRequest(ctx);
  return { status: res.status, body: await res.json() };
}
let r = await call('GET');
ok(r.status === 200 && r.body.config.ads.length === 4 && r.body.config.version === 0, '저장 전에는 기본 설정을 돌려준다');
ok((await call('GET', null, { t: 'bad.token.x' })).status === 401, '잘못된 토큰으로 조회 불가');
const base = () => { const c = JSON.parse(JSON.stringify(r.body.config)); delete c.version; delete c.updatedAt; delete c.updatedBy; return c; };
ok((await call('PUT', { baseVersion: 0, config: base() }, { origin: 'https://evil.com' })).status === 403, '다른 사이트 출처의 저장 요청은 거부(CSRF)');
ok((await call('PUT', { baseVersion: 0, config: base() }, { hdr: false })).status === 403, '관리자 헤더가 없는 저장 요청은 거부');
{ const c = base(); c.ads[0].enabled = false; c.ads[3].enabled = false; const s = await call('PUT', { baseVersion: 0, config: c });
  ok(s.status === 200 && s.body.config.version === 1 && s.body.config.updatedBy === 'me@gmail.com', '저장 성공(버전 1, 저장한 사람 기록)');
  ok(s.body.history[0].note.includes('끔'), '변경 기록에 켜고 끈 내용이 남는다'); }
{ const c = base(); const s = await call('PUT', { baseVersion: 0, config: c }); ok(s.status === 409, '오래된 화면에서 저장하면 409(덮어쓰기 방지)'); }
{ const c = base(); c.ads[0].link = 'ftp://x'; const s = await call('PUT', { baseVersion: 1, config: c }); ok(s.status === 400 && s.body.errors.length > 0, '잘못된 내용은 400 과 오류 목록'); }
{ const res = await publicAds.onRequestGet({ request: new Request('https://wontupoint.com/api/ads'), env });
  const pj = await res.json(); ok(pj.ads.length === 2 && pj.v === 1, '저장 후 방문자용 API 에는 켜진 광고 2개만 나온다');
  ok(res.headers.get('cache-control').includes('s-maxage=60'), '방문자용 API 는 짧게 캐시(최대 1~2분 반영)'); }
{ const broken = { ...env, ADS_KV: { get: async () => { throw new Error('kv down'); }, put: async () => {} }, ASSETS: { fetch: async () => { throw new Error('x'); } } };
  const pj = await (await publicAds.onRequestGet({ request: new Request('https://wontupoint.com/api/ads'), env: broken })).json();
  ok(pj.ads.length === 0 && pj.enabled === false, '저장소 오류 시 광고를 숨긴다(꺼 둔 광고가 우연히 보이지 않게)'); }

console.log(`\n통과 ${pass} / 실패 ${fail}`);
process.exit(fail ? 1 : 0);
