from services.Resolutions.resolutions_classes import *

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

conn='&+_^U>=' #lista dei connettivi binari disponibili, in ordine di priorità
logic_con='01'