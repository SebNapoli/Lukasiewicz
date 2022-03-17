from z3 import *
from services.algoritmiNumerici import *
from services.costruzioneFormule import *
from services.debug import debugFormula
from services.scansioneIniziale import *
from services.controlloRagionamento import *
from services.modalitaRagionamento import *
from services.linguaggioNaturale import *

#create the formulas for table coding
def formulas_construction(table, var_name, comparison, row, col, N): 
  set=[]

  [maxs, mins]=MaxMin(table, row, col) #find maxs and mis 

  for i in range(row):
    for j in range(col):
      den=maxs[j]-mins[j]
      if comparison[j]=='max':
        num=table[i][j]-mins[j]
      else:
        num=maxs[j]-table[i][j]

      if num==den: #if it's the max value, the coding formula is x=1
        set.append(var_name[i][j]+'=1')

      elif num==0: #if it's the min value, the coding formula
        set.append(var_name[i][j]+'=0')

      else:
        div=MCD(den, num)
        den=int(den/div)
        num=int(num/div)
        if N=="inf": #if the user's will is a exact coding
          f1=Cformula(float(num/den), den, 1-num, var_name[i][j])
          f2=Cformula2(float(num/den), -den, 1+num, var_name[i][j])
          set.append('('+f1+')^('+f2+')')

        else:
          N=int(N)
          if N>=den: #if it's possible to find a exact code (the wanted precison is smaller than the fraction step)
            f1=Cformula(float(num/den), den, 1-num, var_name[i][j])
            f2=Cformula2(float(num/den), -den, 1+num, var_name[i][j])
            set.append('('+f1+')^('+f2+')')
          
          else:  
            for k in range(N): #find the gap
              if float(num/den)<float((k+1)/N):
                if k==0:
                  f1='1'
                else:  
                  f1=Cformula(float(k/N), N, 1-k, var_name[i][j])

                if k==(N-1):
                  f2='1'
                else:
                  f2=Cformula2(float((k+1)/N), -N, 1+(k+1), var_name[i][j])
                set.append('('+f1+')^('+f2+')')
                break
         
  return set #return the set for formulas


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