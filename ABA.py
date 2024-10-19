from Literal import Literal
from Parser import Parser
from itertools import combinations
from Argument import Argument
from Negation import Negation
from Rule import Rule
from Preference import Preference

class ABA:

    def __init__(self, L, R, A, C, P):
        self.L = L # Language
        self.R = R # Rules
        self.A = A # Assumptions
        self.C = C # Négations
        self.P = P # Preferences
    
    def __str__(self) -> str:
        # String for the language
        str = "L = {"
        for i, literal in enumerate(self.L):
            str += literal.to_string()
            if i < len(self.L) - 1:
                str += "; "
        str += "}\n"
        
        # String for the rules
        str += "R = {"
        for i, rule in enumerate(self.R):
            str += rule.to_string()
            if i < len(self.R) - 1:
                str += "; "
        str += "}\n"
        
        # String for the assumptions
        str += "A = {"
        for i, literal in enumerate(self.A):
            str += literal.to_string()
            if i < len(self.A) - 1:
                str += "; "
        str += "}\n"
        
        # String for the négations
        str += "C = {"
        for i, negation in enumerate(self.C):
            str += negation.to_string()
            if i < len(self.C) - 1:
                str += "; "
        str += "}\n"
        
        # String for the preferences
        str += "P = {"
        for i, preference in enumerate(self.P):
            str += preference.to_string()
            if i < len(self.P) - 1:
                str += "; "
        str += "}\n"
        
        return str
    
    # Function to create the set of arguments
    def create_argument(self):
        argument_list = set()
        axiomes = set() # Set of axioms (rules with no premises)
        all_conclusion = set() 
        # Create the argument for the assumptions
        for literal in self.A:
            argument_list.add(Argument({literal},literal,f"A{len(argument_list)+1}"))
        # Create the argument for the rules with no premises
        for rule in self.R:
            if rule.get_premises() == {}:
                argument_list.add(Argument(set(),rule.get_conclusion(),f"A{len(argument_list)+1}"))
                axiomes.add(rule.get_conclusion())
        # List of all the conclusion
        for arg in self.R:
            all_conclusion.add(arg.get_conclusion())
        
        # Create the argument for the other rules
        for rule in self.R:
            if rule.get_premises() == {}:
                continue
            premises = rule.get_premises()
            new_premises = set()
            # Remove the axioms from the premises
            for premise in premises:
                if premise not in axiomes:
                    new_premises.add(premise)
            last_literal = set()
            # ?
            for premise in new_premises:
                if type(premise) == set:
                    print("erreur premise : ")
                    for lit in premise:
                        print(lit.to_string())
                    break
                res = self.dernier_literal(all_conclusion,premise)
                last_literal = last_literal.union(res)
            argument_list.add(Argument(last_literal,rule.get_conclusion(),f"A{len(argument_list)+1}"))
                   
        return argument_list
    
    # Function to find the last literal of a rule
    def dernier_literal(self,conclusion,literal):
        if literal in conclusion:
            for rule in self.R:
                if rule.get_conclusion() == literal:
                    if len(rule.get_premises()) == 0:
                        return {}
                    else:
                        temp = set()
                        for lit in rule.get_premises():
                            res = self.dernier_literal(conclusion,lit)
                            temp = temp.union(res)
                        return temp
        else:
            if type(literal) == set:
                for lit in literal:
                    print(lit.to_string())
            return {literal}
        
    # Function to create the set of attacks
    def create_attacks(self,args):
        attacks = []
        for arg in args:
            for arg2 in args:
                premis = arg.get_leaves()
                conclusion = arg2.get_claim()
                for att in self.C:
                    if att.get_attacker() == conclusion and att.get_attacked() in premis:
                        attacks.append([arg2,arg])
        return attacks
    
    # Function to check if the ABA is atomic
    # An ABA is atomic if all the rules have only assumptions as premises
    def is_atomic(self):
        for rule in self.R:
            if rule.get_premises() != {}:
                for premise in rule.get_premises():
                    if premise not in self.A:
                        return False
        return True
    
    # Function to check if the ABA is circular
    def is_circular(self):
        for rule in self.R:
            literal_in_path = set()
            # Add the premises to the path
            for premise in rule.get_premises():
                literal_in_path.add(premise)
            new_literal_added = True
            
            while new_literal_added:
                new_literal_added = False
                for rule2 in self.R:
                    if rule == rule2:
                        continue
                    # Check if the conclusion of the rule is in the path
                    if rule2.get_conclusion() in literal_in_path:
                        for premise in rule2.get_premises():
                            if premise not in literal_in_path:
                                literal_in_path.add(premise)
                                new_literal_added = True
            # Check if the conclusion of the rule is in the path
            if rule.get_conclusion() in literal_in_path:
                return True
        return False
    
    # Function to create a non circular ABA
    def create_non_cicular(self):
        if self.is_circular():
            l_copy = self.L.copy()
            r_copy = self.R.copy()
            self.R = set()
            k = len(self.L) - len(self.A) # Number of literals which are not assumptions
            
            # Add new literals to the language
            for l in l_copy:
                # If the literal is not an assumption
                if l not in self.A:                    
                    # Create the new literals and add them
                    for i in range(1,k):
                        self.L.add(Literal(l.get_name() + str(i)))

                        
            for rule in r_copy:
                # If it is an atomic rule
                if rule.get_conclusion() not in self.A and include_literal(rule.get_premises(),self.A):
                    # Create a new rule for each new literal
                    conclusion = Literal(rule.get_conclusion().get_name())
                    premises = rule.get_premises()
                    for i in range(1,k+1):
                        if i == k:
                            new_rule = Rule(premises,Literal(conclusion.get_name()),1,Literal(f"r{len(self.R)+1}"))
                        else:
                            new_rule = Rule(premises,Literal(conclusion.get_name() + str(i)),1,Literal(f"r{len(self.R)+1}"))
                        self.R.add(new_rule)
                # If it is not an atomic rule
                else:
                    # Create a new rule for each new literal from 2 to k
                    for i in range(2,k+1):
                        new_premises = set()
                        for premise in rule.get_premises():
                            new_premises.add(Literal(premise.get_name() + str(i-1)))
                        if i == k:
                            new_conclusion = Literal(rule.get_conclusion().get_name())
                        else:
                            new_conclusion = Literal(rule.get_conclusion().get_name() + str(i))
                        new_rule = Rule(new_premises,new_conclusion,1,Literal(f"r{len(self.R)+1}"))
                        self.R.add(new_rule)
        return self
    
    # Function to create an atomic ABA from a non circular 
    def non_circular_into_atomic(self):
        a_prime = self.A.copy()
        l_prime = self.L.copy()
        r_prime = self.R.copy()
        c_prime = self.C.copy()
        
        # For each literal which is not an assumption
        for literal in self.L:
            if literal not in self.A:
                # Create the new literals
                literal_dependant = Literal(f"{literal.get_name()}d")
                literal_non_dependant = Literal(f"{literal.get_name()}nd")
                # Add the new literals to the language and the assumptions
                a_prime.add(literal_dependant)
                a_prime.add(literal_non_dependant)
                l_prime.add(literal_dependant)
                l_prime.add(literal_non_dependant)
                # Add the new negations
                c_prime.add(Negation(literal_non_dependant,literal_dependant))
                c_prime.add(Negation(literal,literal_non_dependant))
                
        # Create the new rules
        for rule in self.R:
            # If the rule is atomic, we keep it
            if include_literal(rule.get_premises(),self.A):
                continue
            else:
                premises = rule.get_premises()
                conclusion = rule.get_conclusion()
                for literal in premises:
                    if literal not in a_prime:
                        premises.remove(literal)
                        premises.add(Literal(f"{literal.get_name()}d"))
                # Replace the rule by the new one
                name_rule = rule.get_reference()
                r_prime = remove_rule(rule,r_prime)        
                new_rule = Rule(premises,conclusion,1,name_rule)
                r_prime.add(new_rule)
                
        self.A = a_prime
        self.L = l_prime
        self.R = r_prime
        self.C = c_prime
        return self
    
    # Function to create the set of normal attacks
    def create_normal_attacks(self, arguments):
        normal_attacks = []
        subsets = get_all_subsets(self.A) # Get all the subsets of the assumptions
        for subsetX in subsets:
            # Range of the subsets X ( attacker set )
            for arg in arguments:
                # If the premises X' of the argument are included in the subset X ( condition 1 )
                arg_premises = arg.get_leaves() # X'
                arg_conclusion = arg.get_claim() # cl(arg)
                if include_literal(arg_premises,subsetX):                
                    # Range of the subsets Y ( attacked set )
                    for subsetY in subsets:
                        # If the conclusion of the argument is the negation of a literal y in the subset Y ( condition 2 )
                        for negation in self.C:
                            neg_attacker = negation.get_attacker() # cl(arg)
                            neg_attacked = negation.get_attacked() # y
                            if neg_attacker == arg_conclusion and neg_attacked in subsetY:
                                # If y is not preferred to all the literals in X' ( condition 3 )
                                preferred = False
                                for preference in self.P:
                                    if preference.get_prefered() == neg_attacked and preference.get_not_prefered() in arg_premises:
                                        preferred = True
                                        break
                                if not preferred:
                                    # Create the normal attack
                                    normal_attacks.append([subsetX,subsetY])                                    
                                    
        # Remove the attacks which are the same                          
        normal_attacks = remove_double_attacks(normal_attacks)
        return normal_attacks
    
    # Function to create the set of reverse attacks
    def create_reverse_attacks(self, arguments):
        reverse_attacks = []
        subsets = get_all_subsets(self.A) # Get all the subsets of the assumptions
        for subsetY in subsets:
            # Range of the subsets Y ( attacked set )
            for arg in arguments:
                # If the premises Y' of the argument are included in the subset Y ( condition 1 )
                arg_premises = arg.get_leaves() # Y'
                arg_conclusion = arg.get_claim() # cl(arg)
                if include_literal(arg_premises,subsetY):                
                    # Range of the subsets X ( attacker set )
                    for subsetX in subsets:
                        # If the conclusion of the argument is the negation of a literal x in the subset X ( condition 2 )
                        for negation in self.C:
                            neg_attacker = negation.get_attacker() # cl(arg)
                            neg_attacked = negation.get_attacked() # x
                            if neg_attacker == arg_conclusion and neg_attacked in subsetX:
                                # If x is preferred to one of the literals in Y' ( condition 3 )
                                preferred = False
                                for preference in self.P:
                                    if preference.get_prefered() == neg_attacked and preference.get_not_prefered() in arg_premises:
                                        preferred = True
                                        break
                                if preferred:
                                    # Create the normal attack
                                    reverse_attacks.append([subsetX,subsetY])
                                    
        # Remove the attacks which are the same                          
        reverse_attacks = remove_double_attacks(reverse_attacks)
        return reverse_attacks
    
