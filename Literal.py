class Literal:
    def __init__(self, value):
        self.value = value # string
        
    def to_string(self):
        return self.value

    def __hash__(self):
        return hash(self.value)
    
    def get_name(self):
        return self.value

    def copy(self):
        return Literal(self.value)

    def __eq__(self, other):
        return self.value == other.value
    
    def __name__(self):
        return self.value