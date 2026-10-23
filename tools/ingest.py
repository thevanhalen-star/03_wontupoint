# -*- coding: utf-8 -*-
"""새 포인트 업로드 → 사이트 규격으로 자동 변환 + points.json / sitemap / rss 자동 갱신.

사용법 (저장소 루트에서)
    python tools/ingest.py            한 번 실행: 새로 올린 원본 포인트를 모두 변환
    python tools/ingest.py --watch    계속 켜 두기: points 폴더를 감시하다가 새 원본이 올라오면 자동 변환

업로드 방법
    points/C536/            ← 새 폴더(번호는 마지막 번호 다음 순서)
        001.html            ← 원본 html (서론 / 본론 / 결론 구조의 기존 작성본)
        002.txt             ← 1줄: 제목 / 2줄: 포인트명 / 3줄: 주소 / 이후: #해시태그
        image/001.jpg …     ← 포인트 사진(001, 002, 003 … 연번)

이미 변환된 페이지(wontupoint-theme 스타일이 있는 페이지)는 건드리지 않습니다.
"""
import html
import json
import re
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))
import build_site as bs  # noqa: E402

POINTS = ROOT / "points"
HEAD_TPL = (Path(__file__).resolve().parent / "templates" / "point_head.html").read_text(encoding="utf-8")

# 광고는 '광고 자리'만 넣는다. 어떤 광고를 보일지·켜고 끌지는 관리자 페이지(/admin/)의 설정이 정한다.
# 자리 번호: 1=도입부 사진 아래, 2=본론 앞쪽, 3=본론 뒤쪽, 4=글 맨 끝 (bs.AD_SLOT 참고)


def esc(s):
    return html.escape(str(s), quote=True)


def ad_block(n, margin):
    return f'<div class="point-media ad-photo ad-slot" data-ad-slot="{bs.AD_SLOT[n]}" style="margin:{margin};text-align:center;"></div>'


def photo_block(name, n, margin):
    return (
        f'<div class="point-media point-photo" style="margin:{margin};text-align:center;"><img src="image/{n:03d}.jpg" '
        f'alt="{esc(name)} 주변 모습 {n}" loading="lazy" style="display:inline-block;width:100%;max-width:100%;height:auto;"></div>'
    )


def media(inner):
    return f"<!-- AUTO_POINT_MEDIA_START -->\n{inner}\n<!-- AUTO_POINT_MEDIA_END -->\n"


# ---------------------------------------------------------------- 원본 파싱
def read_meta(folder: Path):
    txt = folder / "002.txt"
    if not txt.exists():
        raise ValueError("002.txt 가 없습니다")
    lines = [x.strip() for x in txt.read_text(encoding="utf-8-sig", errors="replace").splitlines() if x.strip()]
    if len(lines) < 3 or lines[1].startswith("#") or lines[2].startswith("#"):
        raise ValueError("002.txt 형식 오류: 1줄 제목 / 2줄 포인트명 / 3줄 주소 / 이후 #해시태그")
    return {"title": lines[0], "name": lines[1], "addr": lines[2], "tags": [x for x in lines[3:] if x.startswith("#")]}


def split_sections(body):
    """<div class="section"> … </div> 를 div 중첩을 세어 분리한다."""
    out, pos = [], 0
    while True:
        m = re.compile(r'<div class="section">').search(body, pos)
        if not m:
            break
        depth, i = 1, m.end()
        for t in re.finditer(r"<div\b|</div>", body[m.end():]):
            depth += 1 if t.group(0).startswith("<div") else -1
            if depth == 0:
                out.append(body[m.end(): m.end() + t.start()])
                pos = m.end() + t.end()
                break
        else:
            raise ValueError("</div> 짝이 맞지 않습니다")
    return out


def is_bracket_section(s):
    """[핵심 요약], [채비 전환 판단 기준] 처럼 제목이 [ ] 로 감싸진 섹션."""
    return bool(re.search(r"<(?:strong|b|h[1-6])\b[^>]*>\s*\[[^\]<]+\]", s))


