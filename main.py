"""Entry program: write one funny 4am commit message to entry.txt.

The message is the note an AI agent leaves in the log after a long night
of chasing down and fixing its own bugs. It is a single UTF-8 text of
1 to 200 characters; the grader runs this program twice and the two runs
must write identical bytes.
"""

import hashlib
import os

TEXT = "fix: 4am. Found the bug. It was me. It was always me. I blamed the human, the tests, and the timezone. I was wrong about all three."

# Gate contract: entry.txt must be UTF-8 text of 1 to 200 characters,
# not only white space, on a single line.
def validate(text):
    """Check the commit message against the bounty gate; raise if invalid."""
    if not 1 <= len(text) <= 200:
        raise AssertionError("commit message must be 1-200 characters")
    if not text.strip():
        raise AssertionError("commit message must not be only white space")
    if "\n" in text or "\r" in text:
        raise AssertionError("commit message must be a single line")
    return text


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "output")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    data = validate(TEXT).encode("utf-8")
    with open(path, "wb") as f:
        f.write(data)
    # Read back and verify the written bytes match the intended text.
    with open(path, "rb") as f:
        written = f.read()
    assert written == data, "entry.txt content mismatch"
    # String-level round trip: the file must decode as UTF-8 to the
    # exact same commit message, with no trailing whitespace added.
    assert written.decode("utf-8") == TEXT, "entry.txt text mismatch"
    assert written == written.rstrip(), "entry.txt has trailing whitespace"
    print(path)
    print(len(data))
    print(hashlib.sha256(data).hexdigest())


if __name__ == "__main__":
    main()
