import re

with open("test.txt", "r") as f:
    data = f.read().replace("\n", "")

test = re.sub(r"(?i)(?=doi).*?(?=<)", "", data)

results = open("results.txt", "w")
results.write(test)
