# Setup and Deployment Guide

Everything you need to run Aether locally, run it in Docker, publish the image to Docker Hub, and put it online.

## 1. Prerequisites

| Need | Details |
|---|---|
| **Python** | 3.10 or newer (3.11 recommended; the Docker image uses 3.11) |
| **Groq API key** | Free at https://console.groq.com/keys |
| **Tavily API key** | Free tier at https://app.tavily.com/ |
| **Docker** (optional) | Docker Desktop on Windows/macOS, or Docker Engine on Linux |
| **Disk / RAM** | The embedding model is downloaded on first run (about 90 MB). PyTorch and the model need a few GB of free disk space |

## 2. Run locally

### 2.1 Windows (Command Prompt or PowerShell)

```bat
git clone https://github.com/Rohit-coder-py/Aether.git
cd Aether

python -m venv .venv
.venv\Scripts\activate

pip install -r requirements.txt

copy env.example .env
notepad .env
streamlit run app.py
```

If PowerShell blocks the activation script, run `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned` once, or use Command Prompt instead.

### 2.2 macOS / Linux

```bash
git clone https://github.com/Rohit-coder-py/Aether.git
cd Aether

python3 -m venv .venv
source .venv/bin/activate

pip install -r requirements.txt

cp env.example .env
nano .env
streamlit run app.py
```

### 2.3 Fill in `.env`

```ini
GROQ_API_KEY=gsk_your_key_here
TAVILY_API_KEY=tvly-your_key_here
```

Open http://localhost:8501. Upload `sample_data/Intro_to_LLMs.pdf` and try the questions in [`demo_questions.md`](demo_questions.md).

> **Important:** the app uses `os.getcwd()` to find the logo, so always start it from the project folder (the one that contains `app.py`).

## 3. Run with Docker

```bash
# Build the image (first build is slow: it installs PyTorch and downloads the embedding model)
docker build -t aether .

# Run it, passing the keys at run time
docker run --env-file .env -p 8501:8501 aether
```

Open http://localhost:8501.

| Flag | Meaning |
|---|---|
| `--env-file .env` | Loads `GROQ_API_KEY` and `TAVILY_API_KEY` into the container. The keys are **not** baked into the image |
| `-p 8501:8501` | Maps the container's Streamlit port to your machine |
| `-d` | (optional) run in the background |
| `--name aether` | (optional) give the container a name |

Check the health of a running container:

```bash
docker ps                      # STATUS shows "healthy" after about 40 s
docker logs -f aether          # if you used --name aether
```

### Optional: docker-compose

Create a `docker-compose.yml` file next to the Dockerfile (this file is safe to commit; it contains no secrets because the keys come from `.env`):

```yaml
services:
  aether:
    build: .
    image: <your-dockerhub-username>/aether:latest
    env_file: .env
    ports:
      - "8501:8501"
    restart: unless-stopped
```

Then run `docker compose up --build`.

## 4. Publish to Docker Hub

1. Create a free account at https://hub.docker.com and a repository named `aether`.
2. Log in from your terminal:

   ```bash
   docker login
   ```

3. Build with your Docker Hub username in the tag, add a version tag and a `latest` tag:

   ```bash
   docker build -t <your-username>/aether:1.0 -t <your-username>/aether:latest .
   ```

4. Push both tags:

   ```bash
   docker push <your-username>/aether:1.0
   docker push <your-username>/aether:latest
   ```

5. Test it the way a stranger would, from a clean state:

   ```bash
   docker rmi <your-username>/aether:latest
   docker run --env-file .env -p 8501:8501 <your-username>/aether:latest
   ```

6. Put the repository link in the README (search for `REPLACE-WITH-YOUR-DOCKER-HUB-LINK`) and, in the Docker Hub repository description, paste a short summary plus the run command above.

> Before pushing, confirm that the image holds no secrets: `.env` is listed in `.dockerignore`, so it should not be copied. You can verify with `docker run --rm --entrypoint ls <image> -a /app`.

## 5. Put it online (live link)

Aether needs to run a Python process with enough memory for the embedding model, and it needs outbound internet access to Groq and Tavily. Typical options:

| Option | How | Things to check |
|---|---|---|
| **Streamlit Community Cloud** | Connect your GitHub repository; set `GROQ_API_KEY` and `TAVILY_API_KEY` in the app's **Secrets** settings | Resource limits of the free tier versus PyTorch and the embedding model; start-up time on first load |
| **Hugging Face Spaces (Docker)** | Create a Docker Space and push the repository | Spaces expect the app on a specific port (7860 by default, configurable with `app_port`); add the keys as Space secrets |
| **Container hosts (Render, Railway, Fly.io, a VPS)** | Deploy your Docker Hub image | Set the two environment variables in the dashboard; expose port 8501; check the free-tier memory limit |

Free tiers and limits change, so read the current documentation of the platform you choose before committing to it. Whichever host you pick:

1. Set the two API keys as **environment variables or secrets**, never in the repository.
2. Open the live URL and run two or three of the demo questions to confirm both tools work.
3. Put the URL in the README (search for `REPLACE-WITH-YOUR-LIVE-LINK`).
4. Remember that free hosts may sleep when idle, so the first load can be slow. Mention that in the README if it applies.

## 6. Troubleshooting

| Symptom | Likely cause | Fix |
|---|---|---|
| `GroqError` / authentication error on startup | `GROQ_API_KEY` missing or wrong | Check `.env` spelling (no spaces around `=` is safest) and restart the app |
| Web questions fail or return nothing | `TAVILY_API_KEY` missing or quota used | Check the key; see your Tavily dashboard |
| `429` / "tokens per minute" error | Groq free-tier rate limit | Wait about a minute and ask again; avoid rapid back-to-back questions |
| "No extractable text found" | The PDF is a scan (images) | Run OCR on it first, or use a text-based PDF |
| First PDF upload is slow | Embedding model downloading (local run) | Wait once; it is cached afterwards. The Docker image already contains it |
| Logo missing or `FileNotFoundError` | App started from the wrong folder | `cd` into the project folder and run `streamlit run app.py` |
| `ModuleNotFoundError` | Dependencies not installed in the active environment | Activate the virtual environment, run `pip install -r requirements.txt` |
| LangChain import errors such as `create_agent` not found | Old LangChain version | `pip install -U -r requirements.txt` (needs LangChain 1.x) |
| Port 8501 already in use | Another Streamlit app is running | Stop it, or use `-p 8600:8501` with Docker / `--server.port 8600` locally |
| Container shows `unhealthy` | Still starting, or the app crashed | Wait 40 s; check `docker logs` |
| After refresh the chats are gone | Chat history is session-only in v1.0 | Expected behaviour; persistent history is on the roadmap |

## 7. Pre-publish security checklist

- [ ] `.env` is **not** in the repository (`git status` and `git ls-files | grep env` should show only `env.example`).
- [ ] `.env` is **not** inside any zip you share. Remove it before zipping.
- [ ] Any API key that was ever pasted into a chat, a screenshot or a shared zip has been **rotated** (create a new key and delete the old one in the provider's dashboard).
- [ ] `env.example` contains only placeholders.
- [ ] Screenshots and recordings do not show keys or private files.
- [ ] The Docker image was checked for secrets (see section 4).

## 8. Updating a deployed version

```bash
git pull
docker build -t <your-username>/aether:1.1 -t <your-username>/aether:latest .
docker push <your-username>/aether:1.1
docker push <your-username>/aether:latest
```

Then redeploy or restart on your host, and update the version number in the README and `docs/PROJECT_REPORT.md`.
