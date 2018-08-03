with open("publication_info/data/THESES.txt") as journals:
    journal_references = []
    for line in journals:
        journal_references.append(line.strip())

journal_index = len(journal_references) - 1
with open("Theses.txt", "w") as myfile:
    while journal_index >= 0:
        journal = journal_references[journal_index].split("|")
        myfile.write("{},{}.{}\n".format(journal[0], journal[1], journal[2]))
        print(journal)
        journal_index = journal_index - 1
