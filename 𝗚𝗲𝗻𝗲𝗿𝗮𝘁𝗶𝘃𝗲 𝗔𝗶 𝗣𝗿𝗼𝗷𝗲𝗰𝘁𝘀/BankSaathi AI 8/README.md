# BankSaathi AI

Banking guidance that speaks your language (Hindi, English, Hinglish).
See `What is BankSaathi AI.md` for the project description.

## Features

| Page | What it does |
|---|---|
| 💬 Chat | Multilingual banking chatbot with memory, language + detail settings |
| 📖 Banking Term Explainer | Type a term (EMI, KYC, IFSC...) -> structured explanation in English + Hindi |
| 🛡️ Scam Message Checker | Paste a suspicious SMS/WhatsApp -> risk level, red flags, what to do |

Safety built in: private details (OTP, PIN, CVV, card numbers) are blocked **before** they reach the AI.

## Run it

```bash
pip install -r requirements.txt
cp .env.example .env        # then put your real GROQ_API_KEY inside .env
streamlit run app/app.py    # run this from the project folder
```

## Which lesson each part comes from

| In `app/app.py` | Your lesson |
|---|---|
| `ChatGroq(model, temperature, max_tokens)` | Chat models, temperature & max tokens |
| `ChatPromptTemplate` with `{format_instructions}` / `{term}` | Prompt templates |
| `SystemMessage`, `HumanMessage`, `AIMessage` + `history` list | Short-term memory with message roles |
| `history[-MAX_HISTORY_MESSAGES:]` | Fixing "memory keeps growing forever" |
| `BankingTerm`, `ScamCheck`, `PydanticOutputParser` | Structured output (EduSage AI v2) |
| `st.session_state`, `st.sidebar`, `st.chat_message`, `st.chat_input` | Streamlit chatbot UI (AI CHATBOT) |
| `.env` + `load_dotenv()` | API key handling |

## Safety rules

- Never commit `.env` to GitHub (it is already in `.gitignore`).
- This project gives general information only. It does not access any bank account.
