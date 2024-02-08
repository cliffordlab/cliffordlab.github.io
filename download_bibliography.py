#!/usr/bin/python3
# 
#  download_bibliography.py
#  ------------------------
#  Pull the citations from the Google Scholar page for Gari Clifford, and
#  save them in bibtex format under `./bibliography/`. Divide the files up
#  by type.

#  Ignore all citations with IDs in the file defined by `SKIP_CITATION_LIST`
#  (a constant at the top of this script).
# 
#  Before using this script, please define the environment variable
#  `SERPAPI_KEY`: the API key for the SerpApi service, which lets us download
#  from the google scholar page programmatically.

import os
import re
from pylatexenc.latexencode import UnicodeToLatexEncoder
from serpapi import GoogleSearch

# Constants 
AUTHOR_ID              = "VwYoZ6gAAAAJ" # Google Scholar ID for Gari Clifford
API_KEY_ENV_VARIABLE   = "SERPAPI_KEY"
SKIP_CITATION_LIST     = "./bibliography/do_not_download_these_citations.txt"

# It would be nice to use argparse and pass various other things as
# parameters, such as the author ID and so on. Maybe later.

def load_citation_ids_to_skip(path_to_list):
    """Read the given file of citation IDs to skip, and return them as a set."""
    ids_to_skip=set()
    with open(path_to_list, 'r') as listf:
        lines = listf.readlines()
    for line in lines:
        # strip out comments, which are anything after a hashtag,
        # and get rid of leading and trailing space.
        id_to_skip = re.sub('#.*$', '', line).strip()
        # each line will either be blank or something to skip
        if id_to_skip != "":
            ids_to_skip.add(id_to_skip)
    return ids_to_skip


def scholar_page_items():
    """Iterator over items on the Scholar page.

    The Scholar page has abbreviated citations, but not full bibliographic
    data---so we still have to request each one with an additional step, if we
    want it. The way to do that is to use `download_citation`, below.
    """

    # go in batches of 100, sorted by publication date (most recent to earliest).
    start_index=0 
    while True:
        # parameters expected by serpapi, defining the search
        params = {
            "api_key": os.environ[API_KEY_ENV_VARIABLE],
            "engine": "google_scholar_author",
            "hl": "en",
            "author_id": AUTHOR_ID,
            "sort": "pubdate",
            "num": "100",
            "start": f"{start_index}"
        }
        search = GoogleSearch(params) # costs API usage (possibly money)
        results = search.get_dict()

        # eventually we run out of pages
        if 'articles' not in results:
            return
        # otherwise, we can return these results (don't worry about 'articles':
        # that's what Google Scholar calls it, even if it's something else)
        for item in results['articles']:
            yield item

        # next 100 results
        start_index += 100

def get_citation_id(item_from_scholar_page):
    """Get the citation ID for the given item from the Google Scholar
    page.
    """
    # the input is a dictionary, and it's the second element under
    # 'citation_id'.
    return item_from_scholar_page['citation_id'].split(':')[1]

def download_citation(citation_id):
    """Request the citation with the given ID from Google Scholar. Return it as a dictionary.
    """
    params = {
        "engine":       "google_scholar_author",
        "view_op":      "view_citation",
        "citation_id":  f"{AUTHOR_ID}:{citation_id}",
        "api_key":      os.environ[API_KEY_ENV_VARIABLE]
    }
    search = GoogleSearch(params) # costs API usage (possibly money)
    results = search.get_dict()
    return results['citation']

def choose_bibtex_citation_type(citation):
    """Determine the type of bibtex file the given citation
    should be saved as. The options are:

       article
       inproceedings
       inbook
       misc
       unpublished

    There are some additional types (book, mastersthesis, manual), but these
    are hard to detect from Google's output, and they come infrequently
    enough that we can edit the types manually when they do appear.

    For more information on bibtex citation types, see the bibtex site:

       https://www.bibtex.com/e/entry-types/

    """
    # putting this first, because some preprint citations
    # show up as journal articles or conference papers
    if is_patent(citation):
        return "misc" # these will still be placed in patents.bib
    if 'journal' in citation:
        return "article" # even if it's a preprint
    if 'book' in citation:
        return "inbook" 
    if 'conference' in citation:
        return "inproceedings"
    if is_preprint(citation): # articles without the journal go in unpublished
        return "unpublished"
    return "misc"

