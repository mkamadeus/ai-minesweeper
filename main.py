from Minesweeper import Minesweeper
from ClipsInstance import ClipsInstance
import random

# instance  = ClipsInstance()

# instance.define_fact('hans-bot', [1,2])
# for i in range(10):
#     instance.define_fact('bomb', [random.randint(0,10), random.randint(0,10)])

# instance.define_rule('find-hans', "(hans-bot 1 2)", "(assert (hehe 999))")

# print(instance.run())

# if(instance.is_fact_exist('hehe')):
#     print('Hans-bot detected')

# for f in instance.get_facts():
#     print(f)

minesweeper = Minesweeper()

minesweeper.initialize_board((2, 2))
minesweeper.print_board()
