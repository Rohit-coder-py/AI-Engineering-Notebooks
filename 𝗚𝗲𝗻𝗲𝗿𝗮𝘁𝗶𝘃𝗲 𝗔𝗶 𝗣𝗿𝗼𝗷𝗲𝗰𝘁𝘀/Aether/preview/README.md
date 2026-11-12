# preview/

Everything the main [`README.md`](../README.md) shows as an image lives here. Add your own screenshots, GIFs or SVGs and the README picks them up.

## What is in this folder

| File | Type | Used for |
|---|---|---|
| `banner.svg` | animated SVG | Hero banner: floating logo, typed tagline, marching stitched border |
| `typing.svg` | animated SVG | Three-line "how it works" tagline that loops forever |
| `divider.svg` | animated SVG | Running-stitch section divider with a needle that travels along it |
| `architecture.svg` | animated SVG | Agent flow with glowing steps and a pulse that follows the data |
| `rag-pipeline.svg` | animated SVG | The six RAG steps lighting up one after another |
| `test-results.svg` | animated SVG | Donut + bars for the 19-case evaluation (18/19 passed) |
| `demo.gif` | GIF | 40 s capture of the manual test run (made from `docs/manual_testing.mp4`) |
| `screenshots/pdf-answer-table.png` | real screenshot | PDF answer with a table and page sources |
| `screenshots/web-research.png` | real screenshot | Live web research with sources |
| `screenshots/pdf-plus-web.png` | real screenshot | One answer using both tools |
| `screenshots/not-in-document.png` | real screenshot | Honest "not found" behaviour |
| `screenshots/home-chat.png` | **placeholder** | Replace with a screenshot of the chat home |
| `screenshots/pdf-upload.png` | **placeholder** | Replace: sidebar uploader + "Document ready" metrics |
| `screenshots/agents-working.png` | **placeholder** | Replace: the live status panel while agents run |
| `screenshots/recent-chats.png` | **placeholder** | Replace: the Recent Chats page |
| `screenshots/about-page.png` | **placeholder** | Replace: the About page |

## Replacing a placeholder

1. Run the app (`streamlit run app.py`) and open the screen.
2. Take a screenshot (Windows: `Win + Shift + S`).
3. Save it in `screenshots/` using **exactly the same file name** as the placeholder, for example `about-page.png`.

No README edit is needed, because the README already points to that file name.

## Adding a new image or SVG

1. Put the file in `preview/` (SVGs) or `preview/screenshots/` (screenshots).
2. Reference it from the README with a **relative path**:

   ```markdown
   <img src="preview/my-new-diagram.svg" alt="Describe the image" width="80%">
   ```

3. Always fill in `alt` text so the README stays readable for screen readers and when an image fails to load.

## Tips for good previews

- **Size**: screenshots around 1200 px wide are sharp without being heavy. Keep each file under about 500 KB.
- **GIFs**: keep them under about 10 MB. To make one from a screen recording:

  ```bash
  ffmpeg -i docs/manual_testing.mp4 -vf "fps=4,scale=720:-1:flags=lanczos,split[a][b];[a]palettegen=max_colors=96[p];[b][p]paletteuse" preview/demo.gif
  ```

- **Privacy**: before committing a screenshot, check it for API keys, personal chats or file names you do not want public.
- **Light and dark mode**: every SVG here draws its own cream background, so it looks the same on GitHub's light and dark themes.

## Editing the animated SVGs

SVGs are plain text, so you can open them in any editor.

- **Change a colour**: search for a hex value such as `#B94E32` (terracotta) and replace it. The palette is the same as the app theme in `.streamlit/config.toml`.
- **Change the text**: edit the text inside the `<text>` elements. Keep lines short so they fit their box.
- **Change the speed**: look for `dur="..."` on `<animate>` elements. Smaller numbers are faster.
- **Keep them self-contained**: GitHub blocks external fonts, scripts and images inside SVGs, so do not link to them. The logo in `banner.svg` is embedded as base64 for that reason.

Animations play on GitHub, in browsers and in most Markdown previews. If a viewer does not support SVG animation it simply shows the final static frame.
