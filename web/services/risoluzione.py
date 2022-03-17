#file content: resolution algoritms
from z3 import *
from services.classi import *
from services.ricercaStringa import *
from services.operazioni_logiche import *

#The app creates the list of all Lukasiewicz's logic variables 
def create_variables(formula, s): 
  variables=[]
    
  Nformula=formula.replace('(', '')
  Nformula=Nformula.replace(')', '')
  Nformula=Nformula.replace('-', '')
  #It deletes useless signs

  i=0
  ini=0
  #Until the end of the formula
  while(i<len(Nformula)): 

    #If it finds a binary connective or it's at the end of the formula
    if Nformula[i] in conn or i==len(Nformula)-1:
      if i==len(Nformula)-1:
        fin=len(Nformula)
      else:
        fin=i

      variab=Nformula[ini:fin]
      #new variable name
      ini=i+1
      #if it isn't a logic constant
      if variab not in logic_con: 
        unique=True

        #control on the list
        for k in range(len(variables)): 
          if variab==variables[k].name:
            unique=False
            break
        
        #add it in the list if it is not already in
        if unique: 
          x=Var_Prop(variab, s)
          variables.append(x)
    
    i+=1

  return variables #return the list


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

#generation for alternative solution for satisfability
def alternatives(mod, variable, N, s): 
  nuovo=0 #number of new solutions found 
  
  #if user wants other solutions
  if N!=0: 

    alternative=[]  

    #WARNING! A reserch on variable names is needed: the output order is not the z3 order 
    for i in range(len(variable)): 
      for d in mod.decls():
        if d.name()==variable[i].name:
          y=variable[i].variable!=mod[d]
          if i==0:
            x=y
          else:
            x=Or(x, y)
          s.add(x) #add the condition "the solution is different than the old one"
          break

    
    while nuovo<N: #the algoritm will end when it find N new solutions 
      if s.check()==sat: #if a different solution exist
        Nmod=s.model() #find it
        output=str(Nmod)
        output=output.replace('[', '')
        output=output.replace(']', '')
        alternative.append(output) #print the solution
        nuovo+=1 #update new solution number 
        for i in range(len(variable)):
          for d in mod.decls():
            if d.name()==variable[i].name:
              y=(variable[i].variable!=Nmod[d])
              if i==0:
                x=y
              else:
                Or(x, y)
              s.add(x) #add the condition "the solution is different than the old one"

      else: #otherwise
        break #end the loop
      
    if nuovo==0: #if new solutions don't exist
      alternative.append("They don't exist")
  
  else:
    alternative=None
  
  return alternative



conn='&+_^U>=' #lista dei connettivi binari disponibili, in ordine di priorità
logic_con='01'