def is_patent(citation):
    """Determine whether to file this item as a patent."""
    return ('inventors' in citation or
            'patent_office' in citation or
            'patent_number' in citation)

def is_preprint(citation):
    """Determine whether to file this item as a preprint."""
    for field in ['journal', 'booktitle', 'conference', 'publisher']:
        # if any of these contain 'arxiv' or 'medrxiv' or 'preprint',
        # return True
        if field in citation:
            publication_lc=citation[field].lower()
            if (re.search('preprint', publication_lc) or
                re.search('arxiv', publication_lc) or
                re.search('medrxiv', publication_lc)):
                    return True
    return False

def get_bibfile_location(citation_type, citation):
    """Return which file a citation of the given type
    should be saved to. The options are

        articles.bib
        books_and_chapters.bib
        conferences.bib
        other.bib
        patents.bib
        preprints.bib
        theses.bib

    (all under ./bibliography/).

    """
    # some of these are 'unpublished', others aren't
    if is_preprint(citation):
        bibliography='preprints'
    elif is_patent(citation):
        bibliography="patents"
    # otherwise, judge by the citation type
    else:
        match citation_type:
            case 'article':
                bibliography='articles'
            case 'book' | 'inbook':
                bibliography='books_and_chapters'
            case 'inproceedings':
                bibliography='conferences'
            case 'manual' | 'misc' :
                bibliography='other'
                # we have to figure out if it's a patent or not
                bibliography='other'
            case 'mastersthesis' | 'phdthesis':
                bibliography='theses'
            case 'unpublished':
                bibliography='preprints'
    return f"./bibliography/{bibliography}.bib"

def get_author(citation):
    """Return an 'and'-separated list of authors, suitable for a BibTeX citation---or `None` if
    the authors are missing.
    """

    if 'authors' in citation:
        author_list=citation['authors'].split(',')
    elif 'inventors' in citation:
        author_list=citation['inventors'].split(',')
    else:
        return None
    return ' and '.join(list(map(str.strip, author_list)))

def get_title(citation):
    """Return the title, or `None` if none exists.
    """

    # The title is sometimes excerpted in the google scholar listing, but it
    # appears in full in the scholar_articles field. Use this whenever
    # possible.

    if 'scholar_articles' in citation and citation['scholar_articles'] != []:
        # This comes as a list of dictionaries. We pick the one with the
        # longest title.
        titles=list(map(lambda dic:dic.get('title', ""), citation['scholar_articles']))
        # Pick the longest
        title=max(titles, key=len)
        if title != "":
            return title
    else:
        # fall back on the title in the listing (or return None)
        return citation.get('title')

def get_date(citation):
    """Return a string in the format yyyy[-mm[-dd]], giving the date for
    the citation `citation` in as much specificity as we can muster.

    Return `None` if there's no date.
    """
    
    if 'publication_date' not in citation:
        return None
    # in Google Scholar the date comes in '/' form
    date_elements=citation['publication_date'].split('/')
    # ensure that the optional month and optional day are
    # two digits rather than one (e.g. 8 -> 08)
    for i in range(1,len(date_elements)):
        if len(date_elements[i]) == 1:
            new_element = f"0{date_elements[i]}"
            date_elements[i] = new_element
    # I don't think we have to worry about publications before
    # the year 1000 or after the year 9999, so we don't have to
    # standardize the length of the year...
    return "-".join(date_elements)

