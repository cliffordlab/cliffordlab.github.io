# Bibliography

The Publications page on this site is automatically generated
from a BibTeX file at `bibliography/gdclifford.bib`. Entries
are automatically organized by category,
and sorted chronologically within each category.

## Initial setup

If you are editing this website, run `./init.sh` before the first
time you commit. This script adds a commit hook to the local repository,
at `.git/hooks/pre-commit`. You don't need to interact with this file at all;
this will simply ensure that `pre-commit` gets executed before
committing changes.
In turn, `pre-commit` does the following actions:

    1. Attempt to generate `publications.md` from the bibliography at `bibliography/gdclifford.bib`.
    2. If the publications list was successfully created, add it to the commit.

The effect of this is that *you don't have to touch the publications page*,
even to add it when it's changed. Both updating it and adding it
are automated. All you need to do is edit `gdclifford.bib`, then
add it to your next commit.

## Currently supported citation types

Currently, these will be cited:

### Journal articles

**article.** Required fields: `author`, `title`, `journal`, and either `date` or `year`.

### Conferences

**conference.** Required fields: `author`, `title`, either `journal` or `booktitle`, and either `date` or `year`.

**inproceedings.** This is currently treated the same as `conference`.

### Books and Chapters

**book.** Required fields: `author`, `title`, `publisher`, and either `date` or `year`.

**inbook.** Required fields: `author`, `title`, `booktitle`, and either `date` or `year`.

**incollection.** This is currently treated the same as `inbook`.

### Other Material

**misc.** Required fields: `author`, `title`, `howpublished`, and either `date` or `year`.

### Theses

**thesis.** Required fields: `author`, `title`, `school`, `type`, `year`.

## How to add a publication

- **Get a BibTeX citation for the publication.** These can be downloaded from
  Google Scholar, the library website, the journal, or another academic
  database. Optionally, you can edit the `url`, `doi`, and `date` fields.
  
  - `url`: ideally, link to a publicly available full-text source for the publication.
  - `doi`: give it in the form `number/number`, rather than `https://doi.org/number/number`.
  - `date`: by default, most of these sources just give `year`.
    If you know the exact date, you can specify it in year-month-day format
    in a `date` field: e.g., 
    replace `year={2023}` with `date={2023-06-23}`.
    If you know the year and the month, you can add it in a `month` field,
    e.g., `month=Jun`.
    Entries are sorted by the available date information in the bibtex file.

- **Add this citation to `gdclifford.bib`.** Make sure it doesn't use the same
    key as another entry already in the bibliography.

- **Try running `make_bibliography.py`.** If it can't parse the file, it will crash and hopefully give
    a useful error message.

## How to change the citation style

In `make_bibliography.py`, edit the functions with the prefix
`format`: for instance,
`format_entry`,
`format_thesis`,
`format_misc`, and so on.

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
