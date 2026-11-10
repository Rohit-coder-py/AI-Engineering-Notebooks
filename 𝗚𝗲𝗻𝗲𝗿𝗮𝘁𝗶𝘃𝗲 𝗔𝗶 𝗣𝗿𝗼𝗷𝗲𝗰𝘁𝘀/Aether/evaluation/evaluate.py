"""
Aether Evaluation Harness
=========================

Measures, with real numbers, how well Aether actually works:

  1. RETRIEVAL   â€” is the right place in the PDF inside the top-k chunks?
  2. GROUNDEDNESSâ€” does the Document Analyst answer ONLY from the document?
  3. GATEKEEPING â€” does it refuse questions the PDF cannot answer?
  4. ROUTING     â€” does the Planner pick the correct agent/tool for a request?

Results are written to evaluation/results.json and evaluation/RESULTS.md.

Usage:
    python evaluation/evaluate.py             # full run (LLM eval needs GROQ_API_KEY)
    python evaluation/evaluate.py --fast      # retrieval metrics only (no API cost)

The golden-QA set is defined against sample_data/Aether_Product_Handbook.pdf,
so the harness is reproducible on any machine without external data.
"""

import argparse
import json
import os
import re
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

from dotenv import load_dotenv

# Locate the project root (evaluation/ lives directly under it)
PROJECT_ROOT = Path(__file__).resolve().parent.parent
load_dotenv(PROJECT_ROOT / ".env")

PDF_PATH = PROJECT_ROOT / "sample_data" / "Aether_Product_Handbook.pdf"

# ----------------------------------------------------------------------
# Configuration (mirrors the exact parameters used by app.py)
# ----------------------------------------------------------------------
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 150
RETRIEVAL_K = 4
EMBEDDING_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
CHAT_MODEL = "openai/gpt-oss-20b"
THROTTLE_SECONDS = 4          # sleep between LLM calls (free-tier friendly)
TIME_BUDGET_SECONDS = 60 * 25 # overall cap; skips remaining work if exceeded

# ----------------------------------------------------------------------
# Golden QA set  ("answer" strings are verbatim-ish fragments of the PDF)
# ----------------------------------------------------------------------
GOLDEN_QA = [
    {
        "id": "q1_chunk_size",
        "question": "What chunk size and overlap does Aether's text splitter use?",
        "answer": "chunk size of 1000 characters and an overlap of 150",
        "keywords": ["1000", "150"],
        "expected_page": 3,
        "type": "fact_lookup",
    },
    {
        "id": "q2_embedding_model",
        "question": "Which embedding model does Aether use?",
        "answer": "sentence-transformers model all-MiniLM-L6-v2",
        "keywords": ["all-minilm-l6-v2"],
        "expected_page": 3,
        "type": "fact_lookup",
    },
    {
        "id": "q3_default_model",
        "question": "Which model is Aether's default chat model and which API serves it?",
        "answer": "openai/gpt-oss-20b, served through the Groq API",
        "keywords": ["gpt-oss-20b", "groq"],
        "expected_page": 4,
        "type": "fact_lookup",
    },
    {
        "id": "q4_search_provider",
        "question": "Which search provider powers the Researcher Agent?",
        "answer": "Tavily Search API",
        "keywords": ["tavily"],
        "expected_page": 2,
        "type": "fact_lookup",
    },
    {
        "id": "q5_retrieval_k",
        "question": "How many chunks does the Document Analyst retrieve at question time?",
        "answer": "top 4 chunks (RETRIEVAL_K = 4)",
        "keywords": ["4"],
        "expected_page": 3,
        "type": "config_lookup",
    },
    {
        "id": "q6_scanned_pdf",
        "question": "What happens if I upload a scanned PDF?",
        "answer": "Scanned PDFs without an extractable text layer are not supported; OCR is planned",
        "keywords": ["scanned"],
        "expected_page": 5,
        "type": "policy",
    },
    {
        "id": "q7_writer_role",
        "question": "Which agent formats the final structured response?",
        "answer": "The Writer Agent",
        "keywords": ["writer"],
        "expected_page": 2,
        "type": "fact_lookup",
    },
    {
        "id": "q8_temperature",
        "question": "What temperature is the planner agent set to?",
        "answer": "0.7",
        "keywords": ["0.7"],
        "expected_page": 4,
        "type": "config_lookup",
    },
    {
        "id": "q9_chat_history",
        "question": "Where is chat history stored and when is it cleared?",
        "answer": "kept in memory only; cleared on refresh or Clear Chat",
        "keywords": ["memory"],
        "expected_page": 5,
        "type": "policy",
    },
    {
        "id": "q10_parser",
        "question": "Which library parses the uploaded PDF page by page?",
        "answer": "pypdf",
        "keywords": ["pypdf"],
        "expected_page": 3,
        "type": "fact_lookup",
    },
    {
        "id": "q11_all_agents",
        "question": "List all four agents in Aether's multi-agent system.",
        "answer": "Planner, Document Analyst, Researcher, Writer",
        "keywords": ["planner", "document analyst", "researcher", "writer"],
        "expected_page": 2,
        "type": "composition",
    },
    {
        "id": "q12_embedding_dimension",
        "question": "What is the embedding dimension of the MiniLM model used by Aether?",
        "answer": "384",
        "keywords": ["384"],
        "expected_page": 7,
        "type": "fact_lookup",
    },
    {
        "id": "q13_mrr_meaning",
        "question": "According to the glossary, what does the metric MRR stand for?",
        "answer": "Mean Reciprocal Rank: average of 1 divided by the rank of the first correct hit",
        "keywords": ["mean reciprocal rank"],
        "expected_page": 8,
        "type": "fact_lookup",
    },
    {
        "id": "q14_api_keys",
        "question": "Which API key variables does Aether need?",
        "answer": "GROQ_API_KEY and TAVILY_API_KEY",
        "keywords": ["groq_api_key", "tavily_api_key"],
        "expected_page": 7,
        "type": "config_lookup",
    },
    {
        "id": "r1_out_of_scope",   # must be REFUSED
        "question": "Who won the FIFA World Cup final in 2022?",
        "answer": "",
        "keywords": [],
        "expected_page": None,
        "type": "must_refuse",
    },
]

