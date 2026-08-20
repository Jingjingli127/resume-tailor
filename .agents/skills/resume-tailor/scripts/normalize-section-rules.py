#!/usr/bin/env python3
"""Normalize existing section-heading paragraph rules in a DOCX."""

from __future__ import annotations

import argparse
from copy import deepcopy
from pathlib import Path

from docx import Document
from docx.oxml import OxmlElement
from docx.oxml.ns import qn


def bordered_paragraphs(document):
    matches = []
    for paragraph in document.paragraphs:
        p_pr = paragraph._p.get_or_add_pPr()
        p_bdr = p_pr.find(qn("w:pBdr"))
        if p_bdr is not None and p_bdr.find(qn("w:bottom")) is not None:
            matches.append(paragraph)
    return matches


def set_zero_horizontal_indents(paragraph):
    p_pr = paragraph._p.get_or_add_pPr()
    ind = p_pr.find(qn("w:ind"))
    if ind is None:
        ind = OxmlElement("w:ind")
        p_pr.append(ind)
    ind.set(qn("w:left"), "0")
    ind.set(qn("w:right"), "0")
    ind.set(qn("w:firstLine"), "0")
    ind.attrib.pop(qn("w:hanging"), None)


def normalize(input_path: Path, output_path: Path) -> int:
    document = Document(input_path)
    headings = bordered_paragraphs(document)
    if not headings:
        raise ValueError("No paragraphs with bottom borders were found.")

    canonical = deepcopy(headings[0]._p.get_or_add_pPr().find(qn("w:pBdr")))
    for paragraph in headings:
        p_pr = paragraph._p.get_or_add_pPr()
        existing = p_pr.find(qn("w:pBdr"))
        if existing is not None:
            p_pr.remove(existing)
        p_pr.insert(0, deepcopy(canonical))
        set_zero_horizontal_indents(paragraph)

    document.save(output_path)
    return len(headings)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("input", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    count = normalize(args.input, args.output)
    print(f"Normalized {count} section rules.")


if __name__ == "__main__":
    main()
