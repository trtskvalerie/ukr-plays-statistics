import sqlite3


database = sqlite3.connect('sys_sample_2.db')
db = database.cursor()

db.execute('''CREATE TABLE pos_variantas
              (pos_id INTEGER,
               freq_x INTEGER,
               subsamples_n INTEGER);''')

pos_tags = db.execute('''SELECT id,
                         "1", "2", "3", "4", "5", "6", "7", "8", "9", "10",
                         "11", "12", "13", "14", "15", "16", "17", "18", "19", "20"
                         FROM pos_stats;''').fetchall()

s = len(pos_tags[0])

for pos in pos_tags:
    freqs = dict()

    for n in range(1, s):
        try:
            freqs[pos[n]] += 1
        except KeyError:
            freqs[pos[n]] = 1

    for freq, subs in freqs.items():
        db.execute('INSERT INTO pos_variantas (pos_id, freq_x, subsamples_n) VALUES(?, ?, ?);',
                   (pos[0], freq, subs))

database.commit()
database.close()