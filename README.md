# still

**still** is a super-minimal static site generator designed for small personal blogs.  
It converts Markdown files into simple HTML pages using Python's `markdown` module and combines them with a header and footer to produce fast, portable, brutally minimal websites.

The goal of still is to make it **as simple as possible to publish a blog**.

---

## Features

- Minimal — just Markdown, HTML, and a build script
- Fast — builds in milliseconds
- Simple file structure
- Front-matter-style metadata for posts (`title`, `date`)
- Auto-generated homepage with post list
- Static output to `/public` (ready to upload anywhere)
- Bring-your-own CSS
- Optional RSS feed generation

---

## Project Structure

```
.
├── still.py
├── content
│   ├── index.md
│   └── posts
│       └── test.md
└── include
    ├── footer.html
    ├── header.html
    ├── img
    └── style.css
```

---

## Post Metadata Format

Each post includes a small metadata block at the top:

```markdown
<!--
title: My First Post
date: 2025-01-01
-->

Post content starts here...
```
- `title` — used as the post title + homepage link text
- `date` — used for sorting + display. Should be in `YYYY-MM-DD` format.

---

## Usage

Install Python's `markdown` module

Build the site:
`python still.py`

The generated HTML files will appear in:
`public/`

---

## Roadmap / Ideas

- favicon, sitemap
- pagination
- subdirectories

## License
MIT
