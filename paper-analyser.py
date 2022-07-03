import PyPDF2
import re
import tkinter as tk
from tkinter import filedialog
import pandas as pd


file_paths = filedialog.askopenfilenames()
files = []
for fp in file_paths:
    
    file = open(fp, 'rb')

    fileReader = PyPDF2.PdfFileReader(file)
    files.append(fileReader)

    print(fileReader.numPages)
    
papers = {}
cited = {}
authorsOf = {}
all_authors = []
first_authors = []


for fileReader in files:
    start = False
    t0 = len(papers.keys())
    

    for page in fileReader.pages:

        if start:
            text = page.extract_text()
            refs = re.split("\[[0-9]+\]",text)
            if len(refs) < 3:
                refs = re.split("[0-9]+\.",text)


        if "\nreferences\n" in page.extract_text().lower():
            start = True
            text = page.extract_text().lower().split("\nreferences\n")[1]
            refs = re.split("\[[0-9]+\]",text)
            #print(text)
            if len(refs) < 3:
                refs = re.split("[0-9]+\.",text)
            #print(refs)


        if not start:
            continue


        for ref in refs:
            if ref in ["\n", ""]:
                continue
            if "“" not in ref:
                continue

            title = re.sub("\n|,", " ",re.split('“|”', ref)[1]).strip().lower()
            if title in papers.keys():
                papers[title] += 1
            else:
                papers[title] = 1

            authors = re.sub("\n|.?and\ ", " ",re.split('“', ref)[0]).strip().split(",")
            year = re.sub("\.", " ",re.split(' ', ref)[-1]).strip()
            
            if "" in authors:
                authors.remove("")

            for a in authors:
                a = a.lower()
                a = a.replace("and", "").strip()
                first_authors.append(a)
                if a in cited.keys():
                    cited[a].append(title)
                else:
                    cited[a] = [title]
                break

            for a in authors:
                a = a.lower()
                a = a.replace("and", "").replace("et al.", "").strip()
                
                if title in authorsOf.keys():
                    authorsOf[title].add(a)
                else:
                    authorsOf[title] = set([a])
                    
                all_authors.append(a)


    print(f"References found: {len(papers.keys())-t0}")


     
    
author_count = {}
for author in all_authors:
    if author in author_count.keys():
        author_count[author] += 1
    else:
        author_count[author] = 1
author_count = dict(sorted(author_count.items(), key=lambda item: item[1], reverse=True))
print("\nMost cited authors: ")
for i in author_count.keys():
    print("{:<27}: {:<3}".format(i,author_count[i]))


paper_count = dict(sorted(papers.items(), key=lambda item: item[1], reverse=True))

df = pd.DataFrame.from_dict(paper_count, orient="index", columns=["citations"])
df = df.reset_index().rename(columns={'index': 'paper'})

for i, j in df.iterrows():
    if j["paper"] in authorsOf.keys():
        df.loc[i, "author"] = ",".join(authorsOf[j["paper"]])
 
col = df.pop("author")
df.insert(0, col.name, col)
    
df.to_csv("paper_summary.csv", index=None, sep=";")        