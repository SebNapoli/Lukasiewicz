#file content: research fuctions

def find_bracket(formula, j): #With an open bracket, find where it is closed
  Bstack=['(']
  i=j+1
  while i<len(formula):
    if formula[i]=='(': 
      Bstack.append('(') #if a new bracket is opened, add it in the stack
    elif formula[i]==')': 
      Bstack.remove(Bstack[len(Bstack)-1]) #if a bracket is closed, remove it from the stack
      if len(Bstack)==0: #if there aren't open brackets
        return i #return the position
    i+=1
  
  return -1 #return the -1 value if the bracket is not closed (error)



def variable_name(formula, i): #return the variable name and scansion position
    j=i
    while j!=len(formula):
      if formula[j] in con:
        break
      else:
        j+=1
    argument=formula[i:j] 

    return argument, j


def open_bracket(formula, j):
  Bstack=[')']
  i=j-1
  while i>0:
    if formula[i]==')': 
      Bstack.append(')') 
    elif formula[i]=='(': 
      Bstack.remove(Bstack[len(Bstack)-1]) 
      if len(Bstack)==0: 
        return i 
    i-=1

  return i

conn='&+_^U>=' 
logic_con='01'
aux='P*'
con=conn+aux