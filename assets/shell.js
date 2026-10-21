/* 포인트 상세 페이지 공통 셸: 왼쪽 지역 카테고리 / 상단 바(뒤로가기·검색) / 하단 바(뒤로가기·맨위로) */
(function () {
  'use strict';
  var REGIONS = [['인천·경기', 'metro'], ['강원', '강원'], ['충남', '충남'], ['전북', '전북'], ['전남', '전남'], ['경북', '경북'], ['경남', '경남'], ['부산·울산', 'southeast'], ['제주', '제주']];
  var ALIAS = {'인천':'인천','인천광역시':'인천','경기':'경기','경기도':'경기','강원특별자치도':'강원','강원도':'강원','강원':'강원','충청남도':'충남','충남':'충남','충청북도':'충북','충북':'충북','전북특별자치도':'전북','전라북도':'전북','전북':'전북','전라남도':'전남','전남':'전남','경상북도':'경북','경북':'경북','경상남도':'경남','경남':'경남','부산광역시':'부산','부산':'부산','울산광역시':'울산','울산':'울산','제주특별자치도':'제주','제주':'제주'};
  function groupOf(addr) {
    var r = ALIAS[String(addr || '').trim().split(/\s+/)[0]] || '';
    if (r === '인천' || r === '경기') return 'metro';
    if (r === '부산' || r === '울산') return 'southeast';
    return r;
  }
  var UPDATING = ['강원', '경북', 'southeast', '제주'];
  function districtOf(addr) { var p = String(addr || '').trim().split(/\s+/); return p.length > 1 ? p[1] : ''; }
  function make(tag, cls, text) { var n = document.createElement(tag); if (cls) n.className = cls; if (text !== undefined) n.textContent = text; return n; }

  var css = ':root{--side:184px}'
    + 'body.wontu-shell{padding-left:var(--side)}'
    + '.ws-side{position:fixed;left:0;top:0;bottom:0;width:var(--side);background:#10283c;color:#c0d0de;overflow:auto;z-index:12;font-family:"Malgun Gothic","Apple SD Gothic Neo",system-ui,sans-serif;font-size:14px;line-height:1.5}'
    + '.ws-brand{height:77px;margin:0 11px;border-bottom:1px solid #30475a;display:flex;align-items:center;gap:6px;color:#f8fcff;text-decoration:none;font-size:15px;font-weight:800;letter-spacing:-.4px;white-space:nowrap}'
    + '.ws-brand svg{width:24px;height:24px;flex:none;color:#65c6ed}'
    + '.ws-cap{font-size:12px;color:#7f9caf;padding:21px 22px 10px}'
    + '.ws-list{padding:0 11px 22px;display:grid;gap:2px}'
    + '.ws-list a{display:flex;justify-content:space-between;align-items:center;color:#c3d2df;text-decoration:none;border-radius:5px;padding:12px 11px;font-weight:700;min-height:39px}'
    + '.ws-list a:hover{background:#203f57}.ws-list a.on{background:#2069a1;color:#fff}.ws-list small{font-size:11px;color:#92abc0;font-weight:400}.ws-list a.on small{color:#deecfa}'
    + '.ws-sub{display:grid;gap:1px;margin:1px 0 6px 10px;padding-left:8px;border-left:1px solid #30475a}'
    + '.ws-list .ws-sub a{font-size:13px;font-weight:400;color:#a9bccc;padding:7px 9px;min-height:30px;border-radius:4px}'
    + '.ws-list .ws-sub a.on{background:#1a4f7a;color:#fff;font-weight:700}'
    + '.ws-top{max-width:1104px;margin:0 auto;padding:14px 20px 0;display:flex;align-items:center;gap:10px;font-family:"Malgun Gothic",system-ui,sans-serif}'
    + '.ws-btn{display:inline-flex;align-items:center;gap:6px;height:38px;padding:0 16px;border:1px solid #cfdce7;background:#fff;color:#14629e;border-radius:6px;font-size:14px;font-weight:700;cursor:pointer;text-decoration:none;white-space:nowrap}'
    + '.ws-btn:hover{background:#e8f1f8}'
    + '.ws-menu{display:none;padding:0 10px}'
    + '.ws-title{margin:0 0 0 6px;font-size:18px;font-weight:800;letter-spacing:-.6px;background:linear-gradient(90deg,#10283c,#1d7fc1);-webkit-background-clip:text;background-clip:text;color:transparent;line-height:1.3}'
    + '.ws-upd{font-size:9.5px;font-weight:400;color:#f2b765;margin-right:5px}'
    + '.ws-search{margin-left:auto;display:flex;gap:7px}'
    + '.ws-search input{width:240px;max-width:100%;height:38px;border:1px solid #cfdce7;border-radius:6px;padding:0 12px;font-size:13px;outline:0;font-family:inherit}'
    + '.ws-search input:focus{border-color:#3c83b4;box-shadow:0 0 0 3px #dceefb}'
    + '.ws-search button{height:38px;background:#14629e;color:#fff;border:0;border-radius:5px;padding:0 17px;cursor:pointer;font-family:inherit}'
    + '.ws-bottom{max-width:1104px;margin:0 auto 18px;padding:0 20px;display:flex;justify-content:center;gap:10px;font-family:"Malgun Gothic",system-ui,sans-serif}'
    + '.ws-shade{display:none}'
    + '@media(max-width:600px){:root{--side:0px}.ws-side{width:230px;transform:translateX(-100%);transition:transform .2s}.ws-side.open{transform:none}'
    + '.ws-shade.open{display:block;position:fixed;inset:0;background:#101b2b80;z-index:11}.ws-menu{display:inline-flex}.ws-top{flex-wrap:wrap;padding:10px 14px 0}.ws-search{margin-left:0;width:100%}.ws-search input{flex:1;width:auto}}';
  var fl = document.createElement('link'); fl.rel = 'stylesheet'; fl.href = 'https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;500;700;800&display=swap'; document.head.appendChild(fl);
  css += 'body.wontu-shell{font-family:"Noto Sans KR","Malgun Gothic",system-ui,sans-serif}'
    + 'body.wontu-shell .container h1.wontu-point-title{font-weight:800;letter-spacing:-.04em;line-height:1.45}'
    + 'body.wontu-shell .container h2,body.wontu-shell main h2{display:block;font-weight:800;letter-spacing:-.03em;border-left:6px solid #336B46;padding-left:13px}'
    + 'body.wontu-shell main h1{font-size:30px;font-weight:800;letter-spacing:-.04em;margin:18px 0 6px;background:linear-gradient(90deg,#10283c,#1d7fc1);-webkit-background-clip:text;background-clip:text;color:transparent}'
    + 'body.wontu-shell main h2{border-left-color:#1d669f;color:#10283c;font-size:20px;margin:34px 0 10px}'
    + 'body.wontu-shell .highlight{font-weight:700;background:linear-gradient(transparent 55%,#cfe9d4 55%)!important;padding:0 2px!important;border-radius:0!important}'
    + 'body.wontu-shell main .lead{font-size:17px;font-weight:500;color:#2a4a63}'
    + 'body.wontu-shell .point-name{letter-spacing:-.3px}';
  css += '@media(max-width:600px){.ws-title{width:100%;margin:2px 0 0;order:5}body.wontu-shell main h1{font-size:25px}}';
  var st = make('style'); st.textContent = css; document.head.appendChild(st);
  document.body.classList.add('wontu-shell');

  function goBack() {
    var same = false;
    try { same = document.referrer && new URL(document.referrer).origin === location.origin; } catch (e) {}
    if (same && history.length > 1) history.back(); else location.href = '/index.html';
  }
  function backBtn() { var b = make('button', 'ws-btn', '← 뒤로가기'); b.type = 'button'; b.addEventListener('click', goBack); return b; }

  // 사이드바
  var side = make('aside', 'ws-side'); side.setAttribute('aria-label', '지역 카테고리');
  side.innerHTML = '<a class="ws-brand" href="/index.html" aria-label="원투포인트 홈"><svg viewBox="0 0 32 32" fill="none" aria-hidden="true"><path d="M3 19c5 0 7-6 13-6 5 0 7 4 13 1M3 24c5 0 7-5 13-5 5 0 7 4 13 0M5 13c4-3 7-7 12-7 4 0 7 3 11 2" stroke="currentColor" stroke-width="3" stroke-linecap="round"/></svg>낚시·차박 포인트</a><div class="ws-cap">지역 카테고리</div>';
  var list = make('nav', 'ws-list'); list.setAttribute('aria-label', '지역 선택'); side.appendChild(list);
  var shade = make('div', 'ws-shade');
  document.body.prepend(shade); document.body.prepend(side);
  shade.addEventListener('click', function () { side.classList.remove('open'); shade.classList.remove('open'); });

  // 상단 바
  var top = make('div', 'ws-top');
  var menu = make('button', 'ws-btn ws-menu', '☰'); menu.type = 'button'; menu.setAttribute('aria-label', '지역 메뉴 열기');
  menu.addEventListener('click', function () { side.classList.toggle('open'); shade.classList.toggle('open'); });
  var form = make('form', 'ws-search'); form.setAttribute('role', 'search'); form.action = '/index.html';
  form.innerHTML = '<input type="search" name="q" placeholder="포인트명, 지역명으로 검색" aria-label="포인트명 또는 지역명 검색"><button type="submit">검색</button>';
  var title = make('div', 'ws-title', '전국 차박·원투·워킹 낚시 포인트');
  top.append(menu, backBtn(), title, form);
  var container = document.querySelector('.container') || document.querySelector('main');
  document.body.insertBefore(top, container);

  // 하단 바
  var bottom = make('div', 'ws-bottom');
  var up = make('button', 'ws-btn', '↑ 맨위로'); up.type = 'button';
  up.addEventListener('click', function () { window.scrollTo({ top: 0, behavior: 'smooth' }); });
  bottom.append(backBtn(), up);
  var foot = document.querySelector('.wontu-foot');
  if (foot) foot.parentNode.insertBefore(bottom, foot); else container.parentNode.insertBefore(bottom, container.nextSibling);

  // 포인트 사진 클릭 → 팝업 확대 (광고 이미지는 제외). ←/→ 로 이전·다음, Esc 또는 바깥 클릭으로 닫기
  var photos = [].slice.call(document.querySelectorAll('.point-photo img'));
  if (photos.length) {
    var lbCss = make('style');
    lbCss.textContent = '.point-photo img{cursor:zoom-in}'
      + '.lb{position:fixed;inset:0;z-index:100;background:rgba(8,16,26,.92);display:none;align-items:center;justify-content:center;padding:16px}'
      + '.lb.on{display:flex}.lb img{max-width:100%;max-height:100%;object-fit:contain;border-radius:4px;box-shadow:0 8px 40px rgba(0,0,0,.5)}'
      + '.lb button{position:absolute;background:rgba(255,255,255,.14);color:#fff;border:0;border-radius:50%;width:44px;height:44px;font-size:22px;cursor:pointer;line-height:1}'
      + '.lb .x:hover{background:rgba(255,255,255,.3)}.lb .x{top:14px;right:14px;z-index:2}'
      // 좌·우 가장자리 영역에 마우스를 올리면 희미한 화살표가 나타나고, 눌러서 이전/다음으로 이동
      + '.lb .p,.lb .n{top:0;bottom:0;width:22%;height:auto;border-radius:0;background:transparent;font-size:54px;font-weight:300;display:flex;align-items:center;color:rgba(255,255,255,0);transition:color .2s,background .2s}'
      + '.lb .p{left:0;justify-content:flex-start;padding-left:26px}.lb .n{right:0;justify-content:flex-end;padding-right:26px}'
      + '.lb .p:hover,.lb .n:hover{color:rgba(255,255,255,.55);background:linear-gradient(90deg,rgba(255,255,255,.06),transparent)}.lb .n:hover{background:linear-gradient(270deg,rgba(255,255,255,.06),transparent)}'
      + '@media(hover:none){.lb .p,.lb .n{color:rgba(255,255,255,.35);width:16%}}'
      + '.lb .c{position:absolute;bottom:14px;left:0;right:0;text-align:center;color:#c9d6e2;font-size:13px;font-family:"Malgun Gothic",system-ui,sans-serif}';
    document.head.appendChild(lbCss);
    var lb = make('div', 'lb'); lb.setAttribute('role', 'dialog'); lb.setAttribute('aria-modal', 'true');
    var lbImg = make('img'), lbCount = make('div', 'c');
    var bx = make('button', 'x', '✕'), bp = make('button', 'p', '‹'), bn = make('button', 'n', '›');
    bx.setAttribute('aria-label', '닫기'); bp.setAttribute('aria-label', '이전 사진'); bn.setAttribute('aria-label', '다음 사진');
    lb.append(lbImg, bx, bp, bn, lbCount); document.body.appendChild(lb);
    var cur = 0;
    function show(i) {
      cur = (i + photos.length) % photos.length;
      lbImg.src = photos[cur].currentSrc || photos[cur].src; lbImg.alt = photos[cur].alt;
      lbCount.textContent = (cur + 1) + ' / ' + photos.length + '  ·  출처 : 카카오맵 (https://map.kakao.com)';
      bp.style.display = bn.style.display = photos.length > 1 ? '' : 'none';
    }
    function close() { lb.classList.remove('on'); document.body.style.overflow = ''; }
    photos.forEach(function (im, i) { im.addEventListener('click', function () { show(i); lb.classList.add('on'); document.body.style.overflow = 'hidden'; }); });
    lb.addEventListener('click', function (e) { if (e.target === lb || e.target === lbImg) close(); });
    bx.addEventListener('click', close);
    bp.addEventListener('click', function (e) { e.stopPropagation(); show(cur - 1); });
    bn.addEventListener('click', function (e) { e.stopPropagation(); show(cur + 1); });
    document.addEventListener('keydown', function (e) {
      if (!lb.classList.contains('on')) return;
      if (e.key === 'Escape') close(); else if (e.key === 'ArrowLeft') show(cur - 1); else if (e.key === 'ArrowRight') show(cur + 1);
    });
  }

  // 카테고리 목록 (points.json → 현재 포인트의 지역/시군 펼침)
  var m = location.pathname.match(/\/points\/([^/]+)\//), id = m && m[1];
  fetch('/points.json').then(function (r) { return r.json(); }).then(function (all) {
    var cur = all.filter(function (x) { return x.id === id; })[0];
    var curG = cur && groupOf(cur.address), curD = cur && districtOf(cur.address);
    var a = make('a', ''); a.href = '/index.html'; a.append(make('span', '', '전체'), make('small', '', String(all.length))); list.appendChild(a);
    REGIONS.forEach(function (r) {
      var items = all.filter(function (x) { return groupOf(x.address) === r[1]; });
      var link = make('a', curG === r[1] ? 'on' : ''); link.href = '/index.html?region=' + encodeURIComponent(r[1]);
      var cn = make('small', ''); if (UPDATING.indexOf(r[1]) >= 0) cn.appendChild(make('span', 'ws-upd', '업데이트중')); cn.append(String(items.length));
      link.append(make('span', '', r[0]), cn); list.appendChild(link);
      if (curG === r[1]) {
        var sub = make('div', 'ws-sub');
        var all0 = make('a', ''); all0.href = link.href; all0.append(make('span', '', '전체'), make('small', '', String(items.length))); sub.appendChild(all0);
        var cities = {}; items.forEach(function (x) { var d = districtOf(x.address); if (d) cities[d] = (cities[d] || 0) + 1; });
        Object.keys(cities).sort(function (x, y) { return x.localeCompare(y, 'ko'); }).forEach(function (c) {
          var s = make('a', c === curD ? 'on' : ''); s.href = link.href + '&city=' + encodeURIComponent(c);
          s.append(make('span', '', c), make('small', '', String(cities[c]))); sub.appendChild(s);
        });
        list.appendChild(sub);
        link.addEventListener('click', function (e) { e.preventDefault(); sub.style.display = sub.style.display === 'none' ? '' : 'none'; });
      }
    });
  }).catch(function () {});
})();
