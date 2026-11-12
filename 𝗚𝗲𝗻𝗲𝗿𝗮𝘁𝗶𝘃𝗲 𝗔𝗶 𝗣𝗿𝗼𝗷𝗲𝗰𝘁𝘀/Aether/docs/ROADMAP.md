# Aether Roadmap

What is known to be imperfect in v1.0, how to fix it, and where the project can go next. Everything marked **Source** comes from the evaluation in [`test_results.md`](test_results.md).

## 1. Priority overview

| ID | Item | Type | Priority | Effort | Source |
|---|---|---|:---:|:---:|---|
| R1 | Time-sensitive questions must always use the Researcher | Bug fix | 🔴 V1.1 | S | Test 09 |
| R2 | Writer keeps inline page citations and lists web URLs under Sources | Bug fix | 🔴 V1.1 | S | Test 01 |
| R3 | Retry with backoff on Groq `429` | Reliability | 🟡 V2 | S | Test 15 |
| R4 | Stop `<br>` tags leaking into tables | Cosmetic | 🟡 V2 | S | Tests 06, 10 |
| R5 | Conversation memory for the Planner | Feature | 🟡 V2 | M | Known limitation |
| R6 | Persistent chat history | Feature | 🟡 V2 | M | Known limitation |
| R7 | Working model selector (or remove it) | UX | 🟡 V2 | S | Known limitation |
| R8 | More precise page citations | Quality | 🟢 Later | M | Observation |
| R9 | Multiple PDFs | Feature | 🟢 Later | M | Backlog |
| R10 | OCR for scanned PDFs | Feature | 🟢 Later | M | Backlog |
| R11 | Automated evaluation and tests | Engineering | 🟢 Later | L | Backlog |
| R12 | CI, docker-compose, observability | Engineering | 🟢 Later | M | Backlog |

Effort: S = under an hour, M = a few hours, L = a day or more.

The code below follows the same style as the rest of the project: small steps, plain names and a comment on every step. Treat each snippet as a starting point and test it with the matching question from [`demo_questions.md`](demo_questions.md).

---

## 2. V1.1: ship blockers

### R1. Time-sensitive questions must use the Researcher

**Problem.** For "Who won the most recent FIFA World Cup?" the Planner answered from stale memory because its prompt allows "If no tool is required, answer accordingly".

**Fix.** Give the Planner today's date and a hard rule. In `app.py`:

```python
# 1. Add this import at the top of the file, with the other imports
from datetime import date
```

```python
# 2. Inside build_planner_agent(), after `rules` has been set (both the PDF and no-PDF cases)

    # Today's date, so the model knows its own memory may be out of date
    today = date.today().strftime("%d %B %Y")

    # A hard rule: anything that can change over time must be searched
    time_rule = (
        "\n    - If the question is about anything current, latest, recent, today, "
        "or any fact that can change over time, you MUST call researcher_agent first. "
        "Never answer these from memory."
    )
    rules = rules + time_rule
```

```python
# 3. In the system_prompt of create_agent(...), add one line under "You are a Planner Agent."
    You are a Planner Agent.
    Today's date is {today}.
```

**Test.** Re-run questions 09 (World Cup), 10 (Python version) and 13 (OpenAI CEO). All three should now show *Researcher* as the tool used.

### R2. Keep inline page citations and web sources

**Problem.** In Test 01 the Writer dropped the page citation. The app already appends a **Sources** line for retrieved pages, but the Writer text itself does not reliably keep inline references.

**Fix.** Add two rules to the Writer's system prompt (`writer_prompt` in `app.py`), next to the existing rules:

```python
            - Keep page references from the Planner output (for example "Page 2") next to the facts they support.
            - If the Planner output contains web URLs, list them under a "Sources" heading at the end.
```

**Test.** Re-run question 01 and a web question such as 11. The answer should mention the page for the PDF fact, and web answers should end with their links.

---

## 3. V2: reliability and usability

### R3. Retry with backoff on rate limits

**Problem.** Groq's free tier limits tokens per minute. Four LLM calls per question can hit the limit when you ask quickly.

**Fix.** Wrap the call in a small retry helper. Add it above the submit handler in `app.py`:

