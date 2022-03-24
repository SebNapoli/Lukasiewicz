#file content: formula construction for reasoning mode
from services.Vague_Reasoning.num_algoritms import *

def Cformula(start, a, b, x): #Mundici algoritm variation

    if a+b==0: 
        return '0'

    elif b==0: 
        if a==1: 
            return x
        else:
            f=str(a)+'*'+x
            return '('+f+')'

    else: 
        f1=Cformula(start, a-1, b, x)
        if f1=='0':
            f1=x
        else:
            f1='(('+f1+')+'+x+')'

        if (a-1)*start>=-b:
            f2=''
        else:
            f2=Cformula(start, a-1, b+1, x)
            f2='&'+f2
        
        return f1+f2


def Cformula2(start, a, b, x): 
  return Cformula(1-start, -a, b+a, '-'+x)


#create the formulas for table coding
def formulas_construction(table, var_name, comparison, row, col, N): 
  set=[]

  [maxs, mins]=MaxMin(table, row, col) #find maxs and mis 

  for i in range(row):
    for j in range(col):
      den=maxs[j]-mins[j]
      if comparison[j]=='max':
        num=table[i][j]-mins[j]
      else:
        num=maxs[j]-table[i][j]

      if num==den: #if it's the max value, the coding formula is x=1
        set.append(var_name[i][j]+'=1')

      elif num==0: #if it's the min value, the coding formula
        set.append(var_name[i][j]+'=0')

      else:
        div=MCD(den, num)
        den=int(den/div)
        num=int(num/div)
        if N=="inf": #if the user's will is a exact coding
          f1=Cformula(float(num/den), den, 1-num, var_name[i][j])
          f2=Cformula2(float(num/den), -den, 1+num, var_name[i][j])
          set.append('('+f1+')^('+f2+')')

        else:
          N=int(N)
          if N>=den: #if it's possible to find a exact code (the wanted precison is smaller than the fraction step)
            f1=Cformula(float(num/den), den, 1-num, var_name[i][j])
            f2=Cformula2(float(num/den), -den, 1+num, var_name[i][j])
            set.append('('+f1+')^('+f2+')')
          
          else:  
            for k in range(N): #find the gap
              if float(num/den)<float((k+1)/N):
                if k==0:
                  f1='1'
                else:  
                  f1=Cformula(float(k/N), N, 1-k, var_name[i][j])

                if k==(N-1):
                  f2='1'
                else:
                  f2=Cformula2(float((k+1)/N), -N, 1+(k+1), var_name[i][j])
                set.append('('+f1+')^('+f2+')')
                break
         
  return set #return the set for formulas
