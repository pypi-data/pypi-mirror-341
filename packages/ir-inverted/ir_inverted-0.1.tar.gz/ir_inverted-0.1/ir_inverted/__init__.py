#initiator
#Inverted Index Code (with frequency counts)

import nltk
from nltk.corpus import stopwords
import re

nltk.download('stopwords')

# Documents
document1 = "The computer science students are appearing for practical examination."
document2 = "computer science practical examination will start tomorrow."

# Stopword list
stop_words = set(stopwords.words('english'))

# Preprocessing: Lowercase, remove punctuation, split
def preprocess(doc):
    doc = doc.lower()
    doc = re.sub(r'[^\w\s]', '', doc)
    tokens = doc.split()
    return [word for word in tokens if word not in stop_words]

tokens1 = preprocess(document1)
tokens2 = preprocess(document2)

# Combine all terms
all_terms = set(tokens1 + tokens2)

# Initialize inverted index
inverted_index = {}
occ_doc1 = {}
occ_doc2 = {}

for term in all_terms:
    docs = []
    
    if term in tokens1:
        docs.append("Document 1")
        occ_doc1[term] = tokens1.count(term)
        
    if term in tokens2:
        docs.append("Document 2")
        occ_doc2[term] = tokens2.count(term)
        
    inverted_index[term] = docs

# Display inverted index
print("Inverted Index with Frequencies:\n")
for term, docs in inverted_index.items():
    print(f"{term} ->", end=" ")
    for doc in docs:
        if doc == "Document 1":
            print(f"{doc}({occ_doc1.get(term, 0)})", end=", ")
        elif doc == "Document 2":
            print(f"{doc}({occ_doc2.get(term, 0)})", end=", ")
    print()



#Simple Document Retrieval for Query: "computer science"


    query = "tomorrow"
query_terms = preprocess(query)

matched_docs = set(["Document 1", "Document 2"])  # Start with all docs

for term in query_terms:
    matched_docs = matched_docs.intersection(set(inverted_index.get(term, [])))

print("\nDocuments matching query 'computer science':")
for doc in matched_docs:
    print(doc)
