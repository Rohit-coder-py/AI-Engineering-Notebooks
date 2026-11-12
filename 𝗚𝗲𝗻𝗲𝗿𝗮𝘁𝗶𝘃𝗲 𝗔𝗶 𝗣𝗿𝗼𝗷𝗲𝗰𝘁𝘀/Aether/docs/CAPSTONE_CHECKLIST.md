# Capstone Checklist and Presentation Kit

A practical guide for turning Aether from a working project into a finished capstone: what to deliver, how it maps to typical evaluation criteria, how to present it and how to answer questions about it.

> Capstone formats differ between institutions. Check the format your guide or study centre asks for, and treat this file as the engineering half of that submission.

## 1. Deliverables checklist

### Done

- [x] Working application: chat page, About page, custom theme
- [x] Clean repository: `requirements.txt`, `env.example`, `.gitignore`, `.dockerignore`
- [x] Dockerfile with CPU-only PyTorch, baked-in model, non-root user and health check
- [x] README with architecture, quick start and results
- [x] Architecture document with diagrams
- [x] Project report draft ([`PROJECT_REPORT.md`](PROJECT_REPORT.md))
- [x] Test plan, 19 test cases, results and failure analysis ([`test_results.md`](test_results.md))
- [x] Screen recording of the test run ([`manual_testing.mp4`](manual_testing.mp4))
- [x] Sample document for reviewers (`sample_data/Intro_to_LLMs.pdf`)
- [x] Setup and deployment guide

### To do before submission

| Done | Task | Where / how |
|:---:|---|---|
| ⬜ | **Rotate your API keys** and make sure `.env` is not in the repo or in any zip you share | [`SETUP_AND_DEPLOYMENT.md`](SETUP_AND_DEPLOYMENT.md), section 7 |
| ⬜ | Fix the two ship blockers (R1, R2) and re-run all 19 tests | [`ROADMAP.md`](ROADMAP.md), section 2 |
| ⬜ | Update `test_results.md` with "Fix applied" notes and the new pass rate | Honest before/after is stronger than a perfect score |
| ⬜ | Push the Docker image and add the Docker Hub link | `REPLACE-WITH-YOUR-DOCKER-HUB-LINK` in README and report |
| ⬜ | Deploy the app and add the live link | `REPLACE-WITH-YOUR-LIVE-LINK` in README and report |
| ⬜ | Replace the five placeholder screenshots with real ones | [`../preview/README.md`](../preview/README.md) |
| ⬜ | Fill in your name, enrolment number and guide in the report | Top of `PROJECT_REPORT.md` |
| ⬜ | Add a `LICENSE` file (MIT is a common choice for portfolio projects) | GitHub: Add file, then Create new file, then type `LICENSE` and pick a template |
| ⬜ | Tag the release | `git tag -a v1.0 -m "Aether v1.0" && git push --tags` |
| ⬜ | Export the report as PDF for submission | Open `PROJECT_REPORT.md` in VS Code or GitHub and print to PDF, or use Pandoc |
| ⬜ | Prepare slides | Section 4 below |
| ⬜ | Record a 2 to 3 minute demo video | Section 5 below |

Tip: search the whole repository for the text `REPLACE-WITH` to find every placeholder link.

## 2. Mapping to typical evaluation criteria

| Criterion | What reviewers look for | Evidence in this repository |
|---|---|---|
| **Problem definition** | A real problem and clear objectives | Report sections 2 and 3 |
| **Technical depth** | More than a tutorial copy | Multi-agent orchestration, RAG, tool-calling middleware, thread-safe state hand-off (`doc_store`) |
| **Design and architecture** | Reasoned structure and trade-offs | [`ARCHITECTURE.md`](ARCHITECTURE.md): diagrams and a design-decision table |
| **Code quality** | Readable, organised, configurable | Single-purpose functions, constants at the top, comments, themed helper module |
| **Testing and evaluation** | Evidence it works, and honesty about where it does not | 19 cases, verification method, failure analysis with root causes |
| **Documentation** | Others can run and understand it | README, setup guide, architecture, report, roadmap |
| **Deployment and reproducibility** | It runs somewhere other than your laptop | Dockerfile, Docker Hub image, live link |
| **User experience** | Usable and polished | Custom theme, live agent status, history, About page |
| **Security and ethics** | Responsible handling of keys and data | Keys via environment, `.dockerignore`, non-root container, privacy notes |
| **Originality and impact** | Your own decisions and improvements | Patchwork theme, dynamic tool list, code-appended sources, honest evaluation |
| **Communication** | Clear presentation and answers | Sections 4 to 6 below |

