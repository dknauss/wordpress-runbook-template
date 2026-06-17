#!/usr/bin/env python3
"""Validate release metadata for a single-document documentation repository."""

from __future__ import annotations

import argparse
import re
import sys
from datetime import datetime
from pathlib import Path

MONTH_PATTERN = re.compile(
    r"^(January|February|March|April|May|June|July|August|September|October|November|December) ([1-9]|[12][0-9]|3[01]), (20[0-9]{2})$"
)
RELEASE_HEADING_PATTERN = re.compile(r"^## ([0-9]+\.[0-9]+(?:\.[0-9]+)?) — ((?:19|20)\d{2}-\d{2}-\d{2})$")


class ValidationError(Exception):
    """Metadata validation failed."""


def normalize_semver(version: str) -> str:
    version = version.strip()
    if not re.fullmatch(r"\d+\.\d+(?:\.\d+)?", version):
        raise ValidationError(f"Version is not semver-like: {version!r}")
    parts = version.split('.')
    if len(parts) == 2:
        parts.append('0')
    return '.'.join(str(int(part)) for part in parts)


def parse_frontmatter(markdown_path: Path) -> tuple[str, str]:
    text = markdown_path.read_text(encoding='utf-8')
    if not text.startswith('---\n'):
        raise ValidationError(f"Markdown file does not start with YAML frontmatter: {markdown_path}")
    version_match = re.search(r'(?m)^version:\s*["\']?([^"\'\n]+)["\']?\s*$', text)
    date_match = re.search(r'(?m)^date:\s*["\']?([^"\'\n]+)["\']?\s*$', text)
    if not version_match:
        raise ValidationError(f"Markdown frontmatter version not found: {markdown_path}")
    if not date_match:
        raise ValidationError(f"Markdown frontmatter date not found: {markdown_path}")
    return version_match.group(1).strip(), date_match.group(1).strip()


def validate_pretty_date(value: str) -> str:
    if not MONTH_PATTERN.fullmatch(value):
        raise ValidationError(f"Date is not in 'Month D, YYYY' form: {value!r}")
    return value


def iso_to_pretty(value: str) -> str:
    dt = datetime.strptime(value, '%Y-%m-%d')
    return f"{dt.strftime('%B')} {dt.day}, {dt.year}"


def parse_expected_date(value: str | None) -> str | None:
    if not value:
        return None
    value = value.strip()
    if re.fullmatch(r'(?:19|20)\d{2}-\d{2}-\d{2}', value):
        return iso_to_pretty(value)
    return validate_pretty_date(value)


def parse_release_headings(changelog_path: Path) -> list[tuple[str, str]]:
    releases: list[tuple[str, str]] = []
    for line in changelog_path.read_text(encoding='utf-8').splitlines():
        match = RELEASE_HEADING_PATTERN.match(line.strip())
        if match:
            version, iso_date = match.groups()
            releases.append((version, iso_to_pretty(iso_date)))
    if not releases:
        raise ValidationError(f"No release heading found in {changelog_path}")
    return releases


def parse_expected_tag(value: str | None) -> str | None:
    if not value:
        return None
    return normalize_semver(value.removeprefix('refs/tags/').removeprefix('v'))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--markdown', required=True, help='Primary Markdown file')
    parser.add_argument('--changelog', default='CHANGELOG.md', help='Changelog path')
    parser.add_argument('--expected-tag', help='Expected git tag such as v1.2.0')
    parser.add_argument('--expected-date', help='Expected release date, either YYYY-MM-DD or Month D, YYYY')
    parser.add_argument('--strict-changelog', action='store_true', help='Require the changelog to contain a release heading matching the current version and date')
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        raw_version, raw_date = parse_frontmatter(Path(args.markdown))
        pretty_date = validate_pretty_date(raw_date)
        normalized_version = normalize_semver(raw_version)
        releases = parse_release_headings(Path(args.changelog))
        latest_version, latest_date = releases[0]
        matching_release = None
        for release_version, release_date in releases:
            if normalize_semver(release_version) == normalized_version:
                matching_release = (release_version, release_date)
                break

        if args.strict_changelog:
            if not matching_release:
                raise ValidationError(
                    f"No changelog release heading matches frontmatter version {raw_version!r}"
                )
            if pretty_date != matching_release[1]:
                raise ValidationError(
                    f"Frontmatter date {raw_date!r} does not match changelog release date {matching_release[1]!r}"
                )

        expected_tag = parse_expected_tag(args.expected_tag)
        if expected_tag and normalized_version != expected_tag:
            raise ValidationError(
                f"Frontmatter version {normalized_version} does not match expected tag {expected_tag}"
            )

        expected_date = parse_expected_date(args.expected_date)
        if expected_date and pretty_date != expected_date:
            raise ValidationError(
                f"Frontmatter date {pretty_date!r} does not match expected release date {expected_date!r}"
            )

        print(f"OK   [Frontmatter version] raw={raw_version} normalized={normalized_version}")
        print(f"OK   [Frontmatter date] {pretty_date}")
        print(f"OK   [Latest changelog release] {latest_version} / {latest_date}")
        if matching_release:
            print(f"OK   [Matching changelog release] {matching_release[0]} / {matching_release[1]}")
        else:
            print(f"OK   [Matching changelog release] none for normalized version {normalized_version}")
        if expected_tag:
            print(f"OK   [Expected tag] {expected_tag}")
        if expected_date:
            print(f"OK   [Expected date] {expected_date}")
        print('Release metadata validation passed.')
        return 0
    except ValidationError as exc:
        print(f"FAIL {exc}", file=sys.stderr)
        return 1


if __name__ == '__main__':
    sys.exit(main())
