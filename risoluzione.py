from z3 import *
from services.classi import *
from services.ricercaStringa import *
from services.operazioni_logiche import *

def generaVariabili(formula, s): #costruisce la lista di tutte le variabili usate nella formula
  variabili=[]
    
  Nformula=formula.replace('(', '')
  Nformula=Nformula.replace(')', '')
  Nformula=Nformula.replace('-', '')
  #rimuove tutti i segni superflui

  i=0
  ini=0
  while(i<len(Nformula)): #fino alla fine della formula

    if Nformula[i] in conn or i==len(Nformula)-1: #se si legge un connettivo binario o si è alla fine della formula, si definisce il nome della variabile
      if i==len(Nformula)-1:
        fin=len(Nformula)
      else:
        fin=i

      variab=Nformula[ini:fin]
      ini=i+1
      if variab not in costanti_logiche: #se la variabile in realtà non è una costante logica
        unico=True

        for k in range(len(variabili)): #controlla se il nome non è già presente nella lista delle variabili
          if variab==variabili[k].nome:
            unico=False
            break
        
        if unico: #se non è presente, crea la variabile
          x=Var_Prop(variab, s)
          variabili.append(x)
    
    i+=1

  return variabili


def sottoformula(formula, var, i): #risolve una sottoformula delimitata da parentesi
  k=trovaParentesi(formula, i)
  x=risolvi(formula[i+1:k], var) 
  i=k+1
  return x, i #restituisce valore e posizione della scansione


def negazione(formula, var, i): #risolve una negazione
  
  if formula[i+1]!='(': #se è negazione di una variabile
    if formula[i+1]=='0':
      x=1
      i+=2
    elif formula[i+1]=='1':
      x=0
      i+=2
    else:
      [argomento, i]=riconoscimentoVariabile(formula, i+1) #riconoscimento nome della variabile
      for k in range(len(var)):
        if var[k].nome==argomento:
          j=i
          break #individua la variabile da associare
      x=compl(var[k].variabile) #effettua l'operazione di complemento
  
  else: #se è negazione di una sottoformula delimitata da parentesi
    [x, i]=sottoformula(formula, var, i+1) #risolve la sottoformula
    x=compl(x) #ne fa il complemento
  return x, i #restituisce valore e posizione della scansione


def risolvi(formula, var): #scasiona la formula e ne resituisce il valore di verità
  
  i=0 #parte dall'inizio della scansione
  while(i<len(formula)): #fino alla fine della formula
    if i==0:  #se ci troviamo all'inizio
      if formula[0]=='-':
        [x, i]=negazione(formula, var, 0) #risolve la negazione della prima sottoformula

      elif formula[0]=='(': 
        [x, i]=sottoformula(formula, var, 0) #risolve la prima sottoformula

      elif formula[0]=='0': 
        x=0 #pone la prima sottoformula pari a zero
        i=1

      elif formula[0]=='1':
        x=1 #pone la prima sottoformula pari ad 1
        i=1

      else:
        [argomento, i]=riconoscimentoVariabile(formula, 0)
        for j in range(len(var)):
          if var[j].nome==argomento:
            break
        x=var[j].variabile

    else: 
      if formula[i+1]=='-':
        [y, k]=negazione(formula, var, i+1) #se si trova un segno di negazione, si da precedenza alla negazione

      elif formula[i+1]=='(':
        [y, k]=sottoformula(formula, var, i+1) #si da precedenza alla sottoformula

      elif formula[i+1]=='0':
        y=0
        k=i+2

      elif formula[i+1]=='1':
        y=1
        k=i+2

      else:
        [argomento, k]=riconoscimentoVariabile(formula, i+1)
        for j in range(len(var)):
          if var[j].nome==argomento:
            break  #se l'argomento è una varibile, si individua la variabile
        y=var[j].variabile

      #in base all'opezione data in input, si esegue l'operzione di Lukasiewicz adatta
      if formula[i]=='&':
        x=tnorm(x, y)
      elif formula[i]=='>':
        x=residuo(x, y)
      elif formula[i]=='^':
        x=minimo(x, y)
      elif formula[i]=='U':
        x=massimo(x, y)
      elif formula[i]=='+':
        x=sommat(x, y)
      elif formula[i]=='_':
        x=difft(x, y)
      else:
        x=doppiaimp(x, y)

      i=k #il programma continua a scansionare

  return x #resituisce il valore di verità di x


def AltreSoluzioni(mod, variabili, N, s): #funzione per generare altre soluzioni
  nuovo=0 #numero di nuove soluzione trovate
  
  if N!=0: #se l'utente voule nuove soluzioni

    alternative=[]  
    #organizzione lista delle soluzioni
    #necessaria ricerca sui nomi perchè l'ordine di creazione variabili diverso da quello di output di z3
    for i in range(len(variabili)): 
      for d in mod.decls():
        if d.name()==variabili[i].nome:
          y=variabili[i].variabile!=mod[d]
          if i==0:
            x=y
          else:
            x=Or(x, y)
          s.add(x)
          break

    
    print("Esito ricerca altre soluzioni: ")
    while nuovo<N: #il ciclo termina quando sono stati raggiunti il numero di soluzioni volute dall'utente
      if s.check()==sat: #se esiste un altra soluzione
        Nmod=s.model() #crea la nuova soluzione
        output=str(Nmod)
        output=output.replace('[', '')
        output=output.replace(']', '')
        alternative.append(output) #stampa la soluzione
        nuovo+=1 #aggiorna il numero di soluzioni diverse ottenute 
        for i in range(len(variabili)):
          for d in mod.decls():
            if d.name()==variabili[i].nome:
              y=(variabili[i].variabile!=Nmod[d])
              if i==0:
                x=y
              else:
                Or(x, y)
              s.add(x) #aggiunge, in ordine di variabili, la soluzione ottenuta

      else: #se non esiste una nuova soluzione
        break #esce dal ciclo
      
    if nuovo==0: #se non esistono soluzioni diverse da quella originale
      alternative.append("Non esistono nuove soluzioni")
  
  else:
    alternative=None
  
  return alternative



conn='&+_^U>=' #lista dei connettivi binari disponibili, in ordine di priorità
costanti_logiche='01'