import argparse
import re
from subprocess import check_output

def main() -> int:

    parser = argparse.ArgumentParser()
    parser.add_argument('filename')
    parser.add_argument('--regex', default=None)
    args = parser.parse_args()

    filename = args.filename
    regex = args.regex
    if regex is None:
        return 0
    branch_name = check_output(["git", "symbolic-ref", "--short", "HEAD"]).decode("utf-8").strip()
    branch_pattern = f"(.*[-,_])?({regex})([-,_].*)?"

    match = re.match(branch_pattern, branch_name)
    if match is None:
        return 0

    if (issue := match.group(2)) is None:
        return 0

    with open(filename, 'r+') as f:
        commit_msg = f.read()
        f.seek(0, 0)
        f.write(f"[{issue}] {commit_msg}")

    return 0

if __name__ == "__main__":
    raise SystemExit(main())
