# -*- coding: utf-8 -*-
"""사이트 구조는 그대로 두고 '글꼴·색·테두리·그림자·제목 스타일'만 바꾼 디자인 시안 3종 생성.
→ tools/samples/theme_A_modern_blue.html / theme_B_forest.html / theme_C_night.html
실제 사이트 파일은 건드리지 않습니다(시안 전용)."""
import base64
import io
from pathlib import Path

import segno
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "tools" / "samples"


def uri(rel, w=640, q=70):
    im = Image.open(ROOT / rel).convert("RGB")
    im.thumbnail((w, w * 2))
    b = io.BytesIO()
    im.save(b, "JPEG", quality=q, optimize=True)
    return "data:image/jpeg;base64," + base64.b64encode(b.getvalue()).decode()


IMG = [uri("points/C001/image/001.jpg", 900), uri("points/C001/image/002.jpg", 600), uri("points/C001/image/003.jpg", 600),
       uri("points/C048/image/001.jpg", 600), uri("points/C048/image/002.jpg", 600), uri("points/C046/image/001.jpg", 600),
       uri("points/C046/image/002.jpg", 600)]
AD = uri("ad_image/001/001.jpg", 420)
buf = io.BytesIO()
segno.make("https://map.kakao.com/?q=test", error="m").save(buf, kind="svg", scale=3, border=1, xmldecl=False, svgns=True)
QR = buf.getvalue().decode()

CARDS = [("황산포구", "인천 강화군 길상면 초지리", 1), ("초지진선착장", "인천 강화군 길상면 초지리", 2), ("안섬포구", "충남 당진시 석문면 교로리", 3),
         ("한진포구(한진선착장)", "충남 당진시 송악읍 한진리", 5), ("석문방조제 주차장", "충남 당진시 석문면 통정리", 4), ("덕진진주차장", "인천 강화군 불은면 덕성리", 6)]
REG = [("전체", 533, ""), ("인천·경기", 44, ""), ("강원", 0, "u"), ("충남", 76, "on"), ("전북", 25, ""), ("전남", 279, ""), ("경북", 2, "u"), ("경남", 103, ""), ("부산·울산", 4, "u"), ("제주", 0, "u")]
WAVE = '<svg viewBox="0 0 32 32" fill="none"><path d="M3 19c5 0 7-6 13-6 5 0 7 4 13 1M3 24c5 0 7-5 13-5 5 0 7 4 13 0M5 13c4-3 7-7 12-7 4 0 7 3 11 2" stroke="currentColor" stroke-width="3" stroke-linecap="round"/></svg>'

