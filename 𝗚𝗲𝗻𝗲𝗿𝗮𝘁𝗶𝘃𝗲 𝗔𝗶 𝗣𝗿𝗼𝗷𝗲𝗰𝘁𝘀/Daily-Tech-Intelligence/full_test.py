import time
from dotenv import load_dotenv
load_dotenv()

from src.graph import run_briefing

def prog(msg, pct):
    print(f"[{pct:0.2f}] {msg}", flush=True)

t0 = time.time()
state = run_briefing(
    progress=prog,
    days=2,
    max_stories=3,
    sections=["Artificial Intelligence", "New AI Tools & Models", "AI Research"],
)
report = state.get("report", "")
elapsed = round(time.time() - t0, 1)

print("\n=== RUN COMPLETE ===")
print("elapsed:", elapsed, "s")
print("candidates:", len(state.get("candidates", [])))
print("report chars:", len(report))
print("revisions:", state.get("revisions", 0))
for sid, audit in state.get("audits", {}).items():
    print(f"  {sid:9s} hard={len(audit.get('hard', []))} soft={len(audit.get('soft', []))} checked={audit.get('checked', 0)}")
for sid, rev in state.get("reviews", {}).items():
    print(f"  {sid:9s} verdict={rev.get('verdict')} problems={len(rev.get('problems', []))}")

open("full_report.md", "w", encoding="utf-8").write(report)
print("written full_report.md")
