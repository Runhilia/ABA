class Negation:
    
    def __init__(self, attacker, attacked):
        self.attacker = attacker # Argument
        self.attacked = attacked # Argument
    
    def to_string(self):
        return f"{self.attacker.get_name()} -> {self.attacked.get_name()}"
    
    def get_attacker(self):
        return self.attacker
    
    def get_attacked(self):
        return self.attacked