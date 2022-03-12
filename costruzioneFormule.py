#file con le funzioni per la costruzione delle formule che codificano tabelle nel ragionamento vago

def Cformula(start, a, b, x): #algoritmo di mundici adattato per la codifica tabella, resa vera se e solo se x>=start
    #per come è scritto il programma, sara a>0, b>0, |a|>=|b|

    if a+b==0: #si può dimostrare che se a+b=0 allora non esiste soluzione
        return '0'

    elif b==0: #se b=0, la formula cercata non è altro che
        if a==1: 
            return x
        else:
            f=str(a)+'*'+x
            return '('+f+')'

    else: #costruzione della formula con un algoritmo simile a quello di Mundici (per ricorsione)
        f1=Cformula(start, a-1, b, x)
        if f1=='0':
            f1=x
        else:
            f1='(('+f1+')+'+x+')'

        if (a-1)*start>=-b:
            f2=''
        else:
            f2=Cformula(start, a-1, b+1, x)
            f2='&'+f2
        
        return f1+f2


#funzione per formule vere per x<=start
def Cformula2(start, a, b, x): 
  return Cformula(1-start, -a, b+a, '-'+x) #utilizzando l'ultimo punto del primo lemma articolo di McNaughton, si
#può, attraverso alcune trasformazioni, ricondurre al caso precedente