```python
import time   # add at the top of the file


def run_with_retry(user_input, max_tries=3):
    """Run the agents again if Groq says we are going too fast (HTTP 429)."""

    for attempt in range(1, max_tries + 1):
        try:
            # Normal path: just run the agents
            return run_multi_agent(user_input)

        except Exception as error:
            is_rate_limit = "429" in str(error)
            is_last_try = attempt == max_tries

            if is_rate_limit and not is_last_try:
                # Wait a little longer each time: 10 s, then 20 s
                wait_seconds = 10 * attempt
                st.write(f"Rate limit reached. Trying again in {wait_seconds} seconds...")
                time.sleep(wait_seconds)
            else:
                # Not a rate limit, or no tries left: let the normal error message appear
                raise
```

Then, in the submit handler, change `run_multi_agent(user_input.strip())` to `run_with_retry(user_input.strip())`.

### R4. `<br>` tags inside tables

Add one rule to the Writer prompt: `- Never use HTML tags such as <br> inside tables. Use plain text.`

### R5. Conversation memory for the Planner

**Problem.** The Planner receives only the current question, so "explain that more simply" has nothing to refer to.

**Fix.** Pass the last few messages. Keep the number small, because more tokens make rate limits (R3) more likely.

```python
from langchain_core.messages import AIMessage   # add next to the HumanMessage import


def build_history_messages(chat, limit=6):
    """Turn the last few chat messages into LangChain messages."""

    history = []

    # chat["messages"][:-1] leaves out the question we are about to ask,
    # because the submit handler has already saved it in the chat
    for message in chat["messages"][:-1][-limit:]:
        if message["role"] == "user":
            history.append(HumanMessage(content=message["content"]))
        else:
            history.append(AIMessage(content=message["content"]))

    return history
```

In `run_multi_agent`, build the message list as `history + [HumanMessage(content=user_input)]` and pass it to `planner_agent.invoke({"messages": ...})`.

### R6. Persistent chat history

Replace `st.session_state.chats` reads and writes with a small SQLite table (`chats`, `messages`) using Python's built-in `sqlite3`. Keep the session state as a cache. Decide first whether storing conversations on disk is acceptable for your privacy story; v1.0 stores nothing on disk by design.

### R7. Model selector

The selector currently lists one model, so it does nothing. Either remove it, or add a second Groq model to the list and build `llm` from `selected_model`. Note that `llm` is currently created before the selector is drawn, so the order of the code needs to change.

---

## 4. Later: quality and features

### R8. More precise page citations

On a 4-page document with `k = 4`, the Sources line often lists every page. Use `similarity_search_with_score` and keep only chunks under a distance threshold, or reduce `k` for short documents.

### R9. Multiple PDFs

Keep a dictionary of `{file name: FAISS index}` in `session_state`, let the uploader accept multiple files, and either merge the indexes (`merge_from`) or let the Planner choose which document to search. Store the file name in each chunk's metadata, which the code already does with `source`.

### R10. OCR for scanned PDFs

When no text is extractable, offer an OCR path (for example render pages to images and run Tesseract) instead of only showing an error.

### R11. Automated evaluation and tests

| Layer | Idea |
|---|---|
| **Unit tests (pytest)** | Test pure functions: chat creation, signature logic, chunk counts for the sample PDF |
| **Retrieval evaluation** | For the 8 PDF questions, assert that the expected page is among the retrieved chunks |
| **Answer evaluation** | RAGAS or LangSmith evaluators for faithfulness and answer relevance |
| **Regression set** | Turn `demo_questions.md` into a JSON file of question, expected tool, expected page; run it after every change |

### R12. Engineering polish

- **GitHub Actions** workflow: install dependencies, run lint and tests on every push.
- **docker-compose.yml** for one-command start (see [`SETUP_AND_DEPLOYMENT.md`](SETUP_AND_DEPLOYMENT.md)).
- **Observability**: LangSmith tracing to see each agent step, token use and latency.
- **Streaming**: show the answer as it is written.
- **Authentication** if the app is ever shared beyond a demo.

---

## 5. Suggested release plan

| Release | Contents | Done when |
|---|---|---|
| **v1.0** | Current version, 18/19 tests passing | Tagged in Git |
| **v1.1** | R1, R2, R4 | Test 09 and Test 01 pass; re-run all 19 and update `test_results.md` |
| **v1.2** | R3, R7 | No raw `429` error in normal use |
| **v2.0** | R5, R6, R8 | Follow-up questions work; chats survive a refresh |
| **v2.x** | R9 to R12 | Automated regression set runs in CI |

Tip: every time you fix an item, add a short "Fix applied" note to the matching failure in `test_results.md` and re-run the affected tests, so the report shows the improvement honestly (for example 18/19 to 19/19).
