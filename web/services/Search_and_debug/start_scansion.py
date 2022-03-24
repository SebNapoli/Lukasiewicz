#file content: initial syntax controll functions
from services.Search_and_debug.scansions import *

#check if a string is a number, is leteral or alphanumerical
def alnum_control(string, connectives, subformulas, i):

    not_alphanum=True #if this variable is true, it means that the string is not alphanumerical

    if string.isdecimal(): #if the string is a number
        not_alphanum=False 
        
        if string not in logic_con:
            condition=True
        else:
            condition=False

        if len(subformulas)==1:
            if condition: #if it's only 1 formula and it's a number != 0 and 1, error
                raise SyntaxError
        #if we are at the start of the formula and it's not followed by a moltiplication (and !=0 and 1), error
        elif i==0:
            if connectives[0]!='*' and condition: 
                raise SyntaxError

        elif i==(len(subformulas)-1):
            #if it's at the end and it isn't preceded by a power symbol, error
            if connectives[i-1]!='P' and condition: 
                raise SyntaxError

        #if it's not 0 and 1 and it's not followed by moltiplication and it's not preceded by power, error
        elif connectives[i-1]!='P' and connectives[i]!='*' and condition:  
            raise SyntaxError
        
        #strings like this have no sense 
        elif connectives[i-1]=='P' and connectives[i]=='*': 
            raise SyntaxError

    elif string.isalpha(): #if it's a literal string
        not_alphanum=False
        if i!=(len(subformulas)-1):
            if connectives[i]=='*':
                raise SyntaxError
        elif i!=0:
            if connectives[i-1]=='P':
                raise SyntaxError

    #the script check if it's followed by a moltiplication or preceded by a power (error)

    elif string.isalnum():
        not_alphanum=False
        if string[0].isdecimal():
            raise ImportError
        
        if i!=(len(subformulas)-1):
            if connectives[i]=='*':
                raise SyntaxError
        elif i!=0:
            if connectives[i-1]=='P':
                raise SyntaxError

    #as before, plus the condition it can't start with a number

    return not_alphanum #return if the string is alphanumerical


#the function checks if the formula is syntatical correct
def initial_scansion(formula): 
    i=0
    n=len(formula)-1

    #Error with connective (=! negation) at the start
    if formula[0] in con:
        raise SyntaxError
    
    #Error with connective at the end
    if (formula[n] in con) or (formula[n]=='-'):
        raise SyntaxError

    #brackets control
    while i<n:
        if formula[i]=='(':
            j=find_bracket(formula, i)
            if j==-1:
                raise IndentationError
            i=j+1
        elif formula[i]==')':
            raise SyntaxError
        i+=1

    #create subformulas
    [subformulas, connectives]=scansion(formula)

    #control on every subformula
    for i in range(len(subformulas)):
        string=subformulas[i]
        not_alphanum=alnum_control(string, connectives, subformulas, i)

        #if there is a negation symbol, check after that
        if string[0]=='-':
            not_alphanum=alnum_control(string[1:], connectives, subformulas, i)

        #if there is a bracket, check the subformula
        elif string[0]=='(':
            initial_scansion(string[1:-1])
        
       
        elif not_alphanum: #error if the checked string is not alphanumerical (symbol not accepted)
            raise NotImplementedError
