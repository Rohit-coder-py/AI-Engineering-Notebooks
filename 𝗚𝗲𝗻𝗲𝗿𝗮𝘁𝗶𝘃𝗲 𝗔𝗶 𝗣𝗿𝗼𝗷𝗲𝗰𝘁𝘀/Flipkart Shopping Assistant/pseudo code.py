import trafilatura

url = input("Enter website URL: ")

html = trafilatura.fetch_url(url)
text = trafilatura.extract(html) if html else None

print(text if text else "Could not extract text.")