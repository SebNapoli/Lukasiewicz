from itertools import permutations
from socket import timeout
from z3 import *
from services.McNaughton_mode.McNaughton import *


def variables_number(formula): 
  variables=[]
  variables_name=[]

  Nformula=formula.replace('(', '')
  Nformula=Nformula.replace(')', '')
  Nformula=Nformula.replace('-', '')
  #It deletes useless signs

  i=0
  ini=0
  #Until the end of the formula
  while(i<len(Nformula)): 

    #If it finds a binary connective or it's at the end of the formula
    if Nformula[i] in conn or i==len(Nformula)-1:
      if i==len(Nformula)-1:
        fin=len(Nformula)
      else:
        fin=i

      variab=Nformula[ini:fin]
      #new variable name
      ini=i+1
      #if it isn't a logic constant
      if variab not in logic_con: 
        unique=True

        #control on the list
        for k in range(len(variables)): 
          if variab==variables_name[k]:
            unique=False
            break
        
        #add it in the list if it is not already in
        if unique: 
          variables_name.append(variab)
          variables.append(Real(variab))
    
    i+=1

  return variables, variables_name #return the list

def create_permutation(N):
  perm=list(permutations(range(0, N)))
  return perm

def poly_permutation(polynomials, perm):
  poly_perm=[]
  for permutation in perm:
    poly_perm.append([])
    for i in permutation:
      poly_perm[len(poly_perm)-1].append(polynomials[i])
  
  return poly_perm

def create_pol_condition(polynomials):
  pols=[]
  for i in range(len(polynomials)):
    c=polynomials[i].coef
    if len(c)>0:
      for j in range(len(c)):
        if j==0:
          x=Real(c[j].name)
          con01=And(x>=0, x<=1)
          pol=c[j].coef_value*x
        else:
          y=Real(c[j].name)
          con01=And(con01, And(y>=0, y<=1))
          pol=pol+c[j].coef_value*y
                                
      pol=pol+polynomials[i].cons_term
    else:
      pol=polynomials[i].cons_term

    pols.append(pol)

  return pols, con01

def create_polyedras(polynomials):
  [pols, con01]=create_pol_condition(polynomials)
  poliedri=[]
  perm=create_permutation(len(pols))
  p_pols=poly_permutation(pols, perm)
  for permutation in p_pols:
    for i in range(len(permutation)):
      if i==0:
        polie=con01
      else:
        polie=And(polie, permutation[i]>=permutation[i-1])
    
    poliedri.append(polie)
  
  return poliedri

def aux_variables(var, var_name):
  var_aux=[]
  for i in range(len(var)+1):
    var_aux.append([])
    for j in range(len(var)):
      x=Real(var_name[j]+str(i))
      var_aux[i].append(x)

  return var_aux

def substitution(var, var_aux, poliedri):
  pol_aux=[]
  for i in range(len(var)+1):
    p=poliedri
    for j in range(len(var)):
      p=substitute(p, (var[j], var_aux[i][j]))
    pol_aux.append(p)

  return pol_aux

def A(var):
  vector=[]
  for i in range(len(var)+1):
    x=Real('A'+str(i))
    vector.append(x)
    if i==0:
      pos_con=(x>=0)
      sum=x
    else:
      pos_con=And(pos_con, x>=0)
      sum=sum+x

  sum_cond_1=(sum==1)
  return vector, pos_con, sum_cond_1

def dis_cond(var_aux):
  disj=None
  for j in range(len(var_aux)):
    for k in range(len(var_aux)):
      if j!=k:
        conj=None
        for i in range(len(var_aux[0])):
          if conj==None:
            conj=(var_aux[j][i]!=var_aux[k][i])
          else:
            conj=Or(conj, (var_aux[j][i]!=var_aux[k][i]))

        if disj==None:
          disj=conj
        else:
          disj=And(disj, conj)

  return disj

def sum_cond(var, var_aux, A_vector):
  for i in range(len(var)):
    for j in range(len(var)+1):
      if j==0:
        x=A_vector[j]*var_aux[j][i]
      else:
        x=x+A_vector[j]*var_aux[j][i]
    
    if i==0:
      sum=(var[i]==x)
    else:
      sum=And(sum, var[i]==x)

  return sum

def trivial_condition(A_vector):
  for i in range(len(A_vector)):
    for j in range(len(A_vector)):
      if j==i:
        x=(A_vector[j]==1)
      else:
        x=(A_vector[j]==0)

      if j==0:
        conj=x
      else:
        conj=And(conj, x)
    
    if i==0:
      disj=conj
    
    else:
      disj=Or(disj, conj)

  return disj

conn="&>+=^U"
s=Solver()
formula="p=q"
[var, var_name]=variables_number(formula)
polynomials=McNaughton(formula)
polynomials=change_list(polynomials) 
polynomials=delete_duplicates(polynomials)
poliedri=create_polyedras(polynomials)
var_aux=aux_variables(var, var_name)
i=5
if True:
  pol_aux=substitution(var, var_aux, poliedri[i])
  [A_vector, pos_con, sum_cond_1]=A(var)
  sum=sum_cond(var, var_aux, A_vector)
  dis=dis_cond(var_aux)
  trivial_cond=trivial_condition(A_vector)
  for j in range(len(var_aux)):
    if j==0:
      v_aux=var_aux[0]
    else:
      v_aux=v_aux+var_aux[j]

  for j in range(len(pol_aux)):
    if j==0:
      p_aux=pol_aux[j]
    else:
      p_aux=And(pol_aux[j], p_aux)

  loop=True
  s.add(ForAll(A_vector+v_aux, And(poliedri[i], Implies(And(p_aux, pos_con, sum_cond_1, sum, dis), trivial_cond))))
  while loop:
    sol=s.check()
    if sol==unsat or sol==unknown:
      break

    else:
      mod=s.model()
      print(str(mod)[1:-1])
      for j in range(len(var)):
        for d in mod.decls():
          if d.name()==var_name[j]:
            y=var[j]!=mod[d]
            if j==0:
              x=y
            else:
              x=Or(x, y)
        
      s.add(x)
