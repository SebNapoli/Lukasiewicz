#file di funzioni ausiliarie per il ragionamento vago

from services.costruzioneFormule import *
from services.scansioni import scansione

#controlla che il nome delle proprietà e degli oggetti non sia errato
def controlloProprietà(proprieta, oggetti, rig, col):
  for j in range(col): #controllo sui nomi delle proprietà (non possono contenere numeri)
    proprieta[j]=proprieta[j].replace(' ', '')
    if proprieta[j]=='' or not(proprieta[j].isalpha()):
      raise NameError
          
  for i in range(rig): #controllo sui nomi degli oggetti (non possono essere stringe vuote)
    stringa=oggetti[i].replace(' ', '')
    if stringa=='':
      raise NameError


#controlla che nella query non siano presenti proprietà differenti da quelle in tabella
def controlloQuery(proprieta, decisione):
    count=0
    lista=[]

    #definizione della lista di nomi delle proprietà presenti nella query
    ini=0
    for i in range(len(decisione)):
        if not(decisione[i].isdecimal()) and not(decisione[i].isalpha()):
            lista.append(decisione[ini:i])
            ini=i+1
        elif i==len(decisione)-1:
            lista.append(decisione[ini:])

    #effettivo controllo
    for j in range(len(proprieta)):
      if proprieta[j] in lista:
        count+=1
    return count


#trasformazione da linguaggio naturale a formula di Lucasiewicz
def linguaggioNaturale(formula):
    [sottoformula, u]=scansione(formula)

    for stringa in sottoformula:
        if ("molto " in stringa) or ("poco " in stringa): 
            
            if ("molto " in stringa) and ("poco " in stringa): #messaggio di errore se entrambe le parole sono presenti per lo stesso parametro
                raise PermissionError
            
            formCostruita=stringa

            while formCostruita[0]==' ': #rimozione spazi inutili
                formCostruita=formCostruita[1:]

            while formCostruita[0]=='(':
                if formCostruita[len(formCostruita)-1]!=')': #se la parentesi non è chiusa si da messaggio di errore
                    raise SyntaxError
                
                else: #altrimenti si eliminano le parentesi (al momento inutili)
                    formCostruita=formCostruita[1:-1]

            count=0
            #costruzione effettiva della formula
            if "molto " in formCostruita:
                while "molto " in formCostruita:
                    count+=1
                    formCostruita=formCostruita[6: ]

                num=count
                den=count+1
                formCostruita=Cformula(float(num/den), den, 1-num, formCostruita)

            else:
                while "poco " in formCostruita:
                    count+=1
                    formCostruita=formCostruita[5: ]
            
                num=1
                den=count+1
                formCostruita=Cformula2(float(num/den), -den, 1+num, formCostruita)

            formula=formula.replace(stringa, formCostruita)

        
    
    return formula


