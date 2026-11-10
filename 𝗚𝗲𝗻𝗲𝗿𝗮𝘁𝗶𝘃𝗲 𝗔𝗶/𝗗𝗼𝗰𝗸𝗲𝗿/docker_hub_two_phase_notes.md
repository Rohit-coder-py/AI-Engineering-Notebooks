# Docker Hub: Two-Phase Practical Notes

**Goal:** Learn Docker in two roles: 1. **Developer:** Package a
completed ML application and publish its image to Docker Hub. 2.
**Consumer / teammate:** Find an existing image on Docker Hub, pull it,
run it, and open it at localhost.

These examples assume a **Python + Streamlit ML app**. Adjust the
startup command and port for Flask, FastAPI, or another framework.

------------------------------------------------------------------------

# Phase 1 --- Developer: publish my project

## 1. Understand the project

Imagine your completed project looks like this:

``` text
my-ml-project/
├── app.py
├── requirements.txt
├── notebook.ipynb
├── artifacts/
│   ├── model.pth
│   ├── scaler.pkl
│   └── encoder.pkl
├── src/                  # Include if app.py imports code from here
│   ├── model.py
│   └── preprocessing.py
├── Dockerfile
└── .dockerignore
```

-   `app.py`: application entry point.
-   `requirements.txt`: Python dependencies.
-   `artifacts/`: trained model, encoder, scaler, and other runtime
    files.
-   `src/`: helper modules imported by the app.
-   `notebook.ipynb`: usually for exploration/training, not needed to
    serve predictions.

**Rule:** Include every file the running app needs. Do not exclude model
weights or artifacts loaded by the app.

## 2. Open PowerShell in the project folder

``` powershell
cd "C:\path\to\my-ml-project"
Get-ChildItem -Force
tree /f
```

Run Docker commands from the project root---the folder containing the
Dockerfile.

## 3. Create the Dockerfile

``` powershell
notepad Dockerfile
```

For a Streamlit app:

``` dockerfile
FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "app.py", "--server.address=0.0.0.0", "--server.port=8501"]
```

### What each instruction does

  -----------------------------------------------------------------------
  Instruction                         Meaning
  ----------------------------------- -----------------------------------
  `FROM`                              Selects the base image with Python
                                      installed.

  `WORKDIR`                           Sets the working directory inside
                                      the container.

  `COPY requirements.txt .`           Copies the dependency list into the
                                      image.

  `RUN pip install ...`               Installs dependencies inside the
                                      image.

  `COPY . .`                          Copies the remaining build-context
                                      files, excluding `.dockerignore`
                                      entries.

  `EXPOSE 8501`                       Documents the port used by the app
                                      inside the container.

  `CMD`                               Defines the command executed when
                                      the container starts.
  -----------------------------------------------------------------------

**Why copy requirements first?** Docker can reuse the
dependency-installation layer when only application code changes, making
later builds faster.

The `CMD` above is specifically for Streamlit. Your app must listen on
`0.0.0.0` inside the container. For another framework, use its correct
startup command and port.

## 4. Create `.dockerignore`

``` powershell
notepad .dockerignore
```

Example:

``` text
.git
.gitignore
__pycache__
*.pyc
.ipynb_checkpoints
venv
.venv
.env
notebook.ipynb
notebooks/
data/
```

Customize this list: - `.git`: Git history is not needed at runtime. -
`__pycache__`, `*.pyc`: generated Python cache files. - `venv`, `.venv`:
your local virtual environment should not be copied into a Linux
image. - `.env`: may contain secrets; never bake secrets into a public
image. - notebooks, datasets: exclude only if the running app does not
need them.

**Do not exclude `artifacts/` or `src/` if your app needs them.**

## 5. Prepare dependencies

``` powershell
notepad requirements.txt
```

Example for a simple Streamlit inference app:

``` text
streamlit
pandas
numpy
scikit-learn
```

Add every package imported by your app. If using PyTorch, include the
correct PyTorch installation for the target environment. CPU-only
installation can avoid downloading CUDA libraries.

For reproducibility, pin tested package versions where practical.
Pickled scikit-learn artifacts can be version-sensitive, so use
compatible versions of scikit-learn, NumPy, and related libraries.

## 6. Verify the project files

``` powershell
Get-ChildItem -Force
tree /f
```

