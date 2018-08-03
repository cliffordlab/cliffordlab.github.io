import regex as re

journals = open("results.txt")

journal_references = []
for line in journals:
    line = line.strip()
    line = re.sub(r"[a-z]\K\,(?!.*([a-z][\,]))", "|", line)
    journal_references.append(line)

with open("results_1.txt", "w") as results:
    for i in range(0, len(journal_references)):
        results.write(journal_references[i] + "\n")
