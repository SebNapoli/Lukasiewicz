from services.modificheMcNaughton import *
from services.ricercaStringa import *
from services.polinomi import polinomio, vincoli


def generaPolinomi(lista, y, coefficiente1, coefficiente2, lim, b):
    nuova_lista=[]
    for k in range(len(lista)):
        x=lista[k]

        for j in range(len(y)):
            val_lim=polinomio(lim)
            z=polinomio((coefficiente1*x.tNoto)+(coefficiente2*y[j].tNoto)+b)
            z.dominio=lista[k].dominio+y[j].dominio

            for var1 in x.coef:
                unico=True
                for var2 in y[j].coef:
                    if var1.nome==var2.nome:
                        z.nuovo_coefficiente(var1.nome, (coefficiente1*var1.coefficiente)+(coefficiente2*var2.coefficiente))
                        unico=False
                        break
                            
                if unico:
                    z.nuovo_coefficiente(var1.nome, (coefficiente1*var1.coefficiente))

            for var2 in y[j].coef:
                unico=True
                for var1 in x.coef:
                    if var1.nome==var2.nome:
                        unico=False
                        break
                            
                if unico:
                    z.nuovo_coefficiente(var2.nome, (coefficiente2*var2.coefficiente))
            
            if lim==0:
                z.aggiungi_cond(z.coef, z.tNoto, lim, ">=")
                elimina=elimina_inconsistenti(z.dominio)
                if not(elimina):
                    nuova_lista.append(z)

                val_lim.aggiungi_cond(z.coef, z.tNoto, lim, "<")
                elimina=elimina_inconsistenti(val_lim.dominio)
                if not(elimina):
                    nuova_lista.append(val_lim)

            else:
                z.aggiungi_cond(z.coef, z.tNoto, lim, "<=")
                elimina=elimina_inconsistenti(z.dominio)
                if not(elimina):
                    nuova_lista.append(z)

                val_lim.aggiungi_cond(z.coef, z.tNoto, lim, ">")
                elimina=elimina_inconsistenti(val_lim.dominio)
                if not(elimina):
                    nuova_lista.append(val_lim)

            

    return nuova_lista

def cambioSegno(x):
    for j in range(len(x)):
        y=polinomio(1-x[j].tNoto)
        var=x[j].coef
        for k in range(len(var)):
            y.nuovo_coefficiente(var[k].nome, -var[k].coefficiente)
        y.dominio=x[j].dominio
        x[j]=y

    return x

def MNsottoformula(formula, i): #risolve una sottoformula delimitata da parentesi
  k=trovaParentesi(formula, i)
  x=McNaughton(formula[i+1:k]) 
  i=k+1
  return x, i #restituisce valore e posizione della scansione

def MNnegazione(formula, i): #risolve una negazione
  
  if formula[i+1]!='(': #se è negazione di una variabile
    if formula[i+1]=='0':
        y=polinomio(1)
        i+=2
    elif formula[i+1]=='1':
        y=polinomio(0)
        i+=2
    else:
        [argomento, i]=riconoscimentoVariabile(formula, i+1) #riconoscimento nome della variabile
        y=polinomio(1)
        y.nuovo_coefficiente(argomento, -1)
    x=[]
    x.append(y)

  else: #se è negazione di una sottoformula delimitata da parentesi
    [x, i]=MNsottoformula(formula, i+1) #risolve la sottoformula
    x=cambioSegno(x)
  return x, i #restituisce valore e posizione della scansione


