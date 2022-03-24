from services.Search_and_debug.scansions import *

#transformation for natural language to Lukasiewicz formulas
def natural_language(formula):
    subformulas=scansion(formula)[0]

    
    for string in subformulas:
        if ("very " in string) or ("quite " in string):
            cons_formula=string

            while cons_formula[0]==' ': #remove useless spaces or negation signs
                cons_formula=cons_formula[1:]

            if cons_formula[0]=='-':
                cons_formula='-'+natural_language(cons_formula[1:])

            elif cons_formula[0]=='(':
                if cons_formula[len(cons_formula)-1]!=')': #error if the bracket is not closed
                    raise SyntaxError
                
                else: 
                    cons_formula='('+natural_language(cons_formula[1:-1])+')'
            
            elif "very "==cons_formula[:5]:
                count=0
                while "very "==cons_formula[:5]:
                    count+=1
                    cons_formula=cons_formula[5:]
                
                cons_formula='('+natural_language(cons_formula)+'P'+str(count+1)+')'
            #if n very are found, we see them as xPn

            elif "quite "==cons_formula[:6]:
                count=0
                while "quite "==cons_formula[:6]:
                    count+=1
                    cons_formula=cons_formula[6:]
                
                cons_formula='('+str(count+1)+'*'+natural_language(cons_formula)+')'
            #if n quite are found, we see them as n*x
            
            else: #if a syntax error is found
                raise SyntaxError

            formula=formula.replace(string, cons_formula)
            #replace the natural language with Lukasiewicz formulas

    return formula  #return the new formula