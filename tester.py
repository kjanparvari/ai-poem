TEST_FILENAME = "./test_set/test_file.txt"


class Tester:
    _set: (str, int)  # (sentence list, answer)
    _ferdowsi_unigrams: dict
    _ferdowsi_bigrams: dict
    _hafez_unigrams: dict
    _hafez_bigrams: dict
    _molavi_unigrams: dict
    _molavi_bigrams: dict
    _vocabulary: dict
    _landa1: float
    _landa2: float
    _landa3: float
    _epsilon: float

    def __init__(self):
        self._set = []
        self._load()
        self._landa1 = 0.09
        self._landa2 = 0.57
        self._landa3 = 0.34
        self._epsilon = 0.00001
        res = self.test()
        print(round(res*100, 2), "%")
        # _max = 0
        # cnt = 0
        # best: tuple = ()
        # for l3 in range(30, 70, 1):
        #     for l2 in range(25, 70, 1):
        #         # for e in range(1, 100, 1):
        #         cnt += 1
        #         print(f"progress: {(cnt / 2500)}")
        #         l1 = 100 - l3 - l2
        #         self._landa1 = l1 / 100
        #         self._landa2 = l2 / 100
        #         self._landa3 = l3 / 100
        #         # self._epsilon = e / 100
        #         self._epsilon = 0.00001
        #         r = self.test()
        #         if r > _max:
        #             _max = r
        #             best = (self._landa1, self._landa2, self._landa3, self._epsilon, r)
        # print(best)

    def _load(self):
        tmp: list
        with open(TEST_FILENAME, "r", encoding='utf-8') as file:
            tmp = file.readlines()
            file.close()
        for sen in tmp:
            lst: list = sen.strip().split()
            answer = lst.pop(0)
            sentence = lst.copy()
            self._set.append((sentence, answer))
            # print((sentence, answer))

        import pickle
        with open("./dist/ferdowsi.kj", "rb") as file:
            self._ferdowsi_unigrams, self._ferdowsi_bigrams = pickle.load(file)
            file.close()
        with open("./dist/hafez.kj", "rb") as file:
            self._hafez_unigrams, self._hafez_bigrams = pickle.load(file)
            file.close()
        with open("./dist/molavi.kj", "rb") as file:
            self._molavi_unigrams, self._molavi_bigrams = pickle.load(file)
            file.close()
        with open("./dist/vocabulary.kj", "rb") as file:
            self._vocabulary = pickle.load(file)
            file.close()

    def computeModelProb(self, sen: list, unigrams: dict, bigrams: dict) -> float:
        result: float = 1.0
        for i in range(1, len(sen)):
            cur_word = sen[i]
            prv_word = sen[i - 1]
            if cur_word != "start" and cur_word != "end" and (not self._vocabulary.keys().__contains__(cur_word)):
                cur_word = "unknown"
            if prv_word != "start" and prv_word != "end" and (not self._vocabulary.keys().__contains__(prv_word)):
                prv_word = "unknown"
            b = u = 0
            if (cur_word, prv_word) not in bigrams.keys():
                b = 0
            else:
                b = self._landa3 * bigrams[(cur_word, prv_word)]
            if cur_word not in unigrams.keys():
                u = 0
            else:
                u = self._landa2 * unigrams[cur_word]
            p = b + u + self._landa1 * self._epsilon
            result *= p
        return result

    def testSentence(self, sen: list, ans: int) -> bool:
        fp = self.computeModelProb(sen, self._ferdowsi_unigrams, self._ferdowsi_bigrams)
        hp = self.computeModelProb(sen, self._hafez_unigrams, self._hafez_bigrams)
        mp = self.computeModelProb(sen, self._molavi_unigrams, self._molavi_bigrams)
        fp *= 36.29
        hp *= 31.45
        mp *= 32.25
        _max = max(fp, hp, mp)
        _my_answer: int = 0
        if fp == _max:
            _my_answer = 1
        elif hp == _max:
            _my_answer = 2
        elif mp == _max:
            _my_answer = 3
        # print(_my_answer, ans)
        if int(_my_answer) != int(ans):
            return False
        return True

    def test(self):
        result = 0
        for (sen, ans) in self._set:
            res = self.testSentence(sen, ans)
            if res:
                result += 1
        result /= len(self._set)
        # print(result)
        return result


def main():
    tester = Tester()


if __name__ == '__main__':
    main()
