#!/usr/bin/python
# 
#  make_publications_page.py
#  ------------------------
#  Read the `.bib` files under `./bibliography/`, and generate a publications
#  page at `./publications.md`. The citation style is roughly Vancouver, but
#  without abbreviating journal titles (too much work to automate), and without
#  abbreviating the list of authors.
# 
#  The title should link to the url in the url field, and there is also a button that
#  reveals a selectable bibtex file.
#  
#  Quality is not guaranteed, so this script is quite forgiving---as long as the
#  BiBTeX parses, it should produce _something_.
# 
#  Publications go in this order:
#    - article
#    - conference papers
#    - books and chapters
#    - preprints
#    - patents
#    - misc
#    - theses 

from pybtex.database import parse_file
from pybtex.scanner import TokenRequired
import codecs
import latexcodec
import dateutil.parser
import os.path
import re

def string2unicode(string):
    """Convert latex special characters to unicode, just in case."""
    return string.encode().decode('latex').replace('{','').replace('}','')

def write_front_matter(output_file_descriptor, page_title=None):
    """Write the front matter of a GitHub Pages publications page to the given
    file, and write the given string as the title."""

    if page_title is None:
        raise ValueError("page_title was not given!")

    copyright_notice=" ".join(['\n<div class="smalltextblock">Papers on this site',
                               'are presented to ensure timely dissemination of',
                               'scholarly and technical work. Copyright and all',
                               'rights therein are retained by authors or by',
                               'other copyright holders. All persons copying',
                               'this information are expected to adhere to the',
                               "terms and constraints invoked by each author's",
                               'copyright. In most cases, these works may not be',
                               'reposted without the explicit permission of the',
                               'copyright holder.</div>\n'])

    output_file_descriptor.write("\n".join(["---",
                                            "layout: page",
                                            f"title: {page_title}",
                                            f"permalink: /{page_title.lower()}",
                                            "---\n",
                                            copyright_notice]))


def format_author_list(entry):
    """Given a pybtex entry, return an author list: Lastname FM, Lastname F,
    Lastname FM, ...

    Note that this bakes in some false assumptions about human names.

        https://www.kalzumeus.com/2010/06/17/falsehoods-programmers-believe-about-names/

    However, we're already given (possibly empty) lists of first names, middle
    names, and last names, for each author. We'll just have to use them.
    """

    def first_initials(author):
        first_names=list(iter(author.rich_first_names))
        middle_names=list(iter(author.rich_middle_names))
        return "".join(n[0].render_as('html') for n in first_names + middle_names)

    def last_name(author):
        return " ".join(n.render_as('html') for n in author.rich_last_names)

    def formatted_name(author):
        ln = last_name(author)
        fi = first_initials(author)
        return " ".join([ln, fi])

    authors=entry.persons['author']
    return ", ".join(formatted_name(a) for a in authors)

def format_title(entry):
    """Return a title which is a hyperlink (if the entry has a link).
    If the entry has a link AND and abstract, use the abstract as hover text.
    """
    title=string2unicode(entry.fields['title'])
    # books and chapters look a little different.
    if entry.type == 'inbook' or entry.type == 'incollection':
        booktitle=string2unicode(entry.fields['booktitle'])
        title = f"\"{title}\" in "+f"<i>{booktitle}</i>"
    elif entry.type == "book":
        title = f"<i>{title}</i>"

    # make it a URL if we can
    if 'url' in entry.fields:
        title = f"<a href=\"{entry.fields['url']}\">{title}</a>"

    return title

def format_journal_name(entry):
    """Format the name of the journal."""
    if 'journal' in entry.fields:
        return string2unicode(entry.fields['journal'])
    return ""

def format_booktitle(entry):
    """Format the title of the book."""
    if 'booktitle' in entry.fields:
        return string2unicode(entry.fields['booktitle'])
    return ""

def format_month(entry):
    """People enter the month in all sorts of formats.
    Always print the full name of the month."""
    if 'month' not in entry.fields['month']:
        return ""

    month=entry.fields['month'].lower()[:3] # first 0 to 3 characters
    # compare with '1' and 'jan', '2' and 'feb', and so on
    for num, monthname in enumerate(["January",
                                     "February",
                                     "March",
                                     "April",
                                     "May",
                                     "June",
                                     "July",
                                     "August",
                                     "September",
                                     "October",
                                     "November",
                                     "December"], start=1):
        if month in [str(num), monthname.lower()[:3]]:
            return monthname

def get_date(entry):
    """Retrieve a sortable datetime object from the entry, substituting defaults
    if necessary. The default year is 0001, the default month is January,
    and the default day is the 1st.

    """
    default_date=dateutil.parser.parse("0001 Jan 1")
    if 'date' in entry.fields:
        try:
            date_obj=dateutil.parser.parse(entry.fields['date'])
            return date_obj
        except dateutil.parser._parser.ParserError as e:
            return default_date
    else:
        date_pieces=[]
        if 'year' in entry.fields:
            date_pieces.append(entry.fields['year'])
            if 'month' in entry.fields:
                date_pieces.append(entry.fields['month'])
                if 'day' in entry.fields:
                    date_pieces.append(entry.fields['day'])
        if date_pieces == []:
            return None
        return dateutil.parser.parse(" ".join(date_pieces), default=default_date)

