import os, time
from dotenv import load_dotenv
load_dotenv()

from src.graph import run_briefing

def prog(msg, pct):
    print(f"[{pct:0.2f}] {msg}", flush=True)

t0 = time.time()
state = run_briefing(progress=prog, days=3, max_stories=2, sections=["AI Research"])
report = state.get("report", "")
print("\n=== elapsed:", round(time.time()-t0, 1), "s")
print("candidates:", len(state.get("candidates", [])))
print("report chars:", len(report))
print("links:", len(report.split("](")) - 1)
print("\n--- first 1500 chars ---\n")
print(report[:1500])
open("smoke_report.md", "w", encoding="utf-8").write(report)
