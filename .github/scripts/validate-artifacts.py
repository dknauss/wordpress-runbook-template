#!/usr/bin/env python3
"""Smoke-check generated PDF, EPUB, and DOCX artifacts."""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path
from typing import Iterable
from xml.etree import ElementTree as ET
from zipfile import ZipFile


FULL_TITLE = "WordPress Operations Runbook"
SHORT_TITLE = "WordPress Operations Runbook"
CANONICAL_TOKENS = (
    "Table of Contents",
    "Conventions",
    "Purpose",
    "Verification",
    "[CUSTOMIZE:",
)
PARITY_PHRASES = (
    FULL_TITLE,
    "Conventions",
    "Purpose",
    "Verification",
    "Dashboard",
    "WP-CLI",
    "[CUSTOMIZE:",
)


class ValidationError(Exception):
    """Artifact validation failed."""


def normalize_text(text: str) -> str:
    text = text.replace("\u2019", "'")
    text = text.replace("\u2014", "-")
    text = text.replace("\u2013", "-")
    return re.sub(r"\s+", " ", text).strip()


def assert_contains(text: str, tokens: Iterable[str], label: str) -> None:
    haystack = normalize_text(text).casefold()
    missing = [token for token in tokens if normalize_text(token).casefold() not in haystack]
    if missing:
        raise ValidationError(f"{label} missing expected text: {', '.join(missing)}")


def ensure_exists(path: Path, label: str) -> None:
    if not path.is_file():
        raise ValidationError(f"{label} not found: {path}")
    if path.stat().st_size <= 0:
        raise ValidationError(f"{label} is empty: {path}")
    print(f"OK   [{label}] exists ({path.stat().st_size} bytes)")


def extract_pdf_text(path: Path) -> str:
    try:
        result = subprocess.run(
            ["pdftotext", str(path), "-"],
            check=True,
            capture_output=True,
            text=True,
        )
    except FileNotFoundError as exc:
        raise ValidationError("pdftotext is required but was not found on PATH") from exc
    except subprocess.CalledProcessError as exc:
        stderr = exc.stderr.strip() or "unknown error"
        raise ValidationError(f"pdftotext failed for {path}: {stderr}") from exc

    if not result.stdout.strip():
        raise ValidationError(f"pdftotext produced no text for {path}")
    return result.stdout


def validate_pdf(path: Path) -> None:
    ensure_exists(path, "PDF")
    text = extract_pdf_text(path)
    assert_contains(text, (FULL_TITLE, SHORT_TITLE, "Version 3.1", *CANONICAL_TOKENS), "PDF")
    print("OK   [PDF] canonical text markers found")
    return text


def extract_xml_text(xml_bytes: bytes) -> str:
    root = ET.fromstring(xml_bytes)
    return " ".join(text for text in root.itertext() if text and text.strip())


def validate_docx(path: Path) -> None:
    ensure_exists(path, "DOCX")
    with ZipFile(path) as archive:
        required = (
            "[Content_Types].xml",
            "_rels/.rels",
            "docProps/core.xml",
            "word/document.xml",
        )
        for member in required:
            if member not in archive.namelist():
                raise ValidationError(f"DOCX missing required member: {member}")

        core = ET.fromstring(archive.read("docProps/core.xml"))
        ns = {"dc": "http://purl.org/dc/elements/1.1/"}
        title = core.findtext("dc:title", namespaces=ns)
        if normalize_text(title or "") != normalize_text(FULL_TITLE):
            raise ValidationError(f"DOCX title metadata mismatch: {title!r}")

        document_text = extract_xml_text(archive.read("word/document.xml"))
        assert_contains(document_text, ("Conventions", "Purpose", "Verification"), "DOCX")

    print("OK   [DOCX] structure, metadata, and canonical text markers found")
    return document_text


def validate_epub(path: Path) -> None:
    ensure_exists(path, "EPUB")
    with ZipFile(path) as archive:
        mimetype = archive.read("mimetype").decode("utf-8", errors="ignore").strip()
        if mimetype != "application/epub+zip":
            raise ValidationError(f"EPUB mimetype mismatch: {mimetype!r}")

        required = (
            "META-INF/container.xml",
            "EPUB/content.opf",
            "EPUB/nav.xhtml",
        )
        for member in required:
            if member not in archive.namelist():
                raise ValidationError(f"EPUB missing required member: {member}")

        opf = ET.fromstring(archive.read("EPUB/content.opf"))
        ns = {"dc": "http://purl.org/dc/elements/1.1/"}
        title = opf.findtext(".//dc:title", namespaces=ns)
        if normalize_text(title or "") != normalize_text(FULL_TITLE):
            raise ValidationError(f"EPUB title metadata mismatch: {title!r}")

        xhtml_members = [name for name in archive.namelist() if name.endswith(".xhtml")]
        if not xhtml_members:
            raise ValidationError("EPUB contains no XHTML content files")

        epub_text = []
        for member in xhtml_members:
            epub_text.append(extract_xml_text(archive.read(member)))
        joined_text = " ".join(epub_text)
        assert_contains(joined_text, ("WordPress Operations Runbook", *CANONICAL_TOKENS), "EPUB")

    print("OK   [EPUB] structure, metadata, and canonical text markers found")
    return joined_text


def validate_markdown(path: Path) -> str:
    ensure_exists(path, "Markdown")
    text = path.read_text(encoding="utf-8")
    assert_contains(text, ("WordPress Operations Runbook", "Conventions", "Dashboard", "WP-CLI", "[CUSTOMIZE:"), "Markdown")
    print("OK   [Markdown] canonical text markers found")
    return text


def validate_cross_format_parity(texts: dict[str, str]) -> None:
    for label, text in texts.items():
        assert_contains(text, PARITY_PHRASES, label)
    print(f"OK   [Parity] canonical phrases match across {len(texts)} formats")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--markdown", default="WP-Operations-Runbook.md", help="Markdown source path")
    parser.add_argument("--pdf", default="WP-Operations-Runbook.pdf", help="PDF artifact path")
    parser.add_argument("--epub", default="WP-Operations-Runbook.epub", help="EPUB artifact path")
    parser.add_argument("--docx", default="WP-Operations-Runbook.docx", help="DOCX artifact path")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        texts = {
            "Markdown": validate_markdown(Path(args.markdown)),
            "PDF": validate_pdf(Path(args.pdf)),
            "EPUB": validate_epub(Path(args.epub)),
            "DOCX": validate_docx(Path(args.docx)),
        }
        validate_cross_format_parity(texts)
    except ValidationError as exc:
        print(f"FAIL {exc}", file=sys.stderr)
        return 1

    print("All artifact and parity checks passed (4 formats).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
