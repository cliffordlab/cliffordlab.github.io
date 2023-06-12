#!/usr/bin/python3
"""
Reading the bibliography file bibliography/gdclifford.bib,
generate a Publications page for this website and save it to
`publications.md`.

Print them in this order:
    - article
    - conference and inproceedings
    - inbook
    - book
    - unpublished
    - misc
    - mastersthesis and phdthesis

"""
import pybtex.database
import urllib.parse # for escaping special characters in a URL, so I can make
                    # a download link...
from datetime import datetime
import codecs
import latexcodec

bibliography="./bibliography/gdclifford.bib"

def string2unicode(string):
    """Convert latex special characters to unicode."""
    return string.encode().decode('latex').replace('{','').replace('}','')

def make_download_link(title, link_text, content):
    """Return an HTML expression for a link saying `link_text` 
    that downloads a text file with title `title` and content `content`.
    """
    return f'<a download="{title}" href="data:application/txt,{urllib.parse.quote(content)}">{link_text}</a>'

def format_author_list(entry):
    """Return an author list: Lastname FI, Lastname FI, Lastname FI."""

    def first_initials(author):
        first_names=list(iter(author.rich_first_names))
        middle_names=list(iter(author.rich_middle_names))
        return "".join(n[0].render_as('markdown') for n in first_names + middle_names)

    def last_name(author):
        return " ".join(n.render_as('markdown') for n in author.rich_last_names)
        
    authors=entry.persons['author']
    return ", ".join(f"{last_name(a)} {first_initials(a)}" for a in authors)

def format_title(entry):
    """Return a title that (if it has a link) links to the url."""
    title=string2unicode(entry.fields['title'])
    if entry.type == 'inbook':
        title = f"\"{title}\" in *{entry.fields['booktitle']}*"
    elif entry.type == 'book':
        title = f"*{title}*"
    # otherwise, just leave it alone 
    
    # make a URL if we can
    if 'url' in entry.fields:
        title = f"[{title}]({entry.fields['url']})"
    
    return title

def format_journal_name(entry):
    """Format the name of the journal."""
    return f"{string2unicode(entry.fields['journal'])}"

def format_booktitle(entry):
    """Format the name of the booktitle."""
    return f"{string2unicode(entry.fields['booktitle'])}"

def format_issue_number(entry):
    """Format the issue number."""
    reference = ""
    if 'volume' in entry.fields:
        reference=entry.fields['volume']    
    if 'issue' in entry.fields:
        iss = entry.fields['issue']
        reference += f" ({iss})"
    return reference

def format_date(entry):
    """Year, then possibly month, then possibly day."""
    if 'date' in entry.fields:
        date_obj = datetime.strptime(entry.fields['date'], "%Y-%m-%d")
        return date_obj.strftime("%Y %B %d")
    datestring=entry.fields['year']
    
    if 'month' in entry.fields:
        datestring += f" {entry.fields['month']}"
        if 'day' in entry.fields:
            datestring += f" {entry.fields['day']}"
    return datestring

def format_doi_link(entry):
    """Return the entry's DOI as a link."""
    doi_number=entry.fields['doi']
    link="https://doi.org/" + urllib.parse.quote(doi_number)
    return f"[{doi_number}]({link})"

def format_pages(entry):
    """Format the page numbers."""
    if 'pages' not in entry.fields:
        return ""
    pages=entry.fields['pages']
    if '-' in pages or ',' in pages:
        return 'pp. ' + pages
    else:
        return 'p. ' + pages

def format_article(entry):
    """Format the entry assuming it's an article."""
    authors=format_author_list(entry)
    title=format_title(entry)
    journal=format_journal_name(entry)
    date=format_date(entry)
    numbers=format_issue_number(entry)
    pages=format_pages(entry)
    
    reference=f"{authors}. {title}. {journal} {date}"
    if numbers != "":
        reference += f"; {numbers}"
    if pages != "":
        reference += f": {pages}"
    reference += "."

    if 'doi' in entry.fields:
        reference += f" {format_doi_link(entry)}."
    
    return reference

def format_conference(entry):
    """Format the entry assuming it's a Conference citation."""
    authors=format_author_list(entry)
    title=format_title(entry)
    if 'booktitle' in entry.fields:
        booktitle=format_booktitle(entry)
    else:
        booktitle=format_journal_name(entry)
    date=format_date(entry)
    numbers=format_issue_number(entry)
    pages=format_pages(entry)
    
    reference=f"{authors}. {title}. {booktitle} {date}"
    if numbers != "":
        reference += f"; {numbers}"
    if pages != "":
        reference += f": {pages}"
    reference += "."

    if 'doi' in entry.fields:
        reference += f" {format_doi_link(entry)}."
    
    return reference

# format for inbook