Confirm: - The file is named exactly `Dockerfile`, not
`Dockerfile.txt`. - `.dockerignore` and `requirements.txt` exist. -
`app.py`, model weights, artifacts, and imported source modules are
present.

If Notepad created `Dockerfile.txt`:

``` powershell
Rename-Item Dockerfile.txt Dockerfile
```

## 7. Build the Docker image

Make sure Docker Desktop is running, then:

``` powershell
docker build -t my-ml-project .
```

-   `docker build`: build an image.
-   `-t my-ml-project`: give the image a name/tag.
-   `.`: use the current directory as the build context.

The build context is the set of files Docker can access for the build,
filtered by `.dockerignore`.

The first build may take several minutes because Docker downloads the
base image and installs dependencies. PyTorch can make the image and
build time significantly larger.

Check the image:

``` powershell
docker images
```

## 8. Run the image locally

``` powershell
docker run -d -p 8501:8501 --name my-ml-container my-ml-project
```

  Part              Meaning
  ----------------- -----------------------------------------------
  `docker run`      Creates and starts a container from an image.
  `-d`              Runs it in the background.
  `-p 8501:8501`    Maps host port 8501 to container port 8501.
  `--name`          Gives the container a convenient name.
  `my-ml-project`   The image used to create the container.

Port mapping:

``` text
YOUR COMPUTER                    CONTAINER
localhost:8501  ───────────────>  app listens on port 8501
(host port)                       (container port)
```

Open **http://localhost:8501**.

If host port 8501 is already occupied:

``` powershell
docker run -d -p 8503:8501 --name my-ml-container my-ml-project
```

Then open **http://localhost:8503**. The right-hand port must match the
app's port inside the container; the left-hand port is chosen on your
computer.

## 9. Test before publishing

Verify all of the following: 1. The application page loads. 2. The model
and preprocessing artifacts load. 3. You can submit valid input. 4. A
prediction is returned. 5. There are no startup or prediction errors.

Useful commands:

``` powershell
docker ps
docker logs my-ml-container
docker ps -a
```

-   `docker ps`: running containers.
-   `docker logs`: application output and errors.
-   `docker ps -a`: running and stopped containers.

Fix errors, rebuild, and retest before publishing.

## 10. Sign in to Docker Hub

Visit **https://hub.docker.com/** and create an account if needed.

In PowerShell:

``` powershell
docker login
```

Complete the authentication flow. Depending on the setup, Docker may
offer browser-based sign-in or ask for credentials/token.

## 11. Create a Docker Hub repository

On Docker Hub: 1. Open **Repositories**. 2. Select **Create
repository**. 3. Enter a repository name, e.g. `my-ml-project`. 4.
Choose **Public** or **Private**. 5. Create it.

A public image can be pulled by anyone. Do not publish credentials,
private data, API keys, or confidential artifacts.

## 12. Tag the local image

Docker Hub image naming format:

``` text
DOCKERHUB_USERNAME/REPOSITORY:TAG
```

Example:

``` text
rohitcoderpy/my-ml-project:latest
```

Tag it:

``` powershell
docker tag my-ml-project rohitcoderpy/my-ml-project:latest
```

-   `my-ml-project`: local image name.
-   `rohitcoderpy/my-ml-project`: Docker Hub namespace/repository.
-   `latest`: tag label; it does not automatically guarantee that the
    image is newest.

Tagging does not rebuild or duplicate the image. It adds another name to
the same local image.

## 13. Push the image

``` powershell
docker push rohitcoderpy/my-ml-project:latest
```

Docker uploads the image layers to Docker Hub.

Typical messages: - `Pushed`: layer uploaded. - `Layer already exists`:
registry already has that layer; no need to upload it again.

A successful push completes without a final error and reports an image
digest.

### If push fails with `broken pipe`

This usually indicates a network/proxy connection interruption during
upload.

1.  Keep the local image; do not delete it.
2.  Check the internet connection and Docker Desktop.
3.  Retry the same `docker push` command.
4.  Docker can reuse layers already present in the registry and retry
    remaining uploads.
5.  If it repeatedly fails, investigate Docker Desktop's network/proxy
    connection.

Stopping a container does **not** cause a push failure. `docker push`
uploads an image, not a running container.

## 14. Verify on Docker Hub

Open:

``` text
https://hub.docker.com/r/rohitcoderpy/my-ml-project
```

