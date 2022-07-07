import PyPDF2
import re
import tkinter as tk
from tkinter import filedialog
import pandas as pd

# READ FILES
file_paths = filedialog.askopenfilenames()
files  = []
journal = []
for fp in file_paths:
    file = open(fp, 'rb')   
    fileReader = PyPDF2.PdfFileReader(file, strict=False)
    files.append(fileReader)
    print("Reading {} with {} pages".format(fp.split("/")[-1], fileReader.numPages))
    
    if "non_ieee" in fp:
        journal.append("other")
    elif "springer" in fp:
        journal.append("springer")
    
    else:
        journal.append("ieee")
    


def get_lastname(s):
    s = s.split(" ")
    if len(s) == 0:
        return s
    
    lastname = ""
    for i in s:
        if len(i) > len(lastname):
            lastname = i

    return lastname


def parse_springer(ref):
    global papers
        
    title = re.sub("\n|,", " ",re.split('\.:', ref)[1].split(".")[0]).strip().lower()
   
    if title in papers.keys():
        papers[title] += 1
    else:
        papers[title] = 1

    # GET AUTHOR
    authors = re.sub("\n", " ",re.split('\.:', ref)[0]).strip().split(".,")
    

    # GET LAST ELEMENT, MOST LIKELY THE YEAR
    if len(re.findall("\(([0-9]{4})\)", ref)) > 0 :
        year = re.findall("\(([0-9]{4})\)", ref)[-1].strip()
    else:
        year = None
    return title, authors, year
        
def parse_acm(ref):
    global papers
    
    title = re.sub("\n|,", " ",re.split('[0-9]{4}\.', ref)[1].split(".")[0]).strip().lower()
    if title in papers.keys():
        papers[title] += 1
    else:
        papers[title] = 1

    # GET AUTHOR
    authors = re.sub("\n", " ",re.split('[0-9]{4}\.', ref)[0]).strip().split(",")

    # GET LAST ELEMENT, MOST LIKELY THE YEAR
    if len(re.findall('[0-9]{4}\.', ref)) > 0 :
        year = re.findall('[0-9]{4}\.', ref)[0].strip()
    else:
        year = None
        
    return title, authors, year
    
    
def parse_ieee(ref):
    global papers
    
    title = re.sub("\n|,", " ",re.split('“|”', ref)[1]).strip().lower()
   
    if title in papers.keys():
        papers[title] += 1
    else:
        papers[title] = 1

    # GET AUTHOR
    authors = re.sub("\n|\.", " ",re.split('“', ref)[0]).strip().split(",")
    

    # GET LAST ELEMENT, MOST LIKELY THE YEAR
    year = re.sub("\.", " ",re.split(' ', ref)[-1]).strip()
    return title, authors, year

def get_scholar_link(x, y):
    return "https://scholar.google.at/scholar?q={}%20{}".format(str(x).replace(" ", "%20"), str(y).replace(",", "%20"))

    
papers = {}
cited = {}
authorsOf = {}
all_authors = []
first_authors = []
failed = []

# LOOP OVER FILES
for fileNumber, fileReader in enumerate(files):
    
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
        else:
            # IF REFERENCES IS FOUND - SLICE PAGE FOR EVERYTHING AFTER REFERENCES AND THEN PARSE 
            text = page.extract_text().lower()

            if "\nreferences\n" in text:
                _refheading = "\nreferences\n"
            elif "\nr\neferences\n" in text:
                _refheading =  "\nr\neferences\n"
            else:
                continue

            start = True
            text = page.extract_text().lower().split(_refheading)[1]
            refs = re.split("\[[0-9]+\]",text)
            if len(refs) < 3:
                refs = re.split("[0-9]+\.",text)

        if not start:
            continue

        # PARSE REFERENCES
        for ref in refs:

            if ref in ["\n", ""]:
                continue
            

            # GET TITLE AND COUNT OCCURENCIES
            if journal[fileNumber] == "ieee":
                if "“" not in ref:
                    continue
                title, authors, year = parse_ieee(ref)
            elif journal[fileNumber] == "springer":
                if ".:" not in ref:
                    continue
                title, authors,year = parse_springer(ref)
            else:
                try:
                    title, authors, year = parse_ieee(ref)
                except:
                    try:
                        title, authors,year = parse_springer(ref)
                    except:
                        try:
                            title, authors,year = parse_acm(ref)
                        except:
                            failed.append(ref)
                            continue
       
            if "" in authors:
                authors.remove("")
            
            # GET FIRST AUTHORS
            for a in authors:
                a = a.lower()
                a = a.replace("and ", " ").replace("et al.", "").replace(".", "").replace(",", "").replace("  ", " ").strip()
                a = get_lastname(a)
                a = "".join(re.findall("([a-z]+)", a))
                if len(a) > 1:
                    first_authors.append(a)
                    if a in cited.keys():
                        cited[a].append(title)
                    else:
                        cited[a] = [title]
                    break

                
            # GET FULL LIST AUTHORS
            for a in authors:
                a = a.lower()
                a = a.replace("and ", " ").replace("et al.", "").replace(".", "")
                a = a.replace(",", "").replace("  ", " ").replace("et ","").replace(" al","").strip()
                a = get_lastname(a)
                a = "".join(re.findall("([a-z]+)", a))
                if len(a) > 1:
                    if title in authorsOf.keys():
                        authorsOf[title].add(a)
                    else:
                        authorsOf[title] = set([a])

                    all_authors.append(a)


    print(f"References found: {len(papers.keys())-t0}")

    
if len(all_authors) > 0:    
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
    
    df["google_scholar"] = df.apply(lambda x: get_scholar_link(x["paper"], x["author"]), axis = 1)
    

    # SAVE
    df.to_csv("paper_summary.csv", index=None, sep=";")   
    pd.DataFrame(failed).to_csv("failed_refs.csv")
else:
    print("No references found in the selected papers")