def format_date(entry):
    """Format the date as a string: year, then possibly month, then possibly
    day."""
    if 'date' in entry.fields:
        date_obj=get_date(entry)
        # this object may have defaults substituted in, so let's look at
        # the original field
        date_elements = entry.fields['date'].split('-')
        if len(date_elements) == 1:
            return date_elements[0] # year, or 'No Date'
        if len(date_elements) == 2:
            return date_obj.strftime("%Y %B")
        if len(date_elements) == 3:
            return date_obj.strftime("%Y %B %-d")
        else:
            return "No Date"

    # otherwise, look for these other fields
    date_elements=[]
    if 'year' in entry.fields:
        date_elements.append(entry.fields['year'])
        if 'month' in entry.fields:
            # hard to parse depending on the format
            month_obj=dateutil.parser.parse(entry.fields['month'])
            # use the full name of the month:
            date_elements.append(month_obj.strftime("%B"))
            if 'day' in entry.fields:
                date_elements.append(entry.fields['day'])
    return " ".join(date_elements)

def format_issue_number(entry):
    """Format the issue number."""
    volume, issue, number = ("", "", "")
    if 'volume' in entry.fields:
        volume = entry.fields['volume']
    if 'issue' in entry.fields:
        issue = entry.fields['issue']
    if 'number' in entry.fields:
        number = entry.fields['number']

    issnum=",".join([i for i in [issue, number] if i!=''])
    if issnum != "":
        issnum = f"({issnum})"
    return string2unicode(" ".join([i for i in [volume, issnum] if i!='']))

def format_pages(entry):
    """Format the page numbers."""
    if 'pages' not in entry.fields:
        return ""
    pages = entry.fields['pages']

    if '-' in pages or ',' in pages:
        return 'pp. ' + pages
    else:
        return 'p. ' + pages

def entry_is_patent(entry):
    """True iff the entry is a patent."""
    if 'howpublished' in entry.fields:
        if re.search("patent", entry.fields['howpublished']):
            return True
    return False

def format_doi(entry):
    """Render a DOI link if one exists. Otherwise, return an empty string."""
    if 'doi' not in entry.fields:
        return ""
    # sometimes people include the full url. we strip this off, and keep the
    # last block of the form [something]/[something].
    doi_entry="/".join(entry.fields['doi'].split('/')[:2])
    return f"DOI: <a href=\"https://doi.org/{doi_entry}\">{doi_entry}</a>"

def render_citation(entry):
    """Render an Entry object as citation in HTML, with a clickable link."""

    # I'm not gonna lie, I didn't feel like learning to use the pybtex formatting,
    # so I'm just formatting it myself by pulling the required fields out.

    # common elements
    author_list=format_author_list(entry)
    title=format_title(entry)
    date=format_date(entry)
    doi=format_doi(entry)

    if entry_is_patent(entry):
        # authors. title. howpublished. date. doi.
        howpublished=entry.fields['howpublished']
        reference_elements=[author_list, title, howpublished, date, doi]

    elif entry.type == "article":
        # authors. title. journal date; volume(number): pages. doi.
        journal=format_journal_name(entry)
        numbers=format_issue_number(entry)
        pages=format_pages(entry)
        numbers_pages=': '.join([e for e in [numbers, pages] if e!=""])
        journal_date=' '.join([e for e in [journal, date] if e!=""])
        journal_date_numbers_pages="; ".join([e for e in [journal_date, numbers_pages] if e!=""]) 
        reference_elements=[author_list, title, journal_date_numbers_pages, doi]

    elif entry.type == "inbook" or entry.type == "incollection":
        # authors. title. date: pages. doi.
        pages=format_pages(entry)
        reference_elements=[author_list, title, date, pages, doi]

    elif entry.type == "book":
        # authors. title. publisher: date. doi.
        publisher=""
        if 'publisher' in entry.fields:
            publisher=entry.fields['publisher']
        publisher_date=": ".join([e for e in [publisher, date] if e != ""])
        reference_elements=[author_list, title, publisher_date, doi]

    elif entry.type == "conference" or entry.type == "inproceedings":
        # authors. title. booktitle date; numbers: pages. doi.
        numbers=format_issue_number(entry)
        pages=format_pages(entry)
        numbers_pages=": ".join([e for e in [numbers, pages] if e != ""])
        booktitle=""
        if 'booktitle' in entry.fields:
            booktitle=entry.fields['booktitle']
        booktitle_date=" ".join([e for e in [booktitle, date] if e != ""])
        booktitle_date_numbers_pages="; ".join([e for e in [booktitle_date, numbers_pages] if e != ""])
        reference_elements=[author_list, title, booktitle_date_numbers_pages, doi]
    elif entry.type == "thesis":
        # authors. title. type, date, school. doi.
        thesis_type=""
        if 'type' in entry.fields:
            thesis_type=entry.fields['type']
        school=""
        if 'school' in entry.fields:
            school=entry.fields['school']
        type_date_school=", ".join([e for e in [thesis_type, date, school] if e != ""]) 
        reference_elements=[author_list, title, type_date_school, doi]
    else:
        # authors. title. date. howpublished. doi.
        howpublished=""
        if 'howpublished' in entry.fields:
            howpublished=entry.fields['howpublished']
        reference_elements=[author_list, title, date, howpublished, doi]

    if reference_elements == []:
        return ""

    joined_string=". ".join([e for e in reference_elements if e!=""]) + "."
    # change ?. -> ?
    return re.sub(r"\?((<[^>]*>)*)\.", r"?\1", joined_string)

