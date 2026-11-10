# Aether â€” Evaluation Results

*Generated 2026-11-10 00:26 UTC Â· model `openai/gpt-oss-20b` Â· embeddings `sentence-transformers/all-MiniLM-L6-v2` Â· 6 pages â†’ 11 chunks â†’ 11 vectors*

| Metric | Value | What it means |
|---|---|---|
| Retrieval Hit@1 | **0.643** | answer found fully inside the single best chunk |
| Retrieval Hit@4 | **1.0** | answer inside any of the 4 chunks actually used |
| MRR | **0.786** | mean reciprocal rank over 14 questions |
| Grounded-accuracy (LLM judge) | **0.933** (15 scored, 0 errors) | answer fully supported by the retrieved context, judged by a strict LLM rubric |
| Gatekeeper accuracy (must-refuse) | **1.0** | out-of-document questions were refused instead of hallucinated |
| Planner routing accuracy | **1.0** (3 cases) | the planner called exactly the right tools |

The full run is reproducible: `python evaluation/evaluate.py` (add `--fast` for retrieval metrics without API cost).