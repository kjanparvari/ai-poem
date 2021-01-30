from trainer import Vocabulary


class Model:
    _unigrams: dict
    _bigrams: dict
    _vocabulary: Vocabulary
    _sentences: [[str]]

    def __init__(self, vocab: Vocabulary, doc_filename):
        self._vocabulary = vocab
        self._sentences = []
        self._unigrams = {}
        self._bigrams = {}
        with open(doc_filename, 'r+', encoding='utf-8') as file:
            lines: list = file.readlines()
            for line in lines:
                self._sentences.append(["start", *line.strip().split(), "end"])
            file.close()
        self._generateUnigrams()
        # for sen in self._sentences:
        #     print(sen)

    def _generateUnigrams(self):
        total_counter: int = 0
        for sen in self._sentences:
            for word in sen:
                if word != "start" or word != "end":
                    if not self._vocabulary.contains(word):
                        word = "unknown"
                    if word in self._unigrams.keys():
                        self._unigrams[word] += 1.0
                    else:
                        self._unigrams[word] = 1.0
                    total_counter += 1.0
        for key in self._unigrams.keys():
            self._unigrams[key] /= total_counter
        # for key, value in self._unigrams.items():
        #     print(key, " : ", value)

    def _generateBigrams(self):
        pass
