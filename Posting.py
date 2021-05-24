"""
    A class used as an abstraction for Posting
"""
class Posting:

    def __init__(self, posting_file, nb_postings, ptr):
        self.index = 0
        self.nb_postings = nb_postings
        self.fp = open(posting_file, "rb")
        self.fp.seek(ptr)

    def next(self):
        """
        This function returns the next tuple of the documents, in the form of (doc_id, doc_normalized_tf)
        """
        if self.index >= self.nb_postings: #if we pass the number of postings(no more left) return None
            return None
        nb_spaces = 0
        value = ""
        self.fp.seek(1, 1)
        while nb_spaces < 2:
            # getting the two needed words only => doc_id and the normalized tf for that doc, that are stored in that order in the file
            current = self.fp.read(1)
            current = current.decode("utf-8")
            if current == " " : nb_spaces += 1
            value += current
        self.fp.seek(-1, 1)
        splitted = value.split(" ")
        doc_id = int(splitted[0])
        doc_normalized_tf = float(splitted[1])
        self.index += 1
        return doc_id, doc_normalized_tf