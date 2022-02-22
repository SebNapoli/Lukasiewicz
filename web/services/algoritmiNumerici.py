#file con tutti algoritmi numerici o per ricavate dai modelli di z3 i valori numerici delle soluzioni

#calcolo massimo comun divisore
def MCD(a, b):
    if b==1:
        return 1
    if b==0:
        return a
    else:
        return MCD(b, a%b)


#per ogni proprietà della tabella, si calcola il minimo e il massimo
def MassimiMinimi(tabella, rig, col):
  massimi=[]
  minimi=[]

  for j in range(col):
    for i in range(rig):
      if i==0:
        x=y=tabella[i][j]
        
      else:
        x=min(x, tabella[i][j])
        y=max(y, tabella[i][j]) 
    
    minimi.append(x)
    massimi.append(y) #calcolo del valore massimo e del valore minimo per ogni proprietà
  
  return massimi, minimi

#ricava dal modello il valore di verità
def valore(nome_var, modello): 
  for d in modello.decls():
    if nome_var==d.name():
      frazione=str(modello[d])
      
      if '/' in frazione:
        ind=frazione.index('/')
        num=int(frazione[:ind])
        den=int(frazione[ind+1:])
      else:
        num=int(frazione)
        den=1

      val=float(num/den)

      return val
