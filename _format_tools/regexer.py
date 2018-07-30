import re

journals = open("publication_info/data/JOURNALS.txt")

journal_references = []
for line in journals:
    line = line.strip()
    line = re.sub(r"\s+", " ", line)
    if line[-1] == ".":
        line = line[:-1]
    url = re.search(r"(?i)(?=http).*?(?<=>)", line)
    if url:
        line = re.sub(r"(?i)(?=http).*?(?<=>)", "", line)
        line = line + "|{}".format(url.group(0)[:-2])
        journal_references.append(line)
    else:
        journal_references.append(line)

with open("results.txt", "w") as results:
    for i in range(0, len(journal_references)):
        results.write(journal_references[i] + "\n")
