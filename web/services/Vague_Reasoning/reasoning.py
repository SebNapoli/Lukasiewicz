from z3 import *
from services.Vague_Reasoning.check_on_reasoning import *
from services.Vague_Reasoning.natural_language import *
from services.Vague_Reasoning.reasoning_modes import *
from services.Vague_Reasoning.formulas_construction import *
from services.Search_and_debug.start_scansion import *
from services.Search_and_debug.debug import *

#base algoritm for reasoning mode
def Rea(row, col, property, objects, table, comparisons, decision, den, mode):
  var_name=[]  


  par_control(property, objects, row, col)
  #control on the names of parametres

  #create all variables name
  for i in range(row):
    var_name.append([])
    for j in range(col):
      var_name[i].append(property[j]+str(i+1))

  if ("very " in decision) or ("quite " in decision):
    decision=natural_language(decision)
  else:
    initial_scansion(decision)

  decision=decision.replace(' ', '') 
  [query, decision]=debugFormula(decision)
  query_control(property, decision)
  #control on the query
  

  #create the set of coding formulas
  if den=="inf" or den.isdecimal():
    formulas=formulas_construction(table, var_name, comparisons, row, col, den)
  else:
    raise TypeError

  
  conj=''
  for string in formulas:
    f=debugFormula(string)[1]
    conj=conj+'&('+f+')'
  conj=conj[1:]

  #choose the right mode
  if mode=='1':
    return formulas, query, Rsatisfiability(decision, var_name, property, objects, conj)
  else:
    return formulas, query, rank(var_name, decision, property, conj, objects)