# Function to check if a set of literals is included in another set
def include_literal(literals,liste):
    included = True
    for lit in literals:
        if lit not in liste:
            included = False
            break   
    return included

# Function to remove a rule from a set of rules
def remove_rule(rule,rules):
    new_rules = set()
    for r in rules:
        if r != rule:
            new_rules.add(r)
    return new_rules

# Function to remove the attacks which are the same
def remove_double_attacks(attacks):
    new_attacks = []
    for att in attacks:
        if att not in new_attacks:
            new_attacks.append(att)
    return new_attacks

# Function to get all the subsets of a set
def get_all_subsets(s):
    all_subsets = set()
    for i in range(0,len(s)+1):
        all_subsets = all_subsets.union(set(combinations(s,i)))
    return all_subsets

# Function to print the attacks
def print_attacks(attacks):
    for att in attacks:
        print("{",end="")
        for i, subset in enumerate(att[0]):
            print(subset.to_string(),end="")
            if i < len(att[0]) - 1:
                print(",",end="")
        print("} -> {",end="")
        for i, subset in enumerate(att[1]):
            print(subset.to_string(),end="")
            if i < len(att[1]) - 1:
                print(",",end="")
        print("}")

def exemple_TD1():
    a = Literal("a")
    b = Literal("b")
    c = Literal("c")
    q = Literal("q")
    p = Literal("p")
    r = Literal("r")
    s = Literal("s")
    t = Literal("t")
    
    L = {a,b,c,q,p,r,s,t}
    
    R1 = Rule({q,a},p,1,Literal("r1"))
    R2 = Rule({},q,1,Literal("r2"))
    R3 = Rule({b,c},r,1,Literal("r3"))
    R4 = Rule({p,c},t,1,Literal("r4"))
    R5 = Rule({t},s,1,Literal("r5"))

    R = {R1,R2,R3,R4,R5}

    A = {a,b,c}
    
    negation1 = Negation(r,a)
    negation2 = Negation(s,b)
    negation3 = Negation(t,c)
    
    C = {negation1,negation2,negation3}
    
    preference1 = Preference(a,b)
    
    P = {preference1}
    
    return ABA(L,R,A,C,P)