Check that the repository exists and the expected tag (e.g. `latest`) is
listed. Only share the link after the push succeeds.

## 15. Add the Docker Hub link to GitHub README

Example:

``` markdown
## Docker

**Docker Hub:** [View image](https://hub.docker.com/r/rohitcoderpy/my-ml-project)

### Pull the image

```bash
docker pull rohitcoderpy/my-ml-project:latest
```

### Run the application

``` bash
docker run -d -p 8501:8501 --name my-ml-container rohitcoderpy/my-ml-project:latest
```

Open http://localhost:8501 in your browser.


    Replace the example username and repository with your actual values. Commit and push the README update to GitHub.

    ## 16. Optional: prove the registry copy works

    Do this only after verifying that the push succeeded.

    Stop and remove the test container:

    ```powershell
    docker stop my-ml-container
    docker rm my-ml-container

Remove the local image references:

``` powershell
docker image rm rohitcoderpy/my-ml-project:latest
docker image rm my-ml-project:latest
```

If Docker reports that an image is still in use, inspect containers
first. Do not force-delete resources unless you understand what depends
on them.

Now download the image from Docker Hub:

``` powershell
docker pull rohitcoderpy/my-ml-project:latest
```

Run it again:

``` powershell
docker run -d -p 8501:8501 --name my-ml-container rohitcoderpy/my-ml-project:latest
```

Open **http://localhost:8501** and test a prediction again.

This proves that the published image---not merely your original local
build---works.

------------------------------------------------------------------------

# Phase 2 --- Consumer / teammate: use an existing Docker Hub image

Imagine another developer has already published an image. You do not
need their notebook, source code, model files, or Dockerfile to run the
published image. You need Docker installed and access to the image.

## 1. Visit Docker Hub

Open **https://hub.docker.com/**.

Search for the project/image name, or open the repository link shared by
the developer. Example:

``` text
https://hub.docker.com/r/rohitcoderpy/medical-insurance-cost-predictor
```

## 2. Inspect the repository

Check: - Repository owner and name. - Public/private visibility. -
Available tags. - README and run instructions. - Required port and
environment variables, if documented.

Do not assume the tag is `latest`; use the tag specified by the
publisher.

For a private repository, you need permission and must sign in.

## 3. Copy the image reference

Format:

``` text
USERNAME/REPOSITORY:TAG
```

Example:

``` text
rohitcoderpy/medical-insurance-cost-predictor:latest
```

## 4. Start Docker Desktop

On Windows: 1. Open Docker Desktop. 2. Wait until its engine is running.
3. Open PowerShell.

Check Docker:

``` powershell
docker --version
docker info
```

If Docker is not running, start Docker Desktop and wait for it to finish
starting.

## 5. Sign in if necessary

Public images can generally be pulled without signing in, subject to
Docker Hub's anonymous pull limits.

For a private image, sign in with an account that has permission:

``` powershell
docker login
```

## 6. Pull the image

``` powershell
docker pull rohitcoderpy/medical-insurance-cost-predictor:latest
```

`docker pull` downloads the image layers from Docker Hub to your
computer.

**Pulling is not the same as running:** after the pull, the image is
local, but no application container has started yet.

## 7. Verify the image

``` powershell
docker images
```

Find the repository and tag in the list.

## 8. Run a container

For the example Streamlit app:

``` powershell
docker run -d -p 8501:8501 --name medical-insurance-app rohitcoderpy/medical-insurance-cost-predictor:latest
```

If port 8501 on your computer is occupied:

``` powershell
docker run -d -p 8503:8501 --name medical-insurance-app rohitcoderpy/medical-insurance-cost-predictor:latest
```

The container-side port (`8501`) must match the port used by the app.
The host-side port (`8503` in the second example) can be chosen by you.

## 9. Open localhost

If you used `-p 8501:8501`, open:

**http://localhost:8501**

If you used `-p 8503:8501`, open:

**http://localhost:8503**

`localhost` means your own computer. Docker forwards the chosen host
port to the application's port inside the container.

## 10. Test the application

1.  Enter sample input.
2.  Submit the form.
3.  Check that the output/prediction appears.
4.  If something fails, collect the error and share it with the image
    publisher.

## 11. Inspect the container and logs

``` powershell
docker ps
docker ps -a
docker logs medical-insurance-app
```

Follow logs live:

``` powershell
docker logs -f medical-insurance-app
```

