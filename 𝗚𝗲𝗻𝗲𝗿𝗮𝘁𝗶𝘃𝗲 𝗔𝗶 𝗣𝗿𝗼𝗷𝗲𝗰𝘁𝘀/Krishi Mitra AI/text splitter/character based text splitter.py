from langchain_text_splitters import CharacterTextSplitter



from langchain_community.document_loaders import TextLoader

splitter = CharacterTextSplitter(
    separator="",
    chunk_size=100,
    chunk_overlap=2)

data = TextLoader(r"C:\Users\rohit\Downloads\AI and Data Science\𝗚𝗲𝗻𝗲𝗿𝗮𝘁𝗶𝘃𝗲 𝗔𝗶 𝗣𝗿𝗼𝗷𝗲𝗰𝘁𝘀\Krishi Mitra AI\krishimitra_ai_notes\farming_knowledge_notes.txt",encoding = "utf-8")

document = data.load()

chunks = splitter.split_documents(document)
print(len(chunks))


for i in chunks:
    print(i.page_content, end="\n\n\n\n")

