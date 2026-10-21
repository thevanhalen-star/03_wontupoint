# -*- coding: utf-8 -*-
"""원투포인트 사이트 공통 요소 일괄 적용 스크립트.

여러 번 실행해도 결과가 같습니다(멱등). 포인트 페이지를 새로 생성·교체한 뒤
이 스크립트를 다시 돌리면 광고 표시, 이미지 출처, 안전 안내, SEO 메타, 파비콘,
상단·하단 메뉴가 다시 붙습니다.

실행:  python tools/build_site.py          (저장소 루트에서)
옵션:  --no-thumbs   썸네일 생성 생략
"""
import html
import json
from urllib.parse import quote
import re
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DOMAIN = "https://wontupoint.com"
SITE = "원투포인트"
EMAIL = "thevanhalen@gmail.com"
TODAY = date.today().isoformat()
POLICY_DATE = "2026년 10월 21일"
# 포인트 사진 출처 표기 (실제 출처와 다르면 여기만 바꾸고 다시 실행)
KAKAO_URL = "https://map.kakao.com"
# 카카오맵 이미지 활용 가이드(2023.01) 표기법: "출처 : 카카오맵 (https://map.kakao.com)"
IMAGE_CREDIT = f'출처 : 카카오맵 (<a href="{KAKAO_URL}" target="_blank" rel="noopener noreferrer">{KAKAO_URL}</a>)'
IMAGE_CREDIT_LONG = "카카오맵 스카이뷰·로드뷰"
IMAGE_DIFF_NOTE = "이 페이지의 지도·사진 이미지는 카카오맵의 실제 서비스 이미지와 다를 수 있습니다."

NAV = [
    ("/", "홈"),
    ("/all-points.html", "전체 포인트"),
    ("/about.html", "소개"),
    ("/contact.html", "문의"),
]
FOOT = [
    ("/about.html", "사이트 소개"),
    ("/all-points.html", "전체 포인트 목록"),
    ("/privacy.html", "개인정보처리방침"),
    ("/terms.html", "이용약관"),
    ("/legal.html", "운영 및 법적 고지"),
    ("/contact.html", "문의"),
]

ICON_LINKS = (
    '<link rel="icon" href="/favicon.ico" sizes="any">'
    '<link rel="icon" href="/assets/favicon.svg" type="image/svg+xml">'
    '<link rel="apple-touch-icon" href="/assets/apple-touch-icon.png">'
    '<link rel="manifest" href="/manifest.webmanifest">'
)


def esc(s):
    return html.escape(str(s), quote=True)


def jsonld(obj):
    return '<script type="application/ld+json">' + json.dumps(obj, ensure_ascii=False).replace("</", "<\\/") + "</script>"


def footer_links():
    return "".join(f'<a href="{h}">{t}</a>' for h, t in FOOT)


# ---------------------------------------------------------------- 공통 문서 페이지
def head(title, desc, path, robots="index,follow", og_image=None):
    url = DOMAIN + path
    og_image = og_image or DOMAIN + "/assets/og-image.jpg"
    return f"""<!doctype html>
<html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)}</title><meta name="description" content="{esc(desc)}"><meta name="robots" content="{robots}">
<meta name="theme-color" content="#10283c"><link rel="canonical" href="{url}">{ICON_LINKS}
<meta property="og:type" content="website"><meta property="og:site_name" content="{SITE}"><meta property="og:locale" content="ko_KR">
<meta property="og:title" content="{esc(title)}"><meta property="og:description" content="{esc(desc)}"><meta property="og:url" content="{url}">
<meta property="og:image" content="{og_image}"><meta name="twitter:card" content="summary_large_image">
<link rel="stylesheet" href="/assets/site.css">"""


def layout(path, title, desc, eyebrow, h1, body, robots="index,follow", extra_head=""):
    nav = "".join(
        f'<a href="{h}"{" aria-current=page" if h == path else ""}>{t}</a>' for h, t in NAV
    )
    crumbs = jsonld({
        "@context": "https://schema.org", "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": SITE, "item": DOMAIN + "/"},
            {"@type": "ListItem", "position": 2, "name": h1, "item": DOMAIN + path},
        ]})
    return (head(title, desc, path, robots) + (crumbs if robots.startswith("index") else "") + extra_head +
            f"""</head><body>
<header class="site-head"><div class="site-head-in"><a class="brand" href="/" aria-label="{SITE} 홈"><img src="/assets/favicon.svg" alt="" width="28" height="28">{SITE}</a><nav class="site-nav" aria-label="주요 메뉴">{nav}</nav></div></header>
<main class="doc"><span class="eyebrow">{eyebrow}</span><h1>{h1}</h1>
{body}
</main>
<footer class="site-foot"><nav aria-label="사이트 정보">{footer_links()}</nav><span>© 2026 {SITE}</span></footer>
</body></html>
""")


def write(rel, text):
    p = ROOT / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text, encoding="utf-8", newline="\n")


def point_count():
    try:
        return len(json.loads((ROOT / "points.json").read_text(encoding="utf-8-sig")))
    except Exception:
        return len(list((ROOT / "points").glob("*/001.html")))