## 3. Make it stand out (pick two or three)

| Idea | Effort | Why it impresses |
|---|:---:|---|
| Fix Test 09 and Test 01, re-run, show **18/19 to 19/19** with the failure analysis kept | S | Shows the full engineering loop: measure, diagnose, fix, verify |
| Add a **retrieval hit-rate** check: for each PDF question, was the right page in the top 4? | M | Evaluates the retrieval step separately from the LLM |
| Show **latency and token use** per agent in the status panel | M | Real-world thinking about cost and speed |
| Add **pytest** tests and a **GitHub Actions** workflow with a green badge | M | Professional engineering habit |
| **Conversation memory** (R5) | M | Fixes the most visible limitation |
| Write a short **blog post or LinkedIn post** explaining one lesson (for example the `st.session_state` thread problem) | S | Communication skill and portfolio visibility |

## 4. Presentation outline (10 minutes, 12 slides)

| # | Slide | Key message | Time |
|---|---|---|:---:|
| 1 | Title | Aether, your AI workplace; your name | 0:20 |
| 2 | The problem | Chatbots: no access to your documents, stale facts, unverifiable answers | 0:50 |
| 3 | The idea | A small team of agents: Plan, Research, Read, Write | 0:50 |
| 4 | Demo preview | The GIF or screenshots from the README | 0:40 |
| 5 | Architecture | Show `architecture.svg` and walk one question through it | 1:10 |
| 6 | RAG pipeline | Six steps, with the real parameters (1000/150, 384-d, k=4) | 1:00 |
| 7 | Agents and prompts | Planner rules, document "context only" rule, Writer "add nothing" rule | 1:00 |
| 8 | Engineering challenges | Worker-thread state, dynamic tool list, re-index signature, Docker size | 1:00 |
| 9 | Testing | 19 tests, 18 passed, 0 hallucinations on trap questions; show `test-results.svg` | 1:00 |
| 10 | The failure | Test 09: what happened, root cause, the fix | 0:50 |
| 11 | Deployment, limits and roadmap | Docker, live link, what V2 adds | 0:50 |
| 12 | Learning and thanks | Skills gained; questions | 0:30 |

Presentation tips:

- Lead with the **problem**, not the technology.
- Show the failure on purpose. Reviewers trust a project that admits and explains its weaknesses.
- Use the animated SVGs from [`../preview/`](../preview/) as slide images (export to PNG, or present from the README in a browser).

## 5. Live demo script (about 4 minutes)

**Before you start (the day before and 10 minutes before)**

- [ ] Both API keys work; run one question to confirm.
- [ ] Wait at least a minute between questions: the free Groq tier limits tokens per minute, and a multi-agent question uses several calls.
- [ ] The embedding model is already downloaded (run the app once beforehand).
- [ ] Have `preview/demo.gif` or `docs/manual_testing.mp4` ready as a backup if the network fails.
- [ ] Browser zoom set so the chat bar and answers are readable on the projector.

**Script**

| Step | Action | What to say |
|---|---|---|
| 1 | Open the app, then the **About** page briefly | "Aether explains itself: a user view and a technical view." |
| 2 | Upload `Intro_to_LLMs.pdf`, open the "Document ready" panel | "4 pages become chunks and vectors, all in memory." |
| 3 | Ask question 03: *embedding and how many numbers does all-MiniLM-L6-v2 produce* | "Answered from page 2, 384 numbers. Note the Sources line." |
| 4 | Ask question 19: *author and publication date* | "The document does not say, and Aether does not invent it." |
| 5 | Ask question 10: *latest stable Python version* | "Now the Planner chooses the web Researcher, with source links." |
| 6 | Ask question 14: *what is RAG, then search the web for 2026 RAG news* | "Both tools in one question; the status panel shows the agents." |
| 7 | Open `test_results.md` or the results chart | "18 of 19 passed. One failure: here is why, and here is the fix." |

## 6. Viva and Q&A preparation

Short model answers based on this project. Put them in your own words.

**1. What is RAG and why did you use it?**
Retrieval-Augmented Generation: retrieve relevant passages from the user's document and put them in the prompt, so the model answers from evidence instead of memory. It reduces hallucination and lets me cite pages.

