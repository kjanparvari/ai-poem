FERDOWSI_TRAIN_FILENAME = "./train_set/ferdowsi_train.txt"  # id: 1
HAFEZ_TRAIN_FILENAME = "./train_set/hafez_train.txt"  # id: 2
MOLAVI_TRAIN_FILENAME = "./train_set/molavi_train.txt"  # id: 3


class Vocabulary:
    _dict: dict

    def __init__(self):
        self._dict = {}
        self._generate()
        print(len(self._dict))
        self._filter()
        print(len(self._dict))
        from model import Model
        ferdowsi_model = Model("ferdowsi", self, FERDOWSI_TRAIN_FILENAME)
        hafez_model = Model("hafez", self, HAFEZ_TRAIN_FILENAME)
        molavi_model = Model("molavi", self, MOLAVI_TRAIN_FILENAME)
        self._save()

    def _add(self, lst: [str]):
        word: str
        for word in lst:
            if word in self._dict.keys():
                self._dict[word] += 1
            else:
                self._dict[word] = 1

    def _generate(self):
        tokens: [(str, int)]
        with open(FERDOWSI_TRAIN_FILENAME, "r", encoding='utf-8') as file:
            tokens = file.read().strip().split()
            file.close()
        self._add(tokens)
        with open(HAFEZ_TRAIN_FILENAME, "r", encoding='utf-8') as file:
            tokens = file.read().strip().split()
            file.close()
        self._add(tokens)
        with open(MOLAVI_TRAIN_FILENAME, "r", encoding='utf-8') as file:
            tokens = file.read().strip().split()
            file.close()
        self._add(tokens)

    def _filter(self):
        removing_list: list = []
        for key in self._dict.keys():
            if self._dict[key] < 2:
                removing_list.append(key)
        for key in removing_list:
            del self._dict[key]

    def contains(self, word: str) -> bool:
        if word in self._dict.keys():
            return True
        else:
            return False

    def _save(self):
        import pickle
        with open("./dist/vocabulary.kj", "wb") as file:
            pickle.dump(self._dict, file)
            file.close()


def main():
    Vocabulary()


if __name__ == '__main__':
    main()
