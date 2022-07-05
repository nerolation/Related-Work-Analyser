# Related Work Analyser

* **Receive an overview of the most relevant literature in a certain domain**
* **Never miss out any relevant paper in your Related Work section**

#### Research-Paper-Analyser is a Python tool to analyse the references of most IEEE, Springer and ACM-style papers. It allows to parse multiple papers and produces a summary of the references found. The tool logs the most cited authors and creates a report with the most referenced papers. 

Select multiple research papers form local system, run the analysis and receive summary of references (most cited authors and papers)


## Installation
```
git clone https://github.com/Nerolation/Related-Work-Analyser.git
```
### Create Virtual Environment (optional)

```
cd Related-Work-Analyser
python3 -m venv ./
source bin/activate
```

### Install Dependencies

```
pip install -r requirements.txt
```

## Run

```
python3 paper-analyser.py
```

### Springer-style papers

Add "springer" to the file name of the Springer paper to indicate not looking for the default IEEE reference style, but for Springer-style references. For ACM papers or any other paper that may not work add "non_ieee" to the filename.

### Example Output 

```java
Most cited authors: 
meiklejohn              : 5  
rufﬁng                  : 5  
moreno-sanchez          : 5  
kate                    : 5  
garman                  : 5  
green                   : 5  
miers                   : 5  
chaum                   : 4  
ron                     : 3  
pomarole                : 3  
jordan                  : 3  
levchenko               : 3  
mccoy                   : 3
           ...
```
```
author;paper;citations
d. ron;quantitative analysis of the full bitcoin transaction graph;3
m. ober,s. katzenbeisser,k. hamacher;structure and anonymity of the bitcoin transaction graph;3
a. miller,j. bonneau,j. clark,e. w. felten,a. narayanan,j. a. kroll;mixcoin: anonymity for bitcoin with accountable mixes;3
s. meiklejohn,d. mccoy,m. pomarole,s. savage,g. m. voelker,g. jordan,k. levchenko;a ﬁstful of bitcoins: characterizing payments among men with no names;2
f. reid m. harrigan,r. fergal m. harrigan;an analysis of anonymity in the bitcoin system;2
p. moreno-sanchez,a. kate,t. rufﬁng;coinshufﬂe: practical decentralized coin mixing for bitcoin;2
p. moreno-sanchez,a. kate,t. rufﬁng;p2p mixing and unlinkable bitcoin transactions;2
m. liberatore,g. bissias,b. n. levine,a. p. ozisik;sybil- resistant mixing for bitcoin;2
l. valenta b. rowan;blindcoin: blinded  accountable mixes for bitcoin;2
a. chiesa,e. tromer,m. green,c. garman,m. virza,i. miers,e. b. sasson;zerocash: decentralized anonymous payments from bitcoin;2
r. matzutt,k. wehrle,m. henze,f. grossmann,j. h. ziegeldorf;secure and anonymous decentralized bitcoin mixing;2
s. meiklejohn,d. mccoy,m. pomarole,s. savage,g. m. voelker,g. jordan,k. levchenko;a fistful of bitcoins: characterizing payments among men with no names;2
s. nakamoto;bitcoin: a peer-to-peer electronic cash system;1
g. karame,t. scherer,e. roulaki,m. roeschlin,s. capkun;evaluating user privacy in bitcoin;1
m. p´osfai,d. kondor,i. csabai,g. vattay;do the rich get richer? an empirical analysis of the bitcoin transaction network;1
m. lischke b. fabian;analyzing the bitcoin network: the ﬁrst four years;1
           ...
```
