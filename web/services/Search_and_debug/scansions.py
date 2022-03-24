from services.Search_and_debug.search_on_string import *

#return subformulas and connectives order
def scansion(formula): 
  i=0 
  subformulas=[] 
  connectives=[] 
  
  #scan the formula
  while i<len(formula): 
    if formula[i] in con: #if it's a connective
      connectives.append(formula[i]) #add in connectives list
      i+=1 
    
    elif formula[i]=='(': #if a bracket is opened
      j=find_bracket(formula, i) #find where it's closed
      subformulas.append(formula[i:j+1]) #add the subformula in the list
      i=j+1 #passa alla scansione dopo la chiusura della parentesi

    elif formula[i]=='-': 
      if formula[i+1]=='(': #as before
        j=find_bracket(formula, i+1)
        subformulas.append('-'+formula[i+1:j+1])
        i=j+1
      
      else:  #if it's a variable
        [argument, i]=variable_name(formula, i+1)
        subformulas.append('-'+argument) #add the variable in subformulas list 
    
    elif formula[i:i+5]=='very ':
      if formula[i+5]=='(':
        j=find_bracket(formula, i+5)
        subformulas.append("very "+formula[i+5:j+1])
        i=j+1
      
      else:
        [argument, i]=variable_name(formula, i+5)
        subformulas.append("very "+argument)

    elif formula[i:i+6]=="quite ":
      if formula[i+6]=='(':
        j=find_bracket(formula, i+6)
        subformulas.append("quite "+formula[i+6:j+1])
        i=j+1

      else:
        [argument, i]=variable_name(formula, i+6)
        subformulas.append("quite "+argument)

    else: 
      [argument, i]=variable_name(formula, i)
      subformulas.append(argument)
  

  return subformulas, connectives 

conn='&+_^U>='
logic_con='01'
aux='P*'
con=conn+aux