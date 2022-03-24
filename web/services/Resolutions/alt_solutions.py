from z3 import *

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
          break

    s.add(x) #add the condition "the solution is different than the old one"

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
                x=Or(x, y)
        
        s.add(x) #add the condition "the solution is different than the old one"

      else: #otherwise
        break #end the loop
      
    if nuovo==0: #if new solutions don't exist
      alternative.append("They don't exist")
  
  else:
    alternative=None
  
  return alternative