def build_static_pages():
    n = point_count()
    mail = f'<a href="mailto:{EMAIL}">{EMAIL}</a>'

    write("about.html", layout(
        "/about.html", f"사이트 소개 | {SITE}",
        f"{SITE}는 전국 바다 원투낚시 포인트 {n}곳의 위치, 진입 동선, 차박 여건, 낚시 스타일을 지역별로 정리한 정보 사이트입니다.",
        "WONTUPOINT · ABOUT", "사이트 소개", f"""
<p class="lead">{SITE}는 전국 바다 원투낚시 포인트 {n}곳을 지역별로 정리한 무료 정보 사이트입니다. 처음 가 보는 포구·방파제·선착장의 분위기와 진입 동선을 출발 전에 가늠할 수 있도록 돕는 것을 목표로 합니다.</p>
<h2>무엇을 볼 수 있나요</h2>
<ul>
<li>지역(시·도, 시·군)별 포인트 목록과 검색</li>
<li>포인트별 위치(지번 기준 주소)와 주변 모습 이미지</li>
<li>진입 동선, 주차·차박 여건, 주변 편의시설, 물때·지형 특성, 어울리는 낚시 스타일, 대안 포인트</li>
</ul>
<h2>정보는 이렇게 만들어집니다</h2>
<p>포인트 안내는 지도·위성·거리 이미지와 공개된 자료 등을 바탕으로 정리한 <strong>참고 정보</strong>입니다. 조황(어획 결과)이나 특정 어종을 보장하지 않으며, 작성 이후 현장의 시설·출입 규정·주차 여건이 바뀌었을 수 있습니다. 포인트 사진은 {IMAGE_CREDIT_LONG} 화면이며 저작권은 카카오 및 원 제공처에 있습니다. 이미지는 카카오맵의 실제 서비스 이미지와 다를 수 있습니다.</p>
<div class="box warn"><strong>방문 전 꼭 확인하세요.</strong> 현장 안내판, 관할 지자체·해양경찰의 출입통제구역 공지, 기상청 해상예보와 물때를 우선해 주세요. 출입통제구역 무단 진입은 과태료 대상이 될 수 있고, 테트라포드·갯바위는 추락 사고 위험이 큽니다. 구명조끼를 착용하고, 금어기·포획금지체장과 지역별 낚시 제한 규정을 지켜 주세요.</div>
<h2>광고 안내</h2>
<p>무료 운영을 위해 일부 페이지에 광고(제휴 링크 포함)가 표시됩니다. 광고에는 ‘광고’ 표시가 붙어 있으며 자세한 내용은 <a href="/legal.html">운영 및 법적 고지</a>를 참고하세요.</p>
<h2>정보 정정 요청</h2>
<p>잘못된 정보, 폐쇄·통제된 포인트, 권리 침해가 의심되는 내용을 발견하시면 {mail}로 알려 주세요. 확인 후 신속히 수정하거나 게시를 중단합니다.</p>
"""))

    write("contact.html", layout(
        "/contact.html", f"문의 | {SITE}",
        f"{SITE} 정보 정정, 권리 침해 신고, 개인정보 및 광고 관련 문의 안내입니다.",
        "WONTUPOINT · CONTACT", "문의", f"""
<p class="lead">사이트 이용 중 궁금한 점이나 바로잡아야 할 정보가 있으면 이메일로 알려 주세요.</p>
<div class="box"><strong>이메일</strong><br>{mail}</div>
<h2>이런 내용을 받습니다</h2>
<ul>
<li><strong>정보 정정</strong>: 주소·시설·출입 규정 변경, 낚시 금지 또는 출입통제 지정, 폐쇄된 포인트</li>
<li><strong>권리 침해 신고</strong>: 저작권·초상권·상표권 침해, 사유지·개인 시설 노출 등 게시 중단 요청</li>
<li><strong>개인정보 관련 문의</strong>: 열람·정정·삭제·처리정지 요청</li>
<li><strong>광고·제휴 문의</strong> 및 기타 운영 문의</li>
</ul>
<h2>빠른 확인을 위해</h2>
<p>문의 시 해당 페이지 주소(예: {DOMAIN}/points/C001/001.html)와 수정이 필요한 내용, 근거(현장 안내판 사진, 지자체 공지 링크 등)를 함께 보내 주시면 처리에 도움이 됩니다. 권리 침해 신고는 권리자임을 확인할 수 있는 정보와 침해 내용을 구체적으로 적어 주세요.</p>
<p>보내 주신 이메일 주소와 문의 내용은 회신과 처리 목적으로만 사용하며, 자세한 내용은 <a href="/privacy.html">개인정보처리방침</a>을 참고하세요. 운영자 1인이 처리하므로 회신까지 며칠이 걸릴 수 있으며, 권리 침해 신고는 우선 처리합니다.</p>
"""))

    write("privacy.html", layout(
        "/privacy.html", f"개인정보처리방침 | {SITE}",
        f"{SITE}의 접속 기록, 쿠키, 광고, 문의 이메일 처리와 이용자 권리에 관한 개인정보처리방침입니다.",
        "WONTUPOINT · PRIVACY", "개인정보처리방침", f"""
<p class="lead">{SITE}(이하 ‘사이트’)는 「개인정보 보호법」 제30조에 따라 이용자의 개인정보를 어떻게 처리하는지 다음과 같이 공개합니다.</p>
<h2>1. 처리하는 개인정보와 수집 방법</h2>
<p>사이트는 회원가입, 로그인, 댓글, 입력 양식(폼)을 제공하지 않으며 이름·전화번호·주소 등을 입력받지 않습니다. 다음 정보만 처리될 수 있습니다.</p>
<ul>
<li><strong>자동으로 생성되는 접속 정보</strong>: IP 주소, 접속 일시, 요청한 페이지 주소, 브라우저·기기 정보, 참조 페이지 — 사이트 접속 시 호스팅 사업자(Cloudflare)가 자동으로 처리</li>
<li><strong>이메일 문의 정보</strong>: 이용자가 직접 보낸 이메일 주소, 문의 내용, 첨부 자료</li>
<li><strong>광고·통계 관련 정보</strong>: 광고 또는 방문 통계 도구를 사용하는 경우 쿠키·광고 식별자, 방문 기록 등(제4항)</li>
</ul>
<h2>2. 처리 목적</h2>
<ul>
<li>사이트 제공, 보안(공격 차단·장애 대응), 부정 이용 방지</li>
<li>문의·정정 요청·권리 침해 신고에 대한 확인과 회신</li>
<li>방문 통계 집계와 서비스 개선, 광고 게재 및 성과 측정</li>
</ul>
<h2>3. 보유 기간과 파기</h2>
<ul>
<li>접속 정보: 호스팅 사업자의 정책에 따른 기간 동안 보관 후 삭제되며, 운영자가 별도로 저장하지 않습니다.</li>
<li>이메일 문의: 처리 완료 후 1년간 보관(재문의·분쟁 대응 목적) 후 지체 없이 삭제합니다. 법령에 보존 의무가 있으면 해당 기간 동안만 보관합니다.</li>
<li>파기 방법: 전자 파일은 복구할 수 없는 방법으로 삭제합니다.</li>
</ul>
<h2>4. 쿠키 등 자동 수집 장치</h2>
<p>사이트 자체는 이용자를 식별하는 쿠키를 만들지 않습니다. 다만 아래 서비스가 쿠키 또는 유사 기술을 사용할 수 있습니다.</p>
<ul>
<li><strong>Cloudflare(호스팅·보안)</strong>: 악성 트래픽 차단을 위한 필수 보안 쿠키를 설정할 수 있습니다.</li>
<li><strong>Cloudflare Web Analytics(방문 통계)</strong>: 사용하는 경우 쿠키나 브라우저 저장소에 식별자를 남기지 않고, 방문 페이지·참조 페이지·브라우저 종류·국가 수준 위치 등 집계용 정보만 처리합니다.</li>
<li><strong>Google AdSense(광고)</strong>: 광고를 게재하는 경우 Google과 광고 파트너(제3자 공급업체)가 쿠키를 사용해 이용자의 이 사이트 및 다른 사이트 방문 기록을 바탕으로 광고를 표시할 수 있습니다. 이때 처리될 수 있는 행태정보는 방문 페이지, 광고 클릭 기록, 브라우저·기기 정보, IP 기반 대략적 위치이며, 운영자는 개인을 식별할 수 있는 형태로 이 정보를 받지 않습니다.</li>
</ul>
<p><strong>거부 방법</strong>: 브라우저 설정에서 쿠키를 차단·삭제할 수 있습니다(Chrome: 설정 › 개인정보 보호 및 보안 › 서드 파티 쿠키, Edge: 설정 › 쿠키 및 사이트 권한, Safari: 설정 › 개인정보 보호). 맞춤 광고는 <a href="https://adssettings.google.com/" rel="noopener" target="_blank">Google 광고 설정</a>, <a href="https://www.aboutads.info/choices/" rel="noopener" target="_blank">aboutads.info</a>에서 끌 수 있습니다. 자세한 내용은 <a href="https://policies.google.com/technologies/partner-sites" rel="noopener" target="_blank">Google이 파트너 사이트의 정보를 사용하는 방식</a>을 참고하세요. 쿠키를 거부해도 사이트 이용에는 지장이 없습니다.</p>
<h2>5. 광고 링크와 외부 사이트</h2>
<p>포인트 페이지의 광고 이미지는 이 사이트에 저장된 파일이라 보는 것만으로는 외부로 정보가 전송되지 않습니다. 광고를 클릭하면 네이버 쇼핑, fish-gear.com 등 외부 사이트로 이동하며, 제휴 수수료 정산을 위해 클릭 경로 정보가 해당 사업자에게 전달될 수 있습니다. 이동한 사이트에서의 개인정보 처리는 각 사이트의 개인정보처리방침을 따릅니다.</p>
<h2>6. 제3자 제공</h2>
<p>사이트는 이용자의 개인정보를 제3자에게 제공하지 않습니다. 다만 법령에 근거한 수사기관 등의 적법한 요청이 있는 경우는 예외로 합니다.</p>
<h2>7. 처리 위탁 및 국외 이전</h2>
<p>사이트 운영을 위해 다음 사업자가 정보를 처리하며, 모두 국외 사업자이므로 개인정보가 국외로 이전될 수 있습니다.</p>
<table>
<thead><tr><th>이전받는 자</th><th>국가·연락처</th><th>이전 항목</th><th>목적</th><th>보유 기간</th></tr></thead>
<tbody>
<tr><td>Cloudflare, Inc.</td><td>미국 · privacy@cloudflare.com</td><td>IP 주소, 접속 일시, 요청 URL, 브라우저 정보</td><td>호스팅, 콘텐츠 전송, 보안(DDoS 방어), 방문 통계</td><td>Cloudflare 정책에 따름</td></tr>
<tr><td>Google LLC<br><small>(광고 게재 시)</small></td><td>미국 · <a href="https://policies.google.com/privacy" rel="noopener" target="_blank">개인정보처리방침</a></td><td>쿠키·광고 식별자, 방문 페이지, 기기·브라우저 정보</td><td>광고 게재 및 측정</td><td>Google 정책에 따름</td></tr>
<tr><td>Google LLC (Gmail)</td><td>미국</td><td>문의 이메일 주소와 내용</td><td>이메일 문의 수신·회신</td><td>제3항과 같음</td></tr>
</tbody></table>
<p>이전 시기와 방법: 사이트 접속, 광고 표시, 이메일 발송 시 네트워크를 통해 전송됩니다. 광고 쿠키는 제4항의 방법으로 거부할 수 있으며, 이메일 대신 다른 연락 수단을 원하시면 요청해 주세요. 사이트 접속 자체에 따르는 호스팅 처리를 거부하면 사이트를 이용할 수 없습니다.</p>
<h2>8. 이용자의 권리와 행사 방법</h2>
<p>이용자는 언제든지 자신의 개인정보 열람, 정정·삭제, 처리정지, 동의 철회를 요구할 수 있습니다. {mail}로 요청하시면 본인 확인 후 지체 없이(10일 이내) 조치하고 결과를 알려 드립니다. 법령에 따라 제한되는 경우에는 그 사유를 안내합니다. 대리인을 통해서도 요청할 수 있으며 이 경우 위임장이 필요합니다.</p>
<h2>9. 안전성 확보 조치</h2>
<ul>
<li>전 구간 HTTPS 암호화 통신과 보안 헤더 적용</li>
<li>개인정보 최소 수집(입력 양식 없음), 문의 메일은 운영자만 접근할 수 있는 계정에서 관리</li>
</ul>
<h2>10. 만 14세 미만 아동</h2>
<p>사이트는 연령을 확인하거나 아동의 개인정보를 별도로 수집하지 않습니다. 만 14세 미만 아동이 문의할 경우 법정대리인의 동의가 필요할 수 있습니다.</p>
<h2>11. 개인정보 보호책임자</h2>
<ul><li>담당: {SITE} 운영자(개인정보 보호책임자)</li><li>이메일: {mail}</li></ul>
<h2>12. 권익 침해 구제 방법</h2>
<p>개인정보 침해에 대한 신고나 상담은 아래 기관에 문의할 수 있습니다.</p>
<ul>
<li>개인정보침해신고센터: privacy.kisa.or.kr / 국번 없이 118</li>
<li>개인정보분쟁조정위원회: www.kopico.go.kr / 1833-6972</li>
<li>대검찰청 사이버수사과: www.spo.go.kr / 국번 없이 1301</li>
<li>경찰청 사이버수사국: ecrm.police.go.kr / 국번 없이 182</li>
</ul>
<h2>13. 방침의 변경</h2>
<p>광고·통계 도구 도입, 기능 변경, 법령 개정에 따라 방침을 바꾸는 경우 시행 7일 전부터 이 페이지에 공지합니다.</p>
<p class="updated">시행일: {POLICY_DATE}</p>
"""))

    write("terms.html", layout(
        "/terms.html", f"이용약관 | {SITE}",
        f"{SITE} 낚시 포인트 정보의 성격, 안전·법규 준수, 광고, 저작권, 책임 범위에 관한 이용약관입니다.",
        "WONTUPOINT · TERMS", "이용약관", f"""
<p class="lead">{SITE}를 이용하기 전에 아래 내용을 확인해 주세요. 사이트를 이용하면 이 약관에 동의한 것으로 봅니다.</p>
<h2>1. 목적</h2>
<p>이 약관은 {SITE}(이하 ‘사이트’)가 제공하는 전국 낚시 포인트 정보 서비스의 이용 조건을 정합니다.</p>
<h2>2. 정보의 성격</h2>
<p>사이트의 포인트 정보는 지도·위성·거리 이미지와 공개 자료 등을 바탕으로 정리한 <strong>참고 정보</strong>입니다. 작성 시점 이후 출입 규정, 시설, 주차 여건, 수심·지형이 바뀌었을 수 있으며 조황이나 특정 어종을 보장하지 않습니다. 출조 여부와 장소 선택은 이용자가 최신 현장 정보를 확인해 스스로 판단해야 합니다.</p>
<h2>3. 안전과 법규 준수</h2>
<ul>
<li>현장 안내판, 관할 지자체·해양경찰의 출입통제·낚시 제한 공지가 사이트 정보보다 우선합니다.</li>
<li>「연안사고 예방에 관한 법률」에 따른 출입통제구역 무단 진입, 「낚시 관리 및 육성법」에 따른 낚시 제한 위반, 「수산자원관리법」에 따른 금어기·포획금지체장 위반은 과태료 등 제재 대상이 될 수 있습니다.</li>
<li>테트라포드·갯바위·방파제 끝단은 추락·고립 위험이 크므로 구명조끼를 착용하고 기상특보·물때를 확인해야 합니다.</li>
<li>어항·마을 시설에서는 어업 활동을 방해하지 말고, 금지된 곳에서의 주차·차박·야영·취사·쓰레기 투기를 하지 않아야 합니다. 사유지에는 소유자 허락 없이 들어가지 마세요.</li>
</ul>
<h2>4. 광고와 제휴 링크</h2>
<p>사이트에는 ‘광고’로 표시된 상품 이미지와 링크가 있습니다. 광고 링크를 통해 구매하면 운영자가 판매 수익 또는 제휴 수수료를 받을 수 있습니다. 상품의 판매·배송·환불은 해당 판매자와 이용자 사이의 거래이며 사이트는 거래 당사자가 아닙니다.</p>
<h2>5. 저작권</h2>
<p>사이트의 글, 편집 구성, 디자인의 저작권은 운영자에게 있습니다. 출처를 밝힌 짧은 인용 외에 무단 복제·대량 전재·재배포는 허용되지 않습니다. 포인트 사진({IMAGE_CREDIT_LONG})의 권리는 카카오 및 원 제공처에 있으므로 사이트에서 내려받아 다시 사용하지 마세요. 사이트는 카카오와 제휴·후원·보증 관계가 없습니다.</p>
<h2>6. 권리 침해 신고와 게시 중단</h2>
<p>사이트의 게시물로 저작권, 초상권, 사생활 등 권리를 침해당했다고 판단되면 <a href="/contact.html">문의</a>에 안내된 이메일로 신고해 주세요. 운영자는 「정보통신망 이용촉진 및 정보보호 등에 관한 법률」 제44조의2의 취지에 따라 확인 즉시 해당 내용을 가리거나 삭제하는 등 필요한 조치를 하고 결과를 알려 드립니다.</p>
<h2>7. 금지 행위</h2>
<p>사이트 정보·이미지를 자동화 도구로 대량 수집하거나, 서버에 과도한 부하를 주거나, 보안을 해치는 행위를 금지합니다.</p>
<h2>8. 서비스의 변경과 중단</h2>
<p>운영자는 유지보수, 정보 정정, 운영상 사유로 사이트 내용을 변경하거나 일부 또는 전부를 중단할 수 있습니다.</p>
<h2>9. 책임의 제한</h2>
<p>사이트는 무료로 “있는 그대로” 제공됩니다. 운영자는 고의 또는 중대한 과실이 없는 한, 이용자가 사이트 정보를 참고해 출조·이동·차박하는 과정에서 생긴 사고나 손해, 현장 정보 변경, 외부 링크 사이트의 내용과 거래에 대해 관련 법령이 허용하는 범위에서 책임을 지지 않습니다. 소비자 보호 법령 등에 따라 배제할 수 없는 이용자의 권리는 영향을 받지 않습니다.</p>
<h2>10. 준거법과 분쟁 해결</h2>
<p>이 약관은 대한민국 법률에 따라 해석됩니다. 분쟁은 먼저 이메일 협의로 해결하도록 노력하며, 소송이 필요한 경우 「민사소송법」에 따른 관할 법원을 따릅니다.</p>
<h2>11. 약관의 변경</h2>
<p>약관을 변경하면 시행 7일 전부터 이 페이지에 공지합니다.</p>
<p class="updated">시행일: {POLICY_DATE}</p>
"""))

    write("legal.html", layout(
        "/legal.html", f"운영 및 법적 고지 | {SITE}",
        f"{SITE} 운영자 정보, 광고·제휴 표시, 이미지 출처, 상표, 안전 고지를 정리한 페이지입니다.",
        "WONTUPOINT · LEGAL", "운영 및 법적 고지", f"""
<p class="lead">{SITE}의 운영 방식과 주요 고지 사항을 한곳에 정리했습니다.</p>
<h2>운영자 및 연락처</h2>
<p>{SITE}는 개인이 운영하는 무료 낚시 포인트 정보 사이트입니다. 운영·개인정보·권리 침해 관련 문의: {mail}</p>
<h2>광고 및 제휴 표시</h2>
<p>「표시·광고의 공정화에 관한 법률」과 공정거래위원회 「추천·보증 등에 관한 표시·광고 심사지침」에 따라 다음을 알려 드립니다.</p>
<ul>
<li>포인트 페이지의 상품 이미지는 <strong>광고</strong>이며 각 이미지에 ‘광고’ 표시를 붙였습니다.</li>
<li>광고 링크(네이버 쇼핑, fish-gear.com 등)에는 운영자가 판매하거나 제휴 수수료를 받는 상품이 포함됩니다. 이 링크를 통해 구매하면 운영자에게 수익이 발생할 수 있습니다.</li>
<li>포인트 안내 본문은 광고주의 요청이나 대가를 받고 작성한 내용이 아닙니다.</li>
<li>향후 Google AdSense 등 디스플레이 광고가 게재될 수 있으며, 쿠키 처리는 <a href="/privacy.html">개인정보처리방침</a> 제4항을 따릅니다.</li>
</ul>
<h2>이미지 출처</h2>
<p>포인트 페이지의 위성·거리 사진은 {IMAGE_CREDIT_LONG} 화면이며, 각 사진 아래와 페이지 하단에 「출처 : 카카오맵 ({KAKAO_URL})」 형식으로 출처를 표시하고, 카카오맵 해당 위치로 바로 갈 수 있는 QR 코드를 넣었습니다. 사이트의 이미지는 카카오맵의 실제 서비스 이미지와 다를 수 있으며, 카카오맵 상표는 수정·변형하지 않고 출처 표기 목적으로만 사용합니다. 사이트는 카카오와 서비스상 제휴·후원 관계가 아니며, 이미지의 저작권은 카카오 및 원 제공처에 있습니다.</p>
<p><img src="/assets/kakaomap/kakaomap_name_EN.png" alt="kakaomap" style="height:18px;width:auto"></p>
<p>광고 이미지는 해당 상품 판매처 또는 운영자의 자료입니다.</p>
<h2>정보의 정확성과 안전</h2>
<p>포인트 정보는 참고용이며 현장 상황, 출입 규정, 기상과 다를 수 있습니다. 방문 전 현장 안내판, 지자체·해양경찰 공지, 기상청 해상예보와 물때를 확인하고, 출입통제구역과 낚시 제한 구역에는 들어가지 마세요. 자세한 내용은 <a href="/terms.html">이용약관</a> 제2·3항을 참고하세요.</p>
<h2>제3자 상표 고지</h2>
<p>사이트에 등장하는 카카오맵, 네이버(네이버 쇼핑·스마트스토어), 바다타임, 기상청, Google, Cloudflare 등의 명칭은 각 권리자의 상표 또는 서비스표이며, 정보의 출처나 이용 방법을 설명하기 위해서만 언급합니다. 사이트는 광고로 표시된 경우를 제외하고 이들과 제휴·후원·보증 관계가 없으며, 특히 카카오와는 어떠한 제휴·계약 관계도 없습니다.</p>
<h2>사업자 정보 표시에 관한 안내</h2>
<p>사이트는 상품을 직접 판매하거나 결제를 받지 않습니다. 광고 링크로 연결되는 상품의 판매자 정보(상호, 사업자등록번호, 통신판매업 신고번호 등)는 각 판매 페이지에 표시되어 있습니다.</p>
<h2>권리 침해 신고</h2>
<p>저작권·초상권·사생활 침해 등으로 게시 중단이 필요하면 {mail}로 알려 주세요. 확인 즉시 비공개 또는 삭제 조치합니다.</p>
<h2>관련 정책</h2>
<p><a href="/privacy.html">개인정보처리방침</a> · <a href="/terms.html">이용약관</a> · <a href="/contact.html">문의</a></p>
<p class="updated">마지막 수정: {POLICY_DATE}</p>
"""))

    write("404.html", layout(
        "/404.html", f"페이지를 찾을 수 없습니다 | {SITE}", "요청한 페이지를 찾을 수 없습니다.",
        "404 NOT FOUND", "페이지를 찾을 수 없습니다", """
<p class="lead">주소가 잘못 입력되었거나 페이지가 이동·삭제되었을 수 있습니다.</p>
<p><a href="/">홈에서 지역별 포인트 보기 →</a></p>
<p><a href="/all-points.html">전체 포인트 목록 보기 →</a></p>
""", robots="noindex,follow"))


