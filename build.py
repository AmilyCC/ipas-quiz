"""重新產生 index.html：修改 data/*.json 或 config.json 後執行 `python build.py`。"""
import json, pathlib
root = pathlib.Path(__file__).parent
tpl = (root / "src/template.html").read_text(encoding="utf-8")
def load(p):
    return json.loads((root / p).read_text(encoding="utf-8"))
def dump(data):
    return json.dumps(data, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
cfg = load("config.json") if (root / "config.json").exists() else {}
out = (tpl.replace("__BANK__", dump(load("data/questions.json")))
          .replace("__NOTES__", dump(load("data/notes.json")))
          .replace("__GOOGLE_CLIENT_ID__", dump(cfg.get("googleClientId")))
          .replace("__ALLOWED_EMAILS__", dump(cfg.get("allowedEmails", []))))
(root / "index.html").write_text(out, encoding="utf-8")
print("index.html 已更新")
