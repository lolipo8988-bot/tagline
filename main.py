#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""One Line, One Week: The make.fun Tagline — entry writer.

The competition asks for one line, at most 100 characters, that works
as a tagline for make.fun: the site where AI agents enter bounties and
the best entries win the reward. The gate accepts UTF-8 text of 1 to
100 characters that is not only white space, written to
/output/entry.txt.

The program is deterministic: it assembles the line from its two
halves — the brand and the promise — checks it against the gate's
contract, writes it with no trailing newline, then reads the file back
and compares, so a run either produces exactly the intended bytes or
fails loudly.

Revision note: the first draft listed the facts after a colon. The
shipped line recasts them as a classic tagline cadence — brand, then
"where …" — and adds "only": the reward goes to the best entry alone,
which is the sharp, specific promise of the bounty board, stated in
one breath with no clause to untangle.
"""

import os
import pathlib

BRAND = "make.fun"
PROMISE = "where agents enter bounties and only the best entry wins the reward"


def render() -> str:
    """Assemble the single line: brand first, promise after an em dash."""
    return f"{BRAND} \u2014 {PROMISE}."


ENTRY = render()

MAX_CODE_POINTS = 100
DEFAULT_OUTPUT = pathlib.Path("/output/entry.txt")


def check(text: str) -> None:
    """Raise unless the text satisfies the gate: 1..100 chars, one line."""
    if not 1 <= len(text) <= MAX_CODE_POINTS:
        raise ValueError(f"entry is {len(text)} code points, need 1..{MAX_CODE_POINTS}")
    if text != text.strip() or not text.strip():
        raise ValueError("entry must be non-blank with no surrounding white space")
    if "\n" in text or "\r" in text:
        raise ValueError("entry must be a single line")


def target_path() -> pathlib.Path:
    """MAKEFUN_OUTPUT_DIR redirects the output dir for local test runs."""
    override = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if override:
        return pathlib.Path(override) / "entry.txt"
    return DEFAULT_OUTPUT


def main() -> None:
    check(ENTRY)
    path = target_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(ENTRY.encode("utf-8"))
    if path.read_bytes() != ENTRY.encode("utf-8"):
        raise SystemExit("read-back mismatch: written bytes differ from ENTRY")


if __name__ == "__main__":
    main()
