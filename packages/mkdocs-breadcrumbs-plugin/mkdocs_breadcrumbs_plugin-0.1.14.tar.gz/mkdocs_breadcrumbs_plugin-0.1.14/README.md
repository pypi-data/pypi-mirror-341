# mkdocs-breadcrumbs-plugin

Mkdocs location-based breadcrumbs navigation.

These directly get prepended to rendered Markdown.

![screenshot](https://github.com/mihaigalos/mkdocs-breadcrumbs-plugin/raw/main/screenshots/mkdocs-breadcrumbs-plugin.png)

## Setup

Install the plugin using pip:

```bash
pip install mkdocs-breadcrumbs-plugin
```

Activate the plugin in `mkdocs.yaml`:

```yaml
plugins:
  - mkdocs-breadcrumbs-plugin:
      delimiter: " / "  # separator between sections
      log_level: "WARNING"  # "DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"
      exclude_paths:
        - "docs/mkdocs/**"
        - "docs/mkdocs"   # avoid generating index.md
      additional_index_folders:
        - temp_dir
      generate_home_index: false
      use_page_titles: true # use page title instead of path in breadcrumbs
      home_text: "Home"
```

## Development

### Running Tests

To run the tests, use the following command:

```bash
pytest
```
