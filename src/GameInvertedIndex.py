class GameInvertedIndex:
    """
    Inverted Game Index for quick searching using a hashmap
    """

    def __init__(self, documents):
        """
        Constructor meta data
        :param documents: the corpus of items you want to have indexed in list form
        :return: None
        """
        if (not isinstance(documents, list)):
            raise RuntimeError('Documents must be a list object')
        elif (isinstance(documents, list) and len(documents) == 0):
            raise RuntimeError('Documents list must contain actual data')

        self.documents = documents
        self.inv_index = {}


    def normalize(self, word):
        """
        Removes punctuation characters and replaces it with ' '
        Some punctuation like ':', ends up leaving two spaces which we replace with one *after* first replace
        Lower case the word to make it case insensitive
        :param word: word you want to normalize
        :return: the word after you've done the normalization
        """
        chars = "',.:?!#$&-"
        for i in chars:
            if i in word:
                word = word.replace(i, '')
        return word.lower()


    def build_index(self):
        """
        For each document, split by space and record in a set (to ensure uniqueness and prevent duplicates)
        :return: None
        """
        for i in range(len(self.documents)):
            if 'name' not in self.documents[i]:
                raise RuntimeError('Input documents are not properly formatted')
            else:
                title = self.documents[i]['name']
                title = self.normalize(title)
                words = title.split(' ')
                for j in words:
                    self.inv_index[j].add(i) if j in self.inv_index else self.inv_index.setdefault(j, set([i]) )

    def search(self, keywords):
        """
        Performs a search on the inverted index storing the game titles
        :param keywords: the compound words or terms you would like to search on
        :return: a list of documents matching the search terms
        """
        if self.inv_index == {}:
            raise RuntimeError("The index is empty.  You may need to build it first.")
        keywords = self.normalize(keywords)
        words = keywords.split(' ')
        final_indices = None
        for i in words:
            if i in self.inv_index:
                if not final_indices:
                    final_indices = self.inv_index[i]
                else:
                    final_indices = final_indices.intersection(self.inv_index[i])
        return [self.documents[i] for i in final_indices]