# Test cases for the Planner router: question -> tools that MUST be used
ROUTING_CASES = [
    {
        "id": "route_doc_only",
        "question": "According to the handbook, what does the Writer Agent do?",
        "expect_tools": {"document_analyst_tool"},
        "expect_none": False,
    },
    {
        "id": "route_doc_and_web",
        "question": "Does the handbook explain what tool-call middleware does, and can you also add current industry context about agent reliability from the web?",
        "expect_tools": {"document_analyst_tool", "researcher_agent"},
        "expect_none": False,
    },
    {
        "id": "route_chat_only",
        "question": "Say hello and tell me you are ready, without using any tools.",
        "expect_tools": set(),
        "expect_none": True,   # planner should not call any tool
    },
]

REFUSAL_PATTERNS = [
    r"not.{0,12}(found|in|contain|available|able)",
    r"(could not|cannot|can't|no)",
    r"only.{0,20}document",
    r".{0,30}i (do not|don't) (have|know)",
]


# ======================================================================
# 1. INDEX BUILDER (same pipeline parameters as app.py)
# ======================================================================
def build_index(pdf_path: Path):
    """Replicates app.py's ingest pipeline and returns (faiss_db, stats)."""
    from pypdf import PdfReader
    from langchain_core.documents import Document
    from langchain_text_splitters import RecursiveCharacterTextSplitter
    from langchain_huggingface import HuggingFaceEmbeddings
    from langchain_community.vectorstores import FAISS

    reader = PdfReader(str(pdf_path))
    documents = []
    for page_number, page in enumerate(reader.pages):
        text = page.extract_text()
        if text and text.strip():
            documents.append(Document(
                page_content=text,
                metadata={"page": page_number + 1, "source": pdf_path.name}))

    splitter = RecursiveCharacterTextSplitter(chunk_size=CHUNK_SIZE,
                                              chunk_overlap=CHUNK_OVERLAP)
    chunks = splitter.split_documents(documents)

    embedding_model = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL_NAME)
    db = FAISS.from_documents(chunks, embedding_model)

    stats = {"pages": len(reader.pages), "chunks": len(chunks),
             "vectors": db.index.ntotal}
    return db, stats