def format_inbook(entry):
    """Format the entry assuming it's a citation for a chapter in a book."""
    authors=format_author_list(entry)
    title=format_title(entry)
    booktitle=format_booktitle(entry)
    date=format_date(entry)
    numbers=format_issue_number(entry)
    pages=format_pages(entry)
    
    reference=f"{authors}. {title}. {booktitle} {date}"
    if pages != "":
        reference += f": {pages}"
    reference += "."

    if 'doi' in entry.fields:
        reference += f" {format_doi_link(entry)}."
    
    return reference

# format for book
def format_book(entry):
    """author. title. publisher: date."""
    authors=format_author_list(entry)
    title=format_title(entry)
    publisher=entry.fields['publisher']
    date=format_date(entry)
    
    reference=f"{authors}. {title}. {date} {publisher}."

    if 'doi' in entry.fields:
        reference += f" {format_doi_link(entry)}."
    
    return reference

def format_incollection(entry):
    return format_inbook(entry)

def format_misc(entry):
    """author. title. howpublished. date."""
    author=format_author_list(entry)
    title=format_title(entry)
    howpublished=entry.fields['howpublished']
    date=format_date(entry)
    return f"{author}. {title}. {howpublished}. {date}."

def format_thesis(entry):
    """Author. Title. Type, year, school."""
    author=format_author_list(entry)
    title=format_title(entry)
    school=entry.fields['school']
    thesis_type=entry.fields['type']
    year=entry.fields['year']
    return f"{author}. {title}. {thesis_type}, {year}, {school}."

def format_entry(entry):
    """Format the given entry as a citation, depending on its type."""
    if entry.type == 'article':
        return format_article(entry)
    if entry.type == 'thesis':
        return format_thesis(entry)
    if entry.type == 'book':
        return format_book(entry)
    if entry.type == 'inbook':
        return format_inbook(entry)
    if entry.type == 'incollection':
        return format_incollection(entry)
    if entry.type == 'conference' or entry.type == 'inproceedings':
        return format_conference(entry)
    return format_misc(entry)

def add_section(file, title,publication_list):
    """Add the section to publications.md"""
    file.write(f"\n## {title}\n")
    file.write("\n|--|--|--|\n")
    for i, (key, entry) in publication_list:
        citation=format_entry(entry)
        link = make_download_link(f"{key}.bib",
                                  "BibTeX entry",
                                  entry.to_string('bibtex'))
        file.write(f"| {i} | {citation} | {link} |\n")

### ---------------------------
### MAIN BEHAVIOR OF THE SCRIPT
### ---------------------------

bib_data = pybtex.database.parse_file(bibliography)

publication_types={}

# separate the bibliography by categories
for (k,e) in bib_data.entries.items():
    if e.type not in publication_types:
        publication_types[e.type] = []
    publication_types[e.type].append((k,e))

# inproceedings same as conference; combine into conference
if 'conference' not in publication_types:
    publication_types['conference'] = []
if 'inproceedings' in publication_types:
    publication_types['conference'] += publication_types['inproceedings']
    del publication_types['inproceedings'] 

# combine books, chapters, incollection
if 'book' not in publication_types:
    publication_types['book'] = []
if 'inbook' in publication_types:
    publication_types['book'] += publication_types['inbook']
    del publication_types['inbook']
if 'incollection' in publication_types:
    publication_types['book'] += publication_types['incollection']
    del publication_types['incollection']

# finally, number each category in reverse chronological order
# (highest numbers first, lowest is 1)

def get_date(entry):
    if 'date' in entry.fields:
        # try parsing as yyyy-mm-dd format
        date = datetime.strptime(entry.fields['date'], '%Y-%m-%d')
        return date.year, date.month, date.day
    
    # parse year, month, and day individually
    year = int(entry.fields['year'])
    month = 1
    day = 1
    
    if 'month' in entry.fields:
        try:
            month = datetime.strptime(entry.fields['month'], '%b').month
        except ValueError:
            month = datetime.strptime(entry.fields['month'], '%B').month
    
    if 'day' in entry.fields:
        day = int(entry.fields['day'])
    
    return year, month, day

for t in publication_types:
    # sort the entries by date
    sorted_entries=sorted(list(publication_types[t]), key=lambda tup: get_date(tup[1]))
    # print them most recent first, numbered in descending order
    publication_types[t] = reversed(list(enumerate(sorted_entries, 1)))

with open("./publications.md", "w") as file:
    file.write("""---
layout: page
title: Publications
permalink: /publications
---
""")
    
    add_section(file,"Journal articles", publication_types['article'])
    add_section(file,"Conferences", publication_types['conference'])
    add_section(file,"Books and Chapters", publication_types['book'])
    add_section(file,"Other Material", publication_types['misc'])
    add_section(file,"Theses", publication_types['thesis'])
