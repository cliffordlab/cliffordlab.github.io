#!/usr/bin/python3
"""
Using the bibliographies under `bibliography/`, generate a Publications page
for this website and save it to `publications.md`.

The bibliographies are separated by category:
    - bibliography/journals.bib (journals)
    - bibliography/reviews_editorials.bib (reviews and editorials)
    - bibliography/educational.bib (manuals, videos, computer programs, teaching aids)
    - bibliography/conferences.bib (conference proceedings)
    - bibliography/other.bib (miscellaneous)
    - bibliography/theses.bib (theses)

"""
import pybtex.database
from inspect import getmembers

# categories of publication
JOURNAL="Journal"
REVIEW="Reviews and Editorials"
EDUCATION="Manuals, Videos, Computer Programs, and Other Teaching Aids"
CONFERENCE="Conferences"
BOOK="Books and Chapters"
OTHER="Other Materials"
THESIS="Theses"

bibliography = { JOURNAL: 
                    "./bibliography/journals.bib",
                 REVIEW:
                    "./bibliography/reviews_editorials.bib",
                 EDUCATION:
                    "./bibliography/educational.bib",
                 CONFERENCE:
                    "./bibliography/conferences.bib",
                 BOOK:
                    "./bibliography/books.bib",
                 OTHER:
                    "./bibliography/other.bib",
                 THESIS:
                    "./bibliography/theses.bib" 
                }

def format_author(entry):
    """Returns an author string in markdown format for a Vancouver-style citation."""
    def first_initials(author):
        first_names = list(iter(author.first_names))
        middle_names = list(iter(author.middle_names))
        return "".join(n[0] for n in first_names + middle_names)
    def last_name(author):
        return " ".join(author.last_names)
    authors = list(iter(entry.persons['author']))
#    if len(authors) >= 6:
#        a = authors[0]
#        author_string = f"{last_name(a)} {first_initials(a)} et al. "
    if len(authors) == 1:
        a = authors[0]
        author_string = f"{last_name(a)} {first_initials(a)}. "
    else:
        first_authors=", ".join([f"{last_name(a)} {first_initials(a)}" for a in authors[:-1]])
        last_author=f"{last_name(authors[-1])} {first_initials(authors[-1])}"
        author_string = first_authors + ", and " + last_author + ". "
    return author_string

def format_title(entry):
    """Return a string in markdown format
    with the title, linking to the URL."""
    title=entry.fields['title']
    if entry.type == 'inbook':
        # then the title is a chapter title
        title = "“" + title + "” in *" + entry.fields['booktitle'] + "*"
    elif entry.type == 'book':
        # the title is a book title
        title = "*" + title + "*"
    # otherwise just leave it alone

    # make a url if we can
    if 'url' in entry.fields:
        title = f"[{title}]({entry.fields['url']})"

    return title

def format_pages(pages):
    """Add either p. or pp. to the page numbers."""
    if '-' in pages or ',' in pages:
        return 'pp. ' + pages
    else:
        return 'p. ' + pages 

def format_journal_name(entry):
    """Return a string in markdown format with
    journal date;volume(issue):pages"""
    journal = entry.fields['journal']
    year = entry.fields['year']
    if 'volume' in entry.fields:
        vol = f"{entry.fields['volume']}"
    else:
        vol = ""
    if 'issue' in entry.fields:
        iss = f"({entry.fields['issue']})"
    else:
        iss = ""
    voliss = "".join([vol,iss])
    return " ".join([journal, year, voliss])

def make_download_link(title, content):
    """Return an HTML expression for a link that downloads a text file
    with title `title` and content `content`."""
    return ('<a download="{{title}}" href="data:application/txt,{{content}}">BibTeX entry</a>'.replace("{{title}}", title)).replace("{{content}}", content)

def format_bibtex_entry(index, entry):
    """Return a formatted bibtex entry as a download link."""
    string = entry.to_string('bibtex')
    string = (string.replace('"', "'")).replace('\n', '')
    filename = next(iter(entry.persons['author'])).last_names[0] + "_" + entry.fields['year'] + "_" + f"{index}" + ".bib"
    return make_download_link(filename, string)

def format_journal_article(entry):
    """Returns a correctly cited journal article."""
    refstring = "".join([format_author(entry),
                         format_title(entry),
                         ". ",
                         format_journal_name(entry)])

    if 'pages' in entry.fields:
        refstring += ", "+format_pages(entry.fields['pages'])
    refstring += "."
    if 'doi' in entry.fields:
        refstring += " DOI: "+entry.fields['doi']
    return refstring

def format_publisher(entry):
    if 'address' in entry.fields:
        return entry.fields['address'] + "; " + entry.fields['publisher']
    else:
        return entry.fields['publisher']

def format_book(entry):
    """Format a book or a chapter in a book as a citation."""
    refstring = "".join([format_author(entry),
                         format_title(entry),
                         ". ",
                         format_publisher(entry),
                         "; ",
                         entry.fields['year']])
    if entry.type == 'inbook':
        refstring += ". " + format_pages(entry.fields['pages'])
    refstring += "."
    return refstring

def format_education(entry):
    refstring = "".join([format_author(entry),
                         format_title(entry),
                        ". "])
    if 'institution' in entry.fields:
        refstring += entry.fields['institution'] + " "
    if 'howpublished' in entry.fields:
        refstring += entry.fields['howpublished'] + " "
    refstring += entry.fields['year'] + '.'
    return refstring

def format_other(entry):
    refstring="".join([format_author(entry),
                      format_title(entry),
                      ". ",
                      entry.fields['howpublished'],
                      ", ",
                      entry.fields['year'],
                      "."])
    return refstring

def format_thesis(entry):
    refstring = "".join([format_author(entry),
                         format_title(entry),
                         ". ",
                         entry.fields['type'],
                         ": ",
                         entry.fields['school'],
                         ", ",
                         entry.fields['year'],
                         "."])
    return refstring

def format_citation(publication_type, entry):
    if publication_type == JOURNAL:
        return format_journal_article(entry)
    elif publication_type == REVIEW:
        return format_journal_article(entry) # change this if needed
    elif publication_type == BOOK:
        return format_book(entry)
    elif publication_type == EDUCATION:
        return format_education(entry)
    elif publication_type == CONFERENCE:
        return format_journal_article(entry) # change this if needed
    elif publication_type == OTHER:
        return format_other(entry) 
    elif publication_type == THESIS:
        return format_thesis(entry)
    return "Not sure how to cite this yet."

with open("./publications.md", "w") as file:
    file.write("""---
layout: page
title: Publications
permalink: /publications
---
""")

    for publication_type, filepath in bibliography.items():
        print(f"Type: {publication_type}. Filepath: {filepath}")
        file.write(f"\n## {publication_type}\n")
        file.write("\n|--|--|--|\n")
        bib_data = pybtex.database.parse_file(filepath)
        # Number them in reverse chronological order by category (highest numbers first)
        entries = reversed(list(enumerate(reversed(list(bib_data.entries.items())),start=1)))
        for i, (key, entry) in entries:
            citation = format_citation(publication_type, entry)
            link = format_bibtex_entry(i, entry)
            file.write(f"| {i} | {citation} | {link} |\n")
