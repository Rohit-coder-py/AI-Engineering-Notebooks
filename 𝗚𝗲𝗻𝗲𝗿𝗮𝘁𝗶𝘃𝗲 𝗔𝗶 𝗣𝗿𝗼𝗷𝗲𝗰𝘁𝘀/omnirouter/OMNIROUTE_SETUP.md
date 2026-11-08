# OmniRoute + Aether — Setup Reference (created 08 Nov 2026)

Poora system ek hi jagah. Kabhi reset/shutdown ho jaye to Section 4 follow karo.

---

## 1. Kya hai ye?

- **OmniRoute** = self-hosted AI gateway (`localhost:20128`), OpenAI-compatible API
- LangChain code sirf OmniRoute se baat karta hai → OmniRoute sipare provider (Groq/Gemini/Mistral)
- Benefit: model switch = sirf string change; free-tier stacking; auto-fallback; usage tracking

## 2. Fixed credentials (yaad rakhne layak)

| Cheez | Value | Kahin hai |
|---|---|---|
| Dashboard password | `Omni-O8YUCR6U71sNgpwsVUoMoUrc` | DB me persisted (`.env` ka INITIAL_PASSWORD ab ignored) |
| OmniRoute API key | `sk-a8b8e46740913dbf-92da87-c9c4b86a` | DB me persisted; aapke omnirouter/.env me bhi |
| Server port | `20128` | API base: `http://localhost:20128/v1` |
| Connected providers | Groq + Gemini + Mistral | DB me persisted, re-add nahi karna |

## 3. Best free models (live-[IDEA]verified IDs — assume mat karo, refresh karo)

- Chat: `groq/openai/gpt-oss-120b` / `gemini/gemini-3.8-flash` / `mistral/mistral-small-latest`
- Code: `mistral/codestral-latest` / `groq/qwen/qwen3.6-27b`
- Embeddings (RAG): `gemini/gemini-embedding-2` (3072-d) ya `mistral/mistral-embed`
- Speech STT: `groq/whisper-large-v3`
- Auto Routing: `auto/chat`, `auto/best-free`, `auto/coding:free`
- Fresh list: `GET /v1/models?free=true` (Bearer = aapki sk- key)

## 4. RESTART PROCEDURE (shutdown ke baad) — 3 steps only

```
1) Server start:  npm.cmd run dev     (folder: ...\useful_repos\OmniRoute)
                  ya double-click:    ...\useful_repos\0-Launch OmniRoute.bat
2) Wait:          http://localhost:20128 khul jaye (~30-60s)
3) Run code:      py chatbot.py       (folder: ...\omnirouter)
```

Keys/password/providers sab SQLite me persist hain — **re-setup ki zarurat nahi.**

## 5. Troubleshooting table

| Problem | Fix |
|---|---|
| 401 Unauthorized | `.env` me OMNIROUTE_API_KEY update karo (new key: dashboard→API Keys) |
| 502 / "no eligible" | Model change karo (groq/gemini… try karo) ya `auto` use karo |
| Dashboard password bhool gaye | `cd OmniRoute` → `node bin\reset-password.mjs` |
| naya machine / node_modules gayab | `cd OmniRoute` → `npm.cmd install` (ek baar) |
| Provider quota khatam | Dashboard → Providers → check health; Gemini/Groq/Mistral rotate yourselves |

## 6. Minimal code pattern (Aether me use karna)

```python
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

load_dotenv()

llm = ChatOpenAI(
    model="groq/openai/gpt-oss-120b",     # ya auto/chat
    api_key=os.getenv("OMNIROUTE_API_KEY"),
    base_url=os.getenv("OMNIROUTE_BASE_URL"),   # http://localhost:20128/v1
    temperature=0.7,
)

print(llm.invoke("your prompt").content)
```

Ek hi `ChatOpenAI` import sab providers chala dega — provider-specific SDK ki zarurat nahi.

## 7. Pending (jab mauka mile)

- Phase 5: OmniRoute ko Streamlit Cloud se alag host karna (VPS/Docker/tunnel,
  REQUIRE_API_KEY=true, HTTPS, .env secrets) — guidance ready hai jab bolo
- Streaming test: `for chunk in llm.stream("..."): print(chunk.content, end="")`
- Tool-calling test: `llm.bind_tools([...])`
- Support docs: `OmniRoute/docs/reference/OPENAI_COMPATIBILITY.md`, `FREE_TIERS.md`

*Keys confidential — in files ko upload/share mat karna (public repo nahi).*
