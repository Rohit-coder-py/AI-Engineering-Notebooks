from langchain_community.document_loaders import WebBaseLoader

url = input("Enter website URL: ").strip()

try:
    loader = WebBaseLoader(url)
    docs = loader.load()

    if docs and docs[0].page_content.strip():
        extracted_text = "\n\n".join(
            doc.page_content for doc in docs if doc.page_content.strip()
        )

        output_file = "extracted_website.txt"

        with open(output_file, "w", encoding="utf-8") as file:
            file.write(f"Source URL: {url}\n\n")
            file.write(extracted_text)

        print(f"\nExtracted text saved to: {output_file}")
        print(f"Characters saved: {len(extracted_text)}")
    else:
        print("No readable text was extracted.")

except Exception as e:
    print(f"Failed to load website: {e}")
