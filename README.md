# My README File

## Setup

```bash
sudo apt install bundler
cd ~/github/AI4you
bundle config set --local path 'vendor/bundle'
bundle
bundle exec jekyll serve --livereload
```

## Custom Theme Customizations

This site uses the minimal-mistakes theme with several customizations:

### Table of Contents (TOC) Depth Control

**File:** `_layouts/single.html`

The TOC depth can be controlled per-post using the `toc_max` front matter parameter:

```yaml
---
toc: true
toc_label: "Contents"
toc_icon: "list"
toc_sticky: true
toc_max: 2  # Shows only h1 and h2 headings (default: 6)
---
```

- `toc_max: 2` - Shows only `#` and `##` headings
- `toc_max: 3` - Shows `#`, `##`, and `###` headings
- `toc_max: 6` - Shows all heading levels (default if not specified)

**Implementation:** Modified `_layouts/single.html` to use `h_max={{ page.toc_max | default: 6 }}`

### Mermaid Diagram Support

**File:** `_includes/head/custom.html`

Mermaid diagrams are supported by loading the mermaid.js library. Use them in posts with:

```markdown
<div class="mermaid">
graph LR
    A[Start] --> B[End]
</div>
```

### Custom Metadata Fields

**Files:** 
- `_includes/page__meta.html` - Display complexity and target_audience in header
- `_data/ui-text.yml` - Labels for custom fields

Posts support additional metadata fields:

```yaml
---
complexity: advanced  # beginner, intermediate, advanced
target_audience: "Python developers and AI enthusiasts"
---
```

These fields display in the post header after the read time estimate.

### Custom Styling

**File:** `_sass/_additional.scss`

Custom SCSS for:
- Background image with opacity
- Site-specific styling overrides

Import is handled in `assets/css/main.scss` via `@import "additional";`

