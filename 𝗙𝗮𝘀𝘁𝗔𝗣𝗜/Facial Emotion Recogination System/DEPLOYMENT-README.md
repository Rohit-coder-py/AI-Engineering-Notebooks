# Facial Emotion Recognition — Render deployment files

Copy these files into the **root of your GitHub repository**, alongside
`fastapi_app.py`, `app.py`, and your `models/` directory.

## Files

- `.python-version` — asks Render to use Python 3.12.10.
- `requirements-api.txt` — dependencies for the FastAPI backend.
- `requirements-streamlit.txt` — dependencies for the Streamlit frontend.
- `requirements.txt` — combined dependency list for platforms that use the
  repository-root requirements file. PyTorch is deliberately excluded.
- `render.yaml` — Render Blueprint configuration. It installs CPU-only
  PyTorch and starts Uvicorn.

## Render setup

If you use the Blueprint (`render.yaml`), connect the repository in Render
and deploy the Blueprint. If you already have a manually created Render
service, either use the following settings or let the Blueprint manage it:

**Build Command**
```bash
pip install -r requirements-api.txt && pip install torch==2.13.0 torchvision==0.28.0 --index-url https://download.pytorch.org/whl/cpu
```

**Start Command**
```bash
uvicorn fastapi_app:app --host 0.0.0.0 --port $PORT
```

Set the health check path to `/health`.

## Streamlit Community Cloud

For the Streamlit app, set the main file to `app.py`. If the deployment
settings allow a custom dependency file, use `requirements-streamlit.txt`.
Otherwise, the root `requirements.txt` is also provided and includes the
frontend dependencies (plus backend packages) but does not install PyTorch.

Set the app's `API_URL` to the actual Render service URL, without a trailing
slash. The frontend should append `/predict` itself.

## Before deploying

1. Confirm `fastapi_app.py` exposes `app = FastAPI(...)`.
2. Confirm model paths in `fastapi_app.py` point to the committed files under
   `models/`, including `resnet18_final.pth` and `class_names.json`.
3. Confirm `/health` exists and returns a successful response.
4. Make sure model files are committed to GitHub and are not excluded by
   `.gitignore`.
5. The free Render instance has only 512 MB RAM. CPU-only PyTorch avoids
   downloading CUDA libraries, but it does **not** guarantee that the
   application will fit in 512 MB at runtime. If it still runs out of memory,
   the service will need more RAM or a lighter inference deployment.

## Git commands

```powershell
git add .python-version requirements.txt requirements-api.txt requirements-streamlit.txt render.yaml DEPLOYMENT-README.md
git commit -m "Add CPU-only Render deployment configuration"
git push origin main
```
