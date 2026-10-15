import filelock
import huggingface_hub.utils._fixes as fixes

# Compatibility workaround for Thonny's bundled filelock
_original_filelock = filelock.FileLock

def compatible_filelock(lock_file, timeout=-1, **kwargs):
    kwargs.pop("mode", None)
    return _original_filelock(lock_file, timeout=timeout)

fixes.FileLock = compatible_filelock

# Import after applying the workaround
from langchain_huggingface import HuggingFaceEmbeddings

embedding = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

texts = [
    "Python is easy to learn.",
    "I enjoy building AI projects.",
    "The weather is pleasant today.",
    "My favorite food is pizza.",
    "Dogs are friendly animals.",
    "I want to become an AI engineer.",
    "Football is a popular sport.",
    "The Earth revolves around the Sun."
]

vector = embedding.embed_documents(texts)

print("Number of sentences:", len(vector))
print("Embedding dimensions:", len(vector[0]))
print("First embedding:", vector[0])