# ---------------------------------------------------------------- 공통 구조 CSS (사이트 현재 구조와 동일한 배치)
BASE = """
*{box-sizing:border-box}body{margin:0;background:#8a97a6;font-family:var(--font);color:var(--text);font-size:14px;-webkit-font-smoothing:antialiased}
a{color:inherit;text-decoration:none}img{display:block}
.doc{max-width:1160px;margin:0 auto;padding:22px 16px 60px}.doc h1.t{color:#fff;font-size:22px;margin:0 0 4px}.doc p.d{color:#e3e9ef;margin:0 0 18px;font-size:14px}
.cap{color:#fff;font-weight:700;margin:26px 0 8px;font-size:15px}
.frame{position:relative;height:740px;overflow:hidden;border-radius:10px;background:var(--page);box-shadow:0 10px 40px #0004;--side:184px}
.scroll{position:absolute;inset:0;overflow:auto}
/* 사이드바 */
.sidebar{position:absolute;left:0;top:0;bottom:0;width:var(--side);background:var(--side-bg);color:var(--side-text);overflow:auto;z-index:12}
.brand{height:77px;margin:0 11px;border-bottom:1px solid var(--side-line);display:flex;align-items:center;gap:6px;color:var(--brand);font-size:15px;font-weight:800;letter-spacing:-.4px;white-space:nowrap;font-family:var(--font-h)}
.brand svg{width:24px;height:24px;flex:none;color:var(--brand-icon)}
.cap2{font-size:12px;color:var(--side-mut);padding:21px 22px 10px}
.rl{padding:0 11px 22px;display:grid;gap:2px}
.rb{display:flex;justify-content:space-between;align-items:center;border-radius:var(--side-radius);padding:12px 11px;font-size:14px;font-weight:700;min-height:39px;color:var(--side-text)}
.rb small{font-size:11px;color:var(--side-mut);font-weight:400}.rb .u{font-size:9.5px;color:var(--warn);margin-right:5px}
.rb:hover{background:var(--side-hover)}.rb.on{background:var(--side-active);color:#fff}.rb.on small{color:#ffffffcc}
.cl{display:grid;gap:1px;margin:1px 0 6px 10px;padding-left:8px;border-left:1px solid var(--side-line)}
.cb{display:flex;justify-content:space-between;padding:7px 9px;font-size:13px;color:var(--side-sub);border-radius:4px;min-height:30px;align-items:center}.cb small{font-size:11px}
.cb.on{background:var(--side-sub-active);color:#fff;font-weight:700}
/* 상단 바(고정) */
.top{position:absolute;top:0;left:var(--side);right:0;z-index:10;background:var(--bar-bg);border-bottom:1px solid var(--bar-line);padding:10px 24px;display:flex;align-items:center;gap:10px}
.btn{display:inline-flex;align-items:center;height:38px;padding:0 16px;border:1px solid var(--btn-line);background:var(--btn-bg);color:var(--btn-text);border-radius:var(--btn-radius);font-size:14px;font-weight:700;white-space:nowrap}
.ttl{margin:0 0 0 6px;font-size:18px;font-weight:800;letter-spacing:-.6px;font-family:var(--font-h);background:var(--h1-grad);-webkit-background-clip:text;background-clip:text;color:transparent}
.sf{margin-left:auto;display:flex;gap:7px}.sf span{display:flex;align-items:center;width:240px;height:38px;border:1px solid var(--input-line);background:var(--input-bg);border-radius:var(--btn-radius);padding:0 12px;font-size:13px;color:var(--mut)}
.sf b{display:flex;align-items:center;background:var(--primary);color:#fff;border-radius:var(--btn-radius);padding:0 17px;font-weight:600;font-size:14px}
.bot{position:absolute;bottom:0;left:var(--side);right:0;z-index:10;background:var(--bar-bg);border-top:1px solid var(--bar-line)}
.bot .bt{display:flex;justify-content:center;gap:10px;padding:8px 20px 4px}.bot .bt .btn{height:34px}
.bot .fl{display:flex;justify-content:space-between;gap:12px;padding:2px 24px 8px;font-size:12px;color:var(--mut)}.bot .fl nav{display:flex;gap:14px}
/* 목록 페이지 */
.main{margin-left:var(--side);padding:27px 35px 20px}
.topbar{display:flex;justify-content:space-between;align-items:center;gap:24px;margin-bottom:19px}
.topbar h1{margin:0;font-size:23px;line-height:1.4;font-weight:800;letter-spacing:-.8px;font-family:var(--font-h);background:var(--h1-grad);-webkit-background-clip:text;background-clip:text;color:transparent}
.subbar{border-bottom:1px solid var(--line);display:flex;justify-content:space-between;align-items:center;padding-bottom:10px;margin-bottom:16px}
.subbar h2{margin:0;font-size:16px;font-weight:700;color:var(--name);font-family:var(--font-h)}.subbar span{font-size:12px;color:var(--mut)}
.cards{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:18px 16px}
.card{display:block;border:var(--card-border);border-radius:var(--card-radius);overflow:hidden;background:var(--card-bg);box-shadow:var(--card-shadow);transition:.2s}
.card:hover{transform:translateY(-3px);box-shadow:var(--card-hover)}
.card.last{border:3px solid var(--last)}
.card .ph{display:block;position:relative;aspect-ratio:1.335/1;overflow:hidden}.card .ph img{width:100%;height:100%;object-fit:cover;transition:transform .5s}.card:hover .ph img{transform:scale(1.05)}
.card .ph:after{content:"";position:absolute;inset:0;box-shadow:var(--img-inset);pointer-events:none}
.ci{padding:10px 14px 12px}.ci b{display:block;font-weight:800;font-size:17px;line-height:1.5;color:var(--name);letter-spacing:-.4px;font-family:var(--font-h);white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.ci em{display:block;font-style:normal;font-size:12px;color:var(--mut);margin-top:2px}
.pager{display:flex;justify-content:center;gap:5px;margin:26px 0 8px}.pager span{min-width:34px;height:34px;display:grid;place-items:center;border:1px solid var(--line);background:var(--card-bg);border-radius:var(--btn-radius);color:var(--btn-text);font-size:13px}.pager .a{background:var(--primary);color:#fff;border-color:var(--primary);font-weight:700}
/* 상세 페이지 */
.wrapd{margin-left:var(--side);padding:76px 0 96px}
.container{max-width:900px;margin:22px auto;padding:36px 46px;background:var(--paper);border:var(--paper-border);border-radius:var(--paper-radius);box-shadow:var(--paper-shadow);color:var(--ptext);font-size:15.5px;line-height:1.9;word-break:keep-all}
.container h1{font-size:30px;line-height:1.45;margin:0;padding:22px 0 24px;font-weight:800;letter-spacing:-.04em;font-family:var(--font-h);color:var(--h1c)}
.divider{height:2px;background:var(--divider);margin:0 0 20px}
.disc{font-size:12.5px;line-height:1.7;color:var(--mut);background:var(--disc-bg);border-radius:6px;padding:8px 12px;margin:0 0 6px}
.photo{position:relative;margin:26px 0;border-radius:var(--photo-radius);overflow:hidden;border:var(--photo-border);box-shadow:var(--photo-shadow);background:var(--photo-bg);padding:var(--photo-pad)}
.photo img{width:100%;border-radius:calc(var(--photo-radius) - 2px)}
.credit{position:absolute;right:calc(8px + var(--photo-pad));bottom:calc(8px + var(--photo-pad));font-size:11px;line-height:1.3;color:#fff;background:rgba(0,0,0,.55);border-radius:3px;padding:3px 7px}
.ad{text-align:center;margin:24px 0}.ad .in{position:relative;display:inline-block;width:300px;border-radius:var(--ad-radius);overflow:hidden;border:var(--ad-border)}.ad img{width:100%}
.adl{position:absolute;top:8px;left:8px;background:rgba(0,0,0,.62);color:#fff;font-size:11px;font-weight:700;padding:4px 6px;border-radius:3px;line-height:1;letter-spacing:.04em}
.container h2{font-size:23px;margin:26px 0 12px;font-weight:800;letter-spacing:-.03em;font-family:var(--font-h);color:var(--h2c);border-left:var(--h2-bar);padding-left:13px}
.container h3{font-size:21px;margin:34px 0 18px;font-weight:800;letter-spacing:-.03em;font-family:var(--font-h);color:var(--h3c);border-left:var(--h3-bar);border-bottom:var(--h3-under);padding:0 0 9px 15px;line-height:1.4}
.container p{margin:0 0 16px}
.hl{font-weight:700;color:var(--hlc);background:var(--hl-bg);padding:0 3px;border-radius:3px}
.pinfo{margin:8px 0 18px;padding:14px 18px;background:var(--box-bg);border:var(--box-border);border-radius:var(--box-radius)}.pinfo b{display:block;font-size:17px;color:var(--name)}.pinfo span{color:var(--mut);font-size:14px}
.kakao{margin:30px 0 0;padding:16px 18px;border:var(--box-border);background:var(--box-bg);border-radius:var(--box-radius);display:flex;gap:18px;align-items:center;font-size:14px;line-height:1.7}
.kakao .qr{width:104px;height:104px;background:#fff;padding:4px;border-radius:4px;flex:none}.kakao .qr svg{width:100%;height:100%}
.safe{margin:22px 0 0;padding:16px 18px;background:var(--safe-bg);border:1px solid var(--safe-line);border-radius:var(--box-radius);font-size:14px;line-height:1.75;color:var(--safe-text)}.safe strong{display:block;margin-bottom:4px;color:var(--safe-h)}.safe ul{margin:6px 0 0;padding-left:18px}
.tags{display:flex;flex-wrap:wrap;gap:8px;justify-content:center;padding:34px 0 6px}.tags span{font-size:13.5px;color:var(--tag-text);background:var(--tag-bg);border:var(--tag-border);padding:3px 13px;border-radius:99px}
"""