def build_all_points():
    p = ROOT / "all-points.html"
    src = p.read_text(encoding="utf-8-sig")
    m = re.search(r"</h1>(.*?)</main>", src, re.S)
    if not m:
        print("all-points.html 구조를 찾지 못해 건너뜀")
        return
    inner = m.group(1).strip()
    inner = re.sub(r'^\s*<div class="point-list">|</div>\s*$', "", inner).strip()
    n = point_count()
    write("all-points.html", layout(
        "/all-points.html", f"전체 포인트 목록 | {SITE}",
        f"전국 원투낚시 포인트 {n}곳을 지역별로 모은 전체 목록입니다. 포인트를 선택하면 진입 동선, 차박 여건, 낚시 스타일을 볼 수 있습니다.",
        "WONTUPOINT · ALL POINTS", "전체 포인트 목록",
        f'<div class="point-list">{inner}</div>'))


# ---------------------------------------------------------------- 포인트 페이지
POINT_CSS = """
.wontu-topnav{display:flex;justify-content:space-between;align-items:center;gap:10px;flex-wrap:wrap;margin:-6px 0 18px;padding-bottom:12px;border-bottom:1px solid #e6ecf1;font-size:14px}
.wontu-topnav a{color:#1d669f;text-decoration:none}.wontu-topnav a:hover{text-decoration:underline}
.wontu-topnav .wontu-brand{display:flex;align-items:center;gap:7px;font-weight:700;color:#10283c}
.wontu-topnav .wontu-brand img{width:22px;height:22px;border-radius:5px}
.wontu-topnav nav{display:flex;gap:14px}
.wontu-disclosure{font-size:13px!important;line-height:1.7;color:#5b6b78;background:#f4f7fa;border-radius:6px;padding:8px 12px;margin:0 0 6px!important}
.wontu-ad-label{display:inline-block;font-size:12px;font-weight:700;line-height:1;color:#fff;background:#56626d;border-radius:3px;padding:4px 7px;margin:0 0 6px;letter-spacing:.05em}
.ad-photo{position:relative}
.wontu-img-credit{font-size:13px;color:#5b6b78;text-align:right;margin-top:4px;line-height:1.5}.wontu-img-credit a{color:inherit}
.wontu-kakao{margin:34px 0 0;padding:16px 18px;border:1px solid #dde6ed;border-radius:8px;display:flex;gap:18px;align-items:center;font-size:14px;line-height:1.7}
.wontu-kakao img.qr{width:120px;height:120px;flex:none;border:1px solid #e6ecf1;border-radius:4px;background:#fff}
.wontu-kakao p{font-size:14px!important;margin:0 0 6px!important}.wontu-kakao .src{display:block}
.wontu-kakao .src img{height:15px;width:auto;vertical-align:-2px;margin-right:6px}
@media(max-width:700px){.wontu-kakao{flex-direction:column;align-items:flex-start}}
.wontu-safety{margin:34px 0 0;padding:16px 18px;background:#fff8ec;border:1px solid #f3dcb2;border-radius:8px;font-size:14px;line-height:1.75;color:#4b4030}
.wontu-safety strong{display:block;margin-bottom:4px;color:#7a4b00}
.wontu-safety ul{margin:6px 0 0;padding-left:18px}
.wontu-safety p{font-size:14px!important;margin:8px 0 0!important}
.wontu-foot{max-width:1104px;margin:0 auto 34px;padding:0 20px;display:flex;justify-content:space-between;gap:12px;flex-wrap:wrap;font-size:12.5px;color:#8aa0b1}
.wontu-foot nav{display:flex;gap:14px;flex-wrap:wrap}.wontu-foot a{color:inherit;text-decoration:none}.wontu-foot a:hover{text-decoration:underline}
@media(max-width:700px){.wontu-foot{padding:14px 19px 0}}
"""


