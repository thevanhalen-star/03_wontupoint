# -*- coding: utf-8 -*-
"""디자인 시안 3종 생성 → tools/samples/design_A_editorial.html, design_B_night.html, design_C_outdoor.html
이미지를 내장한 단독 파일입니다(글꼴만 인터넷 연결 시 구글 폰트로 로딩)."""
import base64
import io
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "tools" / "samples"


def uri(rel, w=640, q=70):
    im = Image.open(ROOT / rel).convert("RGB")
    im.thumbnail((w, w * 2))
    b = io.BytesIO()
    im.save(b, "JPEG", quality=q, optimize=True)
    return "data:image/jpeg;base64," + base64.b64encode(b.getvalue()).decode()


IMG = [
    uri("points/C001/image/001.jpg", 1100),
    uri("points/C001/image/002.jpg", 640),
    uri("points/C001/image/003.jpg", 640),
    uri("points/C048/image/001.jpg", 640),
    uri("points/C048/image/002.jpg", 640),
    uri("points/C046/image/001.jpg", 640),
    uri("points/C046/image/002.jpg", 640),
]
AD = uri("ad_image/001/001.jpg", 420)

CARDS = [
    ("황산포구", "인천 강화군 길상면", 1, ["차박", "원투"]),
    ("초지진선착장", "인천 강화군 길상면", 2, ["워킹", "원투"]),
    ("안섬포구", "충남 당진시 석문면", 3, ["차박", "원투"]),
    ("한진포구", "충남 당진시 송악읍", 5, ["워킹", "차박"]),
    ("석문방조제 주차장", "충남 당진시 석문면", 4, ["차박", "워킹"]),
    ("덕진진주차장", "인천 강화군 불은면", 6, ["원투", "워킹"]),
]
REGIONS = ["전체", "인천·경기", "강원", "충남", "전북", "전남", "경북", "경남", "부산·울산", "제주"]
WAVE = '<svg viewBox="0 0 32 32" width="26" height="26" fill="none"><path d="M3 19c5 0 7-6 13-6 5 0 7 4 13 1M3 24c5 0 7-5 13-5 5 0 7 4 13 0M5 13c4-3 7-7 12-7 4 0 7 3 11 2" stroke="currentColor" stroke-width="3" stroke-linecap="round"/></svg>'
FONTS = '<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'

BODY_P = ("강화 남단 갯벌 포인트는 밀물 타이밍을 놓치면 어떤 채비로도 낚시 자체가 성립하지 않습니다. "
          "간조 시 광범위한 갯벌이 드러나는 구조로, 물때 확인이 입장 판단의 전부를 결정하는 곳입니다.")
BODY_P2 = ("초지대교 인근 연륙교로 연결된 황산도에 자리한 소형 어항입니다. 물양장과 선착장이 정비되어 "
           "차를 대고 하룻밤 머물며 들물 타이밍에 맞춰 채비를 던지기 좋은 환경입니다.")


def cards_html(kind):
    out = []
    for i, (n, a, im, tg) in enumerate(CARDS):
        tags = "".join(f'<i class="tg">{t}</i>' for t in tg)
        out.append(f'<a class="card c{i}" href="#"><span class="ph"><img src="{IMG[im]}" alt="">{tags}</span>'
                   f'<span class="tx"><b>{n}</b><em>{a}</em></span></a>')
    return "\n".join(out)


def wrap(title, css, body, fonts_href):
    return f"""<!doctype html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title}</title>{FONTS}<link rel="stylesheet" href="{fonts_href}">
<style>*{{box-sizing:border-box}}body{{margin:0}}a{{color:inherit;text-decoration:none}}img{{display:block}}{css}</style></head><body>{body}</body></html>"""


