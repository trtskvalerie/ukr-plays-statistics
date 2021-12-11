import sqlite3, icu, re


class Dict:
    lemmas = dict()
    pos = dict()
    collator = icu.Collator.createInstance(icu.Locale('de_DE.UTF-8'))

    def __init__(self, filename):
        self.filename = filename

    def generate_lemmas(self):
        database = sqlite3.connect(self.filename)
        db = database.cursor()

        rows = db.execute('SELECT word_form, lemma FROM dict;').fetchall()

        for row in rows:
            if row[0] not in self.lemmas.keys():
                self.lemmas[row[0]] = list()
                self.lemmas[row[0]].append(row[1])
            else: self.lemmas[row[0]].append(row[1])

        for key in self.lemmas.keys():
            self.lemmas[key] = sorted(list(set(self.lemmas[key])), key=self.collator.getSortKey)

    def generate_pos(self):
        database = sqlite3.connect(self.filename)
        db = database.cursor()

        rows = db.execute('SELECT lemma, gram FROM dict;').fetchall()

        for row in rows:
            if row[0] not in self.pos.keys(): self.pos[row[0]] = re.findall(r'^[a-z]+?(?:(?=:)|$)', row[1])[0]