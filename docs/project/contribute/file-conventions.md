---
title: Source file conventions
description: How new .md files should be formatted
---

## File name

When you create a new .md file for new content, make sure: 
- File names are as short as possible
- Try to keep the file name to one word or two words
- Use a dash to separate words. For example:
        - `add-seats.md`  and `remove-seats.md`.
        - `multiplatform-images` preferred to `multi-platform-images`.

## Frontmatter

The front-matter of a given page is in a section at the top of the Markdown
file that starts and ends with three hyphens. It includes YAML content.
The title and description are required.

| Key         | Required | Description                                                                                    |
|-------------|----------|------------------------------------------------------------------------------------------------|
| title       | yes      | The page title. This is added to the HTML output as a `<h1>` level header.                     |
| description | yes      | A sentence that describes the page contents. This is added to the HTML metadata. It's not rendered on the page. |
| hide        | no       | A YAML list of page elements to hide (`toc`, `navigation`).                                     |

Here's an example of a valid (but contrived) page metadata. The order of
the metadata elements in the front-matter isn't important.

```yaml
---
title: Kleened installation
description: Describes the Kleened installation steps
---
```

## Navigation

A new page must also be added to the navigation in `docs/SUMMARY.md`, or the
build fails (the site is built in strict mode). Place the entry in the section
matching the page's location in the `docs/` directory.

## Body

The body of the page starts after the frontmatter.

### Text length

Splitting long lines (preferably up to 80 characters) can make it easier to provide feedback on small chunks of text.