def strip_tags(s):
    s = re.sub(r"<br\s*/?>", " ", s, flags=re.I)
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", "", s))).strip()


def replace_block(text, name, block, anchor_re, before=True):
    start, end = f"<!-- {name}_START -->", f"<!-- {name}_END -->"
    text = re.sub(re.escape(start) + r".*?" + re.escape(end) + r"\n?", "", text, flags=re.S)
    wrapped = f"{start}\n{block}\n{end}\n"
    m = re.search(anchor_re, text, re.S)
    if not m:
        raise ValueError(f"anchor not found for {name}")
    pos = m.start() if before else m.end()
    return text[:pos] + wrapped + text[pos:]


def process_point(path: Path):
    import segno
    globals()["segno"] = segno
    pid = path.parent.name
    t = path.read_text(encoding="utf-8-sig")
    orig = t
    rel = f"/points/{pid}/001.html"
    url = DOMAIN + rel

    title_m = re.search(r"<title>(.*?)</title>", t, re.S)
    title = strip_tags(title_m.group(1)) if title_m else pid
    name, addr = "", ""
    txt = path.parent / "002.txt"
    if txt.exists():
        lines = [x.strip() for x in txt.read_text(encoding="utf-8-sig", errors="replace").splitlines() if x.strip()]
        if len(lines) >= 3 and not lines[1].startswith("#"):
            name, addr = lines[1], lines[2]
    if not name:
        name_m = re.search(r'<div class="point-name"[^>]*>(.*?)</div>', t, re.S)
        addr_m = re.search(r'<div class="point-address"[^>]*>(.*?)</div>', t, re.S)
        name = strip_tags(name_m.group(1)) if name_m else title.split(",")[0]
        addr = strip_tags(addr_m.group(1)) if addr_m else ""

    intro = ""
    im = re.search(r'class="intro-heading".*?</h2>(.*?)<!-- SECTION_INTRO_END', t, re.S)
    if im:
        body = re.sub(r'<!-- WONTU_POINT_INFO_START -->.*?<!-- WONTU_POINT_INFO_END -->', "", im.group(1), flags=re.S)
        ps = re.findall(r"<p>(.*?)</p>", body, re.S)
        intro = " ".join(strip_tags(x) for x in ps[:2])
        for lead in (name, addr):
            if lead and intro.startswith(lead):
                intro = intro[len(lead):].strip()
    loc = f"{name}({addr}) " if addr else f"{name} "
    desc = loc + intro if intro else loc + "원투낚시 포인트 — 진입 동선, 차박 여건, 편의시설, 지형과 어울리는 낚시 스타일 안내."
    desc = desc.strip()
    if len(desc) > 155:
        desc = desc[:152].rstrip() + "…"
    img_abs = f"{DOMAIN}/points/{pid}/image/001.jpg"

    # 1) 깨진 해시태그 aria-label 수정
    t = re.sub(r'(<div class="wontu-hashtags" aria-label=")[^"]*(")', r"\1해시태그\2", t)

    # 2) 광고 표시 라벨
    def ad_fix(m):
        block = m.group(0)
        if "wontu-ad-label" in block:
            return block
        return re.sub(r"(<div class=\"point-media ad-photo\"[^>]*>)", r'\1<span class="wontu-ad-label">광고</span><br>', block, count=1)
    t = re.sub(r'<div class="point-media ad-photo".*?</div>', ad_fix, t, flags=re.S)

    # 3) 포인트 사진 alt + 출처(카카오맵 가이드 표기법)
    def photo_fix(m):
        block = re.sub(r'<div class="wontu-img-credit">.*?</div>', "", m.group(0), flags=re.S)
        block = re.sub(r'alt="[^"]*(?:포인트 이미지|주변 모습) (\d+)"', lambda a: f'alt="{esc(name)} 주변 모습 {a.group(1)}"', block)
        return block[: -len("</div>")] + f'<div class="wontu-img-credit">{IMAGE_CREDIT}</div></div>'
    t = re.sub(r'<div class="point-media point-photo"[^>]*><img[^>]*>(?:<div class="wontu-img-credit">.*?</div>)?</div>', photo_fix, t, flags=re.S)

    # 4) head: SEO·파비콘·공통 스타일
    ld = [
        {"@context": "https://schema.org", "@type": "Article", "headline": title[:110], "description": desc,
         "image": [img_abs], "inLanguage": "ko-KR", "mainEntityOfPage": url,
         "author": {"@type": "Organization", "name": SITE, "url": DOMAIN + "/"},
         "publisher": {"@type": "Organization", "name": SITE, "logo": {"@type": "ImageObject", "url": DOMAIN + "/assets/icon-512.png"}},
         "about": {"@type": "Place", "name": name, "address": {"@type": "PostalAddress", "streetAddress": addr, "addressCountry": "KR"}}},
        {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": SITE, "item": DOMAIN + "/"},
            {"@type": "ListItem", "position": 2, "name": "전체 포인트", "item": DOMAIN + "/all-points.html"},
            {"@type": "ListItem", "position": 3, "name": name, "item": url}]},
    ]
    head_block = (
        f'<meta name="description" content="{esc(desc)}">\n<meta name="robots" content="index,follow">\n'
        f'<meta name="theme-color" content="#10283c">\n<link rel="canonical" href="{url}">\n{ICON_LINKS}\n'
        f'<meta property="og:type" content="article"><meta property="og:site_name" content="{SITE}"><meta property="og:locale" content="ko_KR">\n'
        f'<meta property="og:title" content="{esc(title)}"><meta property="og:description" content="{esc(desc)}">\n'
        f'<meta property="og:url" content="{url}"><meta property="og:image" content="{img_abs}"><meta name="twitter:card" content="summary_large_image">\n'
        f"{jsonld(ld)}\n<style id=\"wontu-chrome\">{POINT_CSS}</style>"
    )
    t = replace_block(t, "WONTU_HEAD", head_block, r"</head>")

    # 5) 본문 상단: 내비 + 광고 고지
    top = (
        f'<div class="wontu-topnav"><a class="wontu-brand" href="/"><img src="/assets/favicon.svg" alt="" width="22" height="22">{SITE}</a>'
        f'<nav aria-label="사이트 메뉴"><a href="/">홈</a><a href="/all-points.html">전체 포인트</a></nav></div>\n'
        f'<p class="wontu-disclosure">이 페이지에는 <strong>광고</strong>(제휴 링크 포함)가 있으며, 광고 링크를 통해 구매하면 운영자가 판매 수익 또는 수수료를 받을 수 있습니다. '
        f'포인트 사진: {IMAGE_CREDIT_LONG}. {IMAGE_DIFF_NOTE}</p>'
    )
    t = replace_block(t, "WONTU_TOPNAV", top, r'<div class="container">\s*', before=False)

    # 5b) 카카오맵 바로가기 QR (가이드 2-3-a) + 출처
    q = quote(addr or name, safe="")
    kurl = f"{KAKAO_URL}/?q={q}"
    qr_path = path.parent / "image" / "qr.svg"
    seg = segno.make(kurl, error="m", micro=False)
    seg.save(str(qr_path), scale=4, border=2, dark="#000000", light="#ffffff", xmldecl=False, svgns=True, nl=False)
    kakao = (
        f'<aside class="wontu-kakao" aria-label="카카오맵 바로가기"><img class="qr" src="image/qr.svg" alt="카카오맵 {esc(name)} 위치 바로가기 QR 코드" width="120" height="120" loading="lazy">'
        f'<div><p><strong>카카오맵 해당 위치로 바로 가기</strong><br>QR 코드를 스캔하거나 <a href="{kurl}" target="_blank" rel="noopener noreferrer">여기를 눌러</a> 카카오맵에서 {esc(addr or name)} 위치를 확인하세요.</p>'
        f'<p class="src"><img src="/assets/kakaomap/kakaomap_name_EN.png" alt="kakaomap">{IMAGE_CREDIT}</p><p>{IMAGE_DIFF_NOTE}</p></div></aside>'
    )
    t = replace_block(t, "WONTU_KAKAO", kakao, r"<!-- WONTU_HASHTAGS_START -->" if "<!-- WONTU_HASHTAGS_START -->" in t else r"</div>\s*</body>")

    # 6) 본문 끝: 안전·법규 안내
    safety = (
        '<aside class="wontu-safety" aria-label="안전 및 법규 안내"><strong>방문 전 확인하세요</strong>'
        '<ul><li>이 글은 참고 정보입니다. 현장 안내판과 지자체·해양경찰 공지가 우선하며, 출입통제구역 무단 진입은 과태료 대상이 될 수 있습니다.</li>'
        '<li>테트라포드·갯바위·방파제 끝단은 추락 위험이 큽니다. 구명조끼를 착용하고 기상특보와 물때를 확인하세요.</li>'
        '<li>금어기·포획금지체장과 낚시 제한 구역을 지키고, 금지된 곳에서의 주차·차박·야영·취사와 쓰레기 투기는 하지 마세요.</li></ul>'
        f'<p>정보가 바뀌었거나 잘못된 내용이 있으면 <a href="/contact.html">문의</a>로 알려 주세요.</p></aside>'
    )
    hs = re.search(r"<!-- WONTU_HASHTAGS_START -->", t)
    if hs:
        t = replace_block(t, "WONTU_SAFETY", safety, r"<!-- WONTU_HASHTAGS_START -->")
    else:
        t = replace_block(t, "WONTU_SAFETY", safety, r"</div>\s*</body>")

    # 7) 페이지 하단 푸터
    foot = f'<footer class="wontu-foot"><nav aria-label="사이트 정보">{footer_links()}</nav><span>© 2026 {SITE}</span></footer>'
    t = replace_block(t, "WONTU_FOOT", foot, r"</body>")

    if t != orig:
        path.write_text(t, encoding="utf-8", newline="\n")
        return True
    return False


