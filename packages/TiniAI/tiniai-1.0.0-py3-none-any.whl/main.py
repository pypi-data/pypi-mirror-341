from sentence_transformers import SentenceTransformer
from scipy.spatial import distance
import time
import json
import nltk

class TinyAI:
    def __init__(self, train_file, quiet=False):
        try:
            from nltk import tokenize

        except:
            print('\rInstalling tokenize from NLTK...' if quiet == False else ('' if quiet == True else '\rInstalling tokenize from NLTK...'), end='')
            nltk.download('tokenize', quiet=True)

        self.tokenize = tokenize
        self.model = SentenceTransformer('distilbert-base-nli-mean-tokens')
        with open(train_file if train_file.endswith('.json') else 'This module can\'t parse other files. Please, use .json train file.', 'r') as self.data:
            print('\rLoading training data...' if quiet == False else ('' if quiet == True else '\rLoading training data...'), end='')
            self.base = json.load(self.data)

        print('\rTinyAI 1.0\nMade by IrbisX7\n' if quiet == False else ('' if quiet == True else '\rtiniai 0.1\nMade by IrbisX7\n'))
        time.sleep(0.2)

    def generate(self, content):
        self.sentence_list = []
        self.sentences_done = []

        for self.userinput_sentence in self.tokenize.sent_tokenize(content):
            self.userinput_sentence = self.userinput_sentence
            for self.userinput in self.userinput_sentence.split(','):
                self.userinput = self.userinput.replace(',', '').replace(', ', '')
                self.sentences = {}

                for self.words in self.base:
                    self.words = self.words
                    if distance.cosine(self.model.encode([self.userinput, self.words])[1], self.model.encode([self.userinput, self.words])[0]) <= 0.17:
                        for self.word in self.base[self.words]:
                            self.word = self.word
                            if len(self.base[self.words]) == 1:
                                self.words_distance = self.model.encode([self.userinput, self.word])
                                self.sentences[self.word] = distance.cosine(self.words_distance[1], self.words_distance[0])

                            else:
                                self.words_distance = self.model.encode([self.userinput, self.word])

                                if distance.cosine(self.words_distance[1], self.words_distance[0]) <= 0.45:
                                    self.sentences[self.word] = distance.cosine(self.words_distance[1], self.words_distance[0])

                self.sentence_list.append(self.sentences)

        try:
            for self.sentences in self.sentence_list:
                self.min_distance = min(tuple([self.sentences[i] for i in list(self.sentences)]))
                self.sentences_done.append(''.join([i if self.sentences[i] == self.min_distance else '' for i in list(self.sentences)]))

            output = ' '.join(self.sentences_done)

        except ValueError:
            output = 'I can\'t understand you.'

        return output