Press `Ctrl + C` to stop following the log stream. This does not stop
the container.

## 12. Stop, start, and remove the container

Stop:

``` powershell
docker stop medical-insurance-app
```

Start the same existing container:

``` powershell
docker start medical-insurance-app
```

Remove it:

``` powershell
docker stop medical-insurance-app
docker rm medical-insurance-app
```

Removing a container does not automatically remove its image.

To remove the local image after no containers are using it:

``` powershell
docker image rm rohitcoderpy/medical-insurance-cost-predictor:latest
```

This removes the local copy only. It does not delete the image from
Docker Hub.

------------------------------------------------------------------------

# Core Docker concepts

  -----------------------------------------------------------------------
  Concept                             Meaning
  ----------------------------------- -----------------------------------
  Dockerfile                          Instructions used to build an
                                      image.

  Image                               Packaged application blueprint,
                                      runtime, dependencies, and included
                                      files.

  Container                           An instance created from an image.

  Registry                            A service that stores and
                                      distributes images, e.g. Docker
                                      Hub.

  Repository                          A named location in a registry for
                                      an image and its tags.

  Tag                                 A label/version such as `latest` or
                                      `v1`.

  Build                               Create an image from a Dockerfile
                                      and build context.

  Run                                 Create and start a container from
                                      an image.

  Push                                Upload an image to a registry.

  Pull                                Download an image from a registry.

  Port mapping                        Connect a host-computer port to a
                                      container port.

  `.dockerignore`                     Excludes files from the Docker
                                      build context.
  -----------------------------------------------------------------------

# Both workflows at a glance

## Phase 1 --- Developer

``` text
Complete ML project
       |
       v
Prepare requirements.txt
       |
       v
Create Dockerfile
       |
       v
Create .dockerignore
       |
       v
docker build
       |
       v
docker run
       |
       v
Test app and predictions
       |
       v
docker login
       |
       v
Create Docker Hub repository
       |
       v
docker tag
       |
       v
docker push
       |
       v
Verify image + update GitHub README
```

## Phase 2 --- Consumer / teammate

``` text
Visit Docker Hub
       |
       v
Find image repository and tag
       |
       v
Start Docker Desktop
       |
       v
docker pull
       |
       v
docker images
       |
       v
docker run -p HOST_PORT:APP_PORT
       |
       v
Open http://localhost:HOST_PORT
       |
       v
Use and test the app
```

# Quick command revision

## Developer

``` powershell
# Build
docker build -t my-ml-project .

# Run locally
docker run -d -p 8501:8501 --name my-ml-container my-ml-project

# Check running containers
docker ps

# View logs
docker logs my-ml-container

# Sign in
docker login

# Tag for Docker Hub
docker tag my-ml-project USERNAME/my-ml-project:latest

# Push
docker push USERNAME/my-ml-project:latest
```

## Consumer

``` powershell
# Pull
docker pull USERNAME/REPOSITORY:TAG

# List local images
docker images

# Run
docker run -d -p 8501:8501 --name my-app USERNAME/REPOSITORY:TAG

# Check containers
docker ps

# View logs
docker logs my-app

# Stop / start
docker stop my-app
docker start my-app

# Remove container
docker rm my-app
```

# Safety and troubleshooting reminders

-   Never include passwords, API keys, private tokens, or `.env` secrets
    in a public image.
-   A public image can be downloaded by other people. Review what files
    are copied into it.
-   A notebook is usually unnecessary for inference; exclude it only if
    the running app does not need it.
-   Keep model weights and preprocessing artifacts if the app loads
    them.
-   Test the image before pushing.
-   If `docker push` fails because of a network interruption, keep the
    local image and retry after checking the connection. Do not rebuild
    automatically.
-   If a container name is already in use, inspect `docker ps -a`; start
    or remove the existing container as appropriate.
-   If a port is already allocated, choose another host port and keep
    the container-side port correct.
-   `docker stop` stops a container; it does not delete it.
-   `docker rm` deletes a container; it does not automatically delete
    the image.
-   `docker pull` downloads an image; `docker run` creates and starts a
    container from it.
-   Docker Hub is an image registry, not by itself a public hosting
    service for your running web app. `localhost` is reachable on the
    computer running the container unless you separately configure
    hosting and networking.

**Learning outcome:** You can now package your own ML application,
publish its Docker image, and run another developer's published image
locally without needing their project source code.
