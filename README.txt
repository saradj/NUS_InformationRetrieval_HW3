This is the README file for A0207386Y's submission

== Python Version ==

I'm (We're) using Python Version <3.7.6> for
this assignment.

== General Notes about this assignment ==

INDEXING:
The indexing part is very similar to Homework 2, in memory indexing using Pickle for on disk persistence. Namely I read every file, and tokenize it using the nltk tools. In order to reduce time in the serch phase, I also calculate and store the normalized tf and the idf(using lnc) in the dictionary file for each term encountered. The index is stored as follows:
(... 'term': ((nb_documents, idf), pointer to posting)...)
The number of documents is needed to know when to stop while serching.

The posting is stored in the following format:
 doc_1 normalized_tf_for_doc_1 doc_2 normalized_tf_for_doc_2...

SEARCHING:
The search part is less similar to Homework 2, namely I read the query file and tokenize it to obtain all the words. Subsequently, I calculate the tf-idf(using ltc) vector of the query. Then I check the cosine similarity for each document(containing some of the query words) and store them in a heap, where I can easily obtain the top 10 most relevant documents.

== Files included with this submission ==

index.py code for iterating through all documents and indexing them

search.py: code for searching given queries using the dictionary and postings files and producing a ranked result of docs

README.txt this file

postings.txt The generated postings file

dictionary.txt Resulting file from index.py, stored form of dictionary

Posting.py code for Posting class, encapsulates postings for easier manipulation

== Statement of individual work ==

Please put a "x" (without the double quotes) into the bracket of the appropriate statement.

[X ] I/We, A0207386Y, certify that I/we have followed the CS 3245 Information
Retrieval class guidelines for homework assignments.  In particular, I/we
expressly vow that I/we have followed the Facebook rule in discussing
with others in doing the assignment and did not take notes (digital or
printed) from the discussions.  

[ ] I/We, A0000000X, did not follow the class rules regarding homework
assignment, because of the following reason:

<Please fill in>

We suggest that we should be graded as follows:

<Please fill in>

== References ==

Python docs for usage of heapq and lambdas

EMAIL: e0445488@u.nus.edu