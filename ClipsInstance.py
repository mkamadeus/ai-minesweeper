from typing import List
import clips


class ClipsInstance:
    def __init__(self) -> None:
        self.env = clips.Environment()

    def define_fact(self, name: str, param: List[int]) -> None:
        fact_string = f'({name} {" ".join(list(map(lambda v: str(v), param)))})'
        try:
            self.env.assert_string(fact_string)
        except:
            print('Duplicate fact detected')

    def get_facts(self) -> List[str]:
        return self.env.facts()

    def define_rule(self, rule_name: str, prerequisites: str, result: str):
        rule = f'''
        (defrule {rule_name}
            {prerequisites}
            =>
            {result}
        )
        '''
        self.env.build(rule)

    def is_fact_exist(self, name: str):
        return bool(self.env.eval(f"(any-factp ((?f {name})) 999)"))

    def run(self):
        self.env.run()

    def reset(self):
        self.env.reset()
