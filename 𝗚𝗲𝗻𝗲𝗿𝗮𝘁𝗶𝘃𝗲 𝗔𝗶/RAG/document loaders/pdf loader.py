# we can use pypdf here as we used in project : Ask Your Pdf


from pypdf import PdfReader

reader = PdfReader(r"C:\Users\rohit\Downloads\AI and Data Science\𝗚𝗲𝗻𝗲𝗿𝗮𝘁𝗶𝘃𝗲 𝗔𝗶 𝗣𝗿𝗼𝗷𝗲𝗰𝘁𝘀\Krishi Mitra AI\krishimitra_ai_notes\ai_notes.pdf")

print(len(reader.pages))


for page in reader.pages:
    print(page.extract_text())
    
    
    
#-----------Methord 2 ; Using langchain community
    
from langchain_community.document_loaders import PyPDFLoader

data = PyPDFLoader(r"C:\Users\rohit\Downloads\AI and Data Science\𝗚𝗲𝗻𝗲𝗿𝗮𝘁𝗶𝘃𝗲 𝗔𝗶 𝗣𝗿𝗼𝗷𝗲𝗰𝘁𝘀\Krishi Mitra AI\krishimitra_ai_notes\ai_notes.pdf")

documents= data.load()

print("Total pages:", len(documents))

for document in documents:
    print(document.page_content)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   


