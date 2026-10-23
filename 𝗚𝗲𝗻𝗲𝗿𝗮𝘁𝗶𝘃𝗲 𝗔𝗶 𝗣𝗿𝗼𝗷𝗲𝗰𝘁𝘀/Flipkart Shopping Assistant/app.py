
import trafilatura
from bs4 import BeautifulSoup

url = input("Enter website URL: ").strip()

text = None

# STEP 1: Try Trafilatura
print("\n[1] Trying Trafilatura...")

try:
    html = trafilatura.fetch_url(url)

    if html:
        text = trafilatura.extract(
            html,
            include_links=True,
            include_tables=True,
            favor_recall=True
        )

    if text and text.strip():
        print("Trafilatura successful!")

except Exception as e:
    print("Trafilatura failed:", e)


# STEP 2: Fallback to BeautifulSoup
if not text or not text.strip():
    print("\n[2] Trying BeautifulSoup...")

    try:
        # Reuse HTML if already fetched; otherwise download it
        if not html:
            import requests

            response = requests.get(
                url,
                headers={
                    "User-Agent": (
                        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                        "AppleWebKit/537.36 (KHTML, like Gecko) "
                        "Chrome/130.0.0.0 Safari/537.36"
                    )
                },
                timeout=15
            )
            response.raise_for_status()
            html = response.text

        soup = BeautifulSoup(html, "html.parser")

        # Remove unnecessary elements
        for tag in soup([
            "script", "style", "noscript", "svg"
        ]):
            tag.decompose()

        text = soup.get_text(
            separator="\n",
            strip=True
        )

        if text and text.strip():
            print("BeautifulSoup successful!")
        else:
            text = None

    except Exception as e:
        print("BeautifulSoup failed:", e)


# STEP 3: Final result
if text and text.strip():
    print("\n========== EXTRACTED TEXT ==========\n")
    print(text)
else:
    print("\nBoth methods failed to extract text.")
