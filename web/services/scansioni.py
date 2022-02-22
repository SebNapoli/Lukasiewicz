from services.ricercaStringa import *

def scansione(formula): #restituisce in ordine di apparizione connettivi e argomenti dei connettivi della formula
  i=0 
  sottoformule=[] #lista di tutte le sottoformule che sono argomenti di qualche connettivo
  connettivi=[] #lista dei connettivi
  
  while i<len(formula): #scansiona sequenzialmente la formula
    if formula[i] in con: #se il carattere in esame è un connettivo
      connettivi.append(formula[i]) #il carattere viene aggiunto alla lista dei connettivi
      i+=1 #passa al carattere successivo
    
    elif formula[i]=='(': #se viene aperta una parentesi
      j=trovaParentesi(formula, i) #scopre dove viene chiusa
      sottoformule.append(formula[i:j+1]) #la formula tra parentesi viene aggiunta come argomento di un connettivo
      i=j+1 #passa alla scansione dopo la chiusura della parentesi

    elif formula[i]=='-': #se si trova una negazione
      
      if formula[i+1]=='(': #passaggi simili al caso precente apertura parentesi
        j=trovaParentesi(formula, i+1)
        sottoformule.append('-'+formula[i+1:j+1])
        i=j+1
      
      else: #se il carattere succesivo al simbolo di negazione è una variabile
        [argomento, i]=riconoscimentoVariabile(formula, i+1)
        sottoformule.append('-'+argomento) #aggiunge la variabile alla lista degli argomenti
    
    else: #se il carattere è una variabile
      [argomento, i]=riconoscimentoVariabile(formula, i)
      sottoformule.append(argomento)
  

  return sottoformule, connettivi #restituisce la lista degli argomenti e quella dei connettivi


conn='&+_^U>=' #lista dei connettivi binari disponibili, in ordine di priorità
costanti_logiche='01'
aus='P*'
con=conn+aus