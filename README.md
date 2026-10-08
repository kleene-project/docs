# Kleene's website source code

This is the source for [Kleene's website](https://kleene.dev).

The site is built with [MkDocs](https://www.mkdocs.org/) using the
[Material for MkDocs](https://squidfunk.github.io/mkdocs-material/) theme.
The `klee` command reference pages are generated at build time from YAML files
produced by the [klee](https://github.com/kleene-project/klee) repository, and
the Kleened API reference is rendered with [redoc](https://redocly.com/redoc/)
from Kleened's OpenAPI spec.

## Building locally

```console
$ python3 -m venv .venv
$ .venv/bin/pip install -r requirements.txt
$ .venv/bin/mkdocs serve
```

The site is then available at http://127.0.0.1:8000/.

See the ['Contribute' section](https://kleene.dev/contribute/overview/) to know
more about how to contribute.
