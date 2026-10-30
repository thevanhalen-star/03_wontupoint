"""포인트 페이지의 FAQ(자주 묻는 질문) 생성.

답변은 새로 지어내지 않고, 해당 페이지에 이미 쓰여 있는 본문 단락에서만 뽑는다.
(그래서 포인트마다 내용이 다르고, 페이지에 없는 정보는 FAQ에도 나오지 않는다.)
섹션 번호 → 질문 종류:
  1 진입·주차 / 2 차박 / 3 편의시설 / 6 어울리는 낚시 / 7 주변 대안
물때 질문은 본문에서 '물때'가 나오는 단락이 있을 때만 만든다.
"""
import html
import re

MAX_ANSWER = 190   # 답변 최대 글자 수(문장 단위로 자른다)
MIN_ANSWER = 50    # 이보다 짧은 답변은 질문째 빼서 얇은 FAQ가 나오지 않게 한다
GUIDE_TIDE = "/guide/tide.html"


def _text(s):
    s = re.sub(r"<br\s*/?>", " ", s, flags=re.I)
    s = re.sub(r"<[^>]+>", "", s)
    return re.sub(r"\s+", " ", html.unescape(s)).strip()


def _sentences(p):
    t = _text(p)
    parts = re.split(r"(?<=[.!?])\s+", t)
    return [x.strip() for x in parts if x.strip()]


def _sections(doc):
    """SECTION_BODY_n 블록의 단락(텍스트) 목록을 {n: [p, ...]} 로."""
    out = {}
    for m in re.finditer(r"<!-- SECTION_BODY_(\d+)_START -->(.*?)<!-- SECTION_BODY_\1_END -->", doc, re.S):
        ps = [_text(x) for x in re.findall(r"<p>(.*?)</p>", m.group(2), re.S)]
        out[int(m.group(1))] = [p for p in ps if len(p) > 20]
    return out


def _pack(sents, limit=MAX_ANSWER):
    """문장을 앞에서부터 한도 안에서 이어 붙인다. 첫 문장이 한도를 넘으면 그 문장만."""
    res = ""
    for s in sents:
        if res and len(res) + 1 + len(s) > limit:
            break
        res = (res + " " + s).strip()
        if len(res) >= limit * 0.6:
            break
    return res


def build_faq(doc, name):
    """[(질문, 답변, 가이드링크 or None), ...] — 4개 미만이면 빈 목록(얇은 FAQ를 만들지 않는다)."""
    sec = _sections(doc)
    qs = []

    def first(n):
        ps = sec.get(n) or []
        return _sentences(ps[0]) if ps else []

    plan = [
        (1, f"{name}, 가는 길과 주차는 어떤가요?"),
        (2, f"{name}에서 차박(야간 체류)은 어떤가요?"),
        (3, f"{name} 근처에 편의점·식당 같은 편의시설이 있나요?"),
    ]
    for n, q in plan:
        a = _pack(first(n))
        if len(a) >= MIN_ANSWER:
            qs.append((q, a, None))

    # 물때: '물때'가 들어간 문장 최대 2개(섹션 4·5 우선)
    tide = []
    for n in (4, 5, 1, 2, 6, 7):
        for p in sec.get(n, []):
            for s in _sentences(p):
                if "물때" in s and s not in tide and len(s) < 140:
                    tide.append(s)
    a = _pack(tide[:2])
    if len(a) >= MIN_ANSWER:
        qs.append((f"{name} 낚시는 물때를 어떻게 봐야 하나요?", a, GUIDE_TIDE))

    for n, q in ((6, f"{name}에는 어떤 낚시가 어울리나요?"), (7, f"{name} 말고 함께 둘러볼 만한 주변 포인트는 어디인가요?")):
        a = _pack(first(n))
        if len(a) >= MIN_ANSWER:
            qs.append((q, a, None))

    return qs if len(qs) >= 4 else []


def render_faq(qs):
    if not qs:
        return ""
    items = []
    for q, a, guide in qs:
        extra = f' <a href="{guide}">물때 보는 법 안내 보기</a>' if guide else ""
        items.append(f'<details class="wontu-faq-item"><summary>{html.escape(q)}</summary><p>{html.escape(a)}{extra}</p></details>')
    return ('<section class="wontu-faq" aria-label="자주 묻는 질문"><h2>자주 묻는 질문</h2>'
            + "".join(items)
            + '<p class="note">위 답변은 이 페이지 본문을 요약한 것입니다. 현장 상황은 수시로 바뀔 수 있으니 출발 전 다시 확인해 주세요.<br>'
              '함께 보면 좋은 안내: <a href="/guide/car-camping.html">차박 낚시 준비물과 매너</a> · <a href="/guide/safety.html">방파제·갯바위 낚시 안전 수칙</a> · '
              '<a href="/guide/wontu-fishing.html">원투낚시 입문</a> · <a href="/guide/walking-fishing.html">워킹낚시 입문</a></p></section>')


def faq_jsonld(qs):
    if not qs:
        return None
    return {"@context": "https://schema.org", "@type": "FAQPage", "inLanguage": "ko-KR",
            "mainEntity": [{"@type": "Question", "name": q,
                            "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a, _ in qs]}