# ============================================================ A. 에디토리얼
def design_a():
    css = """
:root{--ink:#0f2233;--sea:#0e7490;--sea2:#164e63;--sand:#f6f3ee;--mut:#6b7f90}
body{font-family:'Noto Sans KR',sans-serif;background:var(--sand);color:var(--ink);line-height:1.7}
.serif{font-family:'Noto Serif KR',serif}
.label{position:sticky;top:0;z-index:50;background:#0f2233;color:#cfe3f0;text-align:center;font-size:13px;padding:8px}
.nav{position:sticky;top:34px;z-index:40;display:flex;align-items:center;gap:26px;padding:14px 5vw;background:rgba(246,243,238,.92);backdrop-filter:blur(10px);border-bottom:1px solid #e4ddd0}
.brand{display:flex;gap:8px;align-items:center;font-weight:800;font-size:18px;color:var(--sea2);letter-spacing:-.5px}
.nav .links{display:flex;gap:22px;font-size:14px;font-weight:500;color:#40576a;margin-left:12px}.nav .links a:hover{color:var(--sea)}
.nav .s{margin-left:auto;background:#fff;border:1px solid #e0d9cb;border-radius:99px;padding:8px 18px;font-size:13px;color:#9aa;width:240px}
.hero{position:relative;height:520px;overflow:hidden;color:#fff}
.hero>img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;filter:saturate(1.1)}
.hero:after{content:"";position:absolute;inset:0;background:linear-gradient(180deg,rgba(8,30,46,.25),rgba(8,30,46,.78))}
.hero .in{position:absolute;z-index:2;left:5vw;right:5vw;bottom:64px;max-width:1100px}
.hero small{display:inline-block;font-size:13px;letter-spacing:.3em;font-weight:700;color:#8fe3f3;margin-bottom:14px}
.hero h1{font-family:'Noto Serif KR',serif;font-size:56px;line-height:1.25;margin:0 0 16px;font-weight:900;letter-spacing:-1.5px}
.hero p{font-size:18px;margin:0 0 28px;color:#d8e8f0;max-width:620px}
.hero .search{display:flex;max-width:560px;background:#fff;border-radius:99px;padding:6px;box-shadow:0 14px 40px #0006}
.hero .search span{flex:1;padding:12px 22px;color:#8a99a6;font-size:15px}.hero .search b{background:var(--sea);color:#fff;border-radius:99px;padding:12px 28px;font-size:15px}
.stats{position:absolute;right:5vw;bottom:64px;z-index:2;display:flex;gap:34px;text-align:right}.stats div b{display:block;font-family:'Noto Serif KR';font-size:38px;font-weight:900}.stats div span{font-size:12px;letter-spacing:.2em;color:#bcd6e2}
.chips{display:flex;gap:10px;flex-wrap:wrap;padding:34px 5vw 6px}.chips a{padding:9px 20px;border-radius:99px;border:1px solid #d9d0bf;background:#fff;font-size:14px;font-weight:600;color:#40576a}
.chips a.on{background:var(--sea2);color:#fff;border-color:var(--sea2)}.chips a:hover:not(.on){border-color:var(--sea)}
.sec{padding:22px 5vw 10px}.sec h2{font-family:'Noto Serif KR';font-size:30px;margin:10px 0 4px;font-weight:900;letter-spacing:-1px}.sec .sub{color:var(--mut);font-size:14px;margin-bottom:22px}
.grid{display:grid;grid-template-columns:repeat(3,1fr);gap:28px 24px}
.card{display:block}.card .ph{position:relative;display:block;aspect-ratio:4/3;border-radius:18px;overflow:hidden;box-shadow:0 8px 24px #0f223314;transition:.35s}
.card .ph img{width:100%;height:100%;object-fit:cover;transition:transform .6s}.card:hover .ph img{transform:scale(1.07)}.card:hover .ph{box-shadow:0 16px 36px #0f223330}
.tg{position:absolute;bottom:12px;left:12px;font-style:normal;font-size:12px;font-weight:700;background:rgba(255,255,255,.92);color:var(--sea2);padding:3px 11px;border-radius:99px}.tg+.tg{left:auto;margin-left:58px}
.tx{display:block;padding:14px 4px 0}.tx b{display:block;font-family:'Noto Serif KR';font-size:20px;font-weight:700;letter-spacing:-.5px}.tx em{font-style:normal;font-size:13px;color:var(--mut)}
.card.c0{grid-column:span 2}.card.c0 .ph{aspect-ratio:2/1}
.adcard{border:1px dashed #cdbfa6;border-radius:18px;padding:14px;display:flex;gap:14px;align-items:center;background:#fffaf0;position:relative}.adcard img{width:110px;height:110px;border-radius:12px;object-fit:cover}
.adtag{position:absolute;top:8px;left:8px;background:rgba(0,0,0,.65);color:#fff;font-size:10.5px;font-weight:700;padding:3px 6px;border-radius:3px}
/* detail */
.ph-detail{max-width:980px;margin:56px auto 0;padding:0 5vw}.frame-title{text-align:center;font-size:12px;letter-spacing:.3em;color:#9a8f7a;margin:70px 0 14px}
.d-hero{position:relative;height:420px;border-radius:0 0 28px 28px;overflow:hidden;color:#fff}.d-hero img{width:100%;height:100%;object-fit:cover}
.d-hero:after{content:"";position:absolute;inset:0;background:linear-gradient(180deg,transparent 30%,rgba(8,30,46,.85))}
.d-hero .in{position:absolute;z-index:2;left:5vw;right:5vw;bottom:34px;max-width:900px}.crumb{font-size:13px;color:#bcd6e2;margin-bottom:10px}
.d-hero h1{font-family:'Noto Serif KR';font-size:38px;line-height:1.35;margin:0 0 14px;font-weight:900;letter-spacing:-1px}
.meta{display:flex;gap:8px;flex-wrap:wrap}.meta span{background:rgba(255,255,255,.18);border:1px solid rgba(255,255,255,.35);backdrop-filter:blur(6px);padding:4px 14px;border-radius:99px;font-size:13px}
.art{max-width:760px;margin:0 auto;padding:44px 5vw 20px;font-size:17px}
.info{display:grid;grid-template-columns:repeat(3,1fr);gap:1px;background:#e3dac8;border-radius:16px;overflow:hidden;margin-bottom:36px}.info div{background:#fff;padding:16px 18px}.info small{display:block;color:var(--mut);font-size:12px;letter-spacing:.1em}.info b{font-size:16px}
.art h3{font-family:'Noto Serif KR';font-size:25px;font-weight:900;margin:42px 0 12px;display:flex;gap:14px;align-items:baseline;letter-spacing:-.8px}.art h3 span{font-size:15px;color:var(--sea);letter-spacing:.1em;font-family:'Noto Sans KR';font-weight:800}
.art p{margin:0 0 16px}.art mark{background:linear-gradient(transparent 58%,#bfeaf2 58%);padding:0 2px;color:inherit}.art .photo{border-radius:16px;overflow:hidden;margin:26px 0}.art .photo img{width:100%}
.art .adbox{position:relative;margin:30px auto;width:min(340px,100%)}.art .adbox img{width:100%;border-radius:12px}
.fixbar{position:sticky;bottom:0;display:flex;justify-content:center;gap:10px;padding:12px;background:rgba(246,243,238,.94);backdrop-filter:blur(8px);border-top:1px solid #e4ddd0}
.fixbar a{padding:9px 22px;border-radius:99px;border:1px solid #cfc6b3;background:#fff;font-size:14px;font-weight:700;color:var(--sea2)}
@media(max-width:820px){.hero h1{font-size:34px}.stats{display:none}.grid{grid-template-columns:1fr 1fr}.card.c0{grid-column:span 2}.nav .links,.nav .s{display:none}.info{grid-template-columns:1fr}}
"""
    chips = "".join(f'<a class="{"on" if i == 3 else ""}" href="#">{r}</a>' for i, r in enumerate(REGIONS))
    body = f"""<div class="label">디자인 시안 A — 에디토리얼 (밝은 매거진 스타일)</div>
<div class="nav"><div class="brand">{WAVE}낚시·차박 포인트</div><div class="links"><a href="#">전체 포인트</a><a href="#">차박</a><a href="#">원투낚시</a><a href="#">워킹낚시</a></div><div class="s">포인트명, 지역명 검색</div></div>
<section class="hero"><img src="{IMG[0]}" alt=""><div class="in"><small>KOREA COASTAL POINTS</small><h1>바다 앞에서 머무는<br>차박·원투·워킹 낚시</h1><p>전국 533곳, 사진과 위치·진입 동선까지 지역별로 한눈에 찾아보세요.</p><div class="search"><span>포인트명, 지역명으로 검색</span><b>검색</b></div></div>
<div class="stats"><div><b>533</b><span>POINTS</span></div><div><b>9</b><span>REGIONS</span></div></div></section>
<div class="chips">{chips}</div>
<div class="sec"><h2>충남 포인트</h2><div class="sub">총 76개 · 최근 업데이트순</div><div class="grid">{cards_html('a')}
<div class="adcard"><span class="adtag">AD 광고</span><img src="{AD}" alt=""><div><b>카드형 광고</b><br><small style="color:#8a7a5a">목록 카드와 어울리는 모양</small></div></div></div></div>
<div class="frame-title">▼ 상세 페이지</div>
<div class="d-hero"><img src="{IMG[0]}" alt=""><div class="in"><div class="crumb">홈 › 인천·경기 › 강화군</div><h1>황산포구, 강화도 잔잔한 물결과 어울리는 차박·낚시 포인트</h1><div class="meta"><span>#차박</span><span>#원투낚시</span><span>#서해 갯벌</span></div></div></div>
<div class="art"><div class="info"><div><small>위치</small><b>인천 강화군 길상면</b></div><div><small>유형</small><b>원투 · 차박</b></div><div><small>베스트 시즌</small><b>가을~초겨울</b></div></div>
<p>{BODY_P} <mark>물때 확인이 입장 판단의 전부</mark>를 결정합니다.</p>
<div class="adbox"><span class="adtag">AD 광고</span><img src="{AD}" alt=""></div>
<h3><span>01</span>진입 동선과 포인트 접근성</h3><p>{BODY_P2}</p>
<div class="photo"><img src="{IMG[1]}" alt=""></div>
<h3><span>02</span>차박 환경과 야간 체류 여건</h3><p>주차 공간이 넉넉하고 해안 산책로 데크가 있어 야간에도 비교적 안전하게 머물 수 있습니다.</p></div>
<div class="fixbar"><a href="#">← 뒤로가기</a><a href="#">↑ 맨위로</a></div>"""
    return wrap("시안 A 에디토리얼", css, body,
                "https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;500;700;800&family=Noto+Serif+KR:wght@700;900&display=swap")


