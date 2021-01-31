from trainer import Vocabulary


class Model:
    _model_name: str
    _unigrams_count: dict
    _bigrams_count: dict
    _vocabulary: Vocabulary
    _sentences: [[str]]
    _total_counter: int

    def __init__(self, name: str, vocab: Vocabulary, doc_filename):
        self._model_name = name
        self._vocabulary = vocab
        self._sentences = []
        self._unigrams_count = {}
        self._bigrams_count = {}
        self._total_counter = 0
        with open(doc_filename, 'r+', encoding='utf-8') as file:
            lines: list = file.readlines()
            for line in lines:
                self._sentences.append(["start", *line.strip().split(), "end"])
            file.close()
        self._generateUnigrams()
        self._generateBigrams()
        # print(self._bigrams_count)
        self._save()

    def _generateUnigrams(self):
        self._unigrams_count["start"] = len(self._sentences)
        self._unigrams_count["end"] = len(self._sentences)
        for sen in self._sentences:
            for i in range(0, len(sen)):
                word = sen[i]
                if word != "start" and word != "end":
                    if not self._vocabulary.contains(word):
                        word = "unknown"
                    if word in self._unigrams_count.keys():
                        self._unigrams_count[word] += 1
                    else:
                        self._unigrams_count[word] = 1
                    self._total_counter += 1
        # for key in self._unigrams.keys():
        #     self._unigrams[key] /= self._total_counter
        # for key, value in self._unigrams.items():
        #     print(key, " : ", value)

    def _generateBigrams(self):
        for sen in self._sentences:
            for i in range(0, len(sen) - 1):
                curr_word = sen[i]
                next_word = sen[i + 1]
                if curr_word != "start" and curr_word != "end" and (not self._vocabulary.contains(curr_word)):
                    curr_word = "unknown"
                if next_word != "start" and next_word != "end" and (not self._vocabulary.contains(next_word)):
                    next_word = "unknown"
                key = (next_word, curr_word)
                if key in self._bigrams_count.keys():
                    self._bigrams_count[key] += 1
                else:
                    self._bigrams_count[key] = 1
        # for (nxt, cur) in self._bigrams_count.keys():
        #     self._bigrams_count[(nxt, cur)] /= self._unigrams_count[cur]
        # for key, value in self._bigrams_count.items():
        #     print(key, " : ", value)

    def _save(self):
        unigram_result: dict = {}
        bigram_result: dict = {}
        for key in self._unigrams_count.keys():
            unigram_result[key] = self._unigrams_count[key] / self._total_counter
        for (nxt, cur) in self._bigrams_count.keys():
            bigram_result[(nxt, cur)] = self._bigrams_count[(nxt, cur)] / self._unigrams_count[cur]

        import pickle
        with open(f"./dist/{self._model_name}.kj", "wb") as file:
            pickle.dump([unigram_result, bigram_result], file)
            file.close()