def strip_qa(s):
    """'Q.' 또는 'A.' 로 시작하는 문단(<p>)을 모두 삭제하고 남은 빈 <br> 줄을 정리한다."""
    def drop(m):
        txt = bs.strip_tags(m.group(0))
        return "" if re.match(r"^(Q|A)\s*[.．:]", txt) else m.group(0)
    s = re.sub(r"<p\b[^>]*>.*?</p>", drop, s, flags=re.S)
    return re.sub(r"(?:\n\s*<br\s*/?>[ \t]*){2,}", "\n<br>", s)


def ad_positions(n_bodies):
    """광고 2·3번을 본론 사이에 고르게 배치 (본론 7개면 2번·5번 뒤)."""
    a2 = max(1, round(n_bodies * 0.3))
    a3 = max(a2 + 1, round(n_bodies * 0.7))
    return {a2: 2, a3: 3} if a3 <= n_bodies else {a2: 2}


def classify(secs):
    """서론(제목+본문) / 본론 / 결론(제목+본문) / 그 밖의 추가 섹션으로 나눈다."""
    pre, intro_p, bodies, concl_h, concl_p, post = [], "", [], None, "", []
    state = "pre"
    for s in secs:
        has_h1 = bool(re.search(r"<h1\b", s))
        has_h23 = bool(re.search(r"<h[23]\b", s))
        if state == "pre":
            if has_h1:
                state = "intro"
            else:
                pre.append(s)
        elif state == "intro":
            if has_h23:
                bodies.append(s); state = "body"
            elif has_h1:
                concl_h = s; state = "concl"
            elif not intro_p and "<p" in s:
                intro_p = s
            else:
                post.append(s)
        elif state == "body":
            if has_h23:
                bodies.append(s)
            elif has_h1:
                concl_h = s; state = "concl"
            else:
                post.append(s)
        else:  # concl
            if not concl_p and "<p" in s and not has_h1 and not has_h23:
                concl_p = s
            else:
                post.append(s)
    return pre, intro_p, bodies, concl_h, concl_p, post


