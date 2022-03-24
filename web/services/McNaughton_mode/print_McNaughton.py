#file content: printing McNaughton's functions
from services.McNaughton_mode.McNaughton_changes import *

def print_domain(do):
    string=''
    
    for condition in do:
        domain=''
        variables=condition.pol
        for k in range(len(variables)):
            if variables[k].coef_value>0:
                if variables[k].coef_value!=1:
                    domain=domain+'+'+str(variables[k].coef_value)+variables[k].name
                else:
                    domain=domain+'+'+variables[k].name
                        
            elif variables[k].coef_value<0:
                if variables[k].coef_value!=-1:
                    domain=domain+str(variables[k].coef_value)+variables[k].name
                else:
                    domain=domain+'-'+variables[k].name

        if condition.cons_term>0:
            domain=domain+'+'+str(condition.cons_term)
        elif condition.cons_term<0 or domain=='':
            domain=domain+str(condition.cons_term)

        if domain[0]=='+':
            domain=domain[1:]

        domain=domain+condition.verse+str(condition.second_member)
        string=string+' and '+domain
    
    return string


def pol_print(polynomials):
    polynomials=change_list(polynomials) 
    polynomials=delete_duplicates(polynomials)     
    #change the list to be more user friendly
    out=[]
    dom=[]

    for i in range(len(polynomials)):
        output=''
        variables=polynomials[i].coef
        for var in variables:
            if var.coef_value==1:
                output=output+'+'+var.name
            elif var.coef_value==-1:
                output=output+'-'+var.name
            elif var.coef_value>0:
                output=output+'+'+str(var.coef_value)+var.name
            elif var.coef_value<0:
                output=output+str(var.coef_value)+var.name
        
        if polynomials[i].cons_term>0:
            output=output+'+'+str(polynomials[i].cons_term)
        elif polynomials[i].cons_term<0 or output=='':
            output=output+str(polynomials[i].cons_term)
        
        if output[0]=='+':
            output=output[1:]

        out.append(output)

        if len(polynomials)==1: #if there is only one polynomial, it is valid in all the space 
            dom.append("everywhere")
        
        elif i==0: #if it's the first polynomial
            dom.append("otherwise")
        
        else:
            do=polynomials[i].domain
            string=print_domain(do)
            string=string[4:]
            doa=polynomials[i].al_domain
            for alter in doa:
                d=print_domain(alter)
                d=d[4:]
                string=string+' <br /> or '+ d
            dom.append(string)
    
    return out, dom