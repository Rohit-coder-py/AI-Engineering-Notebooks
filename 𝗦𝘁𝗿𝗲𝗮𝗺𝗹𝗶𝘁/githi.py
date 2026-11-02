import os
import git
import tempfile

repo_url = input("Enter GitHub Repository URL: ")

with tempfile.TemporaryDirectory() as temp_dir:

    repo_path = os.path.join(temp_dir, "repository")

    git.Repo.clone_from(repo_url, repo_path)

    for root, dirs, files in os.walk(repo_path):

        dirs[:] = [d for d in dirs if d != ".git"]

        for file in files:

            file_path = os.path.join(root, file)

            with open(file_path, "r", encoding="utf-8") as f:

                print(f"\n{'=' * 60}")
                print(f"FILE: {file}")
                print("=" * 60)

                print(f.read())

print("\nExtraction completed!")