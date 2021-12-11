import matplotlib.pyplot as plt
import sqlite3


database = sqlite3.connect('sys_sample.db')
db = database.cursor()

pos_ids = db.execute('SELECT DISTINCT pos_id FROM pos_variantas ORDER BY pos_id ASC;').fetchall()

colours = ['b', 'g', 'r', 'c', 'm', 'y', 'k']

for pos in pos_ids:
    pos_title = db.execute('SELECT pos FROM pos_stats WHERE id = ?;', (pos[0],)).fetchall()[0][0]

    varianta_set = db.execute('''SELECT freq_x, subsamples_n
                                 FROM pos_variantas
                                 WHERE pos_id = ?
                                 ORDER BY freq_x ASC;''', (pos[0],)).fetchall()

    x = [varianta[0] for varianta in varianta_set]
    n = [varianta[1] for varianta in varianta_set]

    max_var = db.execute('SELECT MAX(freq_x) FROM pos_variantas WHERE pos_id = ?;', (pos[0],)).fetchall()[0][0]
    min_var = db.execute('SELECT MIN(freq_x) FROM pos_variantas WHERE pos_id = ?;', (pos[0],)).fetchall()[0][0]
    max_n = db.execute('SELECT MAX(subsamples_n) FROM pos_variantas WHERE pos_id = ?;', (pos[0],)).fetchall()[0][0]
    min_n = db.execute('SELECT MIN(subsamples_n) FROM pos_variantas WHERE pos_id = ?;', (pos[0],)).fetchall()[0][0]

    plt.xlim(min_var-5, max_var+5)
    plt.ylim(min_n-1, max_n+1)

    plt.xlabel('варіанти')
    plt.ylabel('к-сть підвибірок')
    plt.title('полігон частот для ' + pos_title)

    plt.plot(x, n, colours[pos[0]%7-1] + 'o-')
    plt.show()

database.close()