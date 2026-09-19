from pathlib import Path
import hashlib,json,datetime
ROOT=Path("."); OUT=ROOT/"agent-output"; OUT.mkdir(exist_ok=True)
cfg=json.loads((ROOT/"factory-agent.json").read_text(encoding="utf-8"))
allowed={".md",".txt",".html",".htm",".json",".yml",".yaml",".py",".js",".ts",".css"}
skip={".git","node_modules","venv",".venv","agent-output"}
items=[]
for p in ROOT.rglob("*"):
    if p.is_file() and p.suffix.lower() in allowed and not any(x in skip for x in p.parts):
        try:
            b=p.read_bytes(); items.append({"path":p.as_posix(),"bytes":len(b),"sha256":hashlib.sha256(b).hexdigest()})
        except Exception: pass
items.sort(key=lambda x:x["path"])
payload={"schema_version":1,"generated_at":datetime.datetime.now(datetime.timezone.utc).isoformat(),"repository":cfg["repo"],"role":cfg["role"],"source_count":len(items),"sources":items,"policy":cfg["policy"],"status":"ready","note":"Free-first deterministic specialist worker; no paid API required."}
(OUT/"manifest.json").write_text(json.dumps(payload,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
print(f"READY {cfg['repo']} / {cfg['role']} / {len(items)} sources")
