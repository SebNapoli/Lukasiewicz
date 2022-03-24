from z3 import *

class Var_Prop: #class of all Lukasiewicz's variables
  def __init__(self, string, s):
      self.name=string
      self.variable=Real(string)
      s.add(And(self.variable<=1, self.variable>=0)) #the propositional variable value has to be between 0 and 1



class Solution: #class of all thuth values from z3
  def __init__(self, name, value):
    self.name=name
    self.variable=value