class Argument:
    def __init__(self, leaves,claim, name):
        self.leaves = leaves # set of Literal
        self.claim = claim # Literal
        self.name = name # string
        
    def to_string(self):
        str = f"{self.name} : "
        str += "{"
        if len(self.leaves) > 0:
            for i, sub_argument in enumerate(self.leaves):
                str += sub_argument.to_string()
                if i < len(self.leaves) - 1:
                    str += ","
        str += "}"
        str += " ⊢ "
        str += self.claim.to_string()
        return str
    
    def __hash__(self) -> int:
        str = ""
        for leaf in self.leaves:
            str += leaf.to_string()
        str += self.claim.to_string()
        return hash(str)
    
    def __eq__(self, value: object) -> bool:
        return hash(self) == hash(value)
    
    def __iter__(self):
        return iter(self.leaves)
        
    def __next__(self):
        return next(self.leaves)
    
    def get_claim(self):
        return self.claim

    def get_leaves(self):
        return self.leaves

    def get_name(self):
        return self.name
    