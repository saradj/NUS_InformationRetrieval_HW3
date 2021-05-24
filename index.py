#!/usr/bin/python3

import nltk
import getopt
import math
import pickle
from os import listdir
from os.path import isfile, join
from nltk.stem.porter import PorterStemmer
import string
import sys


def usage():
    print("usage: " + sys.argv[0] + " -i directory-of-documents -d dictionary-file -p postings-file")

def build_index(in_dir, out_dict, out_postings):
    """
    build index from documents stored in the input directory,
    then output the dictionary file and postings file
    """
    print('indexing...')
    punctuationList = set(string.punctuation) #the set of all punctuation signs to skip
    stemmer = PorterStemmer()
    all_files = [file for file in listdir(in_dir)
                 if isfile(join(in_dir, file))]
    total_files = len(all_files)
    df = {}
    posting = {}

    for file in all_files:
        tf = {}
        text = open(join(in_dir, file), "r")
        for line in text:
            for sent_tokens in nltk.sent_tokenize(line):
                for word in nltk.word_tokenize(sent_tokens): #tokenizing the input to words
                    stem = stemmer.stem("".join(char for char in word if char not in punctuationList))
                    #stemming while taking only non - punctuation chars
                    stem = stem.lower() #case folding
                    if stem in tf: tf[stem] += 1
                    else: tf[stem] = 1
        # getting the log term freq
        for term in tf:
            tf[term] = 1 + math.log10(tf[term])
        sum = 0
        for val in tf.values():
            sum += math.pow(val,2)
        magnitude_of_vector = math.sqrt(sum) # the magnitude of the tf vector for all terms for this document
        for term in tf:
            tf_normalized = tf[term] / magnitude_of_vector
            if term in df:
                if file not in posting[term]: df[term] += 1
            else:
                posting[term] = {}
                df[term] = 1

            posting[term][file] = tf_normalized #updating the postings list for this file(doc)

    idf = {}
    for term in df:
        idf_term = math.log10(float(total_files) / float(df[term])) #calculating the idf
        idf[term] = (df[term], idf_term)

    acc_fp_post = 0
    out_fp = open(out_postings, "w")
    for post in posting:
        sorted_posting = sorted(map(lambda key: (int(key), posting[post][key]), posting[post].keys())) #sorts the postings list
        postings_string = ""
        for tup in sorted_posting:
            # The postings is kept as a sorted list od doc_id followed by the normalized tf for that doc_id
            postings_string += " " + str(tup[0]) + " " + str(tup[1])
        out_fp.write(postings_string )
        idf[post] = (idf[post], acc_fp_post)
        acc_fp_post += len(postings_string )
    out_fp.close()
    pickle.dump(idf, open(out_dict, "wb")) #saving the dict using pickle

input_directory = output_file_dictionary = output_file_postings = None

try:
    opts, args = getopt.getopt(sys.argv[1:], 'i:d:p:')
except getopt.GetoptError:
    usage()
    sys.exit(2)

for o, a in opts:
    if o == '-i': # input directory
        input_directory = a
    elif o == '-d': # dictionary file
        output_file_dictionary = a
    elif o == '-p': # postings file
        output_file_postings = a
    else:
        assert False, "unhandled option"

if input_directory == None or output_file_postings == None or output_file_dictionary == None:
    usage()
    sys.exit(2)

build_index(input_directory, output_file_dictionary, output_file_postings)

