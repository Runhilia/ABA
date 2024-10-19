class Rule:
    def __init__(self, premises, conclusion, weight, reference):
        self.premises = premises # set of Literal
        self.conclusion = conclusion # Literal
        self.weight = weight # int
        self.reference = reference # Literal
        
    def to_string(self):
        str = ""
        str += self.reference.to_string()
        str += " : "
        if len(self.premises) > 0:
            for i, premise in enumerate(self.premises):
                str += premise.to_string()
                if i < len(self.premises) - 1:
                    str += ", "
        str += " -> "
        str += self.conclusion.to_string()
        # if self.weight != 99:
        #     str += f" {self.weight}"
        str += " "
        return str

    def get_premises(self):
        return self.premises
    
    def get_conclusion(self):
        return self.conclusion
    
    def get_weight(self):
        return self.weight

    def get_reference(self):
        return self.reference

    def copy(self):
        return Rule(self.premises.copy(), self.conclusion.copy(), self.weight, self.reference.copy())
    
    def __hash__(self) -> int:
        str = ""
        for premise in self.premises:
            str += premise.to_string()
        str += self.conclusion.to_string()
        return hash(str)
        
    def __eq__(self, other) -> bool:
        return self.__hash__() == other.__hash__()