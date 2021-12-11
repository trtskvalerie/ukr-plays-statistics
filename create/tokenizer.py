import re


class Tokenizer:
    @staticmethod
    def tokenize(text):
        text = re.sub(r'([.!?][)"]*?[ \n])([("]*?[А-ЯЄІЇ])', r'\1$$\2', text, flags=re.M)
        text = text.replace(' $$', '$$')
        sentences = text.split('$$')

        r = len(sentences)
        for n in range(r): sentences[n] = sentences[n].split()

        return sentences