# ---------------------------------------------------------------- 홈
HOME_HEAD = f"""{ICON_LINKS}
<meta property="og:locale" content="ko_KR"><meta property="og:image" content="{DOMAIN}/assets/og-image.jpg"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
{{LD}}"""


def build_home():
    p = ROOT / "index.html"
    t = p.read_text(encoding="utf-8-sig")
    ld = jsonld([
        {"@context": "https://schema.org", "@type": "WebSite", "name": SITE, "url": DOMAIN + "/", "inLanguage": "ko-KR",
         "potentialAction": {"@type": "SearchAction", "target": DOMAIN + "/?q={search_term_string}", "query-input": "required name=search_term_string"}},
        {"@context": "https://schema.org", "@type": "Organization", "name": SITE, "url": DOMAIN + "/", "logo": DOMAIN + "/assets/icon-512.png", "email": EMAIL},
    ])
    t = replace_block(t, "WONTU_HEAD", HOME_HEAD.replace("{LD}", ld), r"\s*<style>", before=True)
    # 푸터
    t = re.sub(r'<footer class="footer">.*?</footer>',
               f'<footer class="footer"><span>© 2026 {SITE}</span><div class="footer-links">{footer_links()}</div></footer>', t, flags=re.S)
    # 썸네일 사용 (없으면 원본으로 대체)
    t = t.replace("const img=make('img','point-photo');img.src=pointUrl(item.image);",
                  "const img=make('img','point-photo');const full=pointUrl(item.image);img.src=full.replace(/\\/001\\.jpg$/,'/thumb.jpg');img.width=640;img.height=480;")
    t = t.replace("img.addEventListener('error',()=>{img.style.background='#e8eff4';img.alt='이미지를 불러올 수 없습니다';},{once:true});",
                  "img.addEventListener('error',function onErr(){if(img.src.endsWith('/thumb.jpg')){img.src=full;return;}img.removeEventListener('error',onErr);img.style.background='#e8eff4';img.alt='이미지를 불러올 수 없습니다';});")
    t = t.replace('<a class="brand" href="./index.html"', '<a class="brand" href="/"')
    p.write_text(t, encoding="utf-8", newline="\n")


