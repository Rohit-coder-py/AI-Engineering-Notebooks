# LinkedIn Post Automation (n8n + Gemini)

Paste a blog URL, get a ready-to-publish LinkedIn post. An AI automation workflow built with [n8n](https://n8n.io) and Google Gemini.

![Workflow overview](docs/images/workflow-overview.png)

## Features

- Simple web form: just enter a blog URL
- Fetches the article and extracts its text automatically
- Gemini writes a LinkedIn post with a hook, short paragraphs, a closing question and hashtags
- Prompt instructs the model not to invent facts
- Result is shown directly on the form's completion page

## How it works

```
Form (blog URL) -> HTTP Request -> HTML extract -> Gemini -> Form result
```

Full node-by-node breakdown: [docs/how-it-works.md](docs/how-it-works.md)

## Tech stack

| Tool | Purpose |
|------|---------|
| n8n | Workflow automation platform |
| Google Gemini API | Text generation |

## Getting started

### Prerequisites

- n8n (self-hosted via `npx n8n` / Docker, or n8n Cloud)
- A free Gemini API key from [Google AI Studio](https://aistudio.google.com/apikey)

### Setup

1. Clone this repo
   ```bash
   git clone https://github.com/<your-username>/linkedin-post-automation.git
   ```
2. Start n8n (local example)
   ```bash
   npx n8n
   ```
   Then open http://localhost:5678.
3. In n8n: **Workflows -> Import from File** and choose `workflows/linkedin-post-automation.json`.
4. Open the **Message a model** node and create a **Google Gemini(PaLM) API** credential with your API key.
5. Click **Execute workflow** (or publish it), open the form URL, paste a blog link and submit.

### Example

Input: `https://example.com/blog/ai-agents`

Output: a LinkedIn-style post with a hook, key insights, a question and 3-5 hashtags.

## Project structure

```
linkedin-post-automation/
├── workflows/
│   └── linkedin-post-automation.json   # n8n workflow export
├── docs/
│   ├── how-it-works.md
│   └── images/workflow-overview.png
├── .github/workflows/validate.yml      # JSON + secret check on every push
├── .env.example
├── .gitignore
├── LICENSE
└── README.md
```

## Security

The exported workflow contains **no API keys**. Your Gemini key lives only inside your own n8n credentials. Never commit `.env` files or credential exports.

## Roadmap

- [ ] Target only the article content (`article`/`main`) instead of the whole `body`
- [ ] Add a tone selector (professional, casual, storytelling) to the form
- [ ] Add a review/approve step, then auto-post via the LinkedIn API
- [ ] Error handling for broken URLs and empty pages
- [ ] Generate multiple post variations

## License

MIT - see [LICENSE](LICENSE).

## Author

Built by **Harsh** as my first AI automation / agentic workflow.
