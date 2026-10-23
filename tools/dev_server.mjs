// 로컬 개발 서버: 사이트 + /api/ads + /admin/ 을 내 PC 에서 그대로 시험해 볼 수 있다.
//   node tools/dev_server.mjs            → http://localhost:8788  (관리자: http://localhost:8788/admin/)
// 실제 배포 코드(functions/)를 그대로 불러 쓰며, 로그인(Access)만 건너뛴다(localhost 전용).
// 저장한 설정은 tools/.dev_kv.json 에 남는다(배포된 사이트와는 무관, git 제외 권장).
import http from 'node:http';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const KV_FILE = path.join(ROOT, 'tools', '.dev_kv.json');
const PORT = Number(process.env.PORT || 8788);

const mod = (p) => import(new URL('../functions/' + p, import.meta.url));
const [publicAds, mw, adminAds] = await Promise.all([mod('api/ads.js'), mod('api/admin/_middleware.js'), mod('api/admin/ads.js')]);

const store = fs.existsSync(KV_FILE) ? JSON.parse(fs.readFileSync(KV_FILE, 'utf8')) : {};
const save = () => fs.writeFileSync(KV_FILE, JSON.stringify(store, null, 2));
const MIME = { '.html': 'text/html; charset=utf-8', '.js': 'text/javascript; charset=utf-8', '.css': 'text/css; charset=utf-8', '.json': 'application/json; charset=utf-8', '.jpg': 'image/jpeg', '.jpeg': 'image/jpeg', '.png': 'image/png', '.webp': 'image/webp', '.svg': 'image/svg+xml', '.ico': 'image/x-icon', '.txt': 'text/plain; charset=utf-8', '.xml': 'application/xml', '.webmanifest': 'application/manifest+json' };

function staticFile(urlPath) {
  let p = decodeURIComponent(urlPath.split('?')[0]);
  let f = path.join(ROOT, p);
  if (!f.startsWith(ROOT)) return null;
  if (fs.existsSync(f) && fs.statSync(f).isDirectory()) f = path.join(f, 'index.html');
  else if (!fs.existsSync(f) && fs.existsSync(f + '.html')) f += '.html';
  return fs.existsSync(f) && fs.statSync(f).isFile() ? f : null;
}

const env = {
  DEV_ACCESS_BYPASS: '1',
  ADS_KV: { get: async (k) => store[k] ?? null, put: async (k, v) => { store[k] = v; save(); } },
  ASSETS: {
    fetch: async (url) => {
      const f = staticFile(new URL(url).pathname);
      return f ? new Response(fs.readFileSync(f), { headers: { 'content-type': MIME[path.extname(f)] || 'application/octet-stream' } }) : new Response('not found', { status: 404 });
    },
  },
};

http.createServer(async (req, res) => {
  const origin = `http://${req.headers.host}`;
  const chunks = [];
  for await (const c of req) chunks.push(c);
  const body = chunks.length ? Buffer.concat(chunks) : undefined;
  const request = new Request(origin + req.url, { method: req.method, headers: req.headers, body: ['GET', 'HEAD'].includes(req.method) ? undefined : body });
  const { pathname } = new URL(request.url);
  let response;
  try {
    if (pathname === '/api/ads' && req.method === 'GET') response = await publicAds.onRequestGet({ request, env, data: {} });
    else if (pathname === '/api/admin/ads') {
      const handler = req.method === 'PUT' ? adminAds.onRequestPut : adminAds.onRequestGet;
      const ctx = { request, env, data: {}, next: async () => handler({ request, env, data: ctx.data }) };
      response = await mw.onRequest(ctx);
    } else {
      const f = staticFile(pathname);
      response = f ? new Response(fs.readFileSync(f), { headers: { 'content-type': MIME[path.extname(f)] || 'application/octet-stream' } }) : new Response('Not found', { status: 404 });
    }
  } catch (e) {
    response = new Response('서버 오류: ' + e.message, { status: 500 });
  }
  res.writeHead(response.status, Object.fromEntries(response.headers));
  res.end(Buffer.from(await response.arrayBuffer()));
}).listen(PORT, '127.0.0.1', () => console.log(`개발 서버: http://localhost:${PORT}   관리자: http://localhost:${PORT}/admin/`));
