"""Core implementation for generating a publications page from Google Scholar."""

from __future__ import annotations

import random
import time
from pathlib import Path
from typing import Iterable

from scholarly import ProxyGenerator, scholarly

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>My Research</title> <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/3.4.1/css/bootstrap.min.css">
    <link href="https://fonts.googleapis.com/css?family=Open+Sans:300,400,400i,600,700" rel="stylesheet">
    <link href="https://fonts.googleapis.com/css?family=Montserrat:400,400i,500,500i,600" rel="stylesheet">
    <link rel="stylesheet" href="https://use.fontawesome.com/releases/v5.8.1/css/all.css">
    <link rel="stylesheet" href="https://cdn.rawgit.com/jpswalsh/academicons/master/css/academicons.min.css">
    <style>
        body { padding-top: 20px; }
        .pub-tag {
            display: inline-block;
            margin-right: 8px;
            font-size: 12px;
            font-weight: 600;
            color: #fff;
            padding: 3px 10px;
            border-radius: 12px;
            vertical-align: middle;
            font-family: 'Montserrat', sans-serif;
        }
        .pub-tag .fas {
            margin-right: 4px;
        }
        .pub-tag.journal {
            background-color: #007bff;
        }
        .pub-tag.conference {
            background-color: #28a745;
        }
        .copy-btn {
            background: none;
            border: none;
            color: #007bff;
            cursor: pointer;
            padding: 0 3px;
            font-size: 12px;
        }
        .copy-btn:hover {
            text-decoration: underline;
        }
        pre.bibtex-source {
            display: none;
        }
    </style>
    </head>
<body class="page-justified">
    <div class="spacer-div-3 hidden-xs hidden-xs"></div>
    <div id="main-container" class="container">
        <div class="row">
            <div class="col-sm-12">
                <h1>Research</h1>

                {content}

            </div>
        </div>
    </div>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/jquery/3.3.1/jquery.min.js"></script>
    <script src="https://stackpath.bootstrapcdn.com/bootstrap/3.4.1/js/bootstrap.min.js" integrity="sha384-aJ21OjlMXNL5UyIl/XNwTMqvzeRMZH2w8c5cRVpzpU8Y5bApTppSuUkhZXN0VxHd" crossorigin="anonymous"></script>
    <script>
    document.addEventListener('DOMContentLoaded', function() {
        document.querySelectorAll('.copy-btn').forEach(copyButton => {
            copyButton.addEventListener('click', function() {
                const codeId = this.getAttribute('data-copy');
                const codeElement = document.getElementById(codeId);
                if (!codeElement) {
                    console.error('Missing BibTeX source for button', codeId);
                    return;
                }

                const codeText = codeElement.textContent;
                const originalLabel = this.textContent;

                navigator.clipboard.writeText(codeText).then(() => {
                    this.textContent = 'Copied!';
                    this.disabled = true;
                    setTimeout(() => {
                        this.textContent = originalLabel;
                        this.disabled = false;
                    }, 2000);
                }).catch(err => {
                    console.error('Failed to copy text: ', err);
                });
            });
        });
    });
    </script>
</body>
</html>
"""


def setup_proxy() -> None:
    """Configure a free proxy to slow down Google Scholar rate limiting."""
    print("Setting up proxy...")
    proxy_generator = ProxyGenerator()
    success = proxy_generator.FreeProxies()

    if not success:
        print("Warning: No proxy found. Scholarly may be blocked.")
        return

    scholarly.use_proxy(proxy_generator)
    print("Proxy setup complete.")


def format_authors(authors_str: str | None, researcher_name: str) -> str:
    """Format the author string while bolding the researcher's name."""
    if not authors_str:
        return "No Author"

    authors_list = [author.strip().strip(",") for author in authors_str.split(" and ")]

    formatted_authors: list[str] = []
    for author in authors_list:
        if not author:
            continue
        if researcher_name in author:
            formatted_authors.append(f"<b>{author}</b>")
        else:
            formatted_authors.append(author)

    if len(formatted_authors) > 1:
        return ", ".join(formatted_authors[:-1]) + " and " + formatted_authors[-1]
    if formatted_authors:
        return formatted_authors[0]
    return "No Author"


