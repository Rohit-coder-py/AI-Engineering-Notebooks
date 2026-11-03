import arxiv

search = arxiv.Search(
    query="large language models",
    max_results=2
)

client = arxiv.Client()
results = client.results(search)

for i, paper in enumerate(results, start=1):
    print(f"\nResult {i}")
    print("Title:", paper.title)
    print("Authors:", [author.name for author in paper.authors])
    print("Summary:", paper.summary[:500])