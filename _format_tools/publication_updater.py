

# OPENS FILES
conferences = open("CONFERENCES.txt")
journals = open("JOURNALS.txt")
theses = open("THESES.txt")
books_chapters = open("BOOKS_CHAPTERS.txt")

# EXAMPLE TEXT FILE FORMAT
# Authors; Title; Publication information; URL

# BOILERPLATE INFORMATION
# MAKE FUNCTION TO JUST WRITE THIS STUFF
# ---
# title: Publications - Clifford Lab
# <!-- permalink: "/publications.html" -->
# layout: default
# ---
#
#
# <style type="text/css">
#         @import url("assets/css/newcss.css");
#     </style>
#    <div style="overflow-x:auto;" class="container">
#
#
#         <div align="center" class="jumbotron">
#             <h1>Publications</h1>
#         </div>
#         <div align="left">
#             <p><b>&nbsp;Papers on this site are presented to ensure timely dissemination of scholarly and technical work. Copyright and all rights therein are retained by authors or by other copyright holders. All persons copying this information are expected
#                 to adhere to the terms and constraints invoked by each author's copyright. In most cases, these works may not be reposted without the explicit permission of the copyright holder.</b></p>
#             <br><p>Citation / impact of articles and open access versions can be found at <a href="https://scholar.google.co.uk/citations?hl=en&user=VwYoZ6gAAAAJ&view_op=list_works&sortby=pubdate">Google Scholar</a> and<a href="https://www.ncbi.nlm.nih.gov/pmc/?term=gari+clifford"> PubMed Central</a>.</p>
#
#         </div><br><br>)

# JOURNAL BOILERPLATE
        # <div class="col-md-6">
        #     <table>
        #
        #         <tr>
        #             <th>
        #             </th>
        #             <th>
        #                 <h3 align="center"><b>Journal</b></h3>
        #             </th>
        #         </tr>

# SOME FOR LOOP TO GENERATE HTML FOR JOURNAL
