"""重新產生 index.html：修改 data/questions.json 或 data/notes.json 後執行 `python build.py`。"""
import json, pathlib
root = pathlib.Path(__file__).parent
tpl = (root / "src/template.html").read_text(encoding="utf-8")
def dump(p):
    data = json.loads((root / p).read_text(encoding="utf-8"))
    return json.dumps(data, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
out = tpl.replace("__BANK__", dump("data/questions.json")).replace("__NOTES__", dump("data/notes.json"))
(root / "index.html").write_text(out, encoding="utf-8")
print("index.html 已更新")