# ======================================================================
# 2. RETRIEVAL METRICS
# ======================================================================
def evaluate_retrieval(db, golden, k_values=(1, 2, 4)):
    """Hit@k: the answer text must appear inside the top-k retrieved chunks."""
    per_item = []
    first_hit_rank = []

    for item in golden:
        if item["type"] == "must_refuse":
            continue
        docs = db.similarity_search(item["question"], k=max(k_values))
        hits = {}
        for k in k_values:
            joined = " ".join(d.page_content.lower() for d in docs[:k])
            hits[k] = all(kw.lower() in joined for kw in item["keywords"])

        rank = None
        for k in k_values:
            if hits[k]:
                rank = k
                break
        if rank:
            first_hit_rank.append(rank)

        per_item.append({"id": item["id"], "expected_page": item["expected_page"],
                         "hit@1": hits.get(1, False), "hit@2": hits.get(2, False),
                         "hit@4": hits.get(4, False), "first_hit_at_k": None if rank is None else rank})

    total = len(per_item)
    mrr = sum(1.0 / r for r in first_hit_rank) / total if total else 0.0
    summary = {
        "n_items": total,
        **{f"hit@{k}": round(sum(1 for p in per_item if p.get(f"hit@{k}")) / total, 3)
           for k in k_values},
        "mrr": round(mrr, 3),
    }
    return summary, per_item


# ======================================================================
# 3. LLM-JUDGED ANSWER QUALITY (Document Analyst end-to-end)
# ======================================================================
DOC_SYSTEM_PROMPT = """
You are a helpful document question-answering assistant.

Your job is to analyse the uploaded PDF, notes, and other documents
and answer the user's questions using the retrieved document context.

Rules:
1. Answer using only the information provided in the context.
2. Do not invent facts or use outside knowledge to fill missing information.
3. If the context does not contain the answer, clearly say that you
   could not find the answer in the uploaded document.
4. Keep the answer clear, relevant, and easy to understand.
5. Use the page information included in the context when mentioning sources.
"""

JUDGE_PROMPT = """
You are a strict evaluator for a retrieval-augmented document assistant.

Document context given to the assistant:
---
{context}
---

Question: {question}
Assistant's answer: {answer}

Score with this rubric and reply with ONLY a single JSON object:
{{"grounded": true/false,            # every factual claim in the answer is supported by the context
  "page_cited": true/false,          # the answer or context trace cites a page number
  "out_of_context": true/false,      # the answer introduces information NOT present in the context
  "refused": true/false}}            # the assistant explicitly declined because the context lacks the answer
"""


def _invoke_json(llm, prompt_text: str) -> dict:
    """Call the LLM and parse the first JSON object in the response."""
    from langchain_core.messages import HumanMessage
    resp = llm.invoke([HumanMessage(content=prompt_text)])
    match = re.search(r"\{.*\}", resp.content, flags=re.DOTALL)
    if not match:
        return {}
    try:
        return json.loads(match.group(0))
    except json.JSONDecodeError:
        return {}


