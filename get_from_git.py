import tempfile

import git
import os
import shutil
import sys
from argparse import ArgumentParser


def log(msg: str = ""):
    print(msg, file=sys.stderr)


def clone(url=None, repo_path="/tmp/tmp/"):
    if not url:
        raise ValueError("URL for cloning cant be empty")

    git.Repo.clone_from(url=url, to_path=repo_path)

    # shutil.rmtree(os.path.join(repo_path, ".git"))


def rm(repo_path="/tmp/tmp/", leave_ext: tuple = (), to_path="/tmp/tmp2/"):
    for dirpath, dirname, files in os.walk(repo_path):
        for filename in files:
            if os.path.splitext(filename)[1].strip('.') not in leave_ext:
                continue
            abspath = os.path.join(dirpath, filename)
            relpath = os.path.relpath(dirpath, repo_path)

            os.makedirs(os.path.join(to_path, relpath), exist_ok=True)
            shutil.copy(abspath, os.path.join(to_path, relpath))


def clear_target_dir(path: str = ""):
    if not os.path.isdir(path):
        raise ValueError("Path should be a directory")
    for filename in os.scandir(path):
        file_path = os.path.join(path, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            log('Failed to delete %s. Reason: %s' % (file_path, e))
            raise


def main(repo_url: str = "", save_path: str = ""):
    clear_target_dir(save_path)

    with tempfile.TemporaryDirectory(dir="/tmp/input", delete=True) as repo_path:
        # tempfile.TemporaryDirectory(dir="/tmp/output") as to_path:
        clone(repo_url, repo_path)
        rm(repo_path, leave_ext=("md", "json", "txt"), to_path=save_path)
        pass


if __name__ == "__main__":
    arg_parser = ArgumentParser()
    arg_parser.add_argument("-u", "--url", help="URL to a repo to clone", required=True)
    arg_parser.add_argument("-o", "--output", help="Directory to copy the resulting files to", required=True)
    args = arg_parser.parse_args()

    main(repo_url=args.url, save_path=args.output)