THEMES = {
    "theme_A_modern_blue": dict(
        name="A. 모던 블루", desc="지금의 네이비·블루 톤을 유지하면서 더 밝고 정돈된 느낌 — 카드 둥글기·그림자·제목 그라데이션을 다듬은 안",
        fonts="family=Noto+Sans+KR:wght@400;500;700;800",
        vars="""--font:'Noto Sans KR',sans-serif;--font-h:'Noto Sans KR',sans-serif;--text:#213b53;--mut:#7a90a4;--page:#f3f6fa;--line:#dfe7ef;
--side-bg:linear-gradient(180deg,#0e2740,#123a5e);--side-text:#c6d6e4;--side-mut:#85a3bb;--side-line:#2c4a66;--brand:#fff;--brand-icon:#63d2f5;--side-radius:8px;--side-hover:#1b4468;--side-active:linear-gradient(90deg,#1f78c0,#2a8fd9);--side-sub:#a9c1d4;--side-sub-active:#1c557f;--warn:#ffc46b;
--bar-bg:#fffffff0;--bar-line:#dfe7ef;--btn-line:#cddbe8;--btn-bg:#fff;--btn-text:#14629e;--btn-radius:10px;--input-line:#cddbe8;--input-bg:#fff;--primary:#1b6fb5;
--h1-grad:linear-gradient(90deg,#0e2740,#1f78c0);--name:#0e2740;
--card-border:1px solid #e1e8f0;--card-radius:16px;--card-bg:#fff;--card-shadow:0 2px 6px #0e274010,0 8px 24px #0e27400a;--card-hover:0 14px 34px #0e274026;--img-inset:inset 0 -40px 40px -40px #0e274044;--last:#f08a24;
--paper:#fff;--paper-border:1px solid #e1e8f0;--paper-radius:18px;--paper-shadow:0 10px 40px #0e27400d;--ptext:#2b3a4a;--h1c:#0e2740;--divider:linear-gradient(90deg,#1f78c0,#8fd3f4,transparent);--disc-bg:#f1f6fb;
--photo-radius:16px;--photo-border:1px solid #dfe7ef;--photo-shadow:0 8px 24px #0e274018;--photo-bg:transparent;--photo-pad:0px;--ad-radius:14px;--ad-border:1px solid #dfe7ef;
--h2c:#0e2740;--h2-bar:5px solid #1f78c0;--h3c:#0e2740;--h3-bar:5px solid #1f78c0;--h3-under:1px solid #dfe7ef;--hlc:#0e2740;--hl-bg:linear-gradient(transparent 55%,#bfe3fa 55%);
--box-bg:#f6f9fc;--box-border:1px solid #dfe7ef;--box-radius:12px;--safe-bg:#fff8ec;--safe-line:#f3dcb2;--safe-text:#4b4030;--safe-h:#7a4b00;--tag-text:#1f78c0;--tag-bg:#eaf4fc;--tag-border:1px solid #cfe5f6;""",
        extra=""),
    "theme_B_forest": dict(
        name="B. 포레스트 캠프", desc="차박·캠핑 감성의 딥그린 + 크림 톤 — 세리프 제목, 사진 인화지 같은 흰 테두리, 따뜻한 강조색",
        fonts="family=Noto+Sans+KR:wght@400;500;700&family=Noto+Serif+KR:wght@600;700;900",
        vars="""--font:'Noto Sans KR',sans-serif;--font-h:'Noto Serif KR',serif;--text:#33413a;--mut:#7d8a7e;--page:#f2eee3;--line:#d9d1bd;
--side-bg:#1e382b;--side-text:#d4dfd2;--side-mut:#8fa896;--side-line:#34533f;--brand:#f6e7c4;--brand-icon:#e3a948;--side-radius:6px;--side-hover:#2a4a39;--side-active:#c77d2a;--side-sub:#b7c9b9;--side-sub-active:#355f46;--warn:#f5c56a;
--bar-bg:#f7f3e8f2;--bar-line:#d9d1bd;--btn-line:#cfc5ab;--btn-bg:#fffdf6;--btn-text:#2c5a3f;--btn-radius:8px;--input-line:#cfc5ab;--input-bg:#fffdf6;--primary:#2c5a3f;
--h1-grad:linear-gradient(90deg,#1e382b,#4d7a3e);--name:#1e382b;
--card-border:1.5px solid #d9cfb4;--card-radius:10px;--card-bg:#fffdf6;--card-shadow:0 2px 0 #d9cfb4;--card-hover:0 6px 0 #c9bb98,0 12px 24px #1e382b22;--img-inset:inset 0 0 0 5px #fffdf6;--last:#c77d2a;
--paper:#fffdf6;--paper-border:1.5px solid #d9cfb4;--paper-radius:14px;--paper-shadow:0 3px 0 #d9cfb4;--ptext:#33413a;--h1c:#1e382b;--divider:repeating-linear-gradient(90deg,#b9a679 0 8px,transparent 8px 14px);--disc-bg:#f4efdf;
--photo-radius:4px;--photo-border:1px solid #d9cfb4;--photo-shadow:0 6px 18px #1e382b26;--photo-bg:#fff;--photo-pad:10px;--ad-radius:6px;--ad-border:6px solid #fff;
--h2c:#1e382b;--h2-bar:0 solid transparent;--h3c:#1e382b;--h3-bar:0 solid transparent;--h3-under:2px dotted #8fa57e;--hlc:#6b3d00;--hl-bg:linear-gradient(transparent 50%,#f3d99a 50%);
--box-bg:#f8f3e4;--box-border:1.5px dashed #c9bb98;--box-radius:10px;--safe-bg:#fbefd8;--safe-line:#e6c98a;--safe-text:#4b3c20;--safe-h:#8a4b00;--tag-text:#2c5a3f;--tag-bg:#e8efdf;--tag-border:1px solid #c9d8bb;""",
        extra=".container h2{padding-left:0}.container h3:before{content:'🌲';margin-right:8px;font-size:.8em}.ad .in{box-shadow:0 6px 16px #1e382b30}"),
    "theme_C_night": dict(
        name="C. 나이트 다크", desc="야간 낚시 분위기의 다크 테마 — 어두운 배경에 청록 포인트, 카드는 마우스를 올리면 은은하게 빛남",
        fonts="family=Noto+Sans+KR:wght@400;500;700;800",
        vars="""--font:'Noto Sans KR',sans-serif;--font-h:'Noto Sans KR',sans-serif;--text:#cdd9e6;--mut:#7f93aa;--page:#0b131e;--line:#1f2f45;
--side-bg:#070d16;--side-text:#aebfd1;--side-mut:#667b93;--side-line:#1a2a40;--brand:#fff;--brand-icon:#38e1ff;--side-radius:10px;--side-hover:#111e30;--side-active:linear-gradient(90deg,#0e5f7a,#0c4666);--side-sub:#8ea5bd;--side-sub-active:#10405a;--warn:#ffb454;
--bar-bg:#0b131ef2;--bar-line:#1f2f45;--btn-line:#26395a;--btn-bg:#111e30;--btn-text:#5fd8f2;--btn-radius:10px;--input-line:#26395a;--input-bg:#0f1a2a;--primary:#1a8fb3;
--h1-grad:linear-gradient(90deg,#ffffff,#38e1ff);--name:#f1f6fb;
--card-border:1px solid #213249;--card-radius:14px;--card-bg:#101b2b;--card-shadow:0 2px 10px #0006;--card-hover:0 0 0 1px #38e1ff55,0 12px 34px #000a,0 0 28px #38e1ff22;--img-inset:inset 0 -50px 40px -40px #101b2b;--last:#ffb454;
--paper:#101a28;--paper-border:1px solid #1f2f45;--paper-radius:16px;--paper-shadow:0 10px 40px #0008;--ptext:#c3d1e0;--h1c:#fff;--divider:linear-gradient(90deg,#38e1ff,#2563eb,transparent);--disc-bg:#0c1522;
--photo-radius:12px;--photo-border:1px solid #223249;--photo-shadow:0 10px 30px #000a;--photo-bg:transparent;--photo-pad:0px;--ad-radius:12px;--ad-border:1px solid #223249;
--h2c:#fff;--h2-bar:4px solid #38e1ff;--h3c:#fff;--h3-bar:4px solid #38e1ff;--h3-under:1px solid #1f2f45;--hlc:#ffb454;--hl-bg:transparent;
--box-bg:#0c1522;--box-border:1px solid #1f2f45;--box-radius:12px;--safe-bg:#1b1508;--safe-line:#5a4417;--safe-text:#d6c49a;--safe-h:#ffb454;--tag-text:#7fe3f8;--tag-bg:#0c2230;--tag-border:1px solid #1d4a5e;""",
        extra=".container h3{box-shadow:-10px 0 24px -14px #38e1ff}.hl{border-bottom:1px dashed #ffb45488;border-radius:0}.card.last{box-shadow:0 0 22px #ffb45455}"),
}


