def end_html(html_file):
    with open(html_file, "a") as publication_file:
        publication_file.write("</div>\n")
        publication_file.write("</div>\n")

def header_html(html_file):
    with open(html_file, "w") as html_file:
        html_file.write("---\n")
        html_file.write("title: Publications - Clifford Lab\n")
        html_file.write("permalink: \"/publications.html\"\n")
        html_file.write("layout: default\n")
        html_file.write("---\n")

        html_file.write("<style type=\"text/css\">\n")
        html_file.write("@import url(\"assets/css/newcss.css\");\n")
        html_file.write("</style>\n")
        html_file.write("<div style=\"overflow-x:auto;\" class=\"container\">\n")

        html_file.write("<div align=\"center\" class=\"jumbotron\">\n")
        html_file.write("<h1>Publications</h1>\n")
        html_file.write("</div>\n")
        html_file.write("<div align=\"left\">\n")
        html_file.write("<p><b>&nbsp;Papers on this site are presented to ensure timely dissemination of scholarly and technical work. Copyright and all rights therein are retained by authors or by other copyright holders. All persons copying this information are expected\n")
        html_file.write("to adhere to the terms and constraints invoked by each author's copyright. In most cases, these works may not be reposted without the explicit permission of the copyright holder.</b></p>\n")
        html_file.write("<br><p>Citation / impact of articles and open access versions can be found at <a href=\"https://scholar.google.co.uk/citations?hl=en&user=VwYoZ6gAAAAJ&view_op=list_works&sortby=pubdate\">Google Scholar</a> and<a href=\"https://www.ncbi.nlm.nih.gov/pmc/?term=gari+clifford\"> PubMed Central</a>.</p>\n")
        html_file.write("</div><br><br>\n")

def conferences(conference_file, html_file):
    with open(conference_file) as conferences:
        conference_references = []
        for line in conferences:
            conference_references.append(line.strip())

    conference_index = len(conference_references) - 1
    with open(html_file, "a") as html_file:

        html_file.write("<div class=\"col-md-6\">\n")
        html_file.write("<table>\n")
        html_file.write("<tr>\n")
        html_file.write("<th>\n")
        html_file.write("</th>\n")
        html_file.write("<th>\n")
        html_file.write("<h3 align=\"center\"><b>Conferences</b></h3>\n")
        html_file.write("</th>\n")
        html_file.write("</tr>\n")

        while conference_index >= 0:
            conference = conference_references[conference_index].split("|")
            html_file.write("<tr>\n")
            html_file.write("  <td>{}</td>\n".format(conference_index + 1))
            html_file.write("  <td>\n")
            html_file.write("    <h4>{}.\n".format(conference[0].strip()))
            html_file.write("<a href=\"{}\">\n".format(conference[3].strip()))
            html_file.write("<b> {}</b></a>.\n".format(conference[1].strip()))
            html_file.write(" {}.</h4></td>\n".format(conference[2].strip()))
            html_file.write("</tr>\n\n")
            conference_index = conference_index - 1

        html_file.write("</table>\n")

def journals(journal_file, html_file):
    with open(journal_file) as journals:
        journal_references = []
        for line in journals:
            journal_references.append(line.strip())

    journal_index = len(journal_references) - 1
    with open(html_file, "a") as html_file:
        html_file.write("<div class=\"col-md-6\">\n")
        html_file.write("<table>\n")
        html_file.write("<tr>\n")
        html_file.write("<th>\n")
        html_file.write("</th>\n")
        html_file.write("<th>\n")
        html_file.write("<h3 align=\"center\"><b>Journal</b></h3>\n")
        html_file.write("</th>\n")
        html_file.write("</tr>\n")
        while journal_index >= 0:
            journal = journal_references[journal_index].split("|")
            html_file.write("<tr>\n")
            html_file.write("  <td>{}</td>\n".format(journal_index + 1))
            html_file.write("  <td>\n")
            html_file.write("    <h4>{}.\n".format(journal[0].strip()))
            html_file.write("<a href=\"{}\">\n".format(journal[3].strip()))
            html_file.write("<b> {}</b></a>.\n".format(journal[1].strip()))
            html_file.write(" {}</h4></td>\n".format(journal[2].strip()))
            html_file.write("</tr>\n\n")
            journal_index = journal_index - 1
        html_file.write("</table>\n")

