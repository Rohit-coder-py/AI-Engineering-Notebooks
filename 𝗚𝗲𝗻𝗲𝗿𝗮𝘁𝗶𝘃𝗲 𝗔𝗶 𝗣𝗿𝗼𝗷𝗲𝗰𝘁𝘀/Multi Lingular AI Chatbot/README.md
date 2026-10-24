<div align="center">

<img src="assets/logo.svg" width="96" alt="Bolo AI logo">

# Bolo AI — Multilingual Chatbot

**Talk in English, हिन्दी or Hinglish — the bot replies in your language.**

![Python](https://img.shields.io/badge/Python-3.10%2B-4F46E5?style=flat-square)
![Streamlit](https://img.shields.io/badge/Streamlit-UI-4F46E5?style=flat-square)
![LangChain](https://img.shields.io/badge/LangChain-Groq-4F46E5?style=flat-square)

### 🔗 [Live App](#) &nbsp;·&nbsp; *add your deployed link here*

</div>

---

## Preview

<p align="center">
  <img src="preview/01_home.png" width="88%" alt="Home screen">
</p>

<p align="center">
  <img src="preview/03_auto_language_chat.png" width="88%" alt="Auto language chat: English, Hindi and Hinglish in one conversation">
</p>

<table>
  <tr>
    <td width="62%"><img src="preview/02_english.png" alt="English reply"></td>
    <td width="38%"><img src="preview/04_mobile.png" alt="Mobile view"></td>
  </tr>
  <tr>
    <td align="center"><sub>Desktop</sub></td>
    <td align="center"><sub>Mobile</sub></td>
  </tr>
</table>

## Features

- **Auto language reply** — write in English, Hindi (देवनागरी) or Hinglish and get a reply in the same language
- **Language override** — force English / Hindi / Hinglish from the sidebar
- **Language badge** — every message shows what language was detected
- **Chat memory** — the bot remembers the whole conversation
- **Creativity slider** — control the model's temperature
- **Clear chat** button, clean minimal UI, works on mobile

## Tech stack

| Part | Tool |
|---|---|
| UI | Streamlit |
| LLM | Groq — `openai/gpt-oss-20b` via `langchain-groq` |
| Prompting | LangChain `ChatPromptTemplate` |
| Memory | `HumanMessage` / `AIMessage` list in `st.session_state` |
| Config | `python-dotenv` |

## How it works

```
User message
   │
   ▼
detect_language()  ── Devanagari? → Hindi │ Roman-Hindi words? → Hinglish │ else English
   │
   ▼
ChatPromptTemplate  ── fills {language_rule} (Auto, or the language picked in the sidebar)
   │
   ▼
System prompt + full chat history  ──►  ChatGroq  ──►  Reply in the same language
```

## Run locally

```bash
# 1. install
pip install -r requirements.txt

# 2. add your key (copy .env.example to .env)
GROQ_API_KEY=your_groq_api_key_here

# 3. run
streamlit run app.py
```

Get a free Groq key at [console.groq.com](https://console.groq.com).

## Project structure

```
├── app.py               # the whole app (UI + logic)
├── assets/              # logo (svg + png)
├── preview/             # screenshots used in this README
├── .streamlit/config.toml   # light theme
├── requirements.txt
├── .env.example         # copy to .env
└── .gitignore           # keeps .env out of GitHub
```

> ⚠️ Never upload your real `.env` to GitHub. It is already listed in `.gitignore`.

## Ideas to extend

- Add more languages (Marathi, Bengali, ...) in `language_rules`
- Stream the reply token by token
- Save and load past chats
