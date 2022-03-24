from z3 import *
from services.Resolutions.resolutions_classes import *
from services.Resolutions.resolution import *
from services.Resolutions.create_variables import *
from services.Vague_Reasoning.num_algoritms import *

#reasoning mode: satisfiability
def Rsatisfiability(query, var_name, property, objects, conj):
  s=Solver()
  results=[]
  var=create_variables(conj, s)
  x1=resolving(conj, var)
  
  for i in range(len(var_name)):
  
    formula=query

    for j in range(len(property)): #create the formula which rapresent the truth value for all objects 
      if property[j] in query:
        formula=formula.replace(property[j], var_name[i][j])
    

    varN=create_variables(formula, s)
    x=resolving(formula, varN)
    s.push()
    s.add(And(x1==1, x<1))
      
    if s.check()==unsat:
      results.append([i, "Yes"])
      
    else:
      results.append([i, "No"])
    s.pop()
        
  output=[]
  for couple in results:
    output.append(objects[couple[0]]+"       ["+str(couple[1])+"]")

  return output



#create the ranking of truth values
def rank(var_name, query, property, conj, objects):
  s=Solver()
  ranking=[]
  val=[]

  var=create_variables(conj, s)
  x1=resolving(conj, var)
  s.add(x1==1)
  s.check()
  modello=s.model()

  
  for i in range(len(var_name)):
    for j in range(len(var_name[i])):
      val.append(Solution(var_name[i][j], value(var_name[i][j], modello)))
  
  for i in range(len(var_name)):
    
    formula=query
    for j in range(len(property)): #create the formula which rapresent the truth value for all objects
      if property[j] in query:
        formula=formula.replace(property[j], var_name[i][j])
        
    x=resolving(formula, val) 

    if i==0:
      ranking.append([i, x]) 

    else:

      for k in range(len(ranking)):
        if x>ranking[k][1]: #if the new truth value is better, place it before the old one
          ranking.insert(k, [i, x])
          break
      
      if k+1==len(ranking): #if it's the worst, place it at the bottom
        ranking.append([i, x])

    output=[]
    for couple in ranking:
      output.append(objects[couple[0]]+"       ["+str(round(couple[1], 3))+"]")

  return output