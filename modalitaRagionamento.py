#file che contiene gli algoritmi nel caso di ricerca Soddisfacibilità o valore numeri
from services.risoluzione import *
from services.algoritmiNumerici import valore

#per soddisfacibilità
def Rsoddisfacibilita(decisione, nome_var, proprieta, oggetti, congiun):
  s=Solver()
  risultati=[]
  var=generaVariabili(congiun, s)
  x1=risolvi(congiun, var)
  
  for i in range(len(nome_var)):
  
    formula=decisione

    for j in range(len(proprieta)): #crea, per ogni oggetto, la formula che codifica il grado di bontà
      if proprieta[j] in decisione:
        formula=formula.replace(proprieta[j], nome_var[i][j])
    

    varN=generaVariabili(formula, s)
    x=risolvi(formula, varN)
    s.push()
    s.add(And(x1==1, x<1))
      
    if s.check()==unsat:
      risultati.append([i, "Si"])
      
    else:
      risultati.append([i, "No"])
    s.pop()
        
  output=[]
  for coppia in risultati:
    output.append(oggetti[coppia[0]]+"       ["+str(coppia[1])+"]")

  return output



#genera una classifica del valore di "bontà" rispetto la query
def Rclassifica(nome_var, decisione, proprieta, congiun, oggetti):
  s=Solver()
  classif=[]
  val=[]

  var=generaVariabili(congiun, s)
  x1=risolvi(congiun, var)
  s.add(x1==1)
  s.check()
  modello=s.model()

  
  for i in range(len(nome_var)):
    for j in range(len(nome_var[i])):
      val.append(Soluzione(nome_var[i][j], valore(nome_var[i][j], modello)))
  
  for i in range(len(nome_var)):
    
    formula=decisione
    for j in range(len(proprieta)): #crea, per ogni oggetto, la formula che codifica il grado di bontà
      if proprieta[j] in decisione:
        formula=formula.replace(proprieta[j], nome_var[i][j])
        
    x=risolvi(formula, val) 

    if i==0:
      classif.append([i, x]) 

    else:

      for k in range(len(classif)):
        if x>classif[k][1]: #se il valore di bontà è migliore rispetto ad un oggetto già analizzato, il nuovo oggetto si pone davanti
          classif.insert(k, [i, x])
          break
      
      if k+1==len(classif): #se è il peggiore, si pone l'oggetto dietro a tutti gli altri
        classif.append([i, x])

    output=[]
    for coppia in classif:
      output.append(oggetti[coppia[0]]+"       ["+str(round(coppia[1], 3))+"]")

  return output