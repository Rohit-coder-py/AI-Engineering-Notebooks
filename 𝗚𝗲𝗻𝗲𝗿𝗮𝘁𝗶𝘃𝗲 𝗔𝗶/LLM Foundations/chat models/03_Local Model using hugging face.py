#download model from hugginface and use locally (free)


from langchain_huggingface import HuggingFacePipeline

llm = HuggingFacePipeline.from_model_id(
    model_id="HuggingFaceTB/SmolLM2-360M-Instruct",
    task="text-generation",
    pipeline_kwargs={
        "do_sample": False,
        "return_full_text": False,
    },
)


res = llm.invoke(
    "Explain Generative AI in simple words."
)

print(res)
