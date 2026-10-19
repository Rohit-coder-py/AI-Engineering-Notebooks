from pypdf import PdfReader

reader = PdfReader(r"C:\Users\rohit\Downloads\sample.pdf")

print("Total Pages:", len(reader.pages))

for page in reader.pages:
    print(page.extract_text())