from Minesweeper import Minesweeper
from ClipsInstance import ClipsFact, ClipsInstance, ClipsRule
import random
import clips

# instance = ClipsInstance()

# instance.define_fact('hans-bot', [1, 2])
# for i in range(10):
#     instance.define_fact(
#         'bomb', [random.randint(0, 10), random.randint(0, 10)])

# instance.define_rule('find-hans', "(hans-bot 1 2)", "(assert (hehe 999))")

# print(instance.run())

# if(instance.is_fact_exist('hehe')):
#     print('Hans-bot detected')

# for f in instance.get_facts():
#     print(f)

# fact1 = ClipsFact(
#     'hans-bot', [ClipsFact('or', [1, 2]), ClipsFact('+', [2, 3])])
# fact2 = ClipsFact(
#     'hans-bot', [ClipsFact('or', [1, 2]), ClipsFact('+', [2, 3])])
# # print(fact.get_fact_string())
# rule = ClipsRule('hans-rule', [fact1], [fact2])
# print(rule.get_rule_string())

# minesweeper = Minesweeper()

# minesweeper.initialize_board((2, 2))
# minesweeper.print_board()
minesweeper = Minesweeper(size=4)
minesweeper.initialize_board((0, 0))
minesweeper.inference()

# env = clips.Environment()
# template_string = """
# (deftemplate template-fact
# (slot template-slot (type SYMBOL)))
# """
# env.build(template_string)
# template = env.find_template('template-fact')
# new_fact = template.new_fact()
# new_fact['template-slot'] = clips.Symbol('a-symbol')
# new_fact.assertit()
# for fact in env.facts():
#     print(fact)
