# Auto-Scholar

Auto-Scholar queries a Google Scholar profile and produces a single static HTML page of your publications. Entries are separated into journal and conference sections, your name is bolded in every author list, and each publication comes with a copyable BibTeX snippet.

## Features
- Fetch publications for any Google Scholar ID using `scholarly`..
- Highlight your name inside the author list.
- Generate “Copy BibTeX” buttons for quick citation grab.
- Group publications into journal and conference sections, sorted by year.
- Support custom HTML templates while shipping a polished default theme.

## Installation

### From PyPI (preferred once released)
```bash
pip install auto-scholar
```

### From source (currently supporting)
```bash
git clone https://github.com/KaziAmitHasan/auto_scholar.git
cd auto_scholar
python -m pip install --upgrade pip
python -m pip install -e .
```

## Usage

After installation the `auto-scholar` command becomes available:

```bash
auto-scholar --id 123456789 --name "Kazi Amit Hasan" --output publications.html
```

**Key options**
- `--id` *(required)* – Google Scholar ID (the last part of the profile URL). For example, in `https://scholar.google.com/citations?user=123456789&hl=en` the ID is `123456789`.
- `--name` *(required)* – Full name that should be bolded in author lists. For example 'Firstname lastname'
- `--output` – Output HTML file (defaults to `publications.html`).
- `--template` – Optional path to a custom HTML template containing `{content}`.
- `--proxy` – Enable a free proxy pool if Google starts throttling requests.

