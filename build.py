"""重新產生 index.html：修改 data/*.json、data/reader/*.md 或 config.json 後執行 `python build.py`。"""
import html, json, pathlib, re

root = pathlib.Path(__file__).parent
tpl = (root / "src/template.html").read_text(encoding="utf-8")


def load(p):
    return json.loads((root / p).read_text(encoding="utf-8"))


def dump(data):
    return json.dumps(data, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")


# ---------- 讀本：把 data/reader/s1.md、s2.md 轉成 HTML ----------
# 語法：# 章 {p:頁}、## 節 {p:頁}、### 小標、表格、- / 1. 清單（可縮排巢狀）、> 引言、**粗體**、`公式`
PDF = {
    1: "https://www.ipas.org.tw/api/proxy/uploads/certification_resource/bf93f438f7be48d295c1b40a34d79f3d/"
       "AI%E6%87%89%E7%94%A8%E8%A6%8F%E5%8A%83%E5%B8%AB%28%E5%88%9D%E7%B4%9A%29-%E5%AD%B8%E7%BF%92%E6%8C%87%E5%BC%95-"
       "%E7%A7%91%E7%9B%AE1_%E4%BA%BA%E5%B7%A5%E6%99%BA%E6%85%A7%E5%9F%BA%E7%A4%8E%E6%A6%82%E8%AB%961141203_20251222172144.pdf",
    2: "https://www.ipas.org.tw/api/proxy/uploads/certification_resource/bf93f438f7be48d295c1b40a34d79f3d/"
       "AI%E6%87%89%E7%94%A8%E8%A6%8F%E5%8A%83%E5%B8%AB%28%E5%88%9D%E7%B4%9A%29-%E5%AD%B8%E7%BF%92%E6%8C%87%E5%BC%95-"
       "%E7%A7%91%E7%9B%AE2_%E7%94%9F%E6%88%90%E5%BC%8FAI%E6%87%89%E7%94%A8%E8%88%87%E8%A6%8F%E5%8A%83114123_20251222172159.pdf",
}


def inline(s):
    s = html.escape(s, quote=False)
    s = re.sub(r"`([^`]+)`", r'<code class="fx">\1</code>', s)
    s = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", s)
    return s


LI = re.compile(r"^(\s*)(-|\d+\.) (.*)$")


def render_list(lines, i):
    """從第 i 行開始解析一個（可巢狀的）清單，回傳 (html, 下一行索引)。"""
    m = LI.match(lines[i])
    base = len(m.group(1))
    tag = "ul" if m.group(2) == "-" else "ol"
    out = [f"<{tag}>"]
    while i < len(lines):
        m = LI.match(lines[i])
        if not m or len(m.group(1)) < base:
            break
        if len(m.group(1)) > base:
            sub, i = render_list(lines, i)
            out[-1] = out[-1][: -len("</li>")] + sub + "</li>"
            continue
        out.append(f"<li>{inline(m.group(3))}</li>")
        i += 1
    out.append(f"</{tag}>")
    return "".join(out), i


def render_block(lines):
    out, i = [], 0
    while i < len(lines):
        ln = lines[i]
        if not ln.strip():
            i += 1
        elif ln.startswith("### "):
            out.append(f"<h4>{inline(ln[4:])}</h4>")
            i += 1
        elif ln.startswith("|"):
            rows = []
            while i < len(lines) and lines[i].startswith("|"):
                rows.append([c.strip() for c in lines[i].strip().strip("|").split("|")])
                i += 1
            head, body = rows[0], [r for r in rows[1:] if not all(re.fullmatch(r":?-+:?", c) for c in r)]
            t = "<thead><tr>" + "".join(f"<th>{inline(c)}</th>" for c in head) + "</tr></thead><tbody>"
            t += "".join("<tr>" + "".join(f"<td>{inline(c)}</td>" for c in r) + "</tr>" for r in body)
            out.append(f'<div class="tablewrap"><table class="rt">{t}</tbody></table></div>')
        elif ln.startswith(">"):
            paras, cur = [], []
            while i < len(lines) and lines[i].startswith(">"):
                t = lines[i][1:].strip()
                if t:
                    cur.append(t)
                elif cur:
                    paras.append(cur)
                    cur = []
                i += 1
            if cur:
                paras.append(cur)
            kind = "warn" if paras and paras[0][0].startswith("⚠") else "tip"
            out.append(f'<div class="callout {kind}">'
                       + "".join("<p>" + "<br>".join(inline(x) for x in p) + "</p>" for p in paras) + "</div>")
        elif LI.match(ln):
            h, i = render_list(lines, i)
            out.append(h)
        else:
            buf = []
            while i < len(lines) and lines[i].strip() and not re.match(r"^(#|\||>|\s*(-|\d+\.) )", lines[i]):
                buf.append(inline(lines[i].strip()))
                i += 1
            out.append("<p>" + "<br>".join(buf) + "</p>")
    return "".join(out)


def build_reader():
    chapters = []
    for subj in (1, 2):
        p = root / f"data/reader/s{subj}.md"
        if not p.exists():
            continue
        ch = sec = None
        for ln in p.read_text(encoding="utf-8").split("\n"):
            m = re.match(r"^(#{1,2}) (.*?)(?: \{p:(\d+)\})?$", ln)
            if m:
                text, page = m.group(2), int(m.group(3) or 0)
                if m.group(1) == "#":
                    no, title = text.split(" ", 1)
                    ch = {"subj": subj, "sec": no, "title": title, "page": page, "pdf": PDF[subj], "parts": []}
                    chapters.append(ch)
                    sec = None
                else:
                    sec = {"h": text, "page": page, "md": []}
                    ch["parts"].append(sec)
                continue
            if sec is not None:
                sec["md"].append(ln)
    for c in chapters:
        for s in c["parts"]:
            s["html"] = render_block(s.pop("md"))
    return chapters


cfg = load("config.json") if (root / "config.json").exists() else {}
out = (tpl.replace("__BANK__", dump(load("data/questions.json")))
          .replace("__NOTES__", dump(load("data/notes.json")))
          .replace("__READER__", dump(build_reader()))
          .replace("__GOOGLE_CLIENT_ID__", dump(cfg.get("googleClientId")))
          .replace("__ALLOWED_EMAILS__", dump(cfg.get("allowedEmails", []))))
(root / "index.html").write_text(out, encoding="utf-8")
print("index.html 已更新")