def convert(folder: Path, raw: str):
    meta = read_meta(folder)
    name, addr, title = meta["name"], meta["addr"], meta["title"]
    m = re.search(r'<div class="container">(.*)</div>\s*</body>', raw, re.S)
    if not m:
        raise ValueError('원본에서 <div class="container"> 영역을 찾지 못했습니다')
    secs = split_sections(m.group(1))
    kept = [s for s in secs if not is_bracket_section(s)]
    if len(kept) != len(secs):
        print(f"  - {folder.name}: [ ] 제목 섹션 {len(secs) - len(kept)}개 삭제")
    pre, intro_p, bodies, concl_h, concl_p, post = classify(kept)
    count = lambda xs: sum(len(re.findall(r"<p\b", x)) for x in xs)  # noqa: E731
    qa_before = count([intro_p, concl_p, *bodies, *post])
    intro_p, concl_p = strip_qa(intro_p), strip_qa(concl_p)
    bodies = [strip_qa(x) for x in bodies]
    post = [strip_qa(x) for x in post]
    if qa_before != count([intro_p, concl_p, *bodies, *post]):
        print(f"  - {folder.name}: Q&A 문단 {qa_before - count([intro_p, concl_p, *bodies, *post])}개 삭제")
    if not bodies:
        raise ValueError("본론(<h2>/<h3> 제목이 있는 섹션)을 찾지 못했습니다")

    photos = sorted(int(p.stem) for p in (folder / "image").glob("[0-9][0-9][0-9].jpg")) if (folder / "image").is_dir() else []
    if 1 not in photos:
        print(f"  ! {folder.name}: image/001.jpg 가 없습니다 (목록 대표 이미지)")

    queue = list(photos)  # 문서 순서대로 사진 슬롯(상단 → 서론 뒤 → 본론 1,2,…)에 한 장씩 배정

    def photo(margin="32px 0"):
        return media(photo_block(name, queue.pop(0), margin)) if queue else ""

    ad_at = ad_positions(len(bodies))

    inner_intro = re.sub(r"^\s*<div[^>]*>|</div>\s*$", "", intro_p).strip()
    out = []
    out.append("<!-- 서론 -->\n<!-- SECTION_INTRO_START -->\n<div class=\"section\">")
    out.append(f'<h1 class="wontu-point-title">{esc(title)}</h1>\n')
    out.append('<!-- WONTU_TITLE_DIVIDER_START -->\n<div class="wontu-title-divider" role="separator" aria-label="제목과 본문 구분"></div>\n<!-- WONTU_TITLE_DIVIDER_END -->')
    out.append(photo("32px 0 0 0") + media(ad_block(1, "0 0 32px 0")) + "</div>\n")
    out.append('<div class="section">\n<h2 class="intro-heading">포인트 안내</h2>')
    out.append('<!-- WONTU_POINT_INFO_START -->\n<div class="wontu-point-info" style="margin:10px 0 22px;line-height:1.8;">\n'
               f'  <div class="point-name" style="font-weight:700;color:inherit;">{esc(name)}</div>\n'
               f'  <div class="point-address" style="color:#64748b;">{esc(addr)}</div>\n</div>\n<!-- WONTU_POINT_INFO_END -->')
    out.append(inner_intro + "\n</div>\n<!-- SECTION_INTRO_END -->\n")
    out.append(photo())
    for s in pre:  # 서론보다 앞에 있던 요약 등은 서론 바로 뒤로
        out.append(f'<div class="section">{s}</div>\n')
    for i, s in enumerate(bodies, 1):
        s = re.sub(r"<(/?)h2\b", r"<\1h3", s)
        out.append(f"\n<!-- 본론 {i} -->\n\n<!-- SECTION_BODY_{i}_START -->\n<div class=\"section\">{s}</div>\n<!-- SECTION_BODY_{i}_END -->\n")
        ad = ad_at.get(i)
        if ad and queue:
            out.append(photo("32px 0 0 0") + media(ad_block(ad, "0 0 32px 0")))
        elif ad:
            out.append(media(ad_block(ad, "32px 0")))
        else:
            out.append(photo())
    out.append("\n<!-- 결론 -->\n\n<!-- SECTION_CONCLUSION_START -->")
    if concl_h:
        h = re.sub(r"<h1\b[^>]*>", '<h2 class="conclusion-heading">', concl_h)
        h = h.replace("</h1>", "</h2>")
        out.append(f'<div class="section">{h}</div>\n')
    if concl_p:
        out.append(f'<div class="section">{concl_p}</div>')
    for s in post:
        out.append(f'<div class="section">{s}</div>')
    out.append("<!-- SECTION_CONCLUSION_END -->\n")
    for ad_n in (2, 3):  # 본론이 너무 적어 배치되지 못한 광고는 결론 뒤에
        if ad_n not in ad_at.values():
            out.append(media(ad_block(ad_n, "32px 0")))
    while queue:  # 남은 사진은 4번 광고 앞에 모두 붙인다
        out.append(photo())
    out.append(media(ad_block(4, "32px 0")))
    tags = "".join(f'    <span class="wontu-hashtag">{esc(t)}</span>\n' for t in meta["tags"])
    out.append(
        '<!-- WONTU_HASHTAGS_START -->\n<div aria-hidden="true" style="height: 10em;"></div>\n'
        '<div class="wontu-hashtags" aria-label="해시태그" style="margin-top: 0; padding: 12px 0 24px; display: flex; flex-wrap: wrap; gap: 10px; '
        'justify-content: center; font-size: 14px; line-height: 1.8; color: #64748b;">\n' + tags + "</div>\n<!-- WONTU_HASHTAGS_END -->\n")
    body = "\n".join(out)
    page = (
        '<!DOCTYPE html>\n<html lang="ko">\n<head>\n    <meta charset="UTF-8">\n'
        '    <meta name="viewport" content="width=device-width, initial-scale=1.0">\n'
        f"    <title>{esc(title)}</title>\n\n{HEAD_TPL}<!-- WONTU_HEAD_START -->\n<!-- WONTU_HEAD_END -->\n</head>\n<body>\n"
        f'<div class="container">\n\n{body}</div>\n<!-- WONTU_FOOT_START -->\n<!-- WONTU_FOOT_END -->\n</body>\n</html>\n'
    )
    return page, meta


