# htmlmark

> CLI tool that converts scraped HTML tables and lists into clean Markdown or CSV with configurable extraction rules.

---

## Installation

```bash
pip install htmlmark
```

Or install from source:

```bash
git clone https://github.com/yourname/htmlmark.git && cd htmlmark && pip install .
```

---

## Usage

```bash
# Convert an HTML file to Markdown
htmlmark convert input.html -o output.md

# Extract tables from a URL and export as CSV
htmlmark convert https://example.com/data --format csv -o table.csv

# Use a custom rules config file
htmlmark convert input.html --rules rules.yaml -o output.md
```

### Rules Config (rules.yaml)

```yaml
target: table          # table | ul | ol
selector: ".main-table"
skip_headers: false
strip_links: true
```

---

## Options

| Flag | Description |
|------|-------------|
| `--format` | Output format: `markdown` (default) or `csv` |
| `--rules` | Path to YAML config for extraction rules |
| `-o` | Output file path |
| `--selector` | CSS selector to target specific elements |

---

## License

This project is licensed under the [MIT License](LICENSE).