def exemple_TD2():
    # Définition des littéraux
    a = Literal("a")
    b = Literal("b")
    x = Literal("x")
    y = Literal("y")
    z = Literal("z")

    # Ensemble des littéraux
    L = {a, b, x, y, z}

    # Règles adaptées aux nouvelles définitions
    R1 = Rule({b}, y, 1, Literal("r1"))  # y <- b
    R2 = Rule({y}, y, 1, Literal("r2"))  # y <- y
    R3 = Rule({x}, x, 1, Literal("r3"))  # x <- x
    R4 = Rule({a}, x, 1, Literal("r4"))  # x <- a
    R5 = Rule({x, y}, z, 1, Literal("r5"))  # z <- x, y

    # Ensemble des règles
    R = {R1, R2, R3, R4, R5}

    # Ensemble des hypothèses
    A = {a, b}

    # Attaques modifiées
    negation1 = Negation(y, a)  # y attaque a (correspond à y = not a)
    negation2 = Negation(x, b)  # x attaque b (correspond à x = not b)

    # Ensemble des attaques
    C = {negation1, negation2}

    return ABA(L,R,A,C, set())

def test():
    a = Literal("a")
    b = Literal("b")
    q = Literal("q")
    p = Literal("p")
    
    L = {a,b,q,p}
    
    A = {a}
    
    r1 = Rule({a,b},q,1,Literal("r1"))
    r2 = Rule({q},p,1,Literal("r2"))
    r3 = Rule({p},a,1,Literal("r3"))
    
    R = {r1,r2,r3}
    
    return ABA(L,R,A,set(), set())
    

