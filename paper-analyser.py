import PyPDF2
import re
import tkinter as tk
from tkinter import filedialog
import pandas as pd

# READ FILES
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

# LOOP OVER FILES
for fileReader in files:
    
    # START GETS TRUE IF "REFERENCES" IS FOUND IN THE DOC
    start = False
    t0 = len(papers.keys())
    

    for page in fileReader.pages:
        
        # DIRECTLY GET EVERY REFERENCE OF THE PAGE
        if start:
            text = page.extract_text()
            refs = re.split("\[[0-9]+\]",text)
            if len(refs) < 3:
                refs = re.split("[0-9]+\.",text)

        # IF REFERENCES IS FOUND - SLICE PAGE FOR EVERYTHING AFTER REFERENCES AND THEN PARSE 
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

        # PARSE REFERENCES
        for ref in refs:
            if ref in ["\n", ""]:
                continue
            if "“" not in ref:
                continue

            # GET TITLE AND COUNT OCCURENCIES
            title = re.sub("\n|,", " ",re.split('“|”', ref)[1]).strip().lower()
            if title in papers.keys():
                papers[title] += 1
            else:
                papers[title] = 1
            
            # GET AUTHOR
            authors = re.sub("\n|.?and\ ", " ",re.split('“', ref)[0]).strip().split(",")
            
            # GET LAST ELEMENT, MOST LIKELY THE YEAR
            year = re.sub("\.", " ",re.split(' ', ref)[-1]).strip()
            
            if "" in authors:
                authors.remove("")
            
            # GET FIRST AUTHORS
            for a in authors:
                a = a.lower()
                a = a.replace("and", "").strip()
                first_authors.append(a)
                if a in cited.keys():
                    cited[a].append(title)
                else:
                    cited[a] = [title]
                break

                
            # GET FULL LIST AUTHORS
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

# MAP AUTHORS
for i, j in df.iterrows():
    if j["paper"] in authorsOf.keys():
        df.loc[i, "author"] = ",".join(authorsOf[j["paper"]])
 
col = df.pop("author")
df.insert(0, col.name, col)
    
# SAVE
df.to_csv("paper_summary.csv", index=None, sep=";")        
