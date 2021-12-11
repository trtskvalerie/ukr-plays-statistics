import re, sqlite3, tokenizer as t, lemmatizer as l, generate_dict as gen


# Generate the dictionary
dic = gen.Dict('dict_corp_lt.db')
dic.generate_lemmas()
dic.generate_pos()

# Connect database
database = sqlite3.connect('complete_sample.db')
db = database.cursor()

# Read texts
with open('plays.txt', 'r', encoding='utf-8') as file:
    text = file.read()

# Tokenize texts
tokenized = t.Tokenizer.tokenize(text)

# Make sents table
for sent in tokenized:
    db.execute("INSERT INTO sentences (sent) VALUES(?);", (' '.join(sent),))

database.commit()

# Lemmatize texts
lemmatized = l.Lemmatizer.lemmatize(tokenized, dic)

# Make words table
a = len(tokenized)

for n in range(a):
    for i in range(len(tokenized[n])):
        clean_word = re.sub(r'[0-9%:;,.!?‘’"“”«»(){}\[\]\n—]', r'', tokenized[n][i])
        if clean_word.lower() in dic.lemmas.keys(): clean_word = clean_word.lower()
        elif clean_word.lower().capitalize() in dic.lemmas.keys():
            clean_word = clean_word.lower().capitalize()

        if clean_word == '' or clean_word == '*' or clean_word == '-' or clean_word == '--': continue

        pos = 'unkn'
        if lemmatized[n][i] in dic.pos.keys(): pos = dic.pos[lemmatized[n][i]]

        db.execute('INSERT INTO words (sent_id, punct_word, word_form, lemma, pos) VALUES(?, ?, ?, ?, ?);',
                   (n+1,
                    tokenized[n][i],
                    clean_word,
                    lemmatized[n][i],
                    pos))
database.commit()

# Close connection to database
database.close()