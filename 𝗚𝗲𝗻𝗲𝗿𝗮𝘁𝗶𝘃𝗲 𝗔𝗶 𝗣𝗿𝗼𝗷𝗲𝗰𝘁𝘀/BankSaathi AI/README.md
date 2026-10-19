<div align="center">

<img src="assests/logo.jpg" alt="BankSaathi AI logo" width="220"/>

# BankSaathi AI

### Your banking companion, in your language.

**Understand everyday banking. Learn safer habits. Recognise suspicious messages.**

<p>
  <a href="https://banksaathi-ai-gen-ai.streamlit.app/"><img src="https://img.shields.io/badge/🚀%20Live%20Demo-Open%20App-FF4B4B?style=for-the-badge" alt="Live demo"/></a>
  <a href="https://github.com/Rohit-coder-py/BankSaathi-AI"><img src="https://img.shields.io/badge/GitHub-Source%20Code-181717?style=for-the-badge&logo=github" alt="Source code"/></a>
</p>

<p>
  <img src="https://img.shields.io/badge/Python-3.x-3776AB?style=flat-square&logo=python&logoColor=white" alt="Python"/>
  <img src="https://img.shields.io/badge/Streamlit-Web%20UI-FF4B4B?style=flat-square&logo=streamlit&logoColor=white" alt="Streamlit"/>
  <img src="https://img.shields.io/badge/LangChain-LLM%20Orchestration-1C3C3C?style=flat-square" alt="LangChain"/>
  <img src="https://img.shields.io/badge/Groq-Inference-F55036?style=flat-square" alt="Groq"/>
  <img src="https://img.shields.io/badge/Pydantic-Structured%20Output-E92063?style=flat-square&logo=pydantic&logoColor=white" alt="Pydantic"/>
  <img src="https://img.shields.io/badge/Languages-Hindi%20%7C%20English%20%7C%20Hinglish-6C5CE7?style=flat-square" alt="Supported languages"/>
</p>

</div>

---

## What is BankSaathi AI?

**BankSaathi AI is an educational, AI-powered banking information assistant for everyday banking questions in India.** Users can ask questions in Hindi, English, or Hinglish and explore banking concepts through three tools: a conversational assistant, a banking-term explainer, and a suspicious-message checker.

The goal is to make banking language easier to understand and encourage safer digital-banking habits—not to replace a bank, financial professional, or official fraud-reporting channel.

## Try the live app

