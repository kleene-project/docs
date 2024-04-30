---
title: Contributing guidelines
description: Guidelines for contributing to Kleene's docs
keywords: contribute, guide, style guide
---

The online docs have been generated from the `main` branch, therefore you must
create pull requests against the `main` branch to update the docs.

There are two ways to contribute a pull request to the docs repository:

1. You can click **Edit this page** option  in the right column of every page on [https://kleene.dev/](/).

    This opens the GitHub editor, which means you don't need to know a lot about Git, or even about Markdown. When you save, Git prompts you to create a fork if you don't already have one, and to create a branch in your fork and submit the pull request.

2. Fork the [docs GitHub repository]({{ site.repo }}). Suggest changes or add new content on your local branch, and submit a pull request (PR) to the `main` branch.

    This is the manual, more advanced version of clicking 'Edit this page' on a published docs page. Initiating a docs changes in a PR from your own branch gives you more flexibility, as you can submit changes to multiple pages or files under a single pull request, and even create new topics.

Have a look at some of the `.md` files to see how to make a header for a new
page. Also, `/_data/toc.yaml` defines the left-hand navigation for the docs.

## Files not edited here

Most of Klee and Kleened's reference docs are genereated from their
repositories so pull requests against these files vil be rejected.

This concerns:

- `engine/api/kleened-*.yaml` files
- `_data/engine-cli/*.yaml` files

## Pull request guidelines

Help us review your PRs more quickly by following these guidelines.

- Try not to touch a large number of files in a single PR if possible.
- Don't change whitespace or line wrapping in parts of a file you are not editing for other reasons.
  Make sure your text editor is not configured to automatically reformat the whole file when saving.
- We highly recommend that you build and test the docs locally before submitting
  a PR.

## Build and preview the docs locally

Start by installing Jekyll using
[Jekyll's installation instructions](https://jekyllrb.com/docs/installation/).

Then clone the docs repo, build the documentation and serve it using Jekyll's
own dev webserver

```console
$ git clone https://github.com/kleene-project/docs.git
$ cd docs
$ bundle exec jekyll serve
                    done in 18.942 seconds.
 Auto-regeneration: enabled for '/path/to/kleene-docs'
    Server address: http://127.0.0.1:4000
  Server running... press ctrl-c to stop.
```

Voila! It's time to preview changes. Note that every time changes have been made
to the docs, Jekyll rebuilds the static site.
