import os
from django.conf import settings
import spacy
import gc

class SemanticSimilarity:
    nlp = None

    def load_nlp(self):
        if self.nlp is None:
            self.nlp = spacy.load(settings.SENTENCE_TRANSFORMER_MODEL_NAME)

    def unload_nlp(self):
        if self.nlp is not None:
            del self.nlp
            gc.collect()

    def getSimilarity(self, query, corpus, minSimilarity):
        # Ensure that self.nlp is loaded before using it
        self.load_nlp()

        query = self.nlp(query)
        corpus = self.nlp.pipe(corpus)
        similarDoc = []

        # print('---------------------')
        # print('------', query.text, '------')
        for doc in corpus:
            similarity = query.similarity(doc)
            if (similarity >= minSimilarity and (len(similarDoc) == 0 or similarity >= similarDoc[0])):
                similarDoc = [round(similarity, 3), doc.text]
                # print(f"{doc.text}: {round(similarity, 3)}")
        # print('---------------------')

        return similarDoc