def build_thumbs():
    from PIL import Image
    made = 0
    for src in sorted((ROOT / "points").glob("*/image/001.jpg")):
        dst = src.with_name("thumb.jpg")
        if dst.exists() and dst.stat().st_mtime >= src.stat().st_mtime:
            continue
        im = Image.open(src).convert("RGB")
        tw, th = 640, 480
        r = max(tw / im.width, th / im.height)
        im = im.resize((round(im.width * r), round(im.height * r)), Image.LANCZOS)
        l, tp = (im.width - tw) // 2, (im.height - th) // 2
        im.crop((l, tp, l + tw, tp + th)).save(dst, "JPEG", quality=72, optimize=True, progressive=True)
        made += 1
    print(f"썸네일 {made}개 생성")


# ---------------------------------------------------------------- 메타 파일
def build_meta_files():
    write("manifest.webmanifest", json.dumps({
        "name": f"{SITE} - 전국 원투낚시 포인트", "short_name": SITE,
        "description": "전국 원투낚시 포인트의 위치, 진입 동선, 차박 여건을 지역별로 찾아보는 정보 사이트",
        "id": "/", "start_url": "/?source=pwa", "scope": "/", "display": "standalone",
        "background_color": "#f6f8fb", "theme_color": "#10283c", "lang": "ko", "dir": "ltr",
        "categories": ["sports", "travel", "lifestyle"],
        "icons": [
            {"src": "/assets/icon-192.png", "sizes": "192x192", "type": "image/png", "purpose": "any"},
            {"src": "/assets/icon-512.png", "sizes": "512x512", "type": "image/png", "purpose": "any"},
            {"src": "/assets/icon-maskable-512.png", "sizes": "512x512", "type": "image/png", "purpose": "maskable"}],
    }, ensure_ascii=False, indent=2) + "\n")

    write("robots.txt", f"""User-agent: *
Allow: /
Disallow: /tools/
Disallow: /SEARCH_ENGINE_SETUP.txt
Disallow: /points/*/002.txt

Sitemap: {DOMAIN}/sitemap.xml
""")

    pages = ["/", "/all-points.html", "/about.html", "/privacy.html", "/terms.html", "/legal.html", "/contact.html"]
    pts = sorted(p.parent.name for p in (ROOT / "points").glob("*/001.html"))
    urls = [(u, "1.0" if u == "/" else "0.6" if u in ("/all-points.html",) else "0.3") for u in pages]
    urls += [(f"/points/{c}/001.html", "0.8") for c in pts]
    body = "\n".join(f"  <url><loc>{DOMAIN}{u}</loc><lastmod>{TODAY}</lastmod><priority>{pr}</priority></url>" for u, pr in urls)
    write("sitemap.xml", f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{body}\n</urlset>\n')

    csp = ("default-src 'self'; base-uri 'self'; object-src 'none'; form-action 'self'; frame-ancestors 'none'; upgrade-insecure-requests; "
           "script-src 'self' 'unsafe-inline' https://static.cloudflareinsights.com https://pagead2.googlesyndication.com https://*.googlesyndication.com https://*.doubleclick.net https://*.googletagservices.com https://*.adtrafficquality.google https://fundingchoicesmessages.google.com https://www.google.com https://www.gstatic.com; "
           "style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; font-src 'self' https://fonts.gstatic.com data:; img-src 'self' https: data:; "
           "connect-src 'self' https://cloudflareinsights.com https://*.googlesyndication.com https://*.doubleclick.net https://*.adtrafficquality.google https://fundingchoicesmessages.google.com https://www.google.com; "
           "frame-src https://*.googlesyndication.com https://*.doubleclick.net https://*.adtrafficquality.google https://fundingchoicesmessages.google.com https://www.google.com")
    write("_headers", f"""/*
  X-Content-Type-Options: nosniff
  Referrer-Policy: strict-origin-when-cross-origin
  Permissions-Policy: camera=(), microphone=(), geolocation=(), payment=(), usb=()
  X-Frame-Options: DENY
  Strict-Transport-Security: max-age=31536000; includeSubDomains
  Content-Security-Policy: {csp}

/assets/*
  Cache-Control: public, max-age=604800

/points/*/image/*
  Cache-Control: public, max-age=604800

/points.json
  Cache-Control: public, max-age=600

/manifest.webmanifest
  Content-Type: application/manifest+json; charset=utf-8

/sitemap.xml
  Content-Type: application/xml; charset=utf-8
  Cache-Control: public, max-age=3600

/tools/*
  X-Robots-Tag: noindex
""")


def main():
    build_static_pages()
    build_all_points()
    build_home()
    changed = 0
    for f in sorted((ROOT / "points").glob("*/001.html")):
        try:
            changed += process_point(f)
        except ValueError as e:
            print("건너뜀:", f, e)
    print(f"포인트 페이지 {changed}개 갱신")
    if "--no-thumbs" not in sys.argv:
        build_thumbs()
    build_meta_files()
    import shutil
    shutil.copyfile(ROOT / "assets" / "favicon.ico", ROOT / "favicon.ico")
    print("완료")


if __name__ == "__main__":
    main()
