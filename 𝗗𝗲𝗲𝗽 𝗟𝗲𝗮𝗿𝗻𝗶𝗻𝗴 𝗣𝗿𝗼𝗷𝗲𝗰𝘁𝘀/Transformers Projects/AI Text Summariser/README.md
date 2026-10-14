
[![Live Demo](https://img.shields.io/badge/▶_LIVE_DEMO-Open_the_App-d9a94a?style=for-the-badge&logo=streamlit&logoColor=white)](https://ai-text-summarizer-transformers.streamlit.app/)
[![Preview](https://img.shields.io/badge/🎬_PREVIEW-Watch_the_Video-ee5f7a?style=for-the-badge)](preview/preview.mp4)

<b>Watch Preview of Project :</b> https://github.com/user-attachments/assets/b8920b59-8407-4204-abbd-bb4407dc8ff7


![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![PyTorch](https://img.shields.io/badge/PyTorch-EE4C2C?style=for-the-badge&logo=pytorch&logoColor=white)
![Hugging Face](https://img.shields.io/badge/🤗_Transformers-FFD21E?style=for-the-badge&logoColor=black)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white)
![Jupyter](https://img.shields.io/badge/Jupyter-F37626?style=for-the-badge&logo=jupyter&logoColor=white)

![Model](https://img.shields.io/badge/model-distilbart--cnn--12--6-2fd1a0?style=flat-square)
![Task](https://img.shields.io/badge/task-abstractive_summarisation-5b94f5?style=flat-square)
![Decoding](https://img.shields.io/badge/decoding-deterministic-a98bfa?style=flat-square)
![Status](https://img.shields.io/badge/status-live-2fd1a0?style=flat-square)

**Paste long text → get a crisp abstractive summary → peek inside the tokenizer and the model.**

[**🚀 Live App**](https://ai-text-summarizer-transformers.streamlit.app/) ·
[**✨ Features**](#-features) ·
[**🖼 Screenshots**](#-screenshots) ·
[**🧠 How it works**](#-how-it-works) ·
[**⚡ Quick start**](#-quick-start)

</div>

---

## 🎬 Preview

<div align="center">

<img src="preview/preview.gif" alt="App preview" width="270"/>

<b>Watch Preview of Project :</b> https://github.com/user-attachments/assets/b8920b59-8407-4204-abbd-bb4407dc8ff7

</div>

---

## ✦ What is this?

**AI Text Summariser** turns long articles into short, readable summaries using **DistilBART** (`sshleifer/distilbart-cnn-12-6`) — a distilled BART encoder–decoder from Hugging Face, running on PyTorch.

It is *abstractive*: the model **writes new sentences** instead of copying lines from the input. The project started as a learning notebook (`ai_test_summerizer.ipynb`) and grew into a full Streamlit web app with a token inspector, a model lab and long-document support.

<div align="center">
<img src="assets/demo.svg" alt="Animated demo: input text becomes a summary" width="100%"/>
</div>

---

## 🌟 Features

| | Feature | What it does |
|---|---|---|
| ✦ | **Abstractive summaries** | DistilBART generates a fresh, concise summary of your text |
| 📏 | **Length presets** | *Short*, *Balanced*, *Detailed* or *Custom* `max_length` / `min_length` |
| 📚 | **Long-text chunking** | Inputs beyond the 1,024-token window are split into sentence-aligned chunks, summarised, then merged |
| 🔬 | **Token Inspector** | See how the BART tokenizer splits text into sub-word tokens and IDs, with a model-window usage bar |
| 🧠 | **Model Lab** | Parameters, layers, hidden size, heads, vocab size and default generation settings read live from the model config |
| 📂 | **File upload** | Drop in a `.txt` or `.md` file instead of pasting |
| 🕘 | **Session history** | Every summary from the session is kept in an expandable list |
| ⬇ | **Download** | Save any summary as `summary.txt` |
| 🎛 | **Advanced controls** | `num_beams`, `no_repeat_ngram_size`, `repetition_penalty`, optional merge pass |
| 🌑 | **Dark editorial UI** | Gold / emerald / sapphire palette, serif headlines, metric cards |

---

## 🖼 Screenshots

<table>
<tr>
<td width="50%"><img src="assets/ui-sum.png" alt="Summarise tab"/><br/><sub><b>✦ Summarise</b> — paste text, get a summary and metrics</sub></td>
<td width="50%"><img src="assets/ui-tok.png" alt="Token Inspector tab"/><br/><sub><b>🔬 Token Inspector</b> — colour-coded sub-word tokens</sub></td>
</tr>
<tr>
<td width="50%"><img src="assets/ui-model.png" alt="Model Lab tab"/><br/><sub><b>🧠 Model Lab</b> — architecture at a glance</sub></td>
<td width="50%"><img src="assets/ui-how.png" alt="How it works tab"/><br/><sub><b>📖 How it works</b> — the pipeline explained in-app</sub></td>
</tr>
</table>

> The images above are renders of the app's UI using the same theme and sample text as the notebook.

---

## 🧠 How it works

<div align="center">
<img src="assets/pipeline.svg" alt="Pipeline: Tokenise, Encode, Decode, Beam search" width="100%"/>
</div>

1. **Tokenise** — text is split into sub-word tokens and mapped to integer IDs.
2. **Encode** — the 12-layer encoder reads every token at once with self-attention.
3. **Decode** — the 6-layer decoder writes the summary one token at a time.
4. **Beam search** — several candidate summaries are explored and the best is kept.

### Dynamic length rule

Taken straight from the notebook's final `summarize_text` function, so tiny inputs never produce a summary longer than the input:

```python
max_len = min(max_len, max(8, input_tokens - 2))
min_len = min(min_len, max(1, max_len // 3))
```

### Long documents

```text
long text ─► split into ≤900-token chunks ─► summarise each chunk ─► (optional) merge pass ─► final summary
```

---

## ⚙️ Generation settings

| Parameter | Meaning |
|---|---|
| `max_length` / `min_length` | Bounds on summary length (tokens) |
| `num_beams` | Beam-search width (1 = greedy) |
| `no_repeat_ngram_size` | Blocks repeated phrases |
| `repetition_penalty` | Discourages repeated tokens |
| `do_sample=False` | Deterministic output — same input, same summary |

Length presets: **Short** `40/10` · **Balanced** `60/20` · **Detailed** `130/40` (max/min tokens).

---

## 📓 The notebook

`ai_test_summerizer.ipynb` is the learning journey behind the app:

- A full **NLP project roadmap** — from business understanding to deployment
- Loading the Hugging Face `summarization` pipeline
- Inspecting the tokenizer (`BartTokenizerFast`) and model (`BartForConditionalGeneration`)
- Understanding `max_length`, `min_length`, `do_sample` and other generation parameters
- Building the final dynamic-length `summarize_text` function and testing on long articles

---

## 🗂 Project structure

```text
AI-Text-Summarizer/
├── app.py                      # Streamlit app
├── ai_test_summerizer.ipynb    # Learning notebook
├── requirements.txt            # Dependencies
├── .streamlit/
│   └── config.toml             # Dark theme
├── assets/                     # README images & animated SVGs
└── preview/                    # 9:16 preview video, GIF and poster
```

---

## ⚡ Quick start

```bash
# 1. Clone
git clone https://github.com/Rohit-coder-py/AI-Text-Summarizer.git
cd AI-Text-Summarizer

# 2. (optional) virtual environment
python -m venv .venv && source .venv/bin/activate      # Windows: .venv\Scripts\activate

# 3. Install
pip install -r requirements.txt

# 4. Run
streamlit run app.py
```

> The first launch downloads the model (~1.2 GB) and may take a minute. After that it is cached.

**Requirements:** `streamlit>=1.35` · `torch` · `transformers<5` · `sentencepiece` · `pandas`

---

## 🛠 Tech stack

| Layer | Tools |
|---|---|
| Model | DistilBART — `sshleifer/distilbart-cnn-12-6` |
| Deep learning | PyTorch |
| NLP | Hugging Face Transformers, SentencePiece |
| Web app | Streamlit |
| Data | Pandas |
| Experiments | Jupyter Notebook |


**Live app → [ai-text-summarizer-transformers.streamlit.app](https://ai-text-summarizer-transformers.streamlit.app/)**

Built with ♥ using PyTorch, Hugging Face and Streamlit · [@Rohit-coder-py](https://github.com/Rohit-coder-py)

⭐ If this project helped you, drop a star!

</div>