def get_bibtex_identifier(citation):
    """Generate a suitable identifier:
      [firstauthor][date][first2wordsoftitle] is usually good.
    """

    if 'authors' in citation and len(citation['authors']) > 0:
        authorlist=list(map(lambda x: x.strip(), citation['authors'].split(',')))
    elif 'inventors' in citation and len(citation['inventors']) > 0:
        authorlist=list(map(lambda x: x.strip(), citation['inventors'].split(',')))
    else:
        authorlist=['Unknown']
    
    # first author, full name, no spaces
    first_author="".join(authorlist[0].split())

    # if the date exists, include it
    if 'publication_date' in citation:
        # underscore rather than hyphen
        date=re.sub('-', '_', get_date(citation))
    else:
        date="UnknownDate"

    # if the title exists, include its first 1 or 2 words.
    if 'title' in citation:
        first_one_or_two_words="".join(citation['title'].split()[:2])
    else:
        first_one_or_two_words="UnknownTitle"
    
    # join them with underscores
    identifier_joined="_".join([first_author, date, first_one_or_two_words])
    # ensure that only numbers, letters, and underscores are in the identifier
    return re.sub(r'[^a-zA-Z0-9_]', '', identifier_joined)

def escape_characters_in_field(field_name, field_string, unicode_encoder):
    """Escape characters (or don't), as needed for the bibtex field.

    We don't replace characters if it's a URL.
    """
    # no changing characters in the URL
    if field_name == "url":
        return field_string
    return unicode_encoder.unicode_to_latex(field_string)

def make_bibtex_entry(bibtex_identifier, citation_id, citation_type, citation, unicode_encoder):
    """Format the bibtex entry according to the citation type."""
    # keep a list of lines; eventually return it as a multiline string.
    lines=["@"+citation_type+"{"+bibtex_identifier+","]

    # mandatory fields get default values if they're missing
    author=get_author(citation)
    if author is None:
        author="Unknown Author"
    author=escape_characters_in_field("author", author, unicode_encoder)
    lines.append(f"\tauthor=\"{author}\",")

    title=get_title(citation)
    if title is None:
        title="Unknown Title"
    title=escape_characters_in_field("title", title, unicode_encoder)
    lines.append(f"\ttitle=\"{title}\",")

    date=get_date(citation)
    if date is None:
        date="No Date"
    lines.append(f"\tdate=\"{date}\",")

    # translate the language of Google Scholar to BibTeX
    for gskey, bxkey in [
        # application_number goes in howpublished
        # authors/inventorsi are mandatory
        ('book', 'booktitle'),
        ('conference', 'booktitle'),
        #('description', 'abstract'), # not downloading abstracts
        # inventors/authors are mandatory
        ('issue', 'issue'),
        ('journal', 'journal'),
        ('link', 'url'),
        ('pages', 'pages'),
        # patent_number goes in howpublished
        # patent_office goes in howpublished
        # publisher gets added to notes, because bibtex doesn't like the publisher field in the article ('publisher', 'publisher'),
        ('report_number', 'number'),
        # resources goes in notes
        # scholar_articles we're not including
        # source we're not including
        # title mandatory
        # total_citations changes, so we're not including it
        ('volume', 'volume')]:
            if gskey in citation:
                # add to our list of lines
                value=escape_characters_in_field(bxkey, citation[gskey], unicode_encoder)
                lines.append(f"\t{bxkey}=\"{value}\",")

    # if there's a publisher and this is a type that supports this field, add it;
    # otherwise, put it in a note.
    if 'publisher' in citation:
        value=escape_characters_in_field('publisher', citation['publisher'], unicode_encoder)
        if citation_type in ['book', 'inbook', 'incollection', 'inproceedings']:
            lines.append(f"\tpublisher=\"{value}\",")
        else:
            # not supported here 
            lines.append(f"\tnote=\"Publisher: {value}\",")

    # format a special howpublished line (only for patents)
    if is_patent(citation):
        howpublished_fields=[]
        # this will end up as a space-separated list of the following elements:
        # 1. the patent office.
        if 'patent_office' not in citation:
            howpublished_fields.append('Unknown patent office')
        else:
            howpublished_fields += [citation['patent_office'], 'Patent']
        # 2. the patent number.
        if 'patent_number' in citation:
            howpublished_fields.append(citation['patent_number'])
        # 3. the application number.
        if 'application_number' in citation:
            howpublished_fields += ['App.', citation['application_number']]
        # put them together.
        howpublished_line=escape_characters_in_field("howpublished",
                                                     " ".join(howpublished_fields), 
                                                     unicode_encoder)
        lines.append(f"\thowpublished=\"{howpublished_line}\",")

    # end the citation
    lines.append("}")

    # return the list of lines as a multiline string
    return "\n".join(lines)

