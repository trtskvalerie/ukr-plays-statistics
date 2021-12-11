from math import sqrt
import sqlite3


database_1 = sqlite3.connect('sys_sample_1.db')
database_2 = sqlite3.connect('sys_sample_2.db')
database_3 = sqlite3.connect('dictionary.db')
sys_1 = database_1.cursor()
sys_2 = database_2.cursor()
rnd_3 = database_3.cursor()

# Write meta into file
with open('results.txt', 'w', encoding='utf-8') as file:
    file.write('s1 - перша механічна вибірка, тексти: драматургія 21 століття\n')
    file.write('s2 - друга механічна вибірка, тексти: драматургія 21 століття\n')
    file.write('s3 - випадкова вибірка, тексти: художня література для дітей\n')

# POS: adverb
# Student's t-test
avg_1 = sys_1.execute('SELECT avg_freq FROM pos_stats WHERE pos = "adv";').fetchall()[0][0]
avg_2 = sys_2.execute('SELECT avg_freq FROM pos_stats WHERE pos = "adv";').fetchall()[0][0]
avg_3 = rnd_3.execute('SELECT mean FROM pos_in_samples WHERE pos = "ADVB";').fetchall()[0][0]
sigmax_1 = sys_1.execute('SELECT sigmax FROM pos_stats WHERE pos = "adv";').fetchall()[0][0]
sigmax_2 = sys_2.execute('SELECT sigmax FROM pos_stats WHERE pos = "adv";').fetchall()[0][0]
sigmax_3 = rnd_3.execute('SELECT mean_square_dev FROM pos_in_samples WHERE pos = "ADVB";').fetchall()[0][0]

t12 = round(abs(avg_1-avg_2) / sqrt(sigmax_1**2 + sigmax_2**2), 5)
t13 = round(abs(avg_1-avg_3) / sqrt(sigmax_1**2 + sigmax_3**2), 5)
t23 = round(abs(avg_2-avg_3) / sqrt(sigmax_2**2 + sigmax_3**2), 5)

# Chi-squared distribution
freqs = list()
freqs.append(sys_1.execute('''SELECT "1", "2", "3", "4", "5", "6", "7", "8", "9", "10",
                              "11", "12", "13", "14", "15", "16", "17", "18", "19", "20"
                              FROM pos_stats WHERE pos = "adv";''').fetchall()[0])
freqs.append(sys_2.execute('''SELECT "1", "2", "3", "4", "5", "6", "7", "8", "9", "10",
                              "11", "12", "13", "14", "15", "16", "17", "18", "19", "20"
                              FROM pos_stats WHERE pos = "adv";''').fetchall()[0])
freqs.append(rnd_3.execute('SELECT * FROM pos_in_samples WHERE pos = "ADVB";').fetchall()[0][2:42:2])

f = (len(freqs[0]) - 1) * (len(freqs) - 1)
N = sum([sum(x) for x in freqs])
n = 0.0

samples = len(freqs)
subsamples = len(freqs[0])
for s in range(samples):
    for sub in range(subsamples):
        n += freqs[s][sub]**2 / (sum(freqs[s] * sum([x[sub] for x in freqs])))
chi_squared = round(N * (n - 1), 5)

# Output results into .txt file
with open('results.txt', 'a', encoding='utf-8') as file:
    file.write('\nPOS: ПРИСЛІВНИК\n')
    file.write('Хі-квадрат: ' + str(chi_squared))
    file.write('\nступені свободи: ' + str(f))
    file.write('\n\n')
    file.write('Критерій Стьюдента')
    file.write('\ns1 and s2: ' + str(t12))
    file.write('\ns1 and s3: ' + str(t13))
    file.write('\ns2 and s3: ' + str(t23))
    file.write('\nступені свободи в усіх 3 випадках: 20 + 20 - 2 = 38')
    file.write('\n')


# POS: adjective
# Student's t-test
avg_1 = sys_1.execute('SELECT avg_freq FROM pos_stats WHERE pos = "adj";').fetchall()[0][0]
avg_2 = sys_2.execute('SELECT avg_freq FROM pos_stats WHERE pos = "adj";').fetchall()[0][0]
avg_3 = rnd_3.execute('SELECT mean FROM pos_in_samples WHERE pos = "ADJF";').fetchall()[0][0]
sigmax_1 = sys_1.execute('SELECT sigmax FROM pos_stats WHERE pos = "adj";').fetchall()[0][0]
sigmax_2 = sys_2.execute('SELECT sigmax FROM pos_stats WHERE pos = "adj";').fetchall()[0][0]
sigmax_3 = rnd_3.execute('SELECT mean_square_dev FROM pos_in_samples WHERE pos = "ADJF";').fetchall()[0][0]

t12 = round(abs(avg_1-avg_2) / sqrt(sigmax_1**2 + sigmax_2**2), 5)
t13 = round(abs(avg_1-avg_3) / sqrt(sigmax_1**2 + sigmax_3**2), 5)
t23 = round(abs(avg_2-avg_3) / sqrt(sigmax_2**2 + sigmax_3**2), 5)

# Chi-squared distribution
freqs = list()
freqs.append(sys_1.execute('''SELECT "1", "2", "3", "4", "5", "6", "7", "8", "9", "10",
                              "11", "12", "13", "14", "15", "16", "17", "18", "19", "20"
                              FROM pos_stats WHERE pos = "adj";''').fetchall()[0])
freqs.append(sys_2.execute('''SELECT "1", "2", "3", "4", "5", "6", "7", "8", "9", "10",
                              "11", "12", "13", "14", "15", "16", "17", "18", "19", "20"
                              FROM pos_stats WHERE pos = "adj";''').fetchall()[0])
freqs.append(rnd_3.execute('SELECT * FROM pos_in_samples WHERE pos = "ADJF";').fetchall()[0][2:42:2])

f = (len(freqs[0]) - 1) * (len(freqs) - 1)
N = sum([sum(x) for x in freqs])
n = 0.0

samples = len(freqs)
subsamples = len(freqs[0])
for s in range(samples):
    for sub in range(subsamples):
        n += freqs[s][sub]**2 / (sum(freqs[s] * sum([x[sub] for x in freqs])))
chi_squared = round(N * (n - 1), 5)

# Output results into .txt file
with open('results.txt', 'a', encoding='utf-8') as file:
    file.write('\nPOS: ПРИКМЕТНИК\n')
    file.write('Хі-квадрат: ' + str(chi_squared))
    file.write('\nступені свободи: ' + str(f))
    file.write('\n\n')
    file.write('Критерій Стьюдента')
    file.write('\ns1 and s2: ' + str(t12))
    file.write('\ns1 and s3: ' + str(t13))
    file.write('\ns2 and s3: ' + str(t23))
    file.write('\nступені свободи в усіх 3 випадках: 20 + 20 - 2 = 38')