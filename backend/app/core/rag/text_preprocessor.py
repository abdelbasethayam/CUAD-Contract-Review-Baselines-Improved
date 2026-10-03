"""Lightweight text preprocessing for CUAD clause classification.

Applied before embedding and before prompt construction. Goals:
- reduce surface noise that hurts retrieval and small/medium LMs
- expand common legal abbreviations so semantic matchers see full forms
- keep the transformation deterministic and reversible in spirit
"""
from __future__ import annotations

import re
from typing import Final


_WS_RE: Final = re.compile(r"\s+")
_MULTI_PUNCT_RE: Final = re.compile(r"([.!?]){2,}")

# Conservative expansions only; do not invent meaning.
_ABBREVIATIONS: Final[dict[str, str]] = {
    r"\bincl\.\b": "including",
    r"\bexcl\.\b": "excluding",
    r"\bw/\b": "with",
    r"\bw/o\b": "without",
    r"\be\.g\.\b": "for example",
    r"\bi\.e\.\b": "that is",
    r"\betc\.\b": "etcetera",
    r"\bvs\.\b": "versus",
    r"\bart\.\b": "article",
    r"\bsec\.\b": "section",
    r"\bpara\.\b": "paragraph",
    r"\bapprox\.\b": "approximately",
    r"\bmax\.\b": "maximum",
    r"\bmin\.\b": "minimum",
}


def normalize_whitespace(text: str) -> str:
    text = text.replace("\u00a0", " ").replace("\t", " ")
    text = _WS_RE.sub(" ", text)
    return text.strip()


def normalize_quotes(text: str) -> str:
    return (
        text.replace("“", '"')
        .replace("”", '"')
        .replace("‘", "'")
        .replace("’", "'")
    )


def expand_legal_abbreviations(text: str) -> str:
    out = text
    for pattern, replacement in _ABBREVIATIONS.items():
        out = re.sub(pattern, replacement, out, flags=re.IGNORECASE)
    return out


def collapse_repeated_punctuation(text: str) -> str:
    return _MULTI_PUNCT_RE.sub(r"\1", text)


def preprocess_clause(text: str, *,
                      expand_abbrevs: bool = True,
                      normalize: bool = True) -> str:
    """Return a cleaned clause suitable for embedding and prompting.

    Parameters
    ----------
    text:
        Raw clause text (may contain OCR / PDF extraction artifacts).
    expand_abbrevs:
        Whether to expand a small set of common legal abbreviations.
    normalize:
        Whether to normalize whitespace and quotes.
    """
    if not text:
        return ""
    out = str(text)
    if normalize:
        out = normalize_quotes(out)
        out = normalize_whitespace(out)
        out = collapse_repeated_punctuation(out)
    if expand_abbrevs:
        out = expand_legal_abbreviations(out)
        if normalize:
            out = normalize_whitespace(out)
    return out


__all__ = [
    "preprocess_clause",
    "normalize_whitespace",
    "normalize_quotes",
    "expand_legal_abbreviations",
]
