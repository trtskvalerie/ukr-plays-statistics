import sqlite3


database = sqlite3.connect('complete_sample.db')
db = database.cursor()

db.execute("""UPDATE words SET pos = 'adv' WHERE lemma == 'шкода' OR lemma == 'можна' OR lemma == 'треба'
              OR lemma == 'немає' OR lemma == 'слід' OR lemma == 'нема' OR lemma == 'завгодно' OR lemma == 'варто'
              OR lemma == 'бозна' OR lemma == 'хтозна' OR lemma == 'бажано' OR lemma == 'небажано'
              OR lemma == 'анічичирк';""")
db.execute("UPDATE words SET pos = 'noun' WHERE lemma == 'енд' OR lemma == 'каюк';")

database.commit()
database.close()