def render_bibtex(entry):
    """Print this entry in BibTeX."""
    return entry.to_string('bibtex')

def add_citation_row(number, unique_citation_id, entry, fd):
    """Given a file descriptor fd, print a table row with the given numbered citation to it, in HTML.
    
    The table will look like this:
    | 1. | citation here     |
    |    | [show BibTeX]     |
    
    And when the button is clicked, it will look like this:
    | 1. | bibtex source here |
    |    | [show citation]    |

    (Click the button again to toggle it back.)

    """
    # the easy part: the number
    fd.write(f"<tr>\n<td>{number}</td>\n")

    # the harder part: adding the citation
    fd.write(f'<td><div class="citation_container">\n')
    # toggle checkbox (hidden)
    fd.write(f'<input type="checkbox" class="toggle-button" id="{unique_citation_id}">\n')

    # -- rendered Vancouver-style citation
    fd.write('<div class="citation">\n')
    fd.write(f'{render_citation(entry)}\n')
    fd.write('</div>\n')

    # -- selectable bibtex citation
    fd.write('<div class="bibtex_source">')
    # -- -- make it a code block
    fd.write(f'<pre>{render_bibtex(entry)}</pre>\n')
    fd.write('</div>') # close the bibtex_source div

    # -- now add labels for the toggle checkbox
    fd.write("\n".join(['<div class="showbibtex">',
                        f'<label for="{unique_citation_id}">[show BibTeX]</label>',
                        '</div>',
                        '<div class="hidebibtex">',
                        f'<label for="{unique_citation_id}">[show citation]</label>',
                        '</div>']))

    fd.write('</div>') # close citation_container
    fd.write('</td>')  # close the table cell
    fd.write('</tr>')  # close the table row

def add_section(section_title, bibtex_file_path, output_fd):
    """Add the given section to the given output file descriptor,
    based on the bibliography in bibtex_file_path.

    If the file doesn't exist, treat that as empty.

    """
    # do nothing if the section is empty.
    if not os.path.isfile(bibtex_file_path):
        return

    # parse the bibliography file for this section
    try:
        bib_data = parse_file(bibtex_file_path)
    except TokenRequired as tkr:
        print(f"Token required in file {bibtex_file_path}!")
        raise tkr

    # Now bib_data.entries is a dictionary mapping bibtex identifiers 
    # (e.g. LisetteCorbin_2023_12_01_Acomparison) to Entry objects, which
    # in turn consist of
    # - a type entry.type ('article')
    # - a dictionary entry.fields mapping bibtex fields to their values
    # - a dictionary entry.persons (we're only interested in 
    #     persons['author'], which is a list of Person objects).

    # sort (identifier,Entry) pairs by date:
    sorted_entries=sorted(list(bib_data.entries.items()), key=lambda tup: get_date(tup[1]))
    # number them in reverse chronological order, with the highest numbers
    # and most recent publications at the start of the list
    publications_list=reversed(list(enumerate(sorted_entries, 1)))

    # write the section header
    print(f"Adding {section_title}...")
    fd.write(f"\n## {section_title}\n")

    # add the beginning of the table
    fd.write("\n<table>\n")

    for number, id_entry in publications_list:
        # add each citation as a row in the table
        unique_citation_id, entry = id_entry
        add_citation_row(number, unique_citation_id, entry, output_fd)
    # add the end of the table
    fd.write("\n</table>\n")

if __name__ == "__main__":

    # specify variables
    output_file='./publications.md'
    bibliography_location='./bibliography'

    # write the header and title
    with open(output_file, 'w') as fd:
        write_front_matter(fd, page_title="Publications")

        # add each section from the corresponding 
        for section, bibfile in [("Journal Articles", "articles.bib"),
                                 ("Conferences", "conferences.bib"),
                                 ("Preprints", "preprints.bib"),
                                 ("Books and Chapters", "books_and_chapters.bib"),
                                 ("Patents", "patents.bib"),
                                 ("Theses", "theses.bib"),
                                 ("Other", "other.bib")]:
            add_section(section, f"{bibliography_location}/{bibfile}", fd)