if __name__ == "__main__":

    #parser = Parser("example1.txt")
    #aba = ABA(parser.L, parser.R, parser.A, parser.C, parser.P)
    aba = exemple_TD1()
    print("ABA basic :\n", aba)
        
    print("Is the framework atomic ?", aba.is_atomic())
    print("Is the framework circular ?", aba.is_circular(), "\n")
    
    aba.create_non_cicular()
    print("ABA non-circular :\n", aba)
    
    print("List of rules :")
    for rule in aba.R:
        print(rule.to_string())
        
    print("\nList of arguments :")
    arguments = aba.create_argument()
    for a in arguments:
        print(a.to_string())
        
    print("Number of arguments : " + str(len(arguments)) + "\n")
        
    print("List of attacks :")
    att = aba.create_attacks(arguments)
    for a in att:
        print(a[0].get_name() + " -> " + a[1].get_name())
        
    print("Number of attacks : " + str(len(att)) + "\n")
    
    normal_attacks = aba.create_normal_attacks(arguments)
    print("List of normal attacks :")
    print_attacks(normal_attacks)
    print ("Number of normal attacks : " + str(len(normal_attacks)) + "\n")
    
    reverse_attacks = aba.create_reverse_attacks(arguments)
    print("List of reverse attacks :")
    print_attacks(reverse_attacks)
    print ("Number of reverse attacks : " + str(len(reverse_attacks)) + "\n")
    
    aba.non_circular_into_atomic()
    print("ABA non-circular and atomic :\n", aba)
    