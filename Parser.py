from Literal import Literal
from Negation import Negation
from Rule import Rule
from Preference import Preference


class Parser:
    def __init__(self, filename):
        self.L = set()
        self.R = set()
        self.A = set()
        self.C = set()
        self.P = set()
        self.parse_file(filename)
        
    def parse_literrals(self, literal_str):
        return {Literal(lit.strip()) for lit in literal_str.strip('[]').split(',')}
    
    def parse_rules(self, rule_str):
        rule_part = rule_str.split('<-')
        conclusion = Literal(rule_part[0].strip())
        premises = {Literal(premise.strip()) for premise in rule_part[1].split(',')} if rule_part[1].strip() else []
        return premises, conclusion
    
    def parse_file(self, filename):
        with open(filename, 'r') as f:
            lines = f.readlines()
            
            for line in lines:
                line.strip()
        
                if line.startswith('L:'):
                    self.L = self.parse_literrals(line[2:].strip())
                    
                elif line.startswith('A:'):
                    self.A = self.parse_literrals(line[2:].strip())
                    
                elif line.startswith('C('):
                    parts = line[2:].split('):')
                    attacker = Literal(parts[1].strip())
                    attacked = Literal(parts[0].strip())
                    self.C.add(Negation(attacker, attacked))
                    
                elif line.startswith('['):
                    rule_id= Literal(line.split(']:')[0].strip('[]'))
                    premises, conclusion = self.parse_rules(line.split(']:')[1].strip())
                    weight = 1
                    self.R.add(Rule(premises, conclusion, weight, rule_id))
                
                elif line.startswith('PREF:'):
                    parts = line[5:].split('>')
                    self.P.add(Preference(Literal(parts[0].strip()), Literal(parts[1].strip())))
                    
                else:
                    raise Exception(f"Invalid line: {line}")