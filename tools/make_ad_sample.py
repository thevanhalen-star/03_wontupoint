# -*- coding: utf-8 -*-
"""광고 배치 예시 페이지(tools/samples/ad_layout_sample.html) 생성 — 이미지를 내장해 단독으로 열리는 한 파일."""
import base64
import io
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parent.parent


def data_uri(rel, width, q=72):
    im = Image.open(ROOT / rel).convert("RGB")
    im.thumbnail((width, width * 2))
    buf = io.BytesIO()
    im.save(buf, "JPEG", quality=q, optimize=True)
    return "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode()


AD = [data_uri(f"ad_image/00{n}/001.jpg", 360) for n in range(1, 5)]
P1 = data_uri("points/C001/image/001.jpg", 900)
P2 = data_uri("points/C001/image/002.jpg", 700)
P3 = data_uri("points/C001/image/003.jpg", 520)

HTML = """<!doctype html>
<html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>광고 배치 예시 (시안)</title>
<style>
:root{--navy:#10283c;--blue:#1d669f;--line:#dee6ed;--bg:#f2f5f9;--tag:#e8590c}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:#213b53;font-family:"Noto Sans KR","Malgun Gothic",system-ui,sans-serif;line-height:1.7}
.wrap{max-width:1180px;margin:0 auto;padding:28px 18px 80px}
h1.doc{font-size:26px;margin:0 0 6px}.lead{color:#5b7186;margin:0 0 26px}
h2.part{font-size:20px;margin:46px 0 14px;padding-left:12px;border-left:6px solid var(--blue)}
.note{display:inline-flex;align-items:center;justify-content:center;width:24px;height:24px;border-radius:50%;background:var(--tag);color:#fff;font-size:13px;font-weight:700;flex:none}
.legend{background:#fff;border:1px solid var(--line);border-radius:10px;padding:14px 18px;margin:0 0 18px}
.legend li{margin:4px 0;list-style:none;display:flex;gap:10px;align-items:flex-start}.legend ul{margin:0;padding:0}
.legend b{color:var(--navy)}
.mock{background:#fff;border:1px solid var(--line);border-radius:12px;overflow:hidden;box-shadow:0 6px 24px #10283c14}
/* ---- 메인 목 ---- */
.m-layout{display:grid;grid-template-columns:184px 1fr}
.m-side{background:var(--navy);color:#c0d0de;padding:16px 12px;font-size:14px;position:relative;min-height:560px}
.m-side b{display:block;color:#fff;font-size:15px;margin-bottom:14px}.m-side div{padding:9px 10px;border-radius:5px;font-weight:700}.m-side .on{background:#2069a1;color:#fff}
.m-main{padding:20px 24px}.m-main h3{margin:0 0 14px;font-size:20px}
.cards{display:grid;grid-template-columns:repeat(3,1fr);gap:14px}
.card{border:1px solid #e0e7ee;border-radius:6px;overflow:hidden;background:#fff;position:relative}
.card .ph{aspect-ratio:1.33;background:#cfd9e2;display:block;width:100%;object-fit:cover}.card .t{padding:8px 10px}.card .t b{font-size:15px}.card .t span{display:block;font-size:12px;color:#7991a6}
.card.ad{border:2px dashed var(--tag)}
.adtag{position:absolute;top:8px;left:8px;z-index:2;background:rgba(0,0,0,.62);color:#fff;font-size:11px;font-weight:700;padding:4px 6px;border-radius:3px;line-height:1}
.pos{position:absolute;z-index:3}.pos.tl{top:-10px;right:-10px}
.side-ad{position:absolute;left:12px;right:12px;bottom:14px;border-radius:6px;overflow:hidden;border:2px dashed var(--tag);background:#fff}
.side-ad img{display:block;width:100%}
.bandwrap{position:relative;margin:16px 0 0}
.band{border:2px dashed var(--tag);border-radius:6px;padding:12px 16px;background:#fff8f3;display:flex;align-items:center;gap:14px;position:relative}
.band img{width:64px;height:64px;border-radius:5px;object-fit:cover}.band small{color:#8a6a58}
/* ---- 상세 목 ---- */
.d-layout{display:grid;grid-template-columns:184px 1fr}
.d-body{padding:24px 38px;background:#f7f8fa}
.article{background:#fff;border:1px solid var(--line);border-radius:12px;padding:30px 40px;max-width:900px;margin:0 auto}
.article h4{font-size:27px;margin:0 0 8px;color:#225032;line-height:1.4}
.article h5{font-size:20px;margin:22px 0 8px;border-bottom:2px solid #336B46;padding-bottom:6px;color:#225032}
.article p{margin:0 0 12px}.article .ph{width:100%;display:block;border-radius:4px}
.slot{position:relative;margin:26px 0;border:2px dashed var(--tag);border-radius:10px;padding:14px;background:#fff8f3}
.slot>.note{position:absolute;top:-12px;left:-12px}
.slot-title{font-size:12px;color:#8a6a58;margin:0 0 8px}
.ad-sq{position:relative;display:block;width:300px;max-width:100%;margin:0 auto}.ad-sq img{display:block;width:100%;border-radius:4px}
.prod{display:grid;grid-template-columns:repeat(3,1fr);gap:12px}
.prod .p{border:1px solid #e0e7ee;border-radius:8px;background:#fff;overflow:hidden;position:relative}
.prod .p img{width:100%;display:block;aspect-ratio:1;object-fit:cover}.prod .p div{padding:8px 10px;font-size:13px}.prod .p b{display:block;font-size:14px}.prod .p em{font-style:normal;color:#c0392b;font-weight:700}
.dnote{font-size:12px;color:#6b7f90;margin-top:8px;text-align:center}
.native{display:flex;gap:14px;align-items:center}.native img{width:110px;height:110px;border-radius:8px;object-fit:cover}
.native b{display:block;font-size:16px}.native span{font-size:13px;color:#5b7186}
.btn{display:inline-block;margin-top:8px;background:var(--blue);color:#fff;font-size:13px;font-weight:700;padding:7px 14px;border-radius:6px}
@media(max-width:820px){.m-layout,.d-layout{grid-template-columns:1fr}.m-side{display:none}.cards{grid-template-columns:1fr 1fr}.prod{grid-template-columns:1fr}.article{padding:20px}.d-body{padding:14px}}
</style></head><body><div class="wrap">

<h1 class="doc">광고 배치 시안 (예시)</h1>
<p class="lead">애드센스 외 광고(제휴 링크·직접 협의 배너)를 붙인다면 이런 모습이라는 시안입니다. 실제 사이트 파일은 바뀌지 않았고, 이 파일은 단독으로 열립니다.</p>
<div class="legend"><ul>
<li><span class="note">!</span><span><b>주황 점선 박스</b> = 광고 자리 / 모든 광고에는 이미지 모퉁이의 <b>AD 광고</b> 표시와 페이지 상단 안내 문구를 유지합니다.</span></li>
<li><span class="note">상품</span><span>상품형(제휴) 광고는 글 내용과 어울리는 용품을 3개 카드로 보여줍니다. 아래 상품명·가격은 자리 표시용 가짜 문구입니다.</span></li>
</ul></div>

<h2 class="part">① 메인(목록) 페이지 — 광고는 적게, 눈에 덜 띄게</h2>
<div class="mock"><div class="m-layout">
 <div class="m-side"><b>낚시·차박 포인트</b><div>전체</div><div class="on">충남</div><div>전북</div><div>전남</div><div>경남</div><div>제주</div>
  <div class="side-ad"><span class="adtag">AD 광고</span><img src="__AD1__" alt=""><span class="note pos tl" style="top:-12px;right:-6px">1</span></div></div>
 <div class="m-main"><h3>충남 포인트</h3>
  <div class="cards">
   <div class="card"><img class="ph" src="__P1__" alt=""><div class="t"><b>황산포구</b><span>인천 강화군 길상면</span></div></div>
   <div class="card"><img class="ph" src="__P2__" alt=""><div class="t"><b>초지진 공영주차장</b><span>인천 강화군 길상면</span></div></div>
   <div class="card"><img class="ph" src="__P3__" alt=""><div class="t"><b>초지진선착장</b><span>인천 강화군 길상면</span></div></div>
   <div class="card"><img class="ph" src="__P2__" alt=""><div class="t"><b>덕진진주차장</b><span>인천 강화군 불은면</span></div></div>
   <div class="card ad"><span class="adtag">AD 광고</span><img class="ph" src="__AD2__" alt="" style="aspect-ratio:1.33;object-position:center"><div class="t"><b>카드형 광고</b><span>목록 카드와 같은 모양 · 9개마다 1개</span></div><span class="note pos tl">2</span></div>
   <div class="card"><img class="ph" src="__P3__" alt=""><div class="t"><b>석문방조제 주차장</b><span>충남 당진시</span></div></div>
  </div>
  <div class="bandwrap"><div class="band"><span class="adtag" style="position:static">AD 광고</span><img src="__AD3__" alt=""><div><b>하단 띠 배너</b><br><small>페이지 맨 아래(페이지 번호 위) 1개 · 높이 낮게</small></div><span class="note pos tl">3</span></div></div>
 </div></div></div>
<div class="legend" style="margin-top:12px"><ul>
<li><span class="note">1</span><span><b>왼쪽 메뉴 아래 작은 배너</b> — 항상 보이지만 본문을 가리지 않는 자리</span></li>
<li><span class="note">2</span><span><b>카드형 광고</b> — 목록 카드 9개마다 1개. 점선·AD 표시로 구분하되 모양은 비슷하게</span></li>
<li><span class="note">3</span><span><b>하단 띠 배너</b> — 목록을 다 본 뒤에 나오는 낮은 배너</span></li>
</ul></div>

<h2 class="part">② 포인트 상세 페이지 — 글 흐름에 맞춰 3~4곳</h2>
<div class="mock"><div class="d-layout">
 <div class="m-side"><b>낚시·차박 포인트</b><div>전체</div><div class="on">인천·경기</div><div>강원</div><div>충남</div></div>
 <div class="d-body"><div class="article">
  <h4>황산포구, 강화도 잔잔한 물결과 어울리는 차박, 낚시 한적한 포인트</h4>
  <p style="font-size:12px;color:#5b6b78;background:#f4f7fa;border-radius:6px;padding:8px 12px">이 페이지에는 <b>광고</b>(제휴 링크 포함)가 있으며, 광고 링크를 통해 구매하면 운영자가 수수료를 받을 수 있습니다.</p>
  <img class="ph" src="__P1__" alt="">
  <div class="slot"><span class="note">A</span><p class="slot-title">사진 바로 아래 · 정사각 배너 1개 (현재 사용 중인 자리)</p>
   <div class="ad-sq"><span class="adtag">AD 광고</span><img src="__AD1__" alt=""></div></div>
  <h5>포인트 안내</h5>
  <p>강화 남단 갯벌 포인트는 밀물 타이밍을 놓치면 어떤 채비로도 낚시 자체가 성립하지 않습니다. 간조 시 광범위한 갯벌이 드러나는 구조로, 물때 확인이 입장 판단의 전부를 결정하는 곳입니다.</p>
  <div class="slot"><span class="note">B</span><p class="slot-title">「포인트 안내」 바로 아래 · 상품형 광고 3개 (가장 클릭이 잘 나오는 자리) — 이 글(서해 갯벌)에 맞는 용품을 고름</p>
   <div class="prod">
    <div class="p"><span class="adtag">AD 광고</span><img src="__AD2__" alt=""><div><b>갯벌용 장화 (예시)</b>상품명 자리 · <em>가격 자리</em></div></div>
    <div class="p"><span class="adtag">AD 광고</span><img src="__AD3__" alt=""><div><b>원투 채비 세트 (예시)</b>상품명 자리 · <em>가격 자리</em></div></div>
    <div class="p"><span class="adtag">AD 광고</span><img src="__AD1__" alt=""><div><b>랜턴·헤드라이트 (예시)</b>상품명 자리 · <em>가격 자리</em></div></div>
   </div><p class="dnote">제휴 링크 상품은 구매 시 수수료를 받는다는 문구를 함께 표시</p></div>
  <h5>1. 진입 동선과 포인트 접근성</h5>
  <img class="ph" src="__P2__" alt="" style="margin-bottom:10px">
  <p>초지대교를 건너 황산도 방향으로 진입하며, 포구 앞 공영 주차 공간이 있습니다…(본문 계속)</p>
  <div class="slot"><span class="note">C</span><p class="slot-title">본문 중간 · 글 속에 녹아드는 네이티브형 1개 (사진 옆 설명 + 버튼)</p>
   <div class="native"><div class="ad-sq" style="width:110px;margin:0"><span class="adtag" style="font-size:9px;top:4px;left:4px;padding:3px 4px">AD</span><img src="__AD4__" alt=""></div>
    <div><b>직접 협의 광고 · 낚시점/차박 장비점 (예시)</b><span>한 줄 소개 문구가 들어가는 자리입니다. 지역 낚시점이면 이 포인트와 가까운 곳으로 연결.</span><br><span class="btn">자세히 보기</span></div></div></div>
  <h5>2. 차박 환경과 야간 체류 여건</h5>
  <p>(본문 계속)…</p>
  <h5 style="margin-top:30px">결론</h5>
  <p>물때와 계절을 맞추면 황산포구가 달라 보입니다…</p>
  <div class="slot"><span class="note">D</span><p class="slot-title">결론 바로 아래 · 정사각 배너 1개 + 자체 쇼핑몰 연결 (읽고 난 뒤 다음 행동을 찾는 지점)</p>
   <div class="ad-sq"><span class="adtag">AD 광고</span><img src="__AD4__" alt=""></div></div>
 </div></div></div></div>
<div class="legend" style="margin-top:12px"><ul>
<li><span class="note">A</span><span><b>사진 아래 배너</b> — 지금 사이트와 같은 자리</span></li>
<li><span class="note">B</span><span><b>포인트 안내 아래 상품 3개</b> — 글 주제(지역·갯벌·차박 등)에 맞춰 상품을 바꿔 끼우는 자리. 수익은 여기서 가장 많이 기대</span></li>
<li><span class="note">C</span><span><b>본문 중간 1개</b> — 글을 자르지 않게 사진 사이에 하나만</span></li>
<li><span class="note">D</span><span><b>결론 아래 배너</b> — 글을 다 읽은 뒤 다음 행동 유도</span></li>
</ul>
<p style="margin:10px 0 0;color:#6b7f90;font-size:13px">짧은 글은 A·B·D 3곳만, 긴 글은 C까지 4곳으로. 모바일에서는 광고 폭을 본문의 70%로 줄이고 화면 하단 고정 광고는 쓰지 않는 것을 권합니다.</p></div>

</div></body></html>
"""

for i, d in enumerate(AD, 1):
    HTML = HTML.replace(f"__AD{i}__", d)
for i, d in enumerate((P1, P2, P3), 1):
    HTML = HTML.replace(f"__P{i}__", d)

out = ROOT / "tools" / "samples" / "ad_layout_sample.html"
out.parent.mkdir(exist_ok=True)
out.write_text(HTML, encoding="utf-8", newline="\n")
print(out, len(HTML) // 1024, "KB")
