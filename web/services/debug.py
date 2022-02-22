#funzione per il debug della formula

from services.ricercaStringa import *
from services.scansioni import *




def merge(con, formula1, formula2): #a partire da un connettivo e due formule na fa l'unione
      formula='('+formula1+con+formula2+')' 
      return formula




def elaborazione(lista, connettivi, sottoformule):
  for x in lista:
    while x in connettivi:
      i=connettivi.index(x) #trova la posizione del connettivo
      sottoformule[i]=merge(x, sottoformule[i], sottoformule[i+1]) #aggiungi parentesi per la sottoformula
      sottoformule[i+1]=''
      sottoformule.remove(sottoformule[i+1])
      connettivi[i]=''
      connettivi.remove(connettivi[i])

  return sottoformule


def parsing(formula): #resituisce la formula con l'aggiunta delle parentesi in maniera tale da rispettare l'ordine standar dei connettivi

  if (formula[0]=='(') and (trovaParentesi(formula, 0)==(len(formula)-1)): #se tutta la formula è racchiusa fra parentesi
    formula=parsing(formula[1:-1]) #svolge il parsing solo sulla formula racchiusa fra parentesi

  [sottoformule, connettivi]=scansione(formula) #esegue la scansione della formula

  if len(sottoformule)!=1:
    for x in aus:
      while x in connettivi:
        i=connettivi.index(x) #trova la posizione del connettivo
        stringa=sottoformule[i]
        if stringa[0]=='-':
          sottoformule[i]='-'+merge(x, sottoformule[i][1:], sottoformule[i+1]) #aggiungi parentesi per la sottoformula
        else:
          sottoformule[i]=merge(x, sottoformule[i], sottoformule[i+1])
        sottoformule[i+1]=''
        sottoformule.remove(sottoformule[i+1])
        connettivi[i]=''
        connettivi.remove(connettivi[i])


  if len(sottoformule)==1: #se non sono presenti connettivi binari (quindi se si tratta di una singola variabile o negazione di sottoformula)
    if formula[0]=='-': #se è presente una negazione
      stringa=parsing(formula[1:])

      return '('+ '-' + stringa +')' #resituisce il parsing della formula racchiusa tra parentesi
    else: 
      return sottoformule[0] #resituisce la formula originaria

  for i in range(len(sottoformule)): #fa il parsing su tutte le sottoformule

    if ('*' in sottoformule[i]) or ('P' in sottoformule[i]):
      stringa='('+parsing(sottoformule[i])+')'
      
    else:
      stringa=parsing(sottoformule[i])

    sottoformule[i]=stringa

  sottoformule=elaborazione(conn, connettivi, sottoformule)

  Nformula=sottoformule[0]

  return Nformula #resituisce la formula con parsing corretto



#trasformazione da una formula con segni di potenza e prodotto ad una formula puramente con linguaggio di Lukasiewicz
def trasformazione(formula):

  while 'P' in formula:
    ind=formula.index('P')
    i=ind-1

    while i>0:
      if formula[i]=='(':
        break
      else:
        i-=1
    
    j=trovaParentesi(formula, i+1)
    argomento=formula[i+1:ind]
    esponente=formula[ind+1:j]
    
    for k in range(int(esponente)):
      if k==0:
        formulaAusiliaria=argomento
      else:
        formulaAusiliaria=formulaAusiliaria+'&'+argomento
    
    formula=formula.replace(formula[i+1:j], formulaAusiliaria)
  
  while '*' in formula:
    ind=formula.index('*')
    i=ind-1
    
    while i>0:
      if formula[i]=='(':
        break
      else:
        i-=1
    
    j=trovaParentesi(formula, i)
    fattore=int(formula[i+1:ind])
    argomento=formula[ind+1:j]

    for k in range(fattore):
      if k==0:
        formulaAusiliaria=argomento
      else:
        formulaAusiliaria=formulaAusiliaria+'+'+argomento

    formula=formula.replace(formula[i+1:j], formulaAusiliaria)

  return formula



def debugFormula(formula):
  formula=formula.replace('--', '') #rimuove le doppie negazioni, equivalenti a una affermazione
  formula=formula.replace(' ', '') #rimuove gli spazi
  formula=parsing(formula) #fa il parsing della formula originaria
  formulaC=trasformazione(formula)
  return formula, formulaC



conn='&+_^U>=' #lista dei connettivi binari disponibili, in ordine di priorità
costanti_logiche='01'
aus='P*'
con=conn+aus