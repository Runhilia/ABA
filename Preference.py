class Preference:
    
    def __init__(self, prefered, not_prefered):
        self.prefered = prefered # Argument
        self.not_prefered = not_prefered # Argument
    
    def to_string(self):
        return f"{self.prefered.get_name()} > {self.not_prefered.get_name()}"
    
    def get_prefered(self):
        return self.prefered
    
    def get_not_prefered(self):
        return self.not_prefered