def evaluate_answers(db, llm, deadline=None):
    """Run the Document Analyst chain on every golden QA and judge the output."""
    results = []
    for item in GOLDEN_QA:
        if deadline and time.time() > deadline:
            results.append({"id": item["id"], "error": "skipped (time budget spent)"})
            continue
        try:
            docs = db.similarity_search(item["question"], k=RETRIEVAL_K)
            context = "\n\n".join(
                f"Page: {d.metadata.get('page', 'Unknown')}\nContent: {d.page_content}"
                for d in docs)

            answer = llm.invoke([
                {"role": "system", "content": DOC_SYSTEM_PROMPT},
                {"role": "user",
                 "content": f"Context:\n{context}\n\nQuestion: {item['question']}"},
            ])
            answer_text = answer.content

            verdict = _invoke_json(llm, JUDGE_PROMPT
                                   .replace("{context}", context)
                                   .replace("{question}", item["question"])
                                   .replace("{answer}", answer_text))
            time.sleep(THROTTLE_SECONDS)

            row = {"id": item["id"], "type": item["type"], "verdict": verdict}

            if item["type"] == "must_refuse":
                lowered = answer_text.lower()
                refused = verdict.get("refused", False) or any(
                    re.search(p, lowered) for p in REFUSAL_PATTERNS)
                row["correct"] = bool(refused and not verdict.get("out_of_context", True))
            else:
                row["correct"] = bool(verdict.get("grounded", False)
                                      and not verdict.get("out_of_context", False))
        except Exception as exc:                      # never fabricate on failure
            row = {"id": item["id"], "error": str(exc)}
        results.append(row)

    scored = [r for r in results if "correct" in r]
    by_type = {}
    for r in scored:
        t = r["type"]
        by_type.setdefault(t, []).append(r["correct"])
    summary = {
        "n_scored": len(scored),
        "n_errors": len(results) - len(scored),
        "accuracy_overall": round(sum(sum(v) for v in by_type.values())
                                  / max(1, sum(len(v) for v in by_type.values())), 3),
        **{f"accuracy_{t}": round(sum(v) / len(v), 3) for t, v in by_type.items() if v},
    }
    return summary, results


# ======================================================================
# 4. PLANNER ROUTING ACCURACY
# ======================================================================
def evaluate_routing(llm, deadline=None):
    from langchain.tools import tool
    from langchain_core.messages import HumanMessage
    from langchain.agents import create_agent
    from langchain.agents.middleware import wrap_tool_call

    # Stub tools: routing is evaluated without spending real API quota.
    EXECUTED_TOOLS: list[str] = []

    @tool
    def _stub_doc(question: str) -> str:
        """Answers questions from the uploaded PDF document."""
        return "STUB: document chunks would be retrieved here."

    @tool
    def _stub_web(topic: str) -> str:
        """Performs web research on a topic."""
        return "STUB: web results would be fetched here."

    tools = [_stub_doc, _stub_web]

    @wrap_tool_call
    def _tag_tools(request, handler):
        EXECUTED_TOOLS.append(request.tool_call["name"])
        return handler(request)

    system_prompt = """
    You are a Planner Agent. Analyze the user's request and decide
    which tools to execute.

    Available tools:
    1. _stub_doc: Answers questions from the uploaded PDF document.
    2. _stub_web: Performs web research on a topic.

    Rules:
    - Use _stub_doc for anything about the uploaded PDF.
    - Use _stub_web for external research.
    - Use both if the request needs the PDF and external research.
    - Do not call unnecessary tools.
    - If no tool is required, just answer directly.
    """
    router = create_agent(model=llm, tools=tools, middleware=[_tag_tools],
                          system_prompt=system_prompt)

    rows, tool_hits = [], []
    for case in ROUTING_CASES:
        if deadline and time.time() > deadline:
            rows.append({"id": case["id"], "error": "skipped (time budget spent)"})
            continue
        EXECUTED_TOOLS.clear()
        try:
            router.invoke({"messages": [HumanMessage(content=case["question"])]})
        except Exception as exc:
            rows.append({"id": case["id"], "error": str(exc)})
            continue
        used = set()
        for name in EXECUTED_TOOLS:
            used.add("document_analyst_tool" if "doc" in name else "researcher_agent")
        correct = (not case["expect_none"] and used == case["expect_tools"]) or \
                  (case["expect_none"] and not used)
        tool_hits.append(correct)
        rows.append({"id": case["id"], "expected": sorted(case["expect_tools"]),
                     "used": sorted(used), "correct": correct})
        time.sleep(THROTTLE_SECONDS)

    summary = {"n_cases": len(tool_hits),
               "routing_accuracy": round(sum(tool_hits) / len(tool_hits), 3)} \
        if tool_hits else {"n_cases": 0, "routing_accuracy": None}
    return summary, rows