**[Open BankSaathi AI](https://banksaathi-ai-gen-ai.streamlit.app/)**

> The live app requires its Groq API key to be configured in Streamlit Community Cloud Secrets. If the demo is temporarily unavailable, you can run the project locally using the instructions below.

## Who is it for?

| Audience | How it can help |
|---|---|
| People new to digital banking | Learn concepts such as UPI, ATM cards, NEFT, RTGS, and IMPS in simpler language. |
| Hindi and Hinglish speakers | Ask questions naturally without needing to phrase everything in formal English. |
| Students and self-learners | Explore banking vocabulary, examples, and basic safety practices. |
| Anyone who receives a suspicious message | Review possible red flags in an SMS, WhatsApp message, or similar text before taking action. |
| Developers learning GenAI | Study a small practical project using an LLM, prompts, structured output, session state, and a web UI. |

## Why use it?

- **Language that feels familiar:** choose Hindi, English, Hinglish, or automatic language matching.
- **Adjustable explanations:** switch between simple and more detailed answers.
- **Three focused tools:** chat about banking, understand a banking term, or inspect a suspicious message.
- **Structured responses:** the term explainer and scam checker use Pydantic models to organise AI output.
- **Safety-minded design:** a local pre-check attempts to block messages that appear to contain sensitive details before they are sent to the model.
- **Practical learning project:** demonstrates how several GenAI components can work together in a Streamlit app.

## Features

### 💬 1. Chat with BankSaathi

Ask general questions about everyday banking and payments. Conversation history is maintained in the current Streamlit session, and the app keeps a bounded number of recent messages.

Example prompts:
- “What is UPI and how does it work?”
- “UPI PIN kya hota hai?”
- “NEFT, RTGS aur IMPS mein kya difference hai?”
- “How can I find my bank statement safely?”

### 📖 2. Banking Term Explainer

Enter a term such as **UPI, EMI, KYC, IFSC, NEFT, RTGS, or debit card** to request a structured explanation, including fields such as:
- Simple meaning and Hindi meaning
- Category
- Real-life example
- How it works
- Safety tip
- Related terms

The output depends on the model response; always verify important or time-sensitive details with official sources.

### 🛡️ 3. Scam Message Checker

Paste a suspicious message to receive an AI-generated assessment with:
- A **Low / Medium / High** risk label
- Possible scam type
- Potential red flags
- Suggested next steps

This is a preliminary educational assessment, **not a definitive fraud detector**. A message marked “Low” may still be malicious, and a “High” result is not proof by itself.

---

## Safety and privacy

> **Never enter your OTP, UPI PIN, ATM PIN, password, CVV, or full card details into a chatbot.**

BankSaathi AI is an independent learning project. It is **not affiliated with or endorsed by any bank, the RBI, NPCI, or a government agency**.

- The app cannot access bank accounts, check balances, verify transactions, transfer money, or block cards.
- The sensitive-information pre-check uses simple rules and is not guaranteed to catch every secret or sensitive value. Do not rely on it as a security boundary.
- AI responses can be inaccurate, incomplete, or out of date. Fees, limits, timings, and bank policies can change.
- Do not paste private customer information or complete messages containing personal data.
- For account-specific help, contact your bank through its official app, website, branch, or verified support channel.
- If you suspect financial cyber fraud in India, contact your bank promptly and use the official [National Cyber Crime Reporting Portal](https://cybercrime.gov.in/) or call **1930** where applicable.

## Technology stack

| Technology | Role in this project |
|---|---|
| [Python](https://www.python.org/) | Application logic and data handling |
| [Streamlit](https://streamlit.io/) | Interactive web interface, sidebar controls, chat UI, and session state |
| [LangChain](https://www.langchain.com/) | Chat-model integration, prompt templates, and output parsing |
| [Groq](https://groq.com/) | Hosted model inference through `langchain-groq` |
| [Pydantic](https://docs.pydantic.dev/) | Typed schemas for banking-term explanations and scam-check results |
| [python-dotenv](https://pypi.org/project/python-dotenv/) | Loads local environment variables from `.env` during development |

### Under the hood

1. The user selects a tool and enters a question or message.
2. For chat, the app builds a system prompt using the chosen language and explanation level, then sends the recent conversation to the model.
3. For the term explainer or scam checker, a prompt requests fields described by a Pydantic schema.
4. `PydanticOutputParser` parses the model response into structured data.
5. Streamlit renders the result in the browser.

## Run locally

### Prerequisites

- Python 3.10 or newer recommended
- A [Groq API key](https://console.groq.com/keys)
- Git (optional, for cloning the repository)

### 1. Clone the repository

```bash
git clone https://github.com/Rohit-coder-py/BankSaathi-AI.git
cd BankSaathi-AI
```

### 2. Create and activate a virtual environment

**Windows (PowerShell):**

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

**macOS / Linux:**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Configure your API key

Create a file named `.env` in the project root:

```dotenv
GROQ_API_KEY=your_actual_groq_api_key
```

Replace the placeholder with your own key. **Never commit `.env` or publish your API key.** The `.gitignore` file excludes `.env`.

### 5. Start the app

Run this command from the repository root:

```bash
streamlit run app/app.py
```

Streamlit will print a local URL, usually `http://localhost:8501`.

## Deploy on Streamlit Community Cloud

1. Push the project to a GitHub repository.
2. Open [Streamlit Community Cloud](https://share.streamlit.io/).
3. Create or select the app and set the entrypoint to `app/app.py`.
4. In the app settings, add the secret below under **Secrets**:

```toml
GROQ_API_KEY = "your_actual_groq_api_key"
```

5. Save the secret and reboot the app if needed.

Do not upload your local `.env` file to GitHub or paste API keys into code, screenshots, issues, or README files.

## Project structure

```text
BankSaathi-AI/
├── .streamlit/
│   └── config.toml       # Streamlit configuration
├── app/
│   └── app.py            # UI, prompts, model calls, parsers, safety checks
├── assests/
│   ├── logo.jpg          # Project logo
│   └── logo_small.jpg    # Small logo used by the app
├── .gitignore
├── README.md
└── requirements.txt
```

> Note: The current repository uses the folder name `assests` (rather than the usual spelling `assets`). Keep that spelling consistent unless you also update the paths in the application code.

## Configuration

The app currently uses the Groq model identifier `openai/gpt-oss-20b`. Model availability and provider policies may change over time. If you change the model, check the provider's current model documentation and ensure the configured account has access.

The app reads `GROQ_API_KEY` from the environment. Locally, `python-dotenv` loads it from `.env`; in Streamlit Community Cloud, configure it through the app's Secrets settings.

## Limitations

- Responses are generated by an AI model and may be incorrect or misleading.
- Scam assessments are heuristic guidance, not a guarantee of safety or a replacement for professional investigation.
- The application does not connect to banking systems or verify transactions.
- Model calls require a working network connection and a valid provider API key.
- The current sensitive-information filter is a basic rule-based check and can miss some formats.
- Banking fees, limits, settlement times, and rules vary; consult your bank and official sources.

## Roadmap ideas

- Add automated tests for sensitive-input handling and structured-output parsing.
- Improve redaction and input validation, with clear privacy guidance.
- Add a small suite of verified banking FAQs and citations to official sources.
- Add clearer error messages for API configuration, rate limits, and model failures.
- Improve accessibility and add representative screenshots of each feature.

## Contributing

Suggestions and bug reports are welcome. If you open an issue, **do not include API keys, OTPs, PINs, account details, or private banking messages**. For code changes, create a branch and submit a pull request with a concise explanation of the change.

## Author

**Rohit Jha**  
GitHub: [@Rohit-coder-py](https://github.com/Rohit-coder-py)

- **Live app:** [BankSaathi AI](https://banksaathi-ai-gen-ai.streamlit.app/)
- **Source code:** [BankSaathi-AI on GitHub](https://github.com/Rohit-coder-py/BankSaathi-AI)

---

<div align="center">

**BankSaathi AI — Banking guidance that speaks your language.**

Built as an educational Generative AI project.

</div>
