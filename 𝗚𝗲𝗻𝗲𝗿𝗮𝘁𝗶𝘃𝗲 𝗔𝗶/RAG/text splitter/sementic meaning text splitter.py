from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader




splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=2)







data = PyPDFLoader(r"C:\Users\rohit\Downloads\AI and Data Science\𝗚𝗲𝗻𝗲𝗿𝗮𝘁𝗶𝘃𝗲 𝗔𝗶 𝗣𝗿𝗼𝗷𝗲𝗰𝘁𝘀\Krishi Mitra AI\krishimitra_ai_notes\ai_notes.pdf")

documents= data.load()

token_chunks = splitter.split_documents(documents)
print(len(token_chunks))


print(token_chunks[0].page_content)



#after we create chunks we store them into Vector DataBases 