# ============================================================ B. 야간(다크)
def design_b():
    css = """
:root{--bg:#070d17;--card:#0f1a2b;--line:#1d2c44;--cy:#38e1ff;--am:#ffb454;--tx:#dbe7f3;--mut:#7f94ad}
body{font-family:'Noto Sans KR',sans-serif;background:var(--bg);color:var(--tx);line-height:1.7;background-image:radial-gradient(900px 500px at 85% -5%,#12385a66,transparent),radial-gradient(700px 420px at 0% 30%,#2a1a5a40,transparent)}
.label{position:sticky;top:0;z-index:50;background:#000;color:#8fb4d0;text-align:center;font-size:13px;padding:8px;border-bottom:1px solid var(--line)}
.layout{display:grid;grid-template-columns:230px 1fr;min-height:100vh}
.side{position:sticky;top:34px;height:calc(100vh - 34px);padding:22px 16px;border-right:1px solid var(--line);background:#0a1220cc;overflow:auto}
.brand{display:flex;gap:9px;align-items:center;font-weight:800;font-size:17px;color:#fff;margin-bottom:26px}.brand svg{color:var(--cy);filter:drop-shadow(0 0 8px var(--cy))}
.side small{display:block;color:var(--mut);font-size:11px;letter-spacing:.2em;margin:0 8px 8px}
.side a{display:flex;justify-content:space-between;padding:10px 12px;border-radius:10px;font-weight:700;font-size:14px;color:#a9bdd2;margin-bottom:3px}.side a em{font-style:normal;color:var(--mut);font-weight:400;font-size:12px}
.side a:hover{background:#14233a}.side a.on{background:linear-gradient(90deg,#0e4560,#0b2a45);color:#fff;box-shadow:inset 3px 0 var(--cy)}
.side .sub{margin:2px 0 8px 14px;padding-left:10px;border-left:1px solid var(--line)}.side .sub a{font-weight:400;font-size:13px;padding:6px 10px}.side .sub a.on{box-shadow:none;background:#12304a}
.main{padding:26px 34px}
.top{display:flex;align-items:center;gap:16px;margin-bottom:24px}.top h1{margin:0;font-size:26px;font-weight:800;letter-spacing:-.8px;background:linear-gradient(90deg,#fff,var(--cy));-webkit-background-clip:text;background-clip:text;color:transparent}
.top .s{margin-left:auto;display:flex;gap:8px}.top .s span{background:#0f1a2b;border:1px solid var(--line);border-radius:12px;padding:10px 16px;width:260px;font-size:13px;color:var(--mut)}.top .s b{background:linear-gradient(135deg,#1aa7c9,#2563eb);color:#fff;border-radius:12px;padding:10px 20px;font-size:14px;box-shadow:0 0 22px #1aa7c955}
.feat{position:relative;height:300px;border-radius:22px;overflow:hidden;border:1px solid var(--line);margin-bottom:26px}.feat img{width:100%;height:100%;object-fit:cover;opacity:.85}
.feat:after{content:"";position:absolute;inset:0;background:linear-gradient(90deg,rgba(7,13,23,.92),rgba(7,13,23,.1))}.feat .in{position:absolute;z-index:2;left:34px;bottom:30px;max-width:520px}
.badge{display:inline-block;font-size:11px;font-weight:800;letter-spacing:.15em;color:#001018;background:var(--am);padding:3px 10px;border-radius:99px;margin-bottom:10px}.feat h2{margin:0 0 6px;font-size:32px;letter-spacing:-1px}.feat p{margin:0;color:#b6c7da}
.grid{display:grid;grid-template-columns:repeat(3,1fr);gap:20px}
.card{display:block;border-radius:20px;background:var(--card);border:1px solid var(--line);overflow:hidden;transition:.3s}
.card:hover{transform:translateY(-6px);border-color:#2b6f8c;box-shadow:0 14px 40px #00000080,0 0 0 1px #38e1ff44,0 0 30px #38e1ff22}
.card .ph{position:relative;display:block;aspect-ratio:4/3;overflow:hidden}.card .ph img{width:100%;height:100%;object-fit:cover;filter:brightness(.88) saturate(1.05);transition:.5s}.card:hover .ph img{transform:scale(1.06);filter:brightness(1)}
.card .ph:after{content:"";position:absolute;inset:0;background:linear-gradient(180deg,transparent 55%,#0f1a2b)}
.tg{position:absolute;z-index:2;top:12px;left:12px;font-style:normal;font-size:11.5px;font-weight:800;color:var(--cy);background:#04101ccc;border:1px solid #38e1ff55;padding:2px 10px;border-radius:99px}.tg+.tg{left:64px;color:var(--am);border-color:#ffb45455}
.tx{display:block;padding:6px 18px 18px}.tx b{display:block;font-size:18px;color:#fff;letter-spacing:-.4px}.tx em{font-style:normal;font-size:13px;color:var(--mut)}
.adcard{position:relative;border-radius:20px;border:1px dashed #ffb45466;background:#1a1408;padding:14px;display:flex;gap:14px;align-items:center}.adcard img{width:100px;height:100px;border-radius:12px;object-fit:cover}
.adtag{position:absolute;top:8px;left:8px;z-index:3;background:rgba(0,0,0,.7);color:#fff;font-size:10.5px;font-weight:700;padding:3px 6px;border-radius:3px;border:1px solid #fff3}
.frame-title{text-align:center;font-size:12px;letter-spacing:.3em;color:#58708c;margin:60px 0 18px}
.art{max-width:800px;margin:0 auto;padding:6px 0 30px;font-size:16.5px}
.art .hero{position:relative;border-radius:22px;overflow:hidden;border:1px solid var(--line);margin-bottom:26px}.art .hero img{width:100%;height:340px;object-fit:cover}.art .hero:after{content:"";position:absolute;inset:0;background:linear-gradient(180deg,transparent 40%,#070d17)}
.art .hero .in{position:absolute;z-index:2;left:26px;right:26px;bottom:20px}.art .hero h1{margin:0 0 8px;font-size:30px;line-height:1.35;letter-spacing:-1px;color:#fff;text-shadow:0 2px 20px #000}
.pills{display:flex;gap:8px;flex-wrap:wrap}.pills span{font-size:12.5px;font-weight:700;padding:3px 13px;border-radius:99px;border:1px solid #38e1ff55;color:var(--cy);background:#04101c99}.pills span.am{color:var(--am);border-color:#ffb45466}
.info{display:grid;grid-template-columns:repeat(3,1fr);gap:12px;margin-bottom:30px}.info div{background:var(--card);border:1px solid var(--line);border-radius:14px;padding:14px 16px}.info small{display:block;color:var(--mut);font-size:12px}.info b{color:#fff}
.art h3{font-size:23px;margin:38px 0 12px;color:#fff;letter-spacing:-.6px;padding-left:14px;border-left:4px solid var(--cy);box-shadow:-8px 0 20px -10px var(--cy)}
.art p{margin:0 0 16px;color:#c3d2e2}.art mark{background:none;color:var(--am);font-weight:700;border-bottom:1px dashed #ffb45488}
.art .photo{border-radius:18px;overflow:hidden;border:1px solid var(--line);margin:24px 0}.art .photo img{width:100%}
.art .adbox{position:relative;margin:28px auto;width:min(320px,100%)}.art .adbox img{width:100%;border-radius:14px;border:1px solid var(--line)}
.fixbar{position:sticky;bottom:0;display:flex;justify-content:center;gap:10px;padding:12px;background:#070d17ee;backdrop-filter:blur(8px);border-top:1px solid var(--line)}
.fixbar a{padding:8px 22px;border-radius:12px;border:1px solid var(--line);background:#0f1a2b;font-size:14px;font-weight:700;color:var(--cy)}
@media(max-width:900px){.layout{grid-template-columns:1fr}.side{display:none}.grid{grid-template-columns:1fr 1fr}.info{grid-template-columns:1fr}.top .s span{width:140px}}
"""
    regs = "".join(f'<a class="{"on" if r == "충남" else ""}" href="#">{r}<em>{n}</em></a>' + ('<div class="sub"><a class="on" href="#">당진시<em>14</em></a><a href="#">태안군<em>33</em></a><a href="#">서산시<em>10</em></a></div>' if r == "충남" else "")
                   for r, n in zip(REGIONS, [533, 44, 0, 76, 25, 279, 2, 103, 4, 0]))
    body = f"""<div class="label">디자인 시안 B — 나이트 (야간 낚시 다크 테마)</div>
<div class="layout"><aside class="side"><div class="brand">{WAVE}낚시·차박 포인트</div><small>REGION</small>{regs}</aside>
<main class="main"><div class="top"><h1>전국 차박·원투·워킹 낚시 포인트</h1><div class="s"><span>포인트명, 지역명 검색</span><b>검색</b></div></div>
<div class="feat"><img src="{IMG[3]}" alt=""><div class="in"><span class="badge">TONIGHT'S PICK</span><h2>안섬포구</h2><p>충남 당진시 · 노을이 지면 불 켜지는 차박 감성 포인트</p></div></div>
<div class="grid">{cards_html('b')}<div class="adcard"><span class="adtag">AD 광고</span><img src="{AD}" alt=""><div><b>카드형 광고</b><br><small style="color:#a89060">목록 카드와 같은 크기</small></div></div></div>
<div class="frame-title">▼ 상세 페이지</div>
<div class="art"><div class="hero"><img src="{IMG[0]}" alt=""><div class="in"><h1>황산포구, 강화도 잔잔한 물결과 어울리는 차박·낚시 포인트</h1><div class="pills"><span>#차박</span><span>#원투낚시</span><span class="am">#서해 갯벌</span></div></div></div>
<div class="info"><div><small>위치</small><b>인천 강화군 길상면</b></div><div><small>유형</small><b>원투 · 차박</b></div><div><small>베스트 시즌</small><b>가을~초겨울</b></div></div>
<p>{BODY_P} <mark>물때 확인이 입장 판단의 전부</mark>를 결정합니다.</p>
<div class="adbox"><span class="adtag">AD 광고</span><img src="{AD}" alt=""></div>
<h3>진입 동선과 포인트 접근성</h3><p>{BODY_P2}</p><div class="photo"><img src="{IMG[1]}" alt=""></div></div></main></div>
<div class="fixbar"><a href="#">← 뒤로가기</a><a href="#">↑ 맨위로</a></div>"""
    return wrap("시안 B 나이트", css, body,
                "https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;500;700;800&display=swap")


