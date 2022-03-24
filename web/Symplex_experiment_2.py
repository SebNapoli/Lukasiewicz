from z3 import *
from services.McNaughton_mode.McNaughton import *
from itertools import combinations, permutations

def create_variables(formula): 
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

def equations_combination(equations, com): #gives the equations combination (for vertices computing)
    eq_com=[]
    for combination in com:
        eq_com.append([])
        for i in combination:
            eq_com[len(eq_com)-1].append(equations[i])
  
    return eq_com

def create_permutation(N):
  perm=list(permutations(range(0, N)))
  return perm

def poly_permutation(polynomials, perm): #gives the equations permutation (for polyhedra computing)
  poly_perm=[]
  for permutation in perm:
    poly_perm.append([])
    for i in permutation:
      poly_perm[len(poly_perm)-1].append(polynomials[i])
  
  return poly_perm

def create_pol_condition(polynomials): #create z3 polynomials
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

def create_polyhedra(polynomials): #create the polyhedra with z3
  [pols, con01]=create_pol_condition(polynomials)
  polyhedra=[]
  perm=create_permutation(len(pols)) #create all polynomials permutation
  p_pols=poly_permutation(pols, perm)

  for permutation in p_pols: #for all permutations
    for i in range(len(permutation)):
      if i==0:
        polie=con01
      else:
        polie=And(polie, permutation[i]>=permutation[i-1])
    
    polyhedra.append(polie) #create the polyhedron of the form pol1>=pol2>=...>=poln
  
  return polyhedra


conn="&>+=^U" #list of all binary connectives
logic_con="01" #logic constains
s=Solver()
formula="-p&q" #test formula (remember to manual parse it)
[var, var_name]=create_variables(formula) #create z3 variables
equations=[]

for i in range(len(var)): #first equations
    equations.append(var[i]==0)
    equations.append(var[i]==1)

#create linear polynomials of McNaughton function
polynomials=McNaughton(formula)
polynomials=change_list(polynomials) 
polynomials=delete_duplicates(polynomials)

for i in range(len(polynomials)):
    domain=polynomials[i].domain
    
    for j in range(len(domain)): #create the constrain equations
        eq=domain[j]
        c=eq.pol
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
                                
            x=x+eq.cons_term
        else:
            x=eq.cons_term

        pos_eq=(x==eq.second_member)

        k=0
        add=True
        while k<len(equations): #verify if the equation is not in the list
            impl1=Implies(pos_eq, equations[k])
            impl2=Implies(equations[k], pos_eq)
            cond=Not(And(impl1, impl2))
            if s.check(cond)==unsat:
                add=False
                break
            else:
                k+=1

        if add: #if not, add it in the list
            equations.append(pos_eq)

com=combinations(range(len(equations)), len(var))
eq_com=equations_combination(equations, com)

vertex=[] #list of all vertices
for combination in eq_com: #for all combinations of n equations
    for i in range(len(combination)):
        if i==0:
            x=combination[i]
        else:
            x=And(x, combination[i])
    
    if s.check(x)==sat: #if the intersection is not empty
        pos_vertex=s.model()
        for i in range(len(var)):
          if i==0:
            y=(var[i]!=pos_vertex.eval(var[i]))
          else:
            y=Or(y, var[i]!=pos_vertex.eval(var[i]))
        
        if s.check(x, y)==unsat: #verify if the solution is unique, if yes, check if the vertex is alreary in the list
          new_vertex=True
          for k1 in range(len(vertex)):
              old_vertex=vertex[k1]
              delete=True
              for k2 in range(len(var)):
                  value1=old_vertex.eval(var[k2])
                  value2=pos_vertex.eval(var[k2])
                  cond=(value1!=value2)

                  if s.check(cond)==sat:
                      delete=False
                      break

              if delete:
                  new_vertex=False
                  break
          
          if new_vertex: #if not, add it
              vertex.append(pos_vertex)

polyhedra=create_polyhedra(polynomials) #create all Mundici's polyhedra

for i in range(len(polyhedra)): #for all polyhedra
  pol_vertex=[] #list of all vertex in the polyedron (empty at the start)
  for k1 in range(len(vertex)):
      v=vertex[k1]
      for k2 in range(len(var)): 
          value=v.eval(var[k2])
          if k2==0:
              check=(var[k2]==value)
          else:
              check=And(check, (var[k2]==value))
      
      if s.check(check, polyhedra[i])==sat: #check if the vertex is in the polyhedron
          pol_vertex.append(v) #if yes, add it

  print(polyhedra[i])
  print(pol_vertex) #print the polyedron (in z3 format) and vertices list
  print("")