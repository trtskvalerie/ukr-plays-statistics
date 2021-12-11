import sqlite3


database = sqlite3.connect('complete_sample.db')
db = database.cursor()

db.execute('CREATE TABLE sentences (id INTEGER PRIMARY KEY, sent TEXT);')
db.execute('''CREATE TABLE words
             (id INTEGER PRIMARY KEY,
              sent_id INTEGER,
              punct_word VARCHAR(255),
              word_form VARCHAR(255),
              lemma VARCHAR(255),
              pos VARCHAR(5));''')

database.commit()
database.close()