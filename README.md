# Bibliography

The Publications page on this site is automatically generated
from a collection of BibTeX files under `bibliography/`.
Entries are organized into category by file, and 
sorted chronologically within each category.

Most of the citations come from [Gari Clifford's Google Scholar profile](https://scholar.google.com/citations?user=VwYoZ6gAAAAJ), with many additions and corrections. The scholar page is checked routinely
via a GitHub Action, which calls `./download_bibliography.py` to
download new entries using [SerpAPI](https://serpapi.com/).
Citations are never downloaded twice, so this makes fewer than 10 API queries a month,
unless the Clifford Lab is extraordinarily prolific that month.

## Initial setup

If you are editing this website, run `./init.sh` before the first
time you commit. This script adds a commit hook to the local repository,
at `.git/hooks/pre-commit`. You don't need to interact with this file at all;
this will simply ensure that `pre-commit` gets executed before
committing changes.
In turn, `pre-commit` does the following actions:

1. Attempt to generate `publications.md` from the bibliography files.
2. If the publications list was successfully created, add it to the commit.

The effect of this is that *you don't have to touch the publications page*,
even to add it when it's changed. Both updating it and adding it
are automated. All you need to do is edit the bibliography files, add those,
commit those, and presto! the publications page is also generated and
included in the commit.

## Currently supported citation types

Currently, these will be cited:

### Journal Articles

  - **article.** Required fields: `author`, `title`, `journal`, and either `date` or `year`.

### Conference Papers

  - **conference.** Required fields: `author`, `title`, either `journal` or `booktitle`, and either `date` or `year`.
  - **inproceedings.** This is currently treated the same as `conference`.

### Books and Chapters

  - **book.** Required fields: `author`, `title`, `publisher`, and either `date` or `year`.
  - **inbook.** Required fields: `author`, `title`, `booktitle`, and either `date` or `year`.
  - **incollection.** This is currently treated the same as `inbook`.

### Other Material (including Patents)

  - **misc.** Required fields: `author`, `title`, `howpublished`, and either `date` or `year`.

### Theses

  - **thesis.** Required fields: `author`, `title`, `school`, `type`, `year`.

## How to add a publication

- **Get a BibTeX citation for the publication.** These can be downloaded from
  Google Scholar, the library website, the journal, or another academic
  database. Optionally, you can edit the `url`, `doi`, and `date` fields.
  
  - `url`: ideally, link to a publicly available full-text source for the publication.
  - `doi`: give it either in the form `number/number`, or `https://doi.org/number/number`.
  - `date`: by default, most of these sources just give `year`.
    If you know the exact date, you can specify it in year-month-day format
    in a `date` field: e.g., 
    replace `year={2023}` with `date={2023-06-23}`.
    If you know the year and the month, you can add it in a `month` field,
    e.g., `month=Jun`.
    Entries are sorted by the available date information in the bibtex file.

- **Add this citation to the bibliography.** Also, make sure it doesn't use the same
    key as another entry already in the bibliography.

- **Try running `make_publications_page.py`.**
   If it can't parse the file, it will crash and hopefully give a useful error message.

## How to fix a wrong citation

To fix a wrong citation, you can edit the BibTeX entry directly. Since this entry will not be redownloaded,
your changes will persist.

To find the BibTeX entry:
- On the site, click “\[show BibTeX\]” and note the BibTeX key.
- Search for the BibTeX key in the `.bib` file under `bibliography` corresponding to the section.

Or if you're very impatient, you can enter `bibliography` in the command line and run
```
grep -br `<some words from the citation>` --ignore-case
```
(with no angle-brackets), and you should see which file and where it is.

## How to remove a citation entirely

Delete the citation from its BibTeX file. If it was automatically downloaded from Google Scholar, make sure that its **Google Scholar citation ID** is still listed in `bibliography/do_not_download_these_citations.txt`. Its BibTeX key will be included in the comment:
```
<citation_id> # <BibTeX key>
```
You may want to move it to the `MANUALLY SKIPPED` section, just to avoid confusing anyone else down the line (including yourself).

## How to restore a citation to the version in Google Scholar

Delete the citation's Google Scholar citation ID from `bibliography/do_not_download_these_citations.txt`.

## How to change the citation style

In `make_publications_page.py`, edit the function `render_citation`.

# Theme

The theme of this website is [Minima](https://jekyll.github.io/minima/),
with customizations. Minima is distributed with the MIT License:

```
The MIT License (MIT)

Copyright (c) 2016-present Parker Moore and the minima contributors

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
```
