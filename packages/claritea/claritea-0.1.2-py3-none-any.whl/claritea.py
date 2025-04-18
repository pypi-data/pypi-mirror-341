import argparse
import io
import os
import sys
from pathlib import Path

import git


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("path", default=os.getcwd(), nargs="?")

    return parser.parse_args()


def main():
    options = parse_args()
    repo_path = options.path
    repo = git.Repo(repo_path, search_parent_directories=True)
    repo_path = repo.working_tree_dir
    if not repo_path:
        return
    abspath = Path(options.path).absolute()
    subpath = abspath.relative_to(repo_path)

    tracked_files = [
        f for (f, _) in repo.index.entries.keys() if str(f).endswith(".py")
    ]
    tracked_files = [
        f
        for f in tracked_files
        if Path(f).absolute().as_posix().startswith(subpath.absolute().as_posix())
    ]
    combined_content = io.StringIO()
    for file_path in tracked_files:
        full_path = os.path.join(repo_path, file_path)
        try:
            with open(full_path, "r", encoding="utf-8") as f:
                content = f.read()
                combined_content.write(f"File: {file_path}\n\n")
                combined_content.write("```python\n")
                combined_content.write(content + "\n```\n\n---\n\n")
        except UnicodeDecodeError:
            print(
                f"Warning: Skipping binary or non-UTF-8 file: {file_path}",
                file=sys.stderr,
            )
        except FileNotFoundError:
            print(
                f"Warning: File not found (shouldn't happen): {file_path}",
                file=sys.stderr,
            )
    print(combined_content.getvalue())


if __name__ == "__main__":
    main()
