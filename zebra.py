from copy import deepcopy
from abc import ABCMeta


class Domain:
    # Domain class isn't used except to initially specify the number of houses allocated to the Variable class.
    # Solution would work the same way without this class and domains specified as an argument of the Variable
    #  constructor.
    def __init__(self):
        # self.type = type
        # self.identifier = identifier

        self.possible_house = [1, 2, 3, 4, 5]


    def get_domain(self):
        return self.possible_house

    def create_domain(self):
        return self.possible_house

    def delete(self):
        del self

    def print_thing(self):
        print self

    def split_in_half(self):
        pass

    def __eq__(self):
        # to compare two domains
        pass

    def is_empty(self):
        return len(self.possible_house) == 0

    def is_reduced_to_only_one_value(self):
        return len(self.possible_house) == 1


class Variable(Domain):

    def __init__(self, name, id_type, Domain):
        self.name = name
        self.id = id_type
        self.domain = Domain.possible_house

    def print_details(self):
        print self.name, self.id, self.domain

    def print_id(self):
        print self.id

    def get_Domain(self):
        print self.domain

    def set_Domain(self, domain):
        self.domain = domain


class Constraint():
    __metaclass__ = ABCMeta
    # does nothing except to provide empty methods for the other constraints to override!

    def create_constraint(self):
        pass

    def delete_constraint(self):
        pass

    def print_constraint(self):
        pass

    def is_satisfied(self):
        pass

    def reduce(self):
        pass


class ConstraintEqualityVarVar(Constraint):

    def __init__(self, varA, varB):
        self.varA = varA
        self.varB = varB

    def is_satisfied(self):
        # satisfied if the variable's domains have at least one value in common.
        for a in self.varA.domain:
            for b in self.varB.domain:
                if a == b:
                    return True
        return False

    def reduce(self):
        # common_values = []
        for a in self.varA.domain[:]:
            # doesn't work without the colons
            if a not in self.varB.domain[:]:
                self.varA.domain.remove(a)
        for b in self.varB.domain[:]:
            if b not in self.varA.domain[:]:
                self.varB.domain.remove(b)

        # Alternative method. Didn't use because seems more roundabout.

        #     for j in self.varB.domain:
        #         if i == j:
        #             common_values.append(i)
        # self.set_domain(common_values)


        # ConstraintEqualityVarVar test

        # glaswegian = Variable("Glaswegian", "nationality1", Domain())
        # glaswegian.set_Domain([1, 2, 3, 4])
        #
        # mexican = Variable("Mexican", "nationality2", Domain())
        # mexican.set_Domain([3, 4, 5, 6])
        #
        # c1 = ConstraintEqualityVarVar(glaswegian, mexican)
        # c1.reduce()
        # glaswegian.get_Domain()
        # mexican.get_Domain()
        # Milk.get_Domain()


class ConstraintEqualityVarCons(Constraint):

    def __init__(self, varA, constant):
        self.varA = varA
        self.constant = constant

    def is_satisfied(self):
        return self.constant in self.varA.domain
        # boolean statement so don't need to explicitly return true or false

    def reduce(self):
        if self.is_satisfied():
            # calls set_Domain on varA with argument constant
            self.varA.set_Domain([self.constant])

# Test ConstraintEqualityVarCons

# glaswegian = Variable("Glaswegian", "nationality1", Domain())
# glaswegian.set_Domain([1, 2, 3, 4])
#
# testcons = ConstraintEqualityVarCons(glaswegian, 3)
# testcons.reduce()
# glaswegian.get_Domain()