def McNaughton(formula):
    lista=[]
    i=0
    while(i<len(formula)): #fino alla fine della formula
        if i==0:  #se ci troviamo all'inizio
            if formula[0]=='-':
                [lista, i]=MNnegazione(formula, 0) #risolve la negazione della prima sottoformula

            elif formula[0]=='(': 
                [lista, i]=MNsottoformula(formula, 0) #risolve la prima sottoformula

            elif formula[0]=='0': 
                lista.append(polinomio(0)) #pone la prima sottoformula pari a zero
                i=1

            elif formula[0]=='1':
                lista.append(polinomio(1)) #pone la prima sottoformula pari ad 1
                lista[0].tNoto=1
                i=1

            else:
                [argomento, i]=riconoscimentoVariabile(formula, 0)
                x=polinomio(0)
                x.nuovo_coefficiente(argomento, 1)
                lista.append(x)

        else: 
            y=[]
            if formula[i+1]=='-':
                [y, k]=MNnegazione(formula, i+1) #se si trova un segno di negazione, si da precedenza alla negazione

            elif formula[i+1]=='(':
                [y, k]=MNsottoformula(formula, i+1) #si da precedenza alla sottoformula

            elif formula[i+1]=='0':
                y.append(polinomio(0))
                k=i+2

            elif formula[i+1]=='1':
                y.append(polinomio(1))
                y[0].tNoto=1
                k=i+2

            else:
                [argomento, k]=riconoscimentoVariabile(formula, i+1)
                y.append(polinomio(0))
                y[0].nuovo_coefficiente(argomento, 1)
                
            #in base all'opezione data in input, si esegue l'operzione di Lukasiewicz adatta
            if formula[i]=='&':
                lista=generaPolinomi(lista, y, 1, 1, 0, -1)
            elif formula[i]=='>':
                lista=generaPolinomi(lista, y, -1, 1, 1, 1)
            elif formula[i]=='+':
                lista=generaPolinomi(lista, y, 1, 1, 1, 0)
            elif formula[i]=='U':
                lista=cambioSegno(lista)
                lista=generaPolinomi(lista, y, 1, 1, 1, 0)
                lista=cambioSegno(lista)
                lista=generaPolinomi(lista, y, 1, 1, 1, 0)[1:]
            elif formula[i]=='^':
                res=generaPolinomi(lista, y, -1, 1, 1, 1)
                lista=generaPolinomi(lista, res, 1, 1, 0, -1)[1:]
            
            elif formula[i]=='_':
                y=cambioSegno(y)
                lista=generaPolinomi(lista, y, 1, 1, 0, -1)
            
            elif formula[i]=='=':
                res1=generaPolinomi(lista, y, -1, 1, 1, 1)
                res2=generaPolinomi(y, lista, -1, 1, 1, 1)
                lista=generaPolinomi(res1, res2, 1, 1, 0, -1)
                
            i=k #il programma continua a scansionare

    return lista


def stampa(polinomi):
            
    for i in range(len(polinomi)):
        output=''
        variabili=polinomi[i].coef
        for k in range(len(variabili)):
            if variabili[k].coefficiente>0:
                if variabili[k].coefficiente!=1:
                    output=output+'+'+str(variabili[k].coefficiente)+variabili[k].nome
                else:
                    output=output+'+'+variabili[k].nome
                
                if output[0]=='+':
                    output=output[1:]

            elif variabili[k].coefficiente<0:
                if variabili[k].coefficiente!=-1:
                    output=output+str(variabili[k].coefficiente)+variabili[k].nome
                else:
                    output=output+'-'+variabili[k].nome
            
        
        if (polinomi[i].tNoto!=0) or (output==''):
            if (polinomi[i].tNoto>0) and (output!=''):
                output=output+'+'+str(polinomi[i].tNoto)    
            else:    
                output=output+str(polinomi[i].tNoto)

        
        stringa=' se '
        do=polinomi[i].dominio
        for k1 in range(len(do)):
            dominio=''
            variabili=do[k1].pol
            for k2 in range(len(variabili)):
                if variabili[k2].coefficiente>0:
                    if variabili[k2].coefficiente!=1:
                        dominio=dominio+'+'+str(variabili[k2].coefficiente)+variabili[k2].nome
                    else:
                        dominio=dominio+'+'+variabili[k2].nome
                    
                    if dominio[0]=='+':
                        dominio=dominio[1:]

                elif variabili[k2].coefficiente<0:
                    if variabili[k2].coefficiente!=-1:
                        dominio=dominio+str(variabili[k2].coefficiente)+variabili[k2].nome
                    else:
                        dominio=dominio+'-'+variabili[k2].nome
            if do[k1].tNoto>0:
                dominio=dominio+'+'+str(do[k1].tNoto)
            else:
                dominio=dominio+str(do[k1].tNoto)

            dominio=dominio+do[k1].verso+str(do[k1].sec)+" "
            stringa+=dominio        
        polinomi[i]=output+stringa

    return polinomi