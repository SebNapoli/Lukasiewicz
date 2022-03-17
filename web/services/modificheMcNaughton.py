#flie content: list modification in McNaughton mode
from z3 import *

#if the script finds a impossible domain, it will delete the associated polynomial
def delete_impossible(pol_list):
    s=Solver()
    for vinc in pol_list:
        #z3 setup for checking domain
        c=vinc.pol
        if len(c)>0:
            for j in range(len(c)):
                if j==0:
                    x=Real(c[j].name)
                    s.add(x>=0, x<=1)
                    x=c[j].coef_value*x
                else:
                    y=Real(c[j].name)
                    s.add(y>=0, y<=1)
                    x=x+c[j].coef_value*y
                                
            x=x+vinc.cons_term
        else:
            x=vinc.cons_term
        
        #sign setup
        if vinc.verse=='<=':
            s.add(x<=vinc.second_member)
        elif vinc.verse=='>=':
            s.add(x>=vinc.second_member)
        elif vinc.verse=='>':
            s.add(x>vinc.second_member)
        elif vinc.verse=='<':
            s.add(x<vinc.second_member)

    if s.check()==unsat: #if the domain is impossible
        delete=True #delete the polynomial
    else:
        delete=False

    return delete              

#if the script finds a polynomial >1 or <0, it will be replaced with 1 or 0 
def change_list(polynomials):
    s=Solver()
    t=Solver()
    i=0
    while i<len(polynomials):
        #z3 setup
        s.push()
        t.push()
        c=polynomials[i].coef
        if len(c)>0:
            for j in range(len(c)):
                if j==0:
                    x=Real(c[j].name)
                    s.add(x>=0, x<=1)
                    t.add(x>=0, x<=1)
                    x=c[j].coef_value*x
                else:
                    y=Real(c[j].name)
                    s.add(y>=0, y<=1)
                    t.add(y>=0, y<=1)
                    x=x+c[j].coef_value*y
                                
            x=x+polynomials[i].cons_term
        
            s.add(x>0)
            if s.check()==unsat: #if the polynomial is always <0
                polynomials[i].coef=[]
                polynomials[i].cons_term=0 #replace it with 0 constant
            else:
                t.add(x<1)
                if t.check()==unsat: #if the polynomial is always >1
                    polynomials[i].coef=[]
                    polynomials[i].cons_term=1 #replace it with 0 constant
            s.pop()
            t.pop()
        
        i+=1


    return polynomials #return the new list

#The app will delete a polynomial if it's equal to another polynomial
def delete_duplicates(polynomials):
    i=0
    while i<len(polynomials):
        j=i+1
        while j<len(polynomials):
            if len(polynomials[i].coef)==len(polynomials[j].coef):
                equality=True
                for k in range(len(polynomials[i].coef)):
                    if polynomials[i].coef[k].coef_value!=polynomials[j].coef[k].coef_value:
                        equality=False
                        break
                
                if equality: #if all coefficients are equals
                    if polynomials[i].cons_term==polynomials[j].cons_term: #if the constant terms are equals too
                        polynomials[i].al_domain.append(polynomials[j].domain)
                        polynomials.remove(polynomials[j]) #remove the polynomial
                    else:
                        j+=1 #continue
                
                else:
                    j+=1 #continue
            
            else:
                j+=1 #continue
            
        i+=1

    return polynomials #return the new list

#delete useless constrains
def useless_constrains(polynomials, List, lim, sign):
    s=Solver()

    c=polynomials.coef
    if len(c)>0:
        for j in range(len(c)):
            if j==0:
                x=Real(c[j].name)
                s.add(x>=0, x<=1)
                x=c[j].coef_value*x
            else:
                y=Real(c[j].name)
                s.add(y>=0, y<=1)
                x=x+c[j].coef_value*y
                                
        x=x+polynomials.cons_term
    else:
        x=polynomials.cons_term

    if sign=='<=':
        ul_cond=x<=lim
    elif sign=='>=':
        ul_cond=x>=lim
    elif sign=='>':
        ul_cond=x>lim
    elif sign=='<':
        ul_cond=x<lim    
    
    s.push()
    s.add(ul_cond)    
    if s.check()==unsat: 
        return False, True
    s.pop()

    cond_pre=None
    for vinc in List:
        c=vinc.pol
        if len(c)>0:
            for j in range(len(c)):
                if j==0:
                    x=Real(c[j].name)
                    s.add(x>=0, x<=1)
                    x=c[j].coef_value*x
                else:
                    y=Real(c[j].name)
                    s.add(y>=0, y<=1)
                    x=x+c[j].coef_value*y
                                
            x=x+vinc.cons_term
        else:
            x=vinc.cons_term
        
        if cond_pre==None:
            if vinc.verse=='<=':
                cond_pre=x<=vinc.second_member
            elif vinc.verse=='>=':
                cond_pre=x>=vinc.second_member
            elif vinc.verse=='>':
                cond_pre=x>vinc.second_member
            elif vinc.verse=='<':
                cond_pre=x<vinc.second_member
        else:
            if vinc.verse=='<=':
                cond_pre=And(cond_pre, x<=vinc.second_member)
            elif vinc.verse=='>=':
                cond_pre=And(cond_pre, x>=vinc.second_member)
            elif vinc.verse=='>':
                cond_pre=And(cond_pre, x>vinc.second_member)
            elif vinc.verse=='<':
                cond_pre=And(cond_pre, x<vinc.second_member)
    if cond_pre!=None:
        s.push()
        s.add(And(cond_pre, Not(ul_cond)))
        if s.check()==unsat:
            return True, False
        s.pop()

        s.push()
        s.add(And(Not(cond_pre), ul_cond))
        if s.check()==unsat:
            return False, True
    
    return False, False