def append_bibtex_entry(citation, citation_id, citation_type, bibfile_location, unicode_encoder):
    """Store `citation` in bibtex format at the end of the file at
    `bibfile_location`, returning the identifier.

    The identifier is the part after `@article{` in
    `@article{gdclifford2023`.
    """
    # generate a suitable identifier. 
    bibtex_identifier=get_bibtex_identifier(citation)
    # format the bibtex entry according to the citation type
    bibtex_entry=make_bibtex_entry(bibtex_identifier,
                                   citation_id,
                                   citation_type,
                                   citation,
                                   unicode_encoder)
    # write it to the end of the file
    with open(bibfile_location, 'a') as bxfile:
        # leave a blank line before it
        bxfile.write("\n")
        bxfile.write(bibtex_entry)
        bxfile.write("\n")
    # return the identifier
    return bibtex_identifier

def add_to_skipped_citation_list(citation_id, bibtex_identifier, path_to_list):
    """Append the given citation ID on the list of citations to skip.

    The line should be like this: `citation_id # latex_identifier`.
    """

    with open(path_to_list, 'a') as slfile:
        slfile.write(f"{citation_id} # {bibtex_identifier}\n")

if __name__ == "__main__":
    # Check that the API key is defined in the current execution environment.
    if API_KEY_ENV_VARIABLE not in os.environ:
       raise EnvironmentError(f"Please define and export {API_KEY_ENV_VARIABLE} before running this script.")

    # Load a set of skipped citation IDs.
    citation_ids_to_skip = load_citation_ids_to_skip(SKIP_CITATION_LIST)

    # Initialize an iterator over items on the scholar page.
    page_items = scholar_page_items()

    # For each item, if it is not in SKIP_CITATION_LIST,
    #   - download the citation
    #   - convert it to a bibtex file
    #   - depending on its type, append it to the appropriate file
    #   - append its id to the end of SKIP_CITATION_LIST

    # initialize and cache an encoder to convert unicode to latex
    u = UnicodeToLatexEncoder(unknown_char_policy='replace',
                              replacement_latex_protection='braces-all')

    # Whether any new articles have been added:
    any_new_articles=False

    for item in page_items:
        citation_id = get_citation_id(item)

        if citation_id in citation_ids_to_skip:
            print(f"Not (re)downloading {citation_id}.")
        else:
            # yes we've found a new article!
            any_new_articles=True

            # retrieve it from Google Scholar using the serpapi
            citation = download_citation(citation_id)

            # the bibtex citation type must be inferred from which fields
            # are included...
            citation_type = choose_bibtex_citation_type(citation)

            # the location depends on the type of item being cited
            # and sometimes on its contents
            bibfile_location = get_bibfile_location(citation_type,
                                                    citation)

            # store it in the bibliography file and save the bibtex
            # identifier (e.g. the part after `@article{` in
            # `@article{gdclifford2023`).
            bibtex_identifier = append_bibtex_entry(citation,
                                                    citation_id,
                                                    citation_type,
                                                    bibfile_location,
                                                    u) # the encoder

            # store it in the skip list so it's not re-downloaded
            add_to_skipped_citation_list(citation_id, bibtex_identifier, SKIP_CITATION_LIST)
            print(f"Downloaded {citation_id}: {bibtex_identifier}.")

    print("Finished!")
    if not any_new_articles:
      print("No new publications!")
