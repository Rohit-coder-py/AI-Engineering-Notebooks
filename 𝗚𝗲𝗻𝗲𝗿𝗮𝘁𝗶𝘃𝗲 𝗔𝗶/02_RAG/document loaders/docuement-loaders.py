# There are several ways to upload agricultural study materials and knowledge into **KrishiMitra AI**, including websites, PDF documents, TXT files, DOCX files, research papers, YouTube transcripts, Excel sheets, images, and scanned documents. This allows farmers to access relevant agricultural information from multiple sources through a single AI-powered assistant. By leveraging Retrieval-Augmented Generation (RAG), KrishiMitra AI retrieves relevant information from these sources and uses large language models (LLMs) to provide context-aware answers to farmers' questions.


from langchain_community.document_loaders import TextLoader

data = TextLoader(r"C:\Users\rohit\Downloads\AI and Data Science\𝗚𝗲𝗻𝗲𝗿𝗮𝘁𝗶𝘃𝗲 𝗔𝗶 𝗣𝗿𝗼𝗷𝗲𝗰𝘁𝘀\Krishi Mitra AI\krishimitra_ai_notes\farming_knowledge_notes.txt"O,encoding = "utf-8")

document = data.load()

print(document[0].page_content)