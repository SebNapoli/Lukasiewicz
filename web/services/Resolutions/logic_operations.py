#file content: Lukasiewicz functions

from z3 import *

def Luk_min(p, q): #the app finds the min between two propositional variables 
  if ((type(p)==int or type(p)==float) and (type(q)==int or type(q)==float)):
    return min(p, q)
  else:
    return If(p<=q, p, q)


def Luk_max(p, q): #the app finds the max between two propositional variables
  if ((type(p)==int or type(p)==float) and (type(q)==int or type(q)==float)):
    return max(p, q)
  else:
    return If(p>=q, p, q)


def tnorm(p, q): #t-norm, truth value of strong conjuction (max{p+q-1, 0})
  return Luk_max(p+q-1, 0)

def residuum(p, q): #residuum, truth value of implication (min{q-p+1, 1})
  return Luk_min(-p+q+1, 1)

def compl(p): #truth value of negation
  return 1-p

def t_sum(p, q): #truth value strong disj (min{p+q, 1})
  return Luk_min(p+q, 1)

def double_imp(p, q): 
  return tnorm(residuum(p, q), residuum(q, p))

def t_diff(p, q):
  return tnorm(p, compl(q))
