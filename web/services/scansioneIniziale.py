#funzione per il controllo che la formula sia scritta correttamente
from services.ricercaStringa import *
from services.scansioni import *

#funzione che controlla se una certa stringa sia numerica, letterale o alfanumerica
def controllo_variabili(stringa, connettivi, sottoformule, i):

    c=True
    if stringa.isdecimal(): #se la stringa è numerica
        c=False #non sono stati trovati simboli non validi
        if stringa not in costanti_logiche:
            condizione=True
        else:
            condizione=False

        if len(sottoformule)==1 and condizione: #se la stringa è conposta da un solo carattere numerico e non è una costante logica
            raise SyntaxError
        elif i==0 and connettivi[0]!='*' and condizione: #se si trova all'inizio della formula e non è seguito da un segno di moltiplicazione
            raise SyntaxError
        elif i==(len(sottoformule)-1) and connettivi[i-1]!='P' and condizione: #se si trova alla fine è non è preceduto da un simbolo di potenza
            raise SyntaxError
        elif condizione: #se è un numero diverso da 0 e 1 
            if connettivi[i-1]!='P' and connettivi[i]!='*': #se questa condizione è rispettata allora sarebbe una variabile
                raise SyntaxError            
        if connettivi[i-1]=='P' and connettivi[i]=='*': #una formula di questo dipo non ha senso
            raise SyntaxError

    elif stringa.isalpha(): #se è una stinga letterale
        c=False
        if i!=(len(sottoformule)-1):
            if connettivi[i]=='*':
                raise SyntaxError
        elif i!=0:
            if connettivi[i-1]=='P':
                raise SyntaxError

    #controlla che non sia preceduta da un simbolo di potenza o seguta da un simbolo di moltiplicazione

    elif stringa.isalnum():
        c=False
        if stringa[0].isdecimal():
            raise ImportError
        
        if i!=(len(sottoformule)-1):
            if connettivi[i]=='*':
                raise SyntaxError
        elif i!=0:
            if connettivi[i-1]=='P':
                raise SyntaxError

    #come sopra ma in più controlla che non inizi con un numero

    return c



def scansioneIniziale(formula): #controlla, prima di qualsiasi operazione, se la sintassi è corretta. Se non lo è, genera un'eccezione differente per il tipo di errore
    i=0
    n=len(formula)-1

    #Errore se la formula inizia o finisce con un connettivo binario o se finisce con un segno di negazione
    if formula[0] in con:
        raise SyntaxError    
    if (formula[n] in con) or (formula[n]=='-'):
        raise SyntaxError

    #controllo che tutte le parentesi siano aperte e chiuse
    while i<n:
        if formula[i]=='(':
            j=trovaParentesi(formula, i)
            if j==-1:
                raise IndentationError
            i=j+1
        elif formula[i]==')':
            raise SyntaxError
        i+=1

    #genera tutte le sottoformule separate da connettivi binari
    [sottoformule, connettivi]=scansione(formula)

    #controllo correttezza su ogni sottoformula
    for i in range(len(sottoformule)):
        stringa=sottoformule[i]
        simboli_invalidi=controllo_variabili(stringa, connettivi, sottoformule, i)

        #se la stringa iniziona con un segno di negazione, si controlla da dopo il segno
        if stringa[0]=='-':
            simboli_invalidi=controllo_variabili(stringa[1:], connettivi, sottoformule, i)

        #se si trova una parentesi, si controlla cosa c'è in parentesi
        elif stringa[0]=='(':
            scansioneIniziale(stringa[1:-1])
        
        #errore se si trovano simboli non validi
        elif simboli_invalidi:
            raise IOError