# ======================================================================
# 5. REPORT GENERATION
# ======================================================================
def write_reports(retrieval, answers, routing, index_stats, llm_used):
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    payload = {
        "generated_at": now,
        "chat_model": CHAT_MODEL,
        "embedding_model": EMBEDDING_MODEL_NAME,
        "llm_evaluation_run": llm_used,
        "index": index_stats,
        "retrieval": retrieval,
        "answer_quality": answers[0] if answers else None,
        "answer_details": answers[1] if answers else None,
        "routing": routing[0] if routing else None,
        "routing_details": routing[1] if routing else None,
    }
    out_dir = PROJECT_ROOT / "evaluation"
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "results.json").write_text(
        json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")

    r = retrieval or {}
    a = payload["answer_quality"] or {}
    rt = payload["routing"] or {}
    lines = [
        "# Aether â€” Evaluation Results",
        "",
        f"*Generated {now} Â· model `{CHAT_MODEL}` Â· embeddings `{EMBEDDING_MODEL_NAME}` Â· "
        f"{index_stats.get('pages', '?')} pages â†’ {index_stats.get('chunks', '?')} chunks â†’ "
        f"{index_stats.get('vectors', '?')} vectors*",
        "",
        "| Metric | Value | What it means |",
        "|---|---|---|",
        f"| Retrieval Hit@1 | **{r.get('hit@1', 'â€”')}** | answer found fully inside the single best chunk |",
        f"| Retrieval Hit@4 | **{r.get('hit@4', 'â€”')}** | answer inside any of the 4 chunks actually used |",
        f"| MRR | **{r.get('mrr', 'â€”')}** | mean reciprocal rank over {r.get('n_items', 0)} questions |",
        f"| Grounded-accuracy (LLM judge) | **{a.get('accuracy_overall', 'â€”')}** "
        f"({a.get('n_scored', 0)} scored, {a.get('n_errors', 0)} errors) | "
        "answer fully supported by the retrieved context, judged by a strict LLM rubric |",
        f"| Gatekeeper accuracy (must-refuse) | **{a.get('accuracy_must_refuse', 'â€”')}** | "
        "out-of-document questions were refused instead of hallucinated |",
        f"| Planner routing accuracy | **{rt.get('routing_accuracy', 'â€”')}** "
        f"({rt.get('n_cases', 0)} cases) | the planner called exactly the right tools |",
        "",
        "The full run is reproducible: `python evaluation/evaluate.py` "
        "(add `--fast` for retrieval metrics without API cost).",
    ]
    (PROJECT_ROOT / "evaluation" / "RESULTS.md").write_text(
        "\n".join(lines), encoding="utf-8")
    print("Reports written to evaluation/results.json and evaluation/RESULTS.md")


# ======================================================================
# MAIN
# ======================================================================
def main():
    parser = argparse.ArgumentParser(description="Aether evaluation harness")
    parser.add_argument("--fast", action="store_true",
                        help="retrieval metrics only (no LLM calls)")
    args = parser.parse_args()

    if not PDF_PATH.exists():
        sys.exit(f"Sample PDF not found at {PDF_PATH}")

    print(f"[1/4] Building index from {PDF_PATH.name} ...")
    db, index_stats = build_index(PDF_PATH)
    print(f"      pages={index_stats['pages']}  chunks={index_stats['chunks']}  "
          f"vectors={index_stats['vectors']}")

    print("[2/4] Evaluating retrieval ...")
    retrieval, _ = evaluate_retrieval(db, GOLDEN_QA)
    print(f"      hit@1={retrieval['hit@1']}  hit@4={retrieval['hit@4']}  mrr={retrieval['mrr']}")

    answers, routing = None, None
    llm_used = False
    if not args.fast:
        from langchain_groq import ChatGroq
        deadline = time.time() + TIME_BUDGET_SECONDS
        llm = ChatGroq(model=CHAT_MODEL,
                       api_key=os.getenv("GROQ_API_KEY"),
                       temperature=0)

        print("[3/4] Judging Document Analyst answers (LLM-as-judge) ...")
        answers = evaluate_answers(db, llm, deadline=deadline)
        print(f"      overall={answers[0]['accuracy_overall']}  must_refuse="
              f"{answers[0].get('accuracy_must_refuse', 'n/a')}")

        print("[4/4] Evaluating planner routing ...")
        routing = evaluate_routing(llm, deadline=deadline)
        print(f"      routing accuracy={routing[0]['routing_accuracy']}")
        llm_used = True

    write_reports(retrieval, answers, routing, index_stats, llm_used)
    print("Done.")


if __name__ == "__main__":
    main()