class ConstraintEqualityVarPlusCons(Constraint):

    def __init__(self, varA, varB, constant):
        self.varA = varA
        self.varB = varB
        self.constant = constant

    def is_satisfied(self):
        for a in self.varA.domain:
            for b in self.varB.domain:
                if a == (b + self.constant):
                    return True
        return False

    def reduce(self):

        for a in self.varA.domain:
            if (a-self.constant) not in self.varB.domain:
                self.varA.domain.remove(a)
        # remove values from varA.domain if a-constant isn't in varB's domain
        # possibly add elseif (a+1) not in etc.

        for b in self.varB.domain:
            if (b+self.constant) not in self.varA.domain:
                self.varB.domain.remove(b)

        # Alternative method gave wrong result, above seems more elegant

        # for a in self.varA.domain:
        #     for b in self.varB.domain:
        #         if a == (b + self.constant):
        #             self.varA.domain.remove(a)
        # for b in self.varB.domain:
        #     for a in self.varA.domain:
        #         if b == (a - self.constant):
        #             self.varB.domain.remove(b)



# ConstraintEqualityVarPlusCons test

# snowman = Bowie + 1

# snowman = Variable("Snowman", "nationality1", Domain())
# snowman.set_Domain([1, 2, 3, 5, 7, 8])
#
# bowie = Variable("Bowie", "nationality1", Domain())
# bowie.set_Domain([1, 2, 3, 4, 7])
#
# test = ConstraintEqualityVarPlusCons(snowman, bowie, 1)
# test.reduce()
# snowman.get_Domain()
# bowie.get_Domain()


class ConstraintDifferenceVarVar(Constraint):

    def __init__(self, varA, varB):
        self.varA = varA
        self.varB = varB

    def is_satisfied(self):
        # boolean expression, 'not' inverts the conditions in brackets
        # not satisfied if both domains are reduced to a single identical value
        return not (len(self.varA.domain) == 1 and len(self.varA.domain) == 1 and self.varA.domain == self.varB.domain)

    def reduce(self):
        # print "Doing difference reduction for {} {}".format(self.varA.name, self.varB.name)
        # checks first one domain then the other to see is either are reduced to one value.
        if len(self.varB.domain) == 1:
            # self.varB.domain returns a list containing one value
            # index returns only remaining value
            if self.varB.domain[0] in self.varA.domain:
                self.varA.domain.remove(self.varB.domain[0])
        if len(self.varA.domain) == 1:
            # self.varA.domain returns a list containing one value
            if self.varA.domain[0] in self.varB.domain:
                self.varB.domain.remove(self.varA.domain[0])


class ConstraintNextTo(Constraint):
    # if varA contains a 1, if varB doesn't have 0 or 2, remove 1 from varA

    def __init__(self, varA, varB):
        self.varA = varA
        self.varB = varB

    def is_satisfied(self):
        for a in self.varA.domain:
            if (a-1) in self.varB.domain or (a+1) in self.varB.domain:
                return True
                # satisfied if there are any values of a +/-1 also present in B
        return False

    def reduce(self):
        for a in self.varA.domain:
            if (a-1) not in self.varB.domain and (a+1) not in self.varB.domain:
                # if a value of a is not a neighbour in either direction of any value in B, remove from A's domain.
                self.varA.domain.remove(a)
        for b in self.varB.domain:
                # repeat
            if (b-1) not in self.varA.domain and (b+1) not in self.varB.domain:
                self.varB.domain.remove(b)

# ConstraintNextTo test:

# snowman = Variable("Snowman", "nationality1", Domain())
# snowman.set_Domain([1, 2, 3, 4, 5])
#
# bowie = Variable("Bowie", "nationality2", Domain())
# bowie.set_Domain([3, 5])
#
# test = ConstraintNextTo(snowman, bowie)
# test.reduce()
# snowman.get_Domain()
# bowie.get_Domain()

# expected output: [2, 4]
# expected output: [3,5]


# Initialise nationality variables

english = Variable("English", "country1", Domain())
spaniard = Variable("Spaniard", "country2", Domain())
ukrainian = Variable("Ukrainian", "country3", Domain())
norwegian = Variable("Norwegian", "country4", Domain())
japanese = Variable("Japanese", "country5", Domain())

# Initialise colour variables

red = Variable("Red", "colour1", Domain())
green = Variable("Green", "colour2", Domain())
ivory = Variable("Ivory", "colour3", Domain())
yellow = Variable("Yellow", "colour4", Domain())
blue = Variable("Blue", "colour5", Domain())