# ---------------------------------------------------------------- 목록 갱신
def json_address(addr):
    toks = addr.split()
    if toks and re.fullmatch(r"\d+(-\d+)?(번지)?", toks[-1]):
        toks.pop()
        if toks and toks[-1] == "산":
            toks.pop()
    return " ".join(toks)


def update_points_json(new):
    path = ROOT / "points.json"
    data = json.loads(path.read_text(encoding="utf-8-sig"))
    by_id = {d["id"]: d for d in data}
    for pid, meta in new.items():
        by_id[pid] = {"id": pid, "name": meta["name"], "address": json_address(meta["addr"]),
                      "url": f"/{pid}/001.html", "image": f"/{pid}/image/001.jpg"}
    out = [by_id[k] for k in sorted(by_id)]
    path.write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    return len(out)


def update_rss(new):
    path = ROOT / "rss.xml"
    if not path.exists():
        return
    t = path.read_text(encoding="utf-8")
    add = ""
    for pid, meta in sorted(new.items()):
        link = f"{bs.DOMAIN}/points/{pid}/001.html"
        if link in t:
            continue
        add += (f"    <item>\n      <title>{esc(meta['name'])}</title>\n      <link>{link}</link>\n      <guid>{link}</guid>\n"
                f"      <description>{esc(meta['name'])} — {esc(json_address(meta['addr']))}. 낚시 포인트의 상세 안내는 링크에서 확인하세요.</description>\n    </item>\n")
    if add:
        t = t.replace("  </channel>", add + "  </channel>", 1)
        path.write_text(t, encoding="utf-8", newline="\n")


# ---------------------------------------------------------------- 실행
def find_raw():
    out = []
    for f in sorted(POINTS.glob("*/001.html")):
        t = f.read_text(encoding="utf-8-sig", errors="replace")
        if 'id="wontupoint-theme"' not in t:
            out.append(f)
    return out


def run_once(quiet=False, seen=None):
    raws = find_raw()
    if seen is not None:  # 감시 모드: 같은 파일의 같은 오류는 한 번만 알림
        # 복사가 끝나지 않은 파일(최근 5초 내 수정)은 다음 순회로 미룬다
        raws = [f for f in raws if (f, f.stat().st_mtime) not in seen and time.time() - f.stat().st_mtime > 5]
        seen.update((f, f.stat().st_mtime) for f in raws)
    if not raws:
        if not quiet:
            print("새로 변환할 원본 포인트가 없습니다.")
        return 0
    done = {}
    for f in raws:
        folder = f.parent
        try:
            raw = f.read_text(encoding="utf-8-sig", errors="replace")
            page, meta = convert(folder, raw)
        except ValueError as e:
            print(f"건너뜀 {folder.name}: {e}")
            continue
        keep = ROOT / "tools" / "originals"
        keep.mkdir(exist_ok=True)
        (keep / f"{folder.name}_001.html").write_text(raw, encoding="utf-8", newline="\n")  # 원본 보관
        f.write_text(page, encoding="utf-8", newline="\n")
        bs.process_point(f)  # 광고 표시·출처·SEO·QR·안전 안내·푸터 등 사이트 공통 요소
        done[folder.name] = meta
        print(f"변환 완료 {folder.name}: {meta['name']}")
    if done:
        n = update_points_json(done)
        update_rss(done)
        bs.build_static_pages()   # 소개 페이지의 포인트 수 등
        bs.build_meta_files()     # sitemap.xml 등
        print(f"points.json {n}개 / sitemap·rss 갱신 완료")
    return len(done)


def main():
    if "--watch" in sys.argv:
        print("감시 중… (Ctrl+C 로 종료) — points 폴더에 새 원본이 올라오면 자동 변환합니다.")
        seen = set()
        while True:
            try:
                run_once(True, seen)
            except Exception as e:  # noqa: BLE001
                print("오류:", e)
            time.sleep(10)
    else:
        run_once()


if __name__ == "__main__":
    main()