def create_html_for_entry(
    publication: dict,
    counter: int,
    paper_type: str,
    researcher_name: str,
) -> str:
    """Render a single publication list item with the BibTeX snippet."""
    bib_data = publication.get("bib", {})
    authors = bib_data.get("author", "No Author")
    title = bib_data.get("title", "No Title")
    year = bib_data.get("pub_year", "")
    venue = bib_data.get(
        "journal",
        bib_data.get("conference", bib_data.get("citation", "No Venue")),
    )

    if year and venue.endswith(f", {year}"):
        venue = venue[: -len(f", {year}")]
    elif year and venue.endswith(f" {year}"):
        venue = venue[: -len(f" {year}")]

    publication_url = publication.get("pub_url", "#")
    code_id = f"code{counter}"

    try:
        first_author_lastname = authors.split(" ")[0].lower().strip(",")
        first_title_word = title.split(" ")[0].lower()
        citation_key = f"{first_author_lastname}{year}{first_title_word}"
    except Exception:  # pragma: no cover - defensive catch for malformed data
        citation_key = f"pub{counter}"

    bib_type = "@misc"
    venue_field = f"howpublished = {{{venue}}}"

    if "journal" in bib_data:
        bib_type = "@article"
        venue_field = f"journal = {{{venue}}}"
        if "volume" in bib_data:
            venue_field += f",\n  volume = {{{bib_data['volume']}}}"
        if "number" in bib_data:
            venue_field += f",\n  number = {{{bib_data['number']}}}"
        if "pages" in bib_data:
            venue_field += f",\n  pages = {{{bib_data['pages']}}}"
    elif "conference" in bib_data:
        bib_type = "@inproceedings"
        venue_field = f"booktitle = {{{venue}}}"
        if "publisher" in bib_data:
            venue_field += f",\n  publisher = {{{bib_data['publisher']}}}"
        if "pages" in bib_data:
            venue_field += f",\n  pages = {{{bib_data['pages']}}}"
    elif "citation" in bib_data:
        bib_type = "@misc"
        venue_field = f"note = {{{venue}}}"
        if "publisher" in bib_data:
            venue_field += f",\n  publisher = {{{bib_data['publisher']}}}"
        if "pages" in bib_data:
            venue_field += f",\n  pages = {{{bib_data['pages']}}}"

    raw_bibtex = f"""{bib_type}{{{citation_key},
  author = {{{authors}}},
  title = {{{title}}},
  {venue_field},
  year = {{{year}}}
}}"""

    bibtex_html = f"""
        [<button data-copy="{code_id}" class="copy-btn">BibTex</button>]
        <pre id="{code_id}" class="bibtex-source">{raw_bibtex}</pre>
    """

    tag_html = ""
    if paper_type == "journal":
        tag_html = '<span class="pub-tag journal"><i class="fas fa-book-open"></i> Journal</span>'
    elif paper_type == "conference":
        tag_html = '<span class="pub-tag conference"><i class="fas fa-users"></i> Conference</span>'

    return f"""
    <li>
       {tag_html} {format_authors(authors, researcher_name)}. <i>{title}.</i>
        <a href="{publication_url}" target="_blank">{venue}</a>, {year}.
        {bibtex_html}
    </li>
    """


def _build_section_content(entries: Iterable[str], heading: str) -> str:
    """Wrap a group of entries with a heading and ordered list."""
    items = "".join(entries)
    return f'<h3 class="push-down-4"><span>{heading}</span></h3>\n<ol>\n{items}\n</ol>\n'


def generate_page(
    scholar_id: str,
    researcher_name: str,
    output_path: str | Path = "publications.html",
    template_path: str | Path | None = None,
    use_proxy: bool = False,
) -> Path:
    """Fetch publications for scholar_id and write an HTML summary page."""
    if use_proxy:
        setup_proxy()
    else:
        print("Skipping proxy setup. If you get blocked, re-run with --proxy.")

    print(f"Fetching author profile for ID: {scholar_id}...")
    try:
        author = scholarly.search_author_id(scholar_id, filled=False)
        author = scholarly.fill(author, sections=["publications"])
    except Exception as error:  # pragma: no cover - depends on external API
        raise RuntimeError(f"Could not fetch author profile: {error}") from error

    print(f"Found author: {author['name']}")

    publications = author.get("publications", [])
    if not publications:
        raise RuntimeError("No publications found for this author.")

    print(f"Found {len(publications)} publications. Fetching details...")

    journal_entries: list[tuple[str, str]] = []
    conference_entries: list[tuple[str, str]] = []

    for index, publication in enumerate(publications, start=1):
        try:
            filled_publication = scholarly.fill(publication, sections=["bib"])
            bib_data = filled_publication.get("bib", {})
            title_preview = bib_data.get("title", "No Title")[:30]
            print(f"  - Processing pub {index}/{len(publications)}: {title_preview}...")

            paper_type = "journal" if "journal" in bib_data else "conference"
            html_entry = create_html_for_entry(
                filled_publication,
                index,
                paper_type,
                researcher_name,
            )

            publication_year = bib_data.get("pub_year", "0")
            if paper_type == "journal":
                journal_entries.append((publication_year, html_entry))
            else:
                conference_entries.append((publication_year, html_entry))

            time.sleep(random.uniform(1.0, 2.5))
        except Exception as error:  # pragma: no cover - defensive logging
            print(f"Warning: Could not process one publication. {error}")

    journal_entries.sort(key=lambda entry: entry[0], reverse=True)
    conference_entries.sort(key=lambda entry: entry[0], reverse=True)

    content = ""
    if journal_entries:
        content += _build_section_content(
            (entry for _, entry in journal_entries),
            "Peer Reviewed Journal Publications",
        )
    if conference_entries:
        content += _build_section_content(
            (entry for _, entry in conference_entries),
            "Peer Reviewed Conference Publications",
        )

    if not content:
        content = "<p>No publications available.</p>"

    template_text = HTML_TEMPLATE
    if template_path:
        template_file = Path(template_path)
        print(f"Loading custom template from {template_file}...")
        try:
            template_text = template_file.read_text(encoding="utf-8")
            if "{content}" not in template_text:
                print("Warning: Custom template missing '{content}' placeholder. Using default template.")
                template_text = HTML_TEMPLATE
        except Exception as error:  # pragma: no cover - I/O handling
            print(f"Warning: Could not load custom template. Using default. {error}")
            template_text = HTML_TEMPLATE

    full_page_html = template_text.replace("{content}", content)

    output = Path(output_path)
    output.write_text(full_page_html, encoding="utf-8")

    print(f"Successfully generated {output}!")
    return output
