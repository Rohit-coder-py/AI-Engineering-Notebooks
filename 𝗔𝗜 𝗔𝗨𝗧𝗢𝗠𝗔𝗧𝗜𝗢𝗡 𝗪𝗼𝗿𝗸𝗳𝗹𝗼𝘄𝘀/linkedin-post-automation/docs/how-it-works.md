# How it works

The workflow is a simple 5-step agentic pipeline in [n8n](https://n8n.io).

| # | Node | Type | What it does |
|---|------|------|--------------|
| 1 | **On form submission** | Form Trigger | Shows a web form ("Blog to LinkedIn Generator") with one required field, `blog_url`. |
| 2 | **HTTP Request** | HTTP Request | Downloads the page at `{{ $json.blog_url }}`. |
| 3 | **HTML** | HTML (extract) | Pulls the text of the page `body` into a field called `article_text`. |
| 4 | **Message a model** | Google Gemini | Sends `article_text` plus a prompt to Gemini and gets back a LinkedIn post. |
| 5 | **Form** | Form Ending | Shows the generated post to the user on the completion screen. |

## The prompt

Gemini is told to act as a professional LinkedIn content writer and to:

- start with an attention-grabbing hook
- highlight the most important insights
- use short paragraphs and a professional, conversational tone
- end with an engaging question
- add 3-5 relevant hashtags
- **not invent facts** (reduces hallucination)

## Data flow

```
Form (blog_url) -> HTTP GET -> extract body text -> Gemini prompt -> show post
```

## Known limitations

- `body` selector also captures menus, footers and scripts, which wastes tokens.
- Very long articles may exceed the model's input limit.
- Pages that need JavaScript to render or that block bots will return little text.
- No human review step before the post is shown (and nothing is auto-posted to LinkedIn).
