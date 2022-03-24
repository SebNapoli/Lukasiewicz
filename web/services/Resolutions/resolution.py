#file content: resolution algoritms
from z3 import *
from services.Search_and_debug.search_on_string import *
from services.Resolutions.logic_operations import *

#subformula (within brackets) resolution
def subformula(formula, var, i): 
  k=find_bracket(formula, i)
  x=resolving(formula[i+1:k], var) 
  i=k+1
  return x, i #return value and position

#negation resolution
def negation(formula, var, i): 
  
  if formula[i+1]!='(': #if it isn't a subformula negation
    if formula[i+1]=='0':
      x=1
      i+=2
    elif formula[i+1]=='1':
      x=0
      i+=2
    else:
      [argument, i]=variable_name(formula, i+1) #find variable name
      for k in range(len(var)):
        if var[k].name==argument:
          break #find the right z3 variable
      x=compl(var[k].variable) #complement
  
  else: 
    [x, i]=subformula(formula, var, i+1) #subformula resolution
    x=compl(x) #complement
  return x, i #return value and position


def find_argument(formula, i, var):
  if formula[i]=='-':
    [x, i]=negation(formula, var, i) 

  elif formula[i]=='(': 
    [x, i]=subformula(formula, var, i) 

  elif formula[i]=='0': 
    x=0 
    i=i+1

  elif formula[i]=='1':
    x=1 
    i=i+1

  else:
    [argument, i]=variable_name(formula, i)
    for j in range(len(var)):
      if var[j].name==argument:
        break
    x=var[j].variable
  
  return x, i
  
#truth value computing
#WARNING: the script is written with this paradigm: it will compute the first
#Lukasiewicz's operation not in brackets. Remember to parse the formula
#before calling this fuction

def resolving(formula, var): 
  
  i=0
  #until the end of the formula
  while(i<len(formula)): 
    if i==0:  #if we are at the start
      [x, i]=find_argument(formula, i, var)
    else: 
      [y, k]=find_argument(formula, i+1, var)

      #The app chooses the right operation
      if formula[i]=='&':
        x=tnorm(x, y)
      elif formula[i]=='>':
        x=residuum(x, y)
      elif formula[i]=='^':
        x=Luk_min(x, y)
      elif formula[i]=='U':
        x=Luk_max(x, y)
      elif formula[i]=='+':
        x=t_sum(x, y)
      elif formula[i]=='_':
        x=t_diff(x, y)
      else:
        x=double_imp(x, y)

      i=k 

  return x #return truth value




conn='&+_^U>=' #lista dei connettivi binari disponibili, in ordine di priorità
logic_con='01'