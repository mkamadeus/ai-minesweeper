from __future__ import annotations
from typing import List, Tuple, Union
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


class ClipsFact:
    def __init__(self, name: str, parameters: List[Union[int, ClipsFact]]):
        self.name = name
        self.parameters = parameters

    def get_fact_string(self):
        return f'({self.name} {" ".join(list(map(lambda v: str(v) if isinstance(v, int) else v.get_fact_string(), self.parameters)))})'


class ClipsRule:
    def __init__(self, name: str, requirements: List[ClipsFact], action: List[ClipsFact]):
        self.name = name
        self.requirements = requirements
        self.action = action

    def get_rule_string(self):
        return f'''
            (defrule {self.name}
                {chr(10).join(list(map(lambda r: r.get_fact_string(), self.requirements)))}
                =>
                {chr(10).join(list(map(lambda r: r.get_fact_string(), self.action)))}
            )
        '''