# Initialise pet variables

dog = Variable("Dog", "pet1", Domain())
snails = Variable("Snails", "pet2", Domain())
fox = Variable("Fox", "pet3", Domain())
horse = Variable("Horse", "pet4", Domain())
zebra = Variable("Zebra", "pet5", Domain())

# Initialise board game variables

Snakes_and_Ladders = Variable("Snakes and Ladders", "boardgame1", Domain())
Cluedo = Variable("Cluedo", "boardgame2", Domain())
Pictionary = Variable("Pictionary", "boardgame3", Domain())
Travel_the_World = Variable("Travel the World", "boardgame4", Domain())
Backgammon = Variable("Backgammon", "boardgame5", Domain())

# Initialise beverage variables

Coffee = Variable("Coffee", "beverage1", Domain())
Tea = Variable("Tea", "beverage2", Domain())
Milk = Variable("Milk", "beverage3", Domain())
Orange_juice = Variable("Orange Juice", "beverage4", Domain())
Water = Variable("Water", "beverage5", Domain())

# Initialise non-contradiction constraints (50 of them)

c1 = ConstraintDifferenceVarVar(english, spaniard)
c2 = ConstraintDifferenceVarVar(english, ukrainian)
c3 = ConstraintDifferenceVarVar(english, norwegian)
c4 = ConstraintDifferenceVarVar(english, japanese)
c5 = ConstraintDifferenceVarVar(norwegian, spaniard)
c6 = ConstraintDifferenceVarVar(norwegian, ukrainian)
c7 = ConstraintDifferenceVarVar(norwegian, japanese)
c8 = ConstraintDifferenceVarVar(spaniard, ukrainian)
c9 = ConstraintDifferenceVarVar(spaniard, japanese)
c10 = ConstraintDifferenceVarVar(ukrainian, japanese)

c11 = ConstraintDifferenceVarVar(Milk, Orange_juice)
c12 = ConstraintDifferenceVarVar(Milk, Tea)
c13 = ConstraintDifferenceVarVar(Milk, Water)
c14 = ConstraintDifferenceVarVar(Milk, Coffee)
c15 = ConstraintDifferenceVarVar(Orange_juice, Tea)
c16 = ConstraintDifferenceVarVar(Orange_juice, Water)
c17 = ConstraintDifferenceVarVar(Orange_juice, Coffee)
c18 = ConstraintDifferenceVarVar(Tea, Water)
c19 = ConstraintDifferenceVarVar(Tea, Coffee)
c20 = ConstraintDifferenceVarVar(Water, Coffee)

c21 = ConstraintDifferenceVarVar(red, green)
c22 = ConstraintDifferenceVarVar(red, yellow)
c23 = ConstraintDifferenceVarVar(red, blue)
c24 = ConstraintDifferenceVarVar(red, ivory)
c25 = ConstraintDifferenceVarVar(green, yellow)
c26 = ConstraintDifferenceVarVar(green, blue)
c27 = ConstraintDifferenceVarVar(green, ivory)
c28 = ConstraintDifferenceVarVar(yellow, blue)
c29 = ConstraintDifferenceVarVar(yellow, ivory)
c30 = ConstraintDifferenceVarVar(blue, ivory)

c31 = ConstraintDifferenceVarVar(Snakes_and_Ladders, Cluedo)
c32 = ConstraintDifferenceVarVar(Snakes_and_Ladders, Pictionary)
c33 = ConstraintDifferenceVarVar(Snakes_and_Ladders, Travel_the_World)
c34 = ConstraintDifferenceVarVar(Snakes_and_Ladders, Backgammon)
c35 = ConstraintDifferenceVarVar(Cluedo, Pictionary)
c36 = ConstraintDifferenceVarVar(Cluedo, Travel_the_World)
c37 = ConstraintDifferenceVarVar(Cluedo, Backgammon)
c38 = ConstraintDifferenceVarVar(Pictionary, Travel_the_World)
c39 = ConstraintDifferenceVarVar(Pictionary, Backgammon)
c40 = ConstraintDifferenceVarVar(Travel_the_World, Backgammon)