**2. Why several agents instead of one big prompt?**
Each role has a short, focused prompt that is easier to write, test and debug. The Planner decides what information is needed, the tools fetch it, and the Writer only formats it.

**3. Why separate a Planner and a Writer?**
Separation of concerns. The Planner is judged on choosing the right tools and keeping sources; the Writer is judged on clarity and is forbidden to add facts.

**4. What is an embedding, and why 384?**
A vector of numbers that captures meaning, so similar texts are close together. 384 is simply the output size of the `all-MiniLM-L6-v2` model.

**5. Why chunk size 1000 and overlap 150?**
Chunks must be small enough to be precise but large enough to keep an idea together. The overlap stops a sentence being cut at a border. These are tunable settings at the top of `app.py`.

**6. Why FAISS in memory instead of a vector database service?**
One PDF per session needs no server and no persistence, which also helps privacy. The trade-off is that nothing survives a restart and one session handles one document.

**7. How do you control hallucination?**
Context-only document prompt with a "say you could not find it" rule, low temperature (0.2), a Writer that must not add facts, and page numbers appended in code. In testing, 0 of 3 missing-information questions produced an invented answer.

**8. What happens when the PDF does not contain the answer?**
Tests 17 to 19 asked for GPT-4 parameters, a subscription price and the author. Aether said the information was not in the document each time.

**9. What failed in testing, and why?**
Test 09 (most recent FIFA World Cup): the Planner skipped the web search and answered from stale memory. The prompt allowed "if no tool is required, answer accordingly", so the model assumed it knew. The fix is a hard rule for time-sensitive questions plus today's date in the prompt.

**10. Why temperature 0.2?**
Factual question answering needs stable, repeatable wording, not creativity.

**11. Why the `doc_store` dictionary?**
Tools run in a worker thread where `st.session_state` is empty, so the vector index is passed through a plain dictionary that is set just before each run.

**12. How does the Planner decide between the PDF and the web?**
From its system prompt and the tool descriptions. The document tool is only offered when a PDF is loaded; the web tool is always available; for mixed questions it can call both.

**13. What data leaves the machine?**
Retrieved passages and the questions go to Groq for the LLM calls, and web queries go to Tavily. The PDF itself and its vectors stay in memory. Keys are read from environment variables and are not baked into the Docker image.

**14. Why Groq and `gpt-oss-20b`?**
Fast inference and a free tier suitable for a student project. The model name is one setting, so it is easy to change.

**15. Could this serve many users?**
Not as it is. State is per browser session in memory, and the free API tiers have rate limits. Scaling would need a persistent vector store, a database for chats, request queuing and paid API limits.

**16. How reliable is your evaluation?**
It is a careful manual evaluation on one short document with 19 cases, so it shows behaviour but is not a statistical benchmark. The next step is an automated regression set and RAGAS-style metrics.

**17. What would you build next?**
Fix R1 and R2, then add conversation memory, persistent history and automated evaluation. See [`ROADMAP.md`](ROADMAP.md).

## 7. Resume and LinkedIn lines

Adapt these, and keep the numbers honest (update them after you re-run the tests).

**Resume bullets**

- Built **Aether**, a multi-agent AI assistant (Planner, Researcher, Document Analyst, Writer) using LangChain 1.x, Groq and Streamlit that answers from a user's PDF and the live web in a single response.
- Implemented a **RAG pipeline** (pypdf, 1000/150 chunking, MiniLM embeddings, FAISS top-4) with page-level citations; achieved **0 hallucinations on 3 missing-information tests**.
- Designed and ran a **19-case end-to-end evaluation (94.7% pass rate)**, diagnosed the single failure to its root cause and documented the fix.
- Packaged the app with **Docker** (CPU-only PyTorch, baked-in model, non-root user, health check) and published it to Docker Hub.

**LinkedIn post starter**

> I built Aether, a small team of AI agents that reads your PDF, searches the live web and writes one clean answer. It passed 18 of 19 manual tests, and the one failure taught me the most: the model confidently answered a "latest" question from stale memory. Here is what I changed... (add live link, repo link and the GIF from `preview/demo.gif`)

## 8. Final pre-submission sweep

- [ ] The README images and animations all load (open the README on GitHub in a private window).
- [ ] Every link in the README and docs works, including the live and Docker Hub links.
- [ ] A friend can follow the Quick start on a clean machine and get the app running.
- [ ] The report PDF opens, shows the diagrams and has your details filled in.
- [ ] No keys, personal chats or private files appear anywhere in the repository history.
