# Auto-Scholar

Auto-Scholar is a tiny CLI that turns any Google Scholar profile into a polished static page. It fetches your publications, splits them into journal vs. conference lists, bolds your name in every author string, and injects copyable BibTeX blocks—complete with optional award badges.

## Features
- Fetch publications for any Scholar profile using `scholarly`, with an optional free-proxy rotation.
- Highlight the researcher’s name inside each author list.
- Render Bootstrap-styled HTML with BibTeX pop-up modals and clipboard support.
- Group and sort publications into journal and conference sections automatically.
- Support custom templates, navbar/footer includes, and a JSON-driven awards/badges system.

## Installation

> The package will be published on PyPI soon; for now install from source.

```bash
git clone https://github.com/KaziAmitHasan/auto_scholar.git
cd auto_scholar
python -m pip install --upgrade pip
python -m pip install -e .
```

## Quick Start

Once installed you get an `auto-scholar` command:

```bash
auto-scholar \
  --id t9ko5DMAAAAJ \
  --name "Kazi Amit Hasan" \
  --output research.html
```

The command writes `research.html` in the current directory. Place the output next to your existing static assets (`navbar.html`, `footer.html`, `css/main.css`, etc.) and you’re done.

### Finding your Google Scholar ID

1. Open your Google Scholar profile in a browser.  
2. Look at the URL— it should look like `https://scholar.google.com/citations?user=t9ko5DMAAAAJ&hl=en`.  
3. Copy the value after `user=` (here `t9ko5DMAAAAJ`) and use it as the `--id` argument. The rest of the URL parameters don’t matter.

### Key CLI options

| Flag | Description |
| --- | --- |
| `--id` | **Required.** Google Scholar ID (last part of the profile URL). |
| `--name` | **Required.** Full name to bold within author lists. |
| `--output` | Destination HTML file (default: `publications.html`). |
| `--template` | Path to a custom HTML template containing `{content}` and optional `{researcher_name}` placeholders. |
| `--awards-config` | Path to `awards.json` that describes badge metadata. When omitted, the tool looks for `./awards.json` and silently skips badges if the file isn’t found. |
| `--proxy` | Enable a free proxy pool if Google starts throttling requests. |

Example with awards and template overrides:

```bash
auto-scholar \
  --id t9ko5DMAAAAJ \
  --name "Kazi Amit Hasan" \
  --output research.html \
  --template templates/research.html \
  --awards-config config/awards.json \
  --proxy
```

## Awards & Badges

Place an `awards.json` file next to your run (or point `--awards-config` somewhere else). Titles are matched case-insensitively and punctuation-insensitively to your publications. If you don’t provide a file the tool simply omits award badges—everything else still renders normally.

```json
{
  "awards": [
    {
      "title": "Understanding Abandonment and Slowdown Dynamics in the Maven Ecosystem.",
      "badges": [
        { "label": "Best Presentation Award", "icon": "fa-trophy" }
      ]
    },
    {
      "title": "An empirical study on developers’ shared conversations with ChatGPT in GitHub pull requests and issues.",
      "badges": [
        { "label": "Co-First Author", "icon": "fa-user-friends" }
      ]
    }
  ]
}
```

Supported formats are flexible, you can also supply a dictionary of titles or a flat list of badge dictionaries. Icons refer to Font Awesome classes already included in the default template.

## Custom Templates & Assets

- **HTML template**: Provide a file with `{content}` (and optionally `{researcher_name}`) placeholders and pass it via `--template`. The generated publication markup will be injected into that slot.
- **Navbar/Footer**: The default theme expects `navbar.html`, `footer.html`, `css/main.css`, and `js/main.js` to live alongside the generated page. Feel free to remove or customize those includes inside your template.


## License

MIT © Kazi Amit Hasan
