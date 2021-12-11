import sqlite3


database = sqlite3.connect('sys_sample_2.db')
db = database.cursor()

db.execute('''CREATE TABLE form_stats
              (id INTEGER PRIMARY KEY,
               form VARCHAR(255),
               freq INTEGER,
               '1' INTEGER,
               '2' INTEGER,
               '3' INTEGER,
               '4' INTEGER,
               '5' INTEGER,
               '6' INTEGER,
               '7' INTEGER,
               '8' INTEGER,
               '9' INTEGER,
               '10' INTEGER,
               '11' INTEGER,
               '12' INTEGER,
               '13' INTEGER,
               '14' INTEGER,
               '15' INTEGER,
               '16' INTEGER,
               '17' INTEGER,
               '18' INTEGER,
               '19' INTEGER,
               '20' INTEGER);''')
db.execute('''CREATE TABLE lem_stats
              (id INTEGER PRIMARY KEY,
               lemma VARCHAR(255),
               freq INTEGER,
               '1' INTEGER,
               '2' INTEGER,
               '3' INTEGER,
               '4' INTEGER,
               '5' INTEGER,
               '6' INTEGER,
               '7' INTEGER,
               '8' INTEGER,
               '9' INTEGER,
               '10' INTEGER,
               '11' INTEGER,
               '12' INTEGER,
               '13' INTEGER,
               '14' INTEGER,
               '15' INTEGER,
               '16' INTEGER,
               '17' INTEGER,
               '18' INTEGER,
               '19' INTEGER,
               '20' INTEGER);''')
db.execute('''CREATE TABLE pos_stats
              (id INTEGER PRIMARY KEY,
               pos VARCHAR(255),
               freq INTEGER,
               '1' INTEGER,
               '2' INTEGER,
               '3' INTEGER,
               '4' INTEGER,
               '5' INTEGER,
               '6' INTEGER,
               '7' INTEGER,
               '8' INTEGER,
               '9' INTEGER,
               '10' INTEGER,
               '11' INTEGER,
               '12' INTEGER,
               '13' INTEGER,
               '14' INTEGER,
               '15' INTEGER,
               '16' INTEGER,
               '17' INTEGER,
               '18' INTEGER,
               '19' INTEGER,
               '20' INTEGER);''')
database.commit()

forms = db.execute('SELECT word_form, COUNT(*) FROM words GROUP BY word_form ORDER BY 2 DESC;').fetchall()
lemmas = db.execute('SELECT lemma, COUNT(*) FROM words GROUP BY lemma ORDER BY 2 DESC;').fetchall()
pos_tags = db.execute('SELECT pos, COUNT(*) FROM words GROUP BY pos ORDER BY 2 DESC;').fetchall()

for form in forms:
    f = list()

    for n in range(0, 20000, 1000):
        f.append(db.execute('''WITH subsample AS
                               (SELECT word_form FROM words LIMIT 1000 OFFSET ''' + str(n) + ''')
                               SELECT COUNT(*) FROM subsample WHERE word_form = ?;''', (form[0],)).fetchall()[0][0])

    db.execute('''INSERT INTO form_stats
                  (form, freq,
                  '1', '2', '3', '4', '5', '6', '7', '8', '9', '10',
                  '11', '12', '13', '14', '15', '16', '17', '18', '19', '20')
                  VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);''',
               (form[0], form[1], f[0], f[1], f[2], f[3], f[4], f[5], f[6], f[7], f[8], f[9], f[10],
                f[11], f[12], f[13], f[14], f[15], f[16], f[17], f[18], f[19]))

database.commit()

for lemma in lemmas:
    f = list()

    for n in range(0, 20000, 1000):
        f.append(db.execute('''WITH subsample AS
                               (SELECT lemma FROM words LIMIT 1000 OFFSET ''' + str(n) + ''')
                               SELECT COUNT(*) FROM subsample WHERE lemma = ?;''', (lemma[0],)).fetchall()[0][0])

    db.execute('''INSERT INTO lem_stats
                  (lemma, freq,
                  '1', '2', '3', '4', '5', '6', '7', '8', '9', '10',
                  '11', '12', '13', '14', '15', '16', '17', '18', '19', '20')
                  VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);''',
               (lemma[0], lemma[1], f[0], f[1], f[2], f[3], f[4], f[5], f[6], f[7], f[8], f[9], f[10],
                f[11], f[12], f[13], f[14], f[15], f[16], f[17], f[18], f[19]))

database.commit()

for pos in pos_tags:
    f = list()

    for n in range(0, 20000, 1000):
        f.append(db.execute('''WITH subsample AS
                               (SELECT pos FROM words LIMIT 1000 OFFSET ''' + str(n) + ''')
                               SELECT COUNT(*) FROM subsample WHERE pos = ?;''', (pos[0],)).fetchall()[0][0])

    db.execute('''INSERT INTO pos_stats
                  (pos, freq,
                  '1', '2', '3', '4', '5', '6', '7', '8', '9', '10',
                  '11', '12', '13', '14', '15', '16', '17', '18', '19', '20')
                  VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);''',
               (pos[0], pos[1], f[0], f[1], f[2], f[3], f[4], f[5], f[6], f[7], f[8], f[9], f[10],
                f[11], f[12], f[13], f[14], f[15], f[16], f[17], f[18], f[19]))

database.commit()
database.close()