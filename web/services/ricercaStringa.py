def trovaParentesi(formula, j): #aperta una parentesi, trova in quale posizione viene chiusa
  pila=['(']
  for i in range(len(formula)):
    if i>j:
      if formula[i]=='(': 
        pila.append('(') #se viene aperta una nouva parentesi, aggiungi un'elemento alla pila
      elif formula[i]==')': 
        pila.remove(pila[len(pila)-1]) #se viene chiusa una parentesi, rimuovila dalla pila
        if len(pila)==0: #se non ci sono più parentesi "attive"
          return i #restituzione della posizione chiusura parentesi
  
  return -1 #restituisce il valore -1 se esite qualche parentesi non chiusa



def riconoscimentoVariabile(formula, i):
    j=i
    while j!=len(formula):
      if formula[j] in con:
        break
      else:
        j+=1
    argomento=formula[i:j] #individua il nome della variabile

    return argomento, j



conn='&+_^U>=' #lista dei connettivi binari disponibili, in ordine di priorità
costanti_logiche='01'
aus='P*'
con=conn+aus