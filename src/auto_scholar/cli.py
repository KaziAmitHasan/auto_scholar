"""Command-line entry point for the auto-scholar tool."""

from __future__ import annotations

import argparse
from typing import Sequence

from .builder import generate_page


def build_parser() -> argparse.ArgumentParser:
    """Define CLI arguments for the auto-scholar tool."""
    parser = argparse.ArgumentParser(
        description="Generate a publications HTML page from Google Scholar.",
    )
    parser.add_argument(
        "--id",
        dest="scholar_id",
        required=True,
        help="Google Scholar ID (e.g. wX4le_QAAAAJ).",
    )
    parser.add_argument(
        "--name",
        dest="researcher_name",
        required=True,
        help='Researcher full name to highlight (e.g. "Yuan Tian").',
    )
    parser.add_argument(
        "--output",
        default="publications.html",
        help="Output HTML path (default: publications.html).",
    )
    parser.add_argument(
        "--template",
        help="Path to a custom HTML template file containing '{content}'.",
    )
    parser.add_argument(
        "--proxy",
        action="store_true",
        help="Use a free proxy pool to reduce the chance of Google blocking the requests.",
    )
    return parser


def main(argv: Sequence[str] | None = None) -> None:
    """Parse CLI arguments and delegate to the builder."""
    parser = build_parser()
    args = parser.parse_args(argv)

    generate_page(
        scholar_id=args.scholar_id,
        researcher_name=args.researcher_name,
        output_path=args.output,
        template_path=args.template,
        use_proxy=args.proxy,
    )


if __name__ == "__main__":
    main()
