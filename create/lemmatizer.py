import re


class Lemmatizer:
    @staticmethod
    def lemmatize(sentences, dictionary):

        lem_sents = list()

        for n in range(len(sentences)):
            lem_sent = list()

            for i in range(len(sentences[n])):
                clean_word = re.sub(r'[0-9%:;,.!?‘’"“”«»(){}\[\]\n—]', r'', sentences[n][i])
                if clean_word.lower() in dictionary.lemmas.keys(): clean_word = clean_word.lower()
                elif clean_word.lower().capitalize() in dictionary.lemmas.keys():
                    clean_word = clean_word.lower().capitalize()
                if clean_word in dictionary.lemmas.keys():
                    if clean_word in dictionary.lemmas[clean_word]: pass
                    else: clean_word = dictionary.lemmas[clean_word][0]
                lem_sent.append(clean_word)
            else: lem_sents.append(lem_sent)

        return lem_sents