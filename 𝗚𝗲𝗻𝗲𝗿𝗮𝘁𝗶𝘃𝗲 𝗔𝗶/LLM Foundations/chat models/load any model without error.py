model_name = input("Enter Model Name you want to download : ")

import filelock
import huggingface_hub.utils._fixes as fixes

# Compatibility workaround for Thonny's bundled filelock
_original_filelock = filelock.FileLock

def compatible_filelock(lock_file, timeout=-1, **kwargs):
    kwargs.pop("mode", None)
    return _original_filelock(lock_file, timeout=timeout)

fixes.FileLock = compatible_filelock

from langchain_huggingface import HuggingFacePipeline

llm = HuggingFacePipeline.from_model_id(
    model_id=model_name,
    task="text-generation",
    pipeline_kwargs={
        "max_new_tokens": 30,
        "do_sample": False,
        "return_full_text": False,
    },
)

print(llm.invoke("What is llm?"))