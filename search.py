#!/usr/bin/python3
import nltk
import sys
import getopt
import pickle
from math import log10
import string
from nltk import word_tokenize
from nltk.stem.porter import PorterStemmer
import heapq
from Posting import *

def usage():
    print("usage: " + sys.argv[0] + " -d dictionary-file -p postings-file -q file-of-queries -o output-file-of-results")

punc = set(string.punctuation)

def run_search(dict_file, postings_file, queries_file, results_file):
    """
    using the given dictionary file and postings file,
    perform searching on the given queries file and output the results to a file
    """
    print('running search on the queries...')
    dict = pickle.load(open(dict_file, "rb"))
    stemmer = PorterStemmer()
    queries = open(queries_file, "r")
    out_file = open(results_file, "w")
    for query in queries:
        query = query.strip()
        (q_words, q_normalized_vector) = normalize_query_vector(query, dict, stemmer) # getting the normalized query vector
        result = get_top_10(q_words, dict, postings_file, q_normalized_vector)# getting the top 10 most relevant documents
        out_file.write(" ".join(result) + "\n") #writing the result
    queries.close()
    out_file.close()



def get_top_10(q_words, dict, posting_file, normalized_query_vector):
    """
    This function computes all relevant documents by calculating its token term frequencies
    based on the query tokens passed as an argument
    """
    vectors_tf = {}
    for word in q_words:
        if word in dict:
            nb_postings = dict[word][0][0]
            pointer = dict[word][1] #getting the pointer to posting for the word from the dictionary
            posting = Posting(posting_file, nb_postings, pointer)
            #creating a posting object given the postings file, the number of postings and the posting pointer
            next = posting.next() #returns a tuple doc_id, doc_normalized_tf
            while next is not None:
                doc_id = str(next[0])
                if doc_id not in vectors_tf: vectors_tf[doc_id] = {}
                vectors_tf[doc_id][word] = next[1] #updating the list accordingly for the doc id with it's normalized tf for the word
                next = posting.next()
    priority_queue = []
    for doc_id in vectors_tf:
        vector_score = 0
        for word in vectors_tf[doc_id]: #vectors_tf[doc_id] contains only 1+log10(tf) for all words contained, no idf multiplication! lnc
            vector_score += vectors_tf[doc_id][word] * normalized_query_vector[word] #calculating cosine similarity
        heapq.heappush(priority_queue, (vector_score, -1 * int(doc_id)))
        # Sorting by decreasing score, but in case of a tie use the smaller doc_id
    return map(lambda doc: str(-1 * doc[1]), heapq.nlargest(10, priority_queue)) # returns the top 10 documents that have the highest ranking

def normalize_query_vector(query, index, stemmer):
    """
    Function to tokenize the query and normalize it by calculating its tf-idf
    """
    q_words = {}
    stemmed_query = map(lambda x: stemmer.stem("".join(ch for ch in x if ch not in punc)).lower(), word_tokenize(query))
    for term in stemmed_query:
        q_words[term] = 1 if (term not in q_words) else q_words[term] + 1 #filling up the tf for each term
    tf_idf_vector = {}
    for term in q_words:
        if term in index:
            tf = 1 + log10(q_words[term])
            idf = index[term][0][1] # we obtain the stored idf from the indexing phase
            tf_idf_vector[term] = tf * idf #compute the tf-idf
    return q_words.keys(), tf_idf_vector #return tuple of all the terms and the normalized vector

dictionary_file = postings_file = file_of_queries = output_file_of_results = None

try:
    opts, args = getopt.getopt(sys.argv[1:], 'd:p:q:o:')
except getopt.GetoptError:
    usage()
    sys.exit(2)

for o, a in opts:
    if o == '-d':
        dictionary_file  = a
    elif o == '-p':
        postings_file = a
    elif o == '-q':
        file_of_queries = a
    elif o == '-o':
        file_of_output = a
    else:
        assert False, "unhandled option"

if dictionary_file == None or postings_file == None or file_of_queries == None or file_of_output == None :
    usage()
    sys.exit(2)

run_search(dictionary_file, postings_file, file_of_queries, file_of_output)
