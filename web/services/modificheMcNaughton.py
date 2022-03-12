from z3 import *
def elimina_inconsistenti(lista):
    s=Solver()
    for vinc in lista:
        c=vinc.pol
        if len(c)>0:
            for j in range(len(c)):
                if j==0:
                    x=Real(c[j].nome)
                    s.add(x>=0, x<=1)
                    x=c[j].coefficiente*x
                else:
                    y=Real(c[j].nome)
                    s.add(y>=0, y<=1)
                    x=x+c[j].coefficiente*y
                                
            x=x+vinc.tNoto
            if vinc.verso=='<=':
                s.add(x<=vinc.sec)
            elif vinc.verso=='>=':
                s.add(x>=vinc.sec)
            elif vinc.verso=='>':
                s.add(x>vinc.sec)
            elif vinc.verso=='<':
                s.add(x<vinc.sec)

    if s.check()==unsat:
        elimina=True
    else:
        elimina=False

    return elimina              

            
def modificaLista(polinomi):
    s=Solver()
    t=Solver()
    i=0
    while i<len(polinomi):
        if False:
            polinomi[0].dominio=["altrimenti"]

        else:
            s.push()
            t.push()
            c=polinomi[i].coef
            if len(c)>0:
                for j in range(len(c)):
                    if j==0:
                        x=Real(c[j].nome)
                        s.add(x>=0, x<=1)
                        t.add(x>=0, x<=1)
                        x=c[j].coefficiente*x
                    else:
                        y=Real(c[j].nome)
                        s.add(y>=0, y<=1)
                        t.add(y>=0, y<=1)
                        x=x+c[j].coefficiente*y
                                
                x=x+polinomi[i].tNoto
                            

                s.add(x>0)
                s.check()
                if s.check()==unsat:
                    polinomi[i].coef=[]
                    polinomi[i].tNoto=0
                else:
                    t.add(x<1)
                    if t.check()==unsat:
                        polinomi[i].coef=[]
                        polinomi[i].tNoto=1
                s.pop()
                t.pop()
        
        i+=1

    i=0

    while i<len(polinomi):
        j=i+1
        c=True
        while j<len(polinomi):
            if len(polinomi[i].coef)==len(polinomi[j].coef):
                ug=True
                for k1 in range(len(polinomi[i].coef)):
                    for k2 in range(len(polinomi[j].coef)):
                        if polinomi[i].coef[k1].nome==polinomi[j].coef[k2].nome:
                            if (polinomi[i].coef[k1].coefficiente)!=(polinomi[j].coef[k2].coefficiente):
                                ug=False
                                break
                
                if ug:
                    if polinomi[i].tNoto==polinomi[j].tNoto:
                        c=False
                        if polinomi[i].dominio==["altrimenti"] or polinomi[j].dominio==[] or polinomi[i].dominio==[]:
                            polinomi.remove(polinomi[j])
                        else:
                            polinomi[j].dominio[0]='oppure se '+polinomi[j].dominio[0]
                            polinomi[i].dominio=polinomi[i].dominio+polinomi[j].dominio
                            polinomi.remove(polinomi[j])
    
            j+=1
        if c:
            i+=1

#    polinomi=elDoppioni(polinomi)
                
    return polinomi