def reviews_editorials(reviews_editorials_file, html_file):
    with open(reviews_editorials_file) as reviews_editorials:
        reviews_editorials_references = []
        for line in reviews_editorials:
            reviews_editorials_references.append(line.strip())

    reviews_editorials_index = len(reviews_editorials_references) - 1
    with open(html_file, "a") as html_file:
        html_file.write("<table>\n")
        html_file.write("<tr>\n")
        html_file.write("<th>\n")
        html_file.write("</th>\n")
        html_file.write("<th>\n")
        html_file.write("<h3 align=\"center\"><b>Reviews and Editorials</b></h3>\n")
        html_file.write("</th>\n")
        html_file.write("</tr>\n")
        while reviews_editorials_index >= 0:
            review = reviews_editorials_references[reviews_editorials_index].split("|")
            html_file.write("<tr>\n")
            html_file.write("  <td>{}</td>\n".format(reviews_editorials_index + 1))
            html_file.write("  <td>\n")
            html_file.write("    <h4>{}.\n".format(review[0].strip()))
            html_file.write("<a href=\"{}\">\n".format(review[3].strip()))
            html_file.write("<b> {}</b></a>.\n".format(review[1].strip()))
            html_file.write(" {}</h4></td>\n".format(review[2].strip()))
            html_file.write("</tr>\n\n")
            reviews_editorials_index = reviews_editorials_index - 1
        html_file.write("</table>\n")

def teaching_aids(teaching_aids_file, html_file):
    with open(teaching_aids_file) as teaching_aids:
        teaching_aids_references = []
        for line in teaching_aids:
            teaching_aids_references.append(line.strip())

    teaching_aids_index = len(teaching_aids_references) - 1
    with open(html_file, "a") as html_file:
        html_file.write("<table>\n")
        html_file.write("<tr>\n")
        html_file.write("<th>\n")
        html_file.write("</th>\n")
        html_file.write("<th>\n")
        html_file.write("<h3 align=\"center\"><b>Manuals, Videos, Computer Programs, and Other Teaching Aids</b></h3>\n")
        html_file.write("</th>\n")
        html_file.write("</tr>\n")
        while teaching_aids_index >= 0:
            aid = teaching_aids_references[teaching_aids_index].split("|")
            html_file.write("<tr>\n")
            html_file.write("  <td>{}</td>\n".format(teaching_aids_index + 1))
            html_file.write("  <td>\n")
            html_file.write("    <h4>{}.\n".format(aid[0].strip()))
            html_file.write("<a href=\"{}\">\n".format(aid[3].strip()))
            html_file.write("<b> {}</b></a>.\n".format(aid[1].strip()))
            html_file.write(" {}</h4></td>\n".format(aid[2].strip()))
            html_file.write("</tr>\n\n")
            teaching_aids_index = teaching_aids_index - 1
        html_file.write("</table>\n")
        html_file.write("</div>\n")

def books_chapters(books_chapters_file, html_file):
    with open(books_chapters_file) as books_chapters:
        books_chapters_references = []
        for line in books_chapters:
            books_chapters_references.append(line.strip())

    books_chapters_index = len(books_chapters_references) - 1
    with open(html_file, "a") as html_file:
        html_file.write("<table>\n")
        html_file.write("<tr>\n")
        html_file.write("<th>\n")
        html_file.write("</th>\n")
        html_file.write("<th>\n")
        html_file.write("<h3 align=\"center\"><b>Books and Chapters</b></h3>\n")
        html_file.write("</th>\n")
        html_file.write("</tr>\n")
        while books_chapters_index >= 0:
            writing = books_chapters_references[books_chapters_index].split("|")
            html_file.write("<tr>\n")
            html_file.write("  <td>{}</td>\n".format(books_chapters_index + 1))
            html_file.write("  <td>\n")
            html_file.write("    <h4>{}.\n".format(writing[0].strip()))
            html_file.write("<a href=\"{}\">\n".format(writing[3].strip()))
            html_file.write("<b> {}</b></a>.\n".format(writing[1].strip()))
            html_file.write(" {}.</h4></td>\n".format(writing[2].strip()))
            html_file.write("</tr>\n\n")
            books_chapters_index = books_chapters_index - 1
        html_file.write("</table>\n")

