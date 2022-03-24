#file content: algoritms for McNaughton's functions
from services.McNaughton_mode.McNaughton_changes import *
from services.McNaughton_mode.polynomials_classes import *
from services.Search_and_debug.search_on_string import *

#domains operatons
def check_domains(pol_list, x, y, lim, sign):
    [el1, el2]=useless_constrains(x, y.domain, lim, sign)
    #check if some conditions can be ignored
    if not(el1): #if the new condition can't be ignored

        if not(el2): #if the old conditions can't be ignored
            y.new_cond(x.coef, x.cons_term, lim, sign) #simply add the new one
        else:
            y.domain=[]
            y.new_cond(x.coef, x.cons_term, lim, sign) #replace the old ones with the new one

    delete=delete_impossible(y.domain)
    #check if it's an empty domain
    if not(delete): #if it isn't
        pol_list.append(y) #add the linear polynomal in the list
    
    return pol_list

#generate the polynomials for all Lukasiewicz's operations
def polynomials_generation(pol_list, y, coef1, coef2, lim, b):
    new_list=[] #This list will contain the new polynomials
    for k in range(len(pol_list)):
        x=pol_list[k]

        for j in range(len(y)):
            #The new polynomials have to respect the old coinstrains
            val_lim=linear_polynomials(lim)
            val_lim.domain=pol_list[k].domain+y[j].domain
            z=linear_polynomials((coef1*x.cons_term)+(coef2*y[j].cons_term)+b)
            z.domain=pol_list[k].domain+y[j].domain

            #creation of new polynomials (see McNaughton's article for base algortim)
            for var1 in x.coef:
                new=True
                for var2 in y[j].coef:
                    if var1.name==var2.name:
                        z.new_coef(var1.name, (coef1*var1.coef_value)+(coef2*var2.coef_value))
                        new=False
                        break #operations between polynomials
                            
                if new: #append the variables of first pol if there isn't the same name in the second_memberond pol
                    z.new_coef(var1.name, (coef1*var1.coef_value))

            #as before
            for var2 in y[j].coef:
                new=True
                for var1 in x.coef:
                    if var1.name==var2.name:
                        new=False
                        break
                            
                if new:
                    z.new_coef(var2.name, (coef2*var2.coef_value))

            #check if there are some useless constrains and if the domain is not empty  
            if lim==0:
                new_list=check_domains(new_list, z, val_lim, lim, '<')
                new_list=check_domains(new_list, z, z, lim, ">=")    
            else:                
                new_list=check_domains(new_list, z, val_lim, lim, '>')
                new_list=check_domains(new_list, z, z, lim, "<=")
    return new_list #return the new list

def change_sign(x): #negation for polynomials
    for j in range(len(x)):
        y=linear_polynomials(1-x[j].cons_term)
        var=x[j].coef
        for k in range(len(var)):
            y.new_coef(var[k].name, -var[k].coef_value)
        y.domain=x[j].domain
        x[j]=y

    return x


def MNsubformula(formula, i): #McNaughton's function computation for a subformula between brackets
  k=find_bracket(formula, i)
  x=McNaughton(formula[i+1:k]) 
  i=k+1
  return x, i #return polynomials and scansion position


def MNnegation(formula, i): #McNaughton's function computation for a negation
  if formula[i+1]!='(': #if it isn't a negation of a subformula
    if formula[i+1]=='0':
        y=linear_polynomials(1)
        i+=2
    elif formula[i+1]=='1':
        y=linear_polynomials(0)
        i+=2
    else:
        [argument, i]=variable_name(formula, i+1) #find the variable name 
        y=linear_polynomials(1)
        y.new_coef(argument, -1)
    x=[]
    x.append(y)
  else: 
    [x, i]=MNsubformula(formula, i+1) #subformula computation
    x=change_sign(x)
  return x, i #return polynomials and scansion position


def McFind_argument(formula, i):
    p_list=[]
    if formula[i]=='-': #if it's a negation
        [p_list, i]=MNnegation(formula, i) 

    elif formula[i]=='(': 
        [p_list, i]=MNsubformula(formula, i) #subformula computation

    elif formula[i]=='0': 
        p_list.append(linear_polynomials(0)) 
        i+=1

    elif formula[i]=='1':
        p_list.append(linear_polynomials(1)) 
        i+=1

    else:
        [argument, i]=variable_name(formula, i)
        x=linear_polynomials(0)
        x.new_coef(argument, 1)
        p_list.append(x)
    
    return p_list, i

#base function for McNaughton's algoritm
def McNaughton(formula):
    i=0
    while(i<len(formula)): #until we are at the end of the formula
        if i==0:  #if we are at the start
            [pol_list, i]=McFind_argument(formula, 0)
        else: 
            [y, k]=McFind_argument(formula, i+1)

            #from Lukasiewicz's operation to polynomials operations
            if formula[i]=='&':
                pol_list=polynomials_generation(pol_list, y, 1, 1, 0, -1)
            elif formula[i]=='>':
                pol_list=polynomials_generation(pol_list, y, -1, 1, 1, 1)
            elif formula[i]=='+':
                pol_list=polynomials_generation(pol_list, y, 1, 1, 1, 0)
            elif formula[i]=='U':
                pol_list=change_sign(pol_list)
                pol_list=polynomials_generation(pol_list, y, 1, 1, 1, 0)
                pol_list=change_sign(pol_list)
                pol_list=polynomials_generation(pol_list, y, 1, 1, 1, 0)
            elif formula[i]=='^':
                res=polynomials_generation(pol_list, y, -1, 1, 1, 1)
                pol_list=polynomials_generation(pol_list, res, 1, 1, 0, -1)
            
            elif formula[i]=='_':
                y=change_sign(y)
                pol_list=polynomials_generation(pol_list, y, 1, 1, 0, -1)
            
            elif formula[i]=='=':
                res1=polynomials_generation(pol_list, y, -1, 1, 1, 1)
                res2=polynomials_generation(y, pol_list, -1, 1, 1, 1)
                pol_list=polynomials_generation(res1, res2, 1, 1, 0, -1)
                
            i=k 

    return pol_list #return the list of all polynomials