# ============================================================ C. 아웃도어
def design_c():
    css = """
:root{--sand:#f2eadb;--ink:#26362b;--ol:#55742f;--or:#e0702b;--cr:#fffaf0;--ln:#d9ccb0}
body{font-family:'Noto Sans KR',sans-serif;background:var(--sand);color:var(--ink);line-height:1.7;
background-image:url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='400' height='400' viewBox='0 0 400 400' fill='none' stroke='%23d9ccb0' stroke-width='1.2'><path d='M-20 80c60-40 120 30 190-10s140 30 250-20M-20 130c60-40 120 30 190-10s140 30 250-20M-20 180c60-40 120 30 190-10s140 30 250-20M-20 230c60-40 120 30 190-10s140 30 250-20M-20 280c60-40 120 30 190-10s140 30 250-20M-20 330c60-40 120 30 190-10s140 30 250-20'/></svg>")}
.hd{font-family:'Black Han Sans',sans-serif;font-weight:400}
.label{position:sticky;top:0;z-index:50;background:var(--ink);color:#e8dcc0;text-align:center;font-size:13px;padding:8px}
.nav{position:sticky;top:34px;z-index:40;display:flex;align-items:center;gap:24px;padding:12px 5vw;background:var(--ink);color:#f2eadb}
.brand{display:flex;gap:8px;align-items:center;font-family:'Black Han Sans';font-size:21px;color:#ffd9b0;letter-spacing:.5px}.brand svg{color:var(--or)}
.nav .links{display:flex;gap:6px;margin-left:10px}.nav .links a{padding:7px 16px;border-radius:8px;font-weight:700;font-size:14px;color:#d8ccb2}.nav .links a.on,.nav .links a:hover{background:var(--or);color:#fff}
.nav .s{margin-left:auto;background:#34473a;border-radius:10px;padding:9px 18px;font-size:13px;color:#a8b8a8;width:240px}
.hero{padding:56px 5vw 36px;display:grid;grid-template-columns:1.1fr .9fr;gap:40px;align-items:center}
.hero small{display:inline-block;background:var(--or);color:#fff;font-weight:800;font-size:12px;letter-spacing:.14em;padding:4px 12px;border-radius:6px;transform:rotate(-2deg);margin-bottom:16px}
.hero h1{font-family:'Black Han Sans';font-weight:400;font-size:60px;line-height:1.15;margin:0 0 16px;letter-spacing:-1px;color:var(--ink)}.hero h1 em{font-style:normal;color:var(--or)}
.hero p{font-size:17px;color:#4b5d4f;margin:0 0 22px;max-width:520px}
.kw{display:flex;gap:10px;flex-wrap:wrap}.kw span{display:flex;gap:8px;align-items:center;background:var(--cr);border:2px solid var(--ink);border-radius:14px;padding:8px 16px;font-weight:800;box-shadow:3px 3px 0 var(--ink)}.kw span i{font-style:normal;font-size:20px}
.polaroid{position:relative;justify-self:center;background:#fff;padding:12px 12px 46px;border-radius:6px;box-shadow:0 14px 34px #26362b40;transform:rotate(3deg);width:min(420px,100%)}
.polaroid img{width:100%;aspect-ratio:4/3;object-fit:cover}.polaroid b{position:absolute;bottom:12px;left:0;right:0;text-align:center;font-family:'Black Han Sans';font-weight:400;font-size:20px;color:var(--ink)}
.polaroid:before{content:"";position:absolute;top:-14px;left:50%;width:90px;height:28px;margin-left:-45px;background:#e0702bcc;transform:rotate(-3deg)}
.bar{display:flex;gap:8px;flex-wrap:wrap;padding:14px 5vw}.bar a{padding:8px 18px;border:2px solid var(--ink);border-radius:99px;background:var(--cr);font-weight:800;font-size:14px;box-shadow:2px 2px 0 var(--ink)}.bar a.on{background:var(--ol);color:#fff;box-shadow:2px 2px 0 var(--ink)}
.sec{padding:10px 5vw}.sec h2{font-family:'Black Han Sans';font-weight:400;font-size:32px;margin:12px 0 18px}.sec h2 span{color:var(--or);font-size:18px;margin-left:8px;font-family:'Noto Sans KR';font-weight:800}
.grid{display:grid;grid-template-columns:repeat(3,1fr);gap:26px 22px}
.card{display:block;background:var(--cr);border:2px solid var(--ink);border-radius:18px;overflow:hidden;box-shadow:5px 5px 0 var(--ink);transition:.2s}
.card:hover{transform:translate(-3px,-3px);box-shadow:8px 8px 0 var(--or)}
.card .ph{position:relative;display:block;aspect-ratio:4/3;border-bottom:2px solid var(--ink)}.card .ph img{width:100%;height:100%;object-fit:cover}
.tg{position:absolute;top:10px;left:10px;font-style:normal;font-size:12px;font-weight:800;background:var(--or);color:#fff;padding:3px 10px;border-radius:6px;border:2px solid var(--ink)}.tg+.tg{left:62px;background:var(--ol)}
.tx{display:block;padding:12px 16px 14px}.tx b{display:block;font-family:'Black Han Sans';font-weight:400;font-size:21px}.tx em{font-style:normal;font-size:13px;color:#6b7a63}
.adcard{position:relative;background:#fff3d6;border:2px dashed var(--or);border-radius:18px;padding:14px;display:flex;gap:14px;align-items:center}.adcard img{width:104px;height:104px;border-radius:10px;object-fit:cover;border:2px solid var(--ink)}
.adtag{position:absolute;top:8px;left:8px;z-index:3;background:var(--ink);color:#fff;font-size:10.5px;font-weight:800;padding:3px 6px;border-radius:3px}
.frame-title{text-align:center;font-family:'Black Han Sans';font-size:18px;color:var(--or);margin:64px 0 14px}
.d-wrap{max-width:900px;margin:0 auto;padding:0 5vw 20px}
.d-top{position:relative;background:var(--cr);border:2px solid var(--ink);border-radius:22px;box-shadow:6px 6px 0 var(--ink);overflow:hidden}
.d-top img{width:100%;height:320px;object-fit:cover;border-bottom:2px solid var(--ink)}.d-top .in{padding:22px 28px}
.d-top h1{font-family:'Black Han Sans';font-weight:400;font-size:34px;line-height:1.3;margin:0 0 12px}
.badges{display:flex;gap:8px;flex-wrap:wrap}.badges span{font-weight:800;font-size:13px;padding:4px 12px;border-radius:8px;border:2px solid var(--ink);background:#fff}.badges .o{background:var(--or);color:#fff}.badges .g{background:var(--ol);color:#fff}
.art{background:var(--cr);border:2px solid var(--ink);border-radius:22px;box-shadow:6px 6px 0 var(--ink);padding:34px 40px;margin-top:26px;font-size:17px}
.info{display:grid;grid-template-columns:repeat(3,1fr);gap:12px;margin-bottom:26px}.info div{border:2px dashed #b9a982;border-radius:12px;padding:12px 14px;background:#fff}.info small{display:block;color:#7a8a6e;font-size:12px;font-weight:700}.info b{font-size:15px}
.art h3{font-family:'Black Han Sans';font-weight:400;font-size:25px;margin:34px 0 12px;display:flex;align-items:center;gap:12px}.art h3 span{background:var(--or);color:#fff;width:36px;height:36px;border-radius:50%;display:grid;place-items:center;font-size:17px;border:2px solid var(--ink);flex:none}
.art p{margin:0 0 16px}.art mark{background:#ffd98a;padding:1px 4px;border-radius:3px;color:inherit;font-weight:700}
.art .photo{border:2px solid var(--ink);border-radius:14px;overflow:hidden;margin:22px 0;box-shadow:4px 4px 0 var(--ink)}.art .photo img{width:100%}
.art .adbox{position:relative;margin:26px auto;width:min(330px,100%)}.art .adbox img{width:100%;border-radius:12px;border:2px solid var(--ink)}
.fixbar{position:sticky;bottom:0;display:flex;justify-content:center;gap:10px;padding:12px;background:var(--ink)}
.fixbar a{padding:8px 22px;border-radius:10px;background:var(--or);color:#fff;font-weight:800;font-size:14px;border:2px solid #fff3}
@media(max-width:860px){.hero{grid-template-columns:1fr}.hero h1{font-size:40px}.grid{grid-template-columns:1fr 1fr}.nav .links,.nav .s{display:none}.info{grid-template-columns:1fr}.art{padding:22px}}
"""
    regs = "".join(f'<a class="{"on" if r == "충남" else ""}" href="#">{r}</a>' for r in REGIONS)
    body = f"""<div class="label">디자인 시안 C — 아웃도어 (캠핑·차박 감성)</div>
<div class="nav"><div class="brand">{WAVE}낚시·차박 포인트</div><div class="links"><a class="on" href="#">전체</a><a href="#">차박</a><a href="#">원투</a><a href="#">워킹</a></div><div class="s">포인트명, 지역명 검색</div></div>
<section class="hero"><div><small>KOREA FISHING & CAR CAMPING</small><h1>바다 따라<br><em>차박</em> · <em>원투</em> · <em>워킹</em></h1><p>전국 해안 533곳의 낚시 포인트와 차박 여건을 직접 확인하고 떠나세요.</p>
<div class="kw"><span><i>🚐</i>차박</span><span><i>🎣</i>원투낚시</span><span><i>🥾</i>워킹낚시</span></div></div>
<div class="polaroid"><img src="{IMG[3]}" alt=""><b>안섬포구 · 충남 당진</b></div></section>
<div class="bar">{regs}</div>
<div class="sec"><h2>충남 포인트<span>총 76개</span></h2><div class="grid">{cards_html('c')}
<div class="adcard"><span class="adtag">AD 광고</span><img src="{AD}" alt=""><div><b>카드형 광고</b><br><small style="color:#9a7a3a">목록 카드 사이에 한 칸</small></div></div></div></div>
<div class="frame-title">▼ 상세 페이지</div>
<div class="d-wrap"><div class="d-top"><img src="{IMG[0]}" alt=""><div class="in"><h1>황산포구, 강화도 잔잔한 물결과 어울리는 차박·낚시 포인트</h1><div class="badges"><span class="o">🚐 차박</span><span class="g">🎣 원투낚시</span><span>🌊 서해 갯벌</span></div></div></div>
<div class="art"><div class="info"><div><small>📍 위치</small><b>인천 강화군 길상면</b></div><div><small>🎣 유형</small><b>원투 · 차박</b></div><div><small>📅 베스트 시즌</small><b>가을~초겨울</b></div></div>
<p>{BODY_P} <mark>물때 확인이 입장 판단의 전부</mark>를 결정합니다.</p>
<div class="adbox"><span class="adtag">AD 광고</span><img src="{AD}" alt=""></div>
<h3><span>1</span>진입 동선과 포인트 접근성</h3><p>{BODY_P2}</p><div class="photo"><img src="{IMG[1]}" alt=""></div></div></div>
<div class="fixbar"><a href="#">← 뒤로가기</a><a href="#">↑ 맨위로</a></div>"""
    return wrap("시안 C 아웃도어", css, body,
                "https://fonts.googleapis.com/css2?family=Black+Han+Sans&family=Noto+Sans+KR:wght@400;500;700;800&display=swap")


OUT.mkdir(exist_ok=True)
for name, fn in (("design_A_editorial", design_a), ("design_B_night", design_b), ("design_C_outdoor", design_c)):
    p = OUT / f"{name}.html"
    p.write_text(fn(), encoding="utf-8", newline="\n")
    print(p.name, p.stat().st_size // 1024, "KB")
