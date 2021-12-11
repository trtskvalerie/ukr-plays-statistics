from math import sqrt
import sqlite3


database = sqlite3.connect('sys_sample_2.db')
db = database.cursor()

db.execute('ALTER TABLE pos_stats ADD COLUMN avg_freq DECIMAL(10,2);')
db.execute('ALTER TABLE pos_stats ADD COLUMN rel_freq DECIMAL(10,5);')
db.execute('ALTER TABLE pos_stats ADD COLUMN standard_dev DECIMAL(10,5);')
db.execute('ALTER TABLE pos_stats ADD COLUMN sigmax DECIMAL(10,5);')
db.execute('ALTER TABLE pos_stats ADD COLUMN var_coeff DECIMAL(10,5);')
db.execute('ALTER TABLE pos_stats ADD COLUMN max_var_coeff DECIMAL(10,5);')
db.execute('ALTER TABLE pos_stats ADD COLUMN stabl_coeff DECIMAL(10,5);')
db.execute('ALTER TABLE pos_stats ADD COLUMN error DECIMAL(10,5);')
db.execute('ALTER TABLE pos_stats ADD COLUMN subsamples_needed INTEGER;')
db.execute('ALTER TABLE pos_stats ADD COLUMN confid_interv_1 DECIMAL(4,1);')
db.execute('ALTER TABLE pos_stats ADD COLUMN confid_interv_2 DECIMAL(4,1);')

pos_stats = db.execute('SELECT id, freq FROM pos_stats;').fetchall()

for pos in pos_stats:
    # Calculate avg freq and relative freq
    avg_freq = round(pos[1]/20, 2)
    rel_freq = pos[1]/20000

    # Calculate standard deviation
    freq_x = db.execute('SELECT freq_x, subsamples_n FROM pos_variantas WHERE pos_id = ?;', (pos[0],)).fetchall()
    d = 0.0
    for x in freq_x:
        d += (x[0] - avg_freq)**2 * x[1]
    sigma = round(sqrt(d/20), 5)

    # Calculate everything else
    sigmax = round(sigma/sqrt(20), 5)
    var_coeff = round(sigma/avg_freq, 5)
    max_var_coeff = round(sqrt(20-1), 5)
    stabl_coeff = round(1-(var_coeff/max_var_coeff), 5)
    error = round(1.96/sqrt(20)*var_coeff, 5)
    subs_needed = round(1.96**2*var_coeff**2/0.05**2)

    # Insert stats into table
    db.execute('''UPDATE pos_stats SET avg_freq = ?,
                                       rel_freq = ?,
                                       standard_dev = ?,
                                       sigmax = ?,
                                       var_coeff = ?,
                                       max_var_coeff = ?,
                                       stabl_coeff = ?,
                                       error = ?,
                                       subsamples_needed = ?
                                       WHERE id = ?;''',
               (avg_freq, rel_freq, sigma, sigmax, var_coeff, max_var_coeff, stabl_coeff, error, subs_needed, pos[0]))

    # Calculate % of freqs in confidence intervals
    db.execute('UPDATE pos_stats SET confid_interv_1 = ? WHERE id = ?;',
               (round(db.execute('''WITH variantas AS (SELECT freq_x, subsamples_n FROM pos_variantas WHERE pos_id = ?)
                                        SELECT SUM(subsamples_n) FROM variantas WHERE freq_x > ? AND freq_x < ?;''',
                                 (pos[0], avg_freq-sigma, avg_freq+sigma)).fetchall()[0][0]/20*100, 1), pos[0]))
    db.execute('UPDATE pos_stats SET confid_interv_2 = ? WHERE id = ?;',
               (round(db.execute('''WITH variantas AS (SELECT freq_x, subsamples_n FROM pos_variantas WHERE pos_id = ?)
                                        SELECT SUM(subsamples_n) FROM variantas WHERE freq_x > ? AND freq_x < ?;''',
                                 (pos[0], avg_freq-2*sigma, avg_freq+2*sigma)).fetchall()[0][0]/20*100, 1), pos[0]))

database.commit()
database.close()