def build(key, th):
    regs = "".join(
        f'<a class="rb {c}" href="#"><span>{n}</span><small>{"<span class=u>업데이트중</span>" if c == "u" else ""}{k}</small></a>'
        + ('<div class="cl"><a class="cb" href="#"><span>전체</span><small>76</small></a><a class="cb on" href="#"><span>당진시</span><small>14</small></a>'
           '<a class="cb" href="#"><span>보령시</span><small>4</small></a><a class="cb" href="#"><span>서산시</span><small>10</small></a><a class="cb" href="#"><span>태안군</span><small>33</small></a></div>' if c == "on" else "")
        for n, k, c in REG)
    regs = regs.replace('class="rb u"', 'class="rb"')
    side = f'<aside class="sidebar"><a class="brand" href="#">{WAVE}낚시·차박 포인트</a><div class="cap2">지역 카테고리</div><nav class="rl">{regs}</nav></aside>'
    cards = "".join(f'<a class="card{" last" if i == 2 else ""}" href="#"><span class="ph"><img src="{IMG[im]}" alt=""></span><span class="ci"><b>{n}</b><em>{a}</em></span></a>'
                    for i, (n, a, im) in enumerate(CARDS))
    index = f"""<div class="frame">{side}<div class="scroll"><div class="main">
<div class="topbar"><h1>전국 차박·원투·워킹 낚시 포인트</h1><div class="sf"><span>포인트명, 지역명으로 검색</span><b>검색</b></div></div>
<div class="subbar"><h2>충남 당진시 포인트</h2><span>총 14개</span></div><div class="cards">{cards}</div>
<div class="pager"><span>이전</span><span class="a">1</span><span>2</span><span>다음</span></div></div></div></div>"""
    detail = f"""<div class="frame">{side}
<div class="top"><span class="btn">← 뒤로가기</span><div class="ttl">전국 차박·원투·워킹 낚시 포인트</div><div class="sf"><span>포인트명, 지역명으로 검색</span><b>검색</b></div></div>
<div class="scroll"><div class="wrapd"><div class="container">
<h1>황산포구, 강화도 인천 강화군 잔잔한 물결과 어울리는 차박, 낚시 한적한 포인트</h1><div class="divider"></div>
<p class="disc">이 페이지에는 <b>광고</b>(제휴 링크 포함)가 있으며, 광고 링크를 통해 구매하면 운영자가 판매 수익 또는 수수료를 받을 수 있습니다.</p>
<div class="photo"><img src="{IMG[0]}" alt=""><span class="credit">출처 : 카카오맵 (https://map.kakao.com)</span></div>
<div class="ad"><div class="in"><span class="adl">AD 광고</span><img src="{AD}" alt=""></div></div>
<h2>포인트 안내</h2><div class="pinfo"><b>황산포구</b><span>인천 강화군 길상면 초지리 1331-19</span></div>
<p>강화 남단 갯벌 포인트는 밀물 타이밍을 놓치면 어떤 채비로도 낚시 자체가 성립하지 않습니다. 황산포구는 간조 시 광범위한 갯벌이 드러나는 구조로, <span class="hl">물때 확인이 입장 판단의 전부를 결정</span>하는 곳입니다.</p>
<h3>1. 진입 동선과 포인트 접근성</h3>
<p>초지대교 인근 연륙교로 연결된 황산도에 자리한 소형 어항입니다. 물양장 조성과 선착장 정비가 완료되어 차량 진입이 수월하고, 포구 앞 공영 주차 공간을 이용할 수 있습니다.</p>
<div class="photo"><img src="{IMG[1]}" alt=""><span class="credit">출처 : 카카오맵 (https://map.kakao.com)</span></div>
<h3>2. 차박 환경과 야간 체류 여건</h3>
<p>해안 산책로 데크가 있어 야간에도 비교적 안전하게 머물 수 있으며, <span class="hl">들물 타이밍</span>에 맞춰 채비를 던지고 차에서 쉬는 출조가 어울립니다.</p>
<div class="kakao"><div class="qr">{QR}</div><div><b>카카오맵 해당 위치로 바로 가기</b><br>QR 코드를 스캔하거나 <u>여기를 눌러</u> 카카오맵에서 위치를 확인하세요.<br><small style="color:var(--mut)">출처 : 카카오맵 (https://map.kakao.com)</small></div></div>
<div class="safe"><strong>방문 전 확인하세요</strong><ul><li>이 글은 참고 정보입니다. 현장 안내판과 지자체·해양경찰 공지가 우선합니다.</li><li>테트라포드·갯바위·방파제 끝단은 추락 위험이 큽니다. 구명조끼를 착용하세요.</li></ul></div>
<div class="tags"><span>#강화도낚시</span><span>#황산포구낚시</span><span>#강화갯벌낚시</span><span>#강화차박</span></div>
</div></div></div>
<div class="bot"><div class="bt"><span class="btn">← 뒤로가기</span><span class="btn">↑ 맨위로</span></div><div class="fl"><nav><span>사이트 소개</span><span>전체 포인트 목록</span><span>개인정보처리방침</span><span>이용약관</span></nav><span>© 2026 차박·원투·워킹 낚시 포인트</span></div></div></div>"""
    html = f"""<!doctype html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>디자인 시안 {th['name']}</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link rel="stylesheet" href="https://fonts.googleapis.com/css2?{th['fonts']}&display=swap">
<style>:root{{{th['vars']}}}{BASE}{th['extra']}</style></head><body><div class="doc">
<h1 class="t">디자인 시안 — {th['name']}</h1><p class="d">{th['desc']}. 사이트 구조(왼쪽 메뉴·상단/하단 고정 바·카드 배치·글 순서)는 지금과 같고, 글꼴·색·테두리·그림자·제목 스타일만 달라졌습니다. 각 화면은 안에서 스크롤됩니다.</p>
<div class="cap">① 목록 페이지</div>{index}<div class="cap">② 포인트 상세 페이지 (상단·하단 바 고정)</div>{detail}</div></body></html>"""
    return html


OUT.mkdir(exist_ok=True)
for k, th in THEMES.items():
    p = OUT / f"{k}.html"
    p.write_text(build(k, th), encoding="utf-8", newline="\n")
    print(p.name, p.stat().st_size // 1024, "KB")