c41 = ConstraintDifferenceVarVar(zebra, fox)
c42 = ConstraintDifferenceVarVar(zebra, dog)
c43 = ConstraintDifferenceVarVar(zebra, snails)
c44 = ConstraintDifferenceVarVar(zebra, horse)
c45 = ConstraintDifferenceVarVar(fox, dog)
c46 = ConstraintDifferenceVarVar(fox, snails)
c47 = ConstraintDifferenceVarVar(fox, horse)
c48 = ConstraintDifferenceVarVar(dog, snails)
c49 = ConstraintDifferenceVarVar(dog, horse)
c50 = ConstraintDifferenceVarVar(snails, horse)

# Set clue constraints
# Englishman = red
clue1 = ConstraintEqualityVarVar(english, red)
# Spaniard = dog
clue2 = ConstraintEqualityVarVar(spaniard, dog)
# coffee = green
clue3 = ConstraintEqualityVarVar(Coffee, green)
# Ukrainian = tea
clue4 = ConstraintEqualityVarVar(ukrainian, Tea)
# green=ivory+1
clue5 = ConstraintEqualityVarPlusCons(green, ivory, 1)
# snakes and ladders = snails
clue6 = ConstraintEqualityVarVar(Snakes_and_Ladders, snails)
# Cluedo = yellow
clue7 = ConstraintEqualityVarVar(Cluedo, yellow)
# milk = 3
clue8 = ConstraintEqualityVarCons(Milk, 3)
# Norwegian = 1
clue9 = ConstraintEqualityVarCons(norwegian, 1)
# Pictionary fox next to
clue10 = ConstraintNextTo(Pictionary, fox)
# Cluedo horse next to
clue11 = ConstraintNextTo(Cluedo, horse)
# Travel the World = orange juice
clue12 = ConstraintEqualityVarVar(Travel_the_World, Orange_juice)
# Japanese = Backgammon
clue13 = ConstraintEqualityVarVar(japanese, Backgammon)
# Norwegian blue next to
clue14 = ConstraintNextTo(norwegian, blue)

VariableList = [english, spaniard, ukrainian, norwegian, japanese, red, green, ivory, yellow, blue, dog, snails, fox,
                horse, zebra, Snakes_and_Ladders, Cluedo, Pictionary, Travel_the_World, Backgammon, Milk, Orange_juice,
                Tea, Coffee, Water]

ConstraintList = [clue1, clue2, clue3, clue4, clue5, clue6, clue7, clue8, clue9, clue10, clue11, clue12, clue13, clue14,
                  c1, c2, c3, c4, c5, c6, c7, c8, c9, c10, c11, c12, c13, c14, c15, c16, c17, c18, c19, c20, c21, c22,
                  c23, c24, c25, c26, c27, c28, c29, c30, c31, c32, c33, c34, c35, c36, c37, c38, c39, c40, c41, c42,
                  c43, c44, c45, c46, c47, c48, c49, c50]


for i in ConstraintList:
    for j in ConstraintList:
        if i.is_satisfied():
            i.reduce()
        if j.is_satisfied():
            j.reduce()


for i in xrange(len(VariableList)):
    print 'Domain for', VariableList[i].name, 'is:', VariableList[i].domain



# class Problem

# define problem constraints

# define constraints between variables, so:

# c1 = constraint_equality_var_var(red, green) (red and green are not the same) etc
# add to problem set
# loop for i in problem set
# problem.reduce

# 64 constraints(?) (50 non contradiction + 14 clues)
# for each constraint:
    # c.reduce
    # until nothing happens, then split domains.
    # So say four domains left for 'Englishman'. Add domain 1,2 to list child1 [], then 3,4 to list child2[]
    # continue to reduce. If nothing happens, reduce again.
