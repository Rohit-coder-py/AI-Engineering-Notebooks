import warnings
import logging

# Ignore Python warnings
warnings.filterwarnings("ignore")

# Reduce Hugging Face / Transformers logs
logging.getLogger("transformers").setLevel(logging.ERROR)
logging.getLogger("huggingface_hub").setLevel(logging.ERROR)
#download model from hugginface and use locally (free)


from langchain_huggingface import HuggingFacePipeline

# Load the model locally (free)
llm = HuggingFacePipeline.from_model_id(
    model_id="HuggingFaceTB/SmolLM2-360M-Instruct",
    task="text-generation",
    pipeline_kwargs={
        "max_new_tokens": 1024,
        "do_sample": False,
        "return_full_text": False,
    },
)

res = llm.invoke(
    "how to generate a  qrcode using python .. Provide code "
)

print(res)
