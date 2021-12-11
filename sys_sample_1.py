import sqlite3


# Connect to database of complete sample
database = sqlite3.connect('complete_sample.db')
db = database.cursor()

# Calculate avg length of sentence in complete sample
sents = db.execute('SELECT COUNT(id) FROM sentences;').fetchall()[0][0]
words = db.execute('SELECT COUNT(id) FROM words;').fetchall()[0][0]
avg_length = words / sents

# Calculate how many sents for sample of 20,000
sent_count = 20000 / avg_length
every_n_sent = round(sents / sent_count)

# Get every n-th sentence
sample = list()
for n in range(2, sents, every_n_sent):
    sample.extend(db.execute('SELECT * FROM words WHERE sent_id = ?;', (n,)).fetchall())
else:
    more_sents = round((20000 - len(sample))/avg_length)
    every_m_sent = round(sents / more_sents)

    for m in range(4, sents, every_m_sent):
        if (m-2)%7 == 0:
            sample.extend(db.execute('SELECT * FROM words WHERE sent_id = ?;', (m+1,)).fetchall())
            continue
        sample.extend(db.execute('SELECT * FROM words WHERE sent_id = ?;', (m,)).fetchall())

database.close()

sample = sorted(sample, key=lambda row: row[0])

database = sqlite3.connect('sys_sample_1.db')
db = database.cursor()

db.execute('''CREATE TABLE words
             (id INTEGER PRIMARY KEY,
              sent_id INTEGER,
              punct_word VARCHAR(255),
              word_form VARCHAR(255),
              lemma VARCHAR(255),
              pos VARCHAR(5));''')

for word in sample:
    db.execute('INSERT INTO words (sent_id, punct_word, word_form, lemma, pos) VALUES(?, ?, ?, ?, ?);',
               (word[1], word[2], word[3], word[4], word[5]))

database.commit()
database.close()