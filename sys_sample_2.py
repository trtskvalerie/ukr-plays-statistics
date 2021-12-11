import sqlite3


# # Get ids of sents in sample 1
# database = sqlite3.connect('sys_sample_1.db')
# db = database.cursor()
# sample_1 = db.execute('SELECT DISTINCT sent_id FROM words;').fetchall()

# Connect to database of complete sample (temp copy)
database = sqlite3.connect('complete_sample_no_1.db')
db = database.cursor()

# # Remove sents from sample 1 from complete sample
# for sent in sample_1:
#     db.execute('DELETE FROM words WHERE sent_id = ?;', (sent[0],))
# database.commit()

# Calculate avg length of sentence in complete sample
sents = db.execute('SELECT COUNT(DISTINCT sent_id) FROM words;').fetchall()[0][0]
words = db.execute('SELECT COUNT(id) FROM words;').fetchall()[0][0]
avg_length = words / sents

# Calculate how many sents for sample of 20,000
sent_count = 20000 / avg_length
every_n_sent = round(sents / sent_count)

# Get every n-th sentence
sample = db.execute('SELECT * FROM words WHERE sent_id % ? == 4;', (every_n_sent,)).fetchall()

database = sqlite3.connect('sys_sample_2.db')
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