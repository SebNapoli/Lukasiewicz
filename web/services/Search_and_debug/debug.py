#file content: debuggin formulas
from services.Search_and_debug.search_on_string import *
from services.Search_and_debug.scansions import *

def merge(c, formula1, formula2): 
      formula='('+formula1+c+formula2+')' 
      return formula




def elaboration(List, connectives, subformulas):
  for x in List:
    while x in connectives:
      i=connectives.index(x) #find the position of the connective
      subformulas[i]=merge(x, subformulas[i], subformulas[i+1]) #add brackets for the formulas
      subformulas[i+1]=''
      subformulas.remove(subformulas[i+1])
      connectives[i]=''
      connectives.remove(connectives[i])

  return subformulas

#return the formula parsing
def parsing(formula):

  if (formula[0]=='(') and (find_bracket(formula, 0)==(len(formula)-1)): 
    formula=parsing(formula[1:-1]) #if all the formula is in brackets, delete the brackets

  [subformulas, connectives]=scansion(formula) #formula scansion

  if len(subformulas)!=1:
    for x in aux:
      while x in connectives:
        i=connectives.index(x) 
        stringa=subformulas[i+1]
        if stringa[0]=='-':
          subformulas[i]=merge(x, subformulas[i], '('+subformulas[i+1]+')') 
        else:
          subformulas[i]=merge(x, subformulas[i], subformulas[i+1])
        subformulas[i+1]=''
        subformulas.remove(subformulas[i+1])
        connectives[i]=''
        connectives.remove(connectives[i])


  if len(subformulas)==1: #if there aren't binary connectives
    if formula[0]=='-': #if there is a negation
      stringa=parsing(formula[1:])

      return '('+ '-' + stringa +')' #return the parsing in the brackets
    else: 
      return subformulas[0] #return the original subformula

  for i in range(len(subformulas)): #parse on all subformulas
    subformulas[i]=parsing(subformulas[i])


  subformulas=elaboration(conn, connectives, subformulas)

  Nformula=subformulas[0]

  return Nformula #return the formula parsed



#from a formula with moltiplication and power signs, return a Lukasiewicz's formula
def transformation(formula):

  while 'P' in formula:
    ind=formula.index('P')
    i=open_bracket(formula, ind)
    j=find_bracket(formula, ind)

    argument=formula[i+1:ind]
    esp=int(formula[ind+1:j])

    for k in range(int(esp)):
      if k==0:
        aux_formula=argument
      else:
        aux_formula=aux_formula+'&'+argument
    
    formula=formula.replace(formula[i+1:j], aux_formula)
  
  while '*' in formula:
    ind=formula.index('*')
    i=open_bracket(formula, ind)
    j=find_bracket(formula, ind)

    factor=int(formula[i+1:ind])
    argument=formula[ind+1:j]

    for k in range(factor):
      if k==0:
        aux_formula=argument
      else:
        aux_formula=aux_formula+'+'+argument

    formula=formula.replace(formula[i+1:j], aux_formula)

  return formula



def debugFormula(formula):
  formula=formula.replace('--', '') #It deletes double negations, which are equivalent to an affemartion
  formula=formula.replace(' ', '')
  formula=parsing(formula)
  new_formula=transformation(formula)
  return formula, new_formula



conn='&+_^U>=' #list of binary connectives
logic_con='01'
aux='P*'
con=conn+aux