def other_material(other_material_file, html_file):
    with open(other_material_file) as other_material:
        other_material_references = []
        for line in other_material:
            other_material_references.append(line.strip())

    other_material_index = len(other_material_references) - 1
    with open(html_file, "a") as html_file:
        html_file.write("<table>\n")
        html_file.write("<tr>\n")
        html_file.write("<th>\n")
        html_file.write("</th>\n")
        html_file.write("<th>\n")
        html_file.write("<h3 align=\"center\"><b>Other Material</b></h3>\n")
        html_file.write("</th>\n")
        html_file.write("</tr>\n")
        while other_material_index >= 0:
            material = other_material_references[other_material_index].split("|")
            html_file.write("<tr>\n")
            html_file.write("  <td>{}</td>\n".format(other_material_index + 1))
            html_file.write("  <td>\n")
            html_file.write("    <h4>{}.\n".format(material[0].strip()))
            html_file.write("<a href=\"{}\">\n".format(material[3].strip()))
            html_file.write("<b> {}</b></a>.\n".format(material[1].strip()))
            html_file.write(" {}.</h4></td>\n".format(material[2].strip()))
            html_file.write("</tr>\n\n")
            other_material_index = other_material_index - 1
        html_file.write("</table>\n")

def theses(theses_file, html_file):
    with open(theses_file) as theses:
        theses_references = []
        for line in theses:
            theses_references.append(line.strip())

    theses_index = len(theses_references) - 1
    with open(html_file, "a") as html_file:
        html_file.write("<table>\n")
        html_file.write("<tr>\n")
        html_file.write("<th>\n")
        html_file.write("</th>\n")
        html_file.write("<th>\n")
        html_file.write("<h3 align=\"center\"><b>Theses</b></h3>\n")
        html_file.write("</th>\n")
        html_file.write("</tr>\n")
        while theses_index >= 0:
            theses = theses_references[theses_index].split("|")
            html_file.write("<tr>\n")
            html_file.write("  <td>{}</td>\n".format(theses_index + 1))
            html_file.write("  <td>\n")
            html_file.write("    <h4>{}.\n".format(theses[0].strip()))
            html_file.write("<a href=\"{}\">\n".format(theses[3].strip()))
            html_file.write("<b> {}</b></a>.\n".format(theses[1].strip()))
            html_file.write(" {}.</h4></td>\n".format(theses[2].strip()))
            html_file.write("</tr>\n\n")
            theses_index = theses_index - 1
        html_file.write("</table>\n")
        html_file.write("</div>\n")

def main():

    """
    This quick script generates the HTML needed for the publications html file
    in the pages folder. One can create another section as long as you include
    the proper HTML in the new method.

    If adding a new section, make sure to add the data in the publication_info
    folder.
    """

    header_html("../pages/publications.html")
    journals("publication_info/data/JOURNALS.txt", "../pages/publications.html")
    reviews_editorials("publication_info/data/REVIEWS_EDITORIALS.txt", "../pages/publications.html")
    teaching_aids("publication_info/data/TEACHING_AIDS.txt", "../pages/publications.html")
    conferences("publication_info/data/CONFERENCES.txt", "../pages/publications.html")
    books_chapters("publication_info/data/BOOKS_CHAPTERS.txt", "../pages/publications.html")
    other_material("publication_info/data/MATERIAL.txt", "../pages/publications.html")
    theses("publication_info/data/THESES.txt", "../pages/publications.html")
    end_html("../pages/publications.html")

if __name__ == "__main__":
    main()
