from services.scansioni import scansione



#trasformazione da linguaggio naturale a formula di Lucasiewicz
def linguaggioNaturale(formula):
    [sottoformule, u]=scansione(formula)

    
    for stringa in sottoformule:
        if ("molto " in stringa) or ("abbastanza " in stringa):
            formCostruita=stringa

            while formCostruita[0]==' ': #rimozione spazi inutili o segni di negazioni
                formCostruita=formCostruita[1:]

            if formCostruita[0]=='-':
                formCostruita='-'+linguaggioNaturale(formCostruita[1:])

            elif formCostruita[0]=='(':
                if formCostruita[len(formCostruita)-1]!=')': #se la parentesi non è chiusa si da messaggio di errore
                    raise SyntaxError
                
                else: #altrimenti si eliminano le parentesi (al momento inutili)
                    formCostruita='('+linguaggioNaturale(formCostruita[1:-1])+')'
            
            elif "molto "==formCostruita[:6]:
                count=0
                while "molto "==formCostruita[:6]:
                    count+=1
                    formCostruita=formCostruita[6:]
                
                formCostruita='('+linguaggioNaturale(formCostruita)+'P'+str(count+1)+')'

            elif "abbastanza "==formCostruita[:11]:
                count=0
                while "abbastanza "==formCostruita[:11]:
                    count+=1
                    formCostruita=formCostruita[11:]
                
                formCostruita='('+str(count+1)+'*'+linguaggioNaturale(formCostruita)+')'

            else:
                raise SyntaxError

            formula=formula.replace(stringa, formCostruita)


    return formula                

