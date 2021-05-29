class NaiveBayesClassifier:

    def __init__(self, alpha=1):
        self.alpha = alpha

    def fit(self, X, y):
        """ Fit Naive Bayes classifier according to X, y. """
        from collections import defaultdict
        y_set = set(y)
        ver_cls = dict()
        for i in y_set:
            ver_cls[i] = y.count(i) / len(y)
        add_data_units_cls = defaultdict(dict)
        add_data_all_cls = defaultdict(int)
        ver_words = defaultdict(dict)
        for sentence in range(len(X)):
            for word in X[sentence].split():
                add_data_all_cls[word] += 1
                if y[sentence] in add_data_units_cls[word].keys():
                    add_data_units_cls[word][y[sentence]] += 1
                else:
                    add_data_units_cls[word][y[sentence]] = 1
        znam = defaultdict(int)
        for key in add_data_units_cls.keys():
            for i in y_set:
                if i in add_data_units_cls[key].keys():
                    znam[i] += add_data_units_cls[key][i]
        print(znam)
        for key in add_data_all_cls.keys():
            for i in y_set:
                if i not in add_data_units_cls[key].keys():
                    add_data_units_cls[key][i] = 0
                ver_words[key][i] = (add_data_units_cls[key][i] + self.alpha) / (
                                znam[i] + self.alpha * len(add_data_all_cls.keys()))
        self.ver_dict = ver_words
        self.ver_cls = ver_cls
        pass

    def predict(self, X):
        """ Perform classification on an array of test vectors X. """
        from math import log
        result = []
        choise_dict = dict()
        for sentence in X:
            for key in self.ver_cls.keys():
                choise_dict[key] = log(self.ver_cls[key])
            for word in sentence.split():
                if word in self.ver_dict.keys():
                    for key in self.ver_cls.keys():
                        choise_dict[key] += log(self.ver_dict[word][key])
            v = list(choise_dict.values())
            k = list(choise_dict.keys())
            result.append(k[v.index(max(v))])
        return result
        pass

    def score(self, X_test, y_test):
        """ Returns the mean accuracy on the given test data and labels. """
        counter = 0
        sr = self.predict(X_test)
        for i in range(len(y_test)):
            if sr[i] == y_test[i]:
                counter += 1
        